#!/usr/bin/env python3
"""p65_wave3_yield_pilot.py -- wave 3 direction-blind yield pilot (unit 2, 2026-11-16).

For each wave 3 language: draw 500 sentences with a fixed seed and flag whether each sentence holds a TIME
expression and a PLACE expression (and, secondarily, a QUANTITY numeral), from UD annotation and small
per-language lexicons. PRESENCE ONLY: nothing here reads, guesses or counts direction.

The screen is validated on English first, against the final Arm A / A3 / A3b time-place classes of the 4,000
coded EWT + GUM sentences (protocol v2: NA = time and place not both literally present; TP/PT directional; PAR,
AMB both present). Recall and precision are weighted by the A3b cell weights (population / coded), so they are
estimates for the whole English pool, not for the stratified sample.

Two place screens:
  BROAD  = place deixis, OR a nominal marked by a STATIC locative (in/at/on..., Loc/Ine/Ade case) whose head is
           not a time word or number, OR a nominal marked by a DIRECTIONAL marker (to/from, Dat/Abl/Ill/Ela/All)
           whose head is a proper noun or a place noun.
  NARROW = place deixis, OR any locative-marked nominal whose head is a proper noun or a place noun.
Time screen (one): time relation (obl:tmod, nmod:tmod, obl:unmarked ...), OR a time-lexicon lemma, OR a year
  (1500-2049), OR a time adposition / subordinator (after, before, during, since, until, when, while ...).

Yield. For language L with N_L sentences and screen-positive share r_L (500 draw and full census), the expected
directional time-place items are
    D_L = N_L * r_L * PPV_dir(English)
where PPV_dir is the weighted share of screen-positive English sentences that are directional (TP or PT). This
TRANSFERS the English precision to L: an assumption, stated in the report, not a measurement.

Usage: python3 -I scripts/p65_wave3_yield_pilot.py --root <repo> [--seed 20261130 --n 500 --boot 2000]
Writes wave3/pilot/p65_wave3_yield-draw_<lang>.tsv (sentence IDs and flags; no text) and prints the report.
"""
import argparse, collections, glob, os, random, re, sys, unicodedata

ARABIC_DIACRITICS = re.compile("[ً-ْٰـ]")
YEAR = re.compile(r"^(1[5-9]\d\d|20[0-4]\d)(年|년)?$")


def norm(s, lang):
    s = unicodedata.normalize("NFC", s)
    if lang == "ar":
        s = ARABIC_DIACRITICS.sub("", s)
        s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    if lang == "ko":
        s = s.split("+")[0]
    return s.lower()


def ko_particles(lemma):
    return set(lemma.split("+")[1:])


W = lambda s: set(s.split())
# Per-language lists. TIME: lemmas that name or locate a time. TFUNC: adpositions / subordinators that make their
# phrase or clause temporal. DEIX: place deixis. PLACE: place nouns (narrow screen). SLOC / DLOC: static and
# directional locative adpositions; SCASE / DCASE: the same as Case feature values.
CFG = {
 "en": dict(
  TIME=W("today yesterday tomorrow tonight now then currently recently soon later ago noon midnight morning evening "
         "night afternoon day week month year hour minute second season summer winter autumn century decade weekend "
         "monday tuesday wednesday thursday friday saturday sunday january february april june july august september "
         "october november december time period era date moment while"),
  TFUNC=W("after before during since until till when whenever while once"),
  DEIX=W("here there home abroad away outside inside upstairs downstairs nearby everywhere somewhere anywhere "
         "overseas downtown elsewhere"),
  PLACE=W("city town country village house home room street road school office park area place region state "
          "building church hospital store shop restaurant hotel kitchen car island coast world county"),
  SLOC=W("in at on near inside outside behind above below under over around along between beside within across "
         "through throughout beyond underneath"),
  DLOC=W("to from into onto toward towards"),
  SCASE=set(), DCASE=set(), TMOD={"obl:tmod", "nmod:tmod", "obl:unmarked", "nmod:unmarked", "advmod:tmod"}),
 "zh": dict(
  TIME=W("今天 昨天 明天 現在 现在 年 月 日 天 時 时 時候 时候 時期 时期 期間 期间 當時 当时 目前 早上 晚上 世紀 世纪 "
         "星期 後來 后来 最近 年代 時代 时代 小時 小时 分鐘 分钟 秋天 冬天 夏天 春天 初 末 至今 今年 去年 明年 曾經 曾经"),
  TFUNC=W("後 后 以後 以后 之後 之后 以前 之前 時 时 當 当 期間 期间 自從 自从 直到"),
  DEIX=W("這裡 这里 那裡 那里 這兒 那兒 此地 當地 当地 本地 國外 国外 海外 附近"),
  PLACE=W("城市 市 國家 国家 村 家 房間 房间 街 學校 学校 地區 地区 地方 省 縣 县 島 岛 城 鎮 镇 區 区 國 国 港"),
  SLOC=W("在 於 于 中 上 裡 里 內 内 外 下 旁 附近 境內 境内 之間 之间 一帶"),
  DLOC=W("從 从 到 至 向 往 自"),
  SCASE=set(), DCASE=set(), TMOD={"nmod:tmod", "obl:tmod"}),
 "ja": dict(
  TIME=W("今日 昨日 明日 今 年 月 日 時 時代 時間 頃 間 朝 夜 当時 現在 週 世紀 とき 時期 以降 以来 午前 午後 "
         "夕方 春 夏 秋 冬 最近 毎日 年代 後半 前半 初め 末 今年 昨年 去年 来年 際"),
  TFUNC=W("後 前 まで 以降 以来 際 とき 時 間 頃 うち"),
  DEIX=W("ここ そこ あそこ 此処 現地 地元 海外 国内 国外 近く"),
  PLACE=W("市 町 村 県 国 都市 家 部屋 学校 地域 地方 場所 駅 島 道 通り 東京 大阪 日本"),
  SLOC=W("で にて 中 内 上 下 外"), DLOC=W("に へ から"),
  SCASE=set(), DCASE=set(), TMOD=set()),
 "tr": dict(
  TIME=W("bugün dün yarın şimdi yıl sene ay gün hafta saat sabah akşam gece zaman sonra önce süre dönem yüzyıl "
         "artık dakika yaz kış bahar sonbahar pazartesi salı çarşamba perşembe cuma cumartesi pazar ocak şubat mart "
         "nisan mayıs haziran temmuz ağustos eylül ekim kasım aralık geçen gelecek henüz hâlâ halen eskiden"),
  TFUNC=W("sonra önce boyunca beri itibaren sırasında iken ken zaman kadar"),
  DEIX=W("burada orada şurada burası orası ora bura yurtdışı dışarı içeri"),
  PLACE=W("şehir kent ülke köy ev oda okul sokak cadde bölge yer il ilçe ada"),
  SLOC=W("içinde üstünde altında yanında arasında önünde arkasında"), DLOC=set(),
  SCASE={"Loc"}, DCASE={"Dat", "Abl"}, TMOD={"obl:tmod", "nmod:tmod"}),
 "ar": dict(
  TIME=W("عام يوم سنة شهر اسبوع ساعة الان امس غد وقت فترة صباح مساء ليلة ليل قرن حاليا دقيقة موسم لحظة مرحلة "
         "يناير فبراير مارس ابريل مايو يونيو يوليو اغسطس سبتمبر اكتوبر نوفمبر ديسمبر عقد"),
  TFUNC=W("بعد قبل خلال منذ اثناء عندما حين لما بعدما قبيل طوال"),
  DEIX=W("هنا هناك هنالك"),
  PLACE=W("مدينة بلد دولة منطقة مكان بيت منزل شارع قرية غرفة مدرسة عاصمة محافظة ارض"),
  SLOC=W("في عند داخل خارج تحت فوق امام خلف بين حول وسط قرب"), DLOC=W("من الى نحو"),
  SCASE=set(), DCASE=set(), TMOD={"obl:tmod", "nmod:tmod"}),
 "hi": dict(
  TIME=W("आज कल अब अभी साल वर्ष दिन महीना माह सप्ताह हफ्ता हफ़्ता घंटा सुबह शाम रात समय दौरान बाद पहले जब फिर वक्त "
         "वक़्त सदी दशक तारीख सोमवार मंगलवार बुधवार गुरुवार शुक्रवार शनिवार रविवार जनवरी फरवरी मार्च अप्रैल मई जून "
         "जुलाई अगस्त सितंबर अक्टूबर नवंबर दिसंबर मिनट हाल"),
  TFUNC=W("बाद पहले दौरान जब तब"),
  DEIX=W("यहाँ यहां वहाँ वहां"),
  PLACE=W("शहर देश गांव गाँव घर जगह क्षेत्र राज्य इलाका स्कूल कमरा सड़क जिला प्रदेश"),
  SLOC=W("में पर पास अंदर बाहर नीचे ऊपर सामने पीछे"), DLOC=W("से तक ओर"),
  SCASE=set(), DCASE=set(), TMOD={"obl:tmod", "nmod:tmod"}),
 "fi": dict(
  TIME=W("nyt tänään eilen huomenna vuosi kuukausi päivä viikko tunti aamu ilta yö aika kun jälkeen ennen aikana "
         "sitten nykyään hetki kesä talvi syksy kevät maanantai tiistai keskiviikko torstai perjantai lauantai "
         "sunnuntai vuosikymmen vuosisata minuutti tammikuu helmikuu maaliskuu huhtikuu toukokuu kesäkuu heinäkuu "
         "elokuu syyskuu lokakuu marraskuu joulukuu silloin aiemmin myöhemmin pian viime"),
  TFUNC=W("jälkeen ennen aikana kun kuluessa asti saakka alkaen"),
  DEIX=W("täällä tuolla siellä täältä sieltä tänne sinne tuonne kotona kotiin ulkomailla"),
  PLACE=W("koti kaupunki maa kylä talo huone koulu katu alue paikka seutu"),
  SLOC=W("luona vieressä alla päällä takana edessä keskellä"), DLOC=set(),
  SCASE={"Ine", "Ade"}, DCASE={"Ela", "Ill", "Abl", "All"}, TMOD={"obl:tmod", "nmod:tmod"}),
 "id": dict(
  TIME=W("hari tahun bulan minggu jam pagi malam sore siang kini sekarang kemarin besok saat ketika waktu setelah "
         "sebelum selama sejak lalu abad masa periode tadi nanti januari februari maret april mei juni juli agustus "
         "september oktober november desember senin selasa rabu kamis jumat sabtu menit dekade"),
  TFUNC=W("setelah sebelum selama sejak ketika saat sewaktu sesudah hingga"),
  DEIX=W("sini situ sana"),
  PLACE=W("kota negara desa rumah kamar sekolah jalan daerah wilayah tempat provinsi kabupaten pulau"),
  SLOC=W("di dalam"), DLOC=W("ke dari"),
  SCASE=set(), DCASE=set(), TMOD={"obl:tmod", "nmod:tmod"}),
 "pcm": dict(  # Naija: NSC lemmas are mostly English-based spellings
  TIME=W("today yesterday tomorrow now naw then den time year day week month morning night evening afternoon hour "
         "minute when wen before after since till during monday sunday saturday friday christmas"),
  TFUNC=W("after before since till until when wen during"),
  DEIX=W("here dere there hia"),
  PLACE=W("house haus village town city country school street road area place market church compound room lagos"),
  SLOC=W("inside in at on for near under ontop"), DLOC=W("to from enter"),
  SCASE=set(), DCASE=set(), TMOD={"obl:tmod", "nmod:tmod"}),
 "ko": dict(
  # 주 (week / give), 시 (hour / city / poem), 분 (minute / person), 해 (year / sun / do) dropped as ambiguous
  TIME=W("오늘 어제 내일 지금 현재 년 월 날 시간 아침 저녁 밤 때 후 동안 당시 최근 이후 이전 세기 시대 시절 "
         "요즘 봄 여름 가을 겨울 올해 작년 내년"),
  TFUNC=set(),
  DEIX=W("여기 거기 저기 이곳 그곳"),
  PLACE=W("곳 집 학교 도시 나라 지역 마을 방 거리 회사 서울 시골"),
  SLOC=set(), DLOC=set(), SCASE=set(), DCASE=set(), TMOD={"obl:tmod", "nmod:tmod"},
  KO_S=W("에서 에"), KO_D=W("으로 로 에게서")),
 "fa": dict(
  TIME=W("امروز دیروز فردا اکنون حالا الان سال ماه روز هفته ساعت صبح شب عصر زمان وقت هنگام دوران دوره قرن امسال "
         "پارسال اخیرا دقیقه بهار تابستان پاییز زمستان"),
  TFUNC=W("پس بعد قبل طی هنگام وقتی هنگامی"),
  DEIX=W("اینجا آنجا"),
  PLACE=W("شهر کشور خانه روستا منطقه جا محل خیابان مدرسه اتاق استان تهران"),
  SLOC=W("در توی روی زیر کنار داخل میان بین"), DLOC=W("به از تا"),
  SCASE=set(), DCASE=set(), TMOD={"obl:tmod", "nmod:tmod"}),
}

LANGS = [  # unit, language code, treebanks pooled, verdict in the feasibility note
    ("English", "en", ["UD_English-EWT", "UD_English-GUM"], "baseline"),
    ("Mandarin", "zh", ["UD_Chinese-GSD", "UD_Chinese-HK"], "MARGINAL"),
    ("Japanese", "ja", ["UD_Japanese-GSD"], "MARGINAL"),
    ("Turkish", "tr", ["UD_Turkish-BOUN"], "MARGINAL"),
    ("Turkish-Kenet", "tr", ["UD_Turkish-Kenet"], "fallback"),
    ("Arabic", "ar", ["UD_Arabic-PADT"], "MARGINAL"),
    ("Indonesian", "id", ["UD_Indonesian-GSD", "UD_Indonesian-CSUI"], "MARGINAL"),
    ("Naija", "pcm", ["UD_Naija-NSC"], "MARGINAL"),
    ("Hindi", "hi", ["UD_Hindi-HDTB"], "FEASIBLE"),
    ("Finnish", "fi", ["UD_Finnish-TDT"], "FEASIBLE"),
    ("Korean", "ko", ["UD_Korean-Kaist"], "reserve"),
    ("Persian", "fa", ["UD_Persian-PerDT"], "reserve"),
]


def read(path):
    meta, rows = {}, []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            if rows:
                yield meta, rows
            meta, rows = {}, []
        elif line.startswith("#"):
            if " = " in line:
                k, v = line[1:].split(" = ", 1)
                meta[k.strip()] = v
        else:
            r = line.split("\t")
            if len(r) == 10 and r[0].isdigit():
                rows.append(r)
    if rows:
        yield meta, rows


def feats(r):
    return dict(f.split("=", 1) for f in r[5].split("|") if "=" in f)


def screen(rows, lang, hits):
    c = CFG[lang]
    ids = {r[0]: r for r in rows}
    kids = collections.defaultdict(list)
    for r in rows:
        kids[r[6]].append(r)
    lem = {r[0]: norm(r[2] if r[2] != "_" else r[1], lang) for r in rows}
    form = {r[0]: norm(r[1], lang) for r in rows}

    def is_time_word(i):
        if ids[i][3] in ("VERB", "AUX"):  # verb lemmas never count as time words (Korean 주+었+다 "gave")
            return False
        return lem[i] in c["TIME"] or form[i] in c["TIME"] or bool(YEAR.match(ids[i][1]))

    def is_place_word(i):
        return lem[i] in c["PLACE"] or form[i] in c["PLACE"] or lem[i] in c["DEIX"] or form[i] in c["DEIX"]

    time = place_b = place_n = quant = False
    for r in rows:
        i, rel, up = r[0], r[7], r[3]
        if rel in c["TMOD"] and not is_place_word(i):
            time = True; hits["T:rel:" + rel] += 1
        if is_time_word(i):
            time = True; hits["T:lex:" + (lem[i] if lem[i] in c["TIME"] else "YEAR")] += 1
        if rel in ("case", "mark") and lem[i] in c["TFUNC"]:
            time = True; hits["T:func:" + lem[i]] += 1
        if lem[i] in c["DEIX"] or form[i] in c["DEIX"]:
            place_b = place_n = True; hits["P:deix:" + lem[i]] += 1
        if up == "NUM" and rel.startswith("nummod") and not YEAR.match(r[1]) and r[6] in ids \
                and not is_time_word(r[6]):
            quant = True
        # locative-marked nominal
        # Korean-Kaist tags many particle-bearing nominals ADV (e.g. 장안+에), so ADV counts there
        if (up in ("NOUN", "PROPN") or (lang == "ko" and up == "ADV")) and rel.split(":")[0] in ("obl", "nmod", "advmod", "root", "conj", "nsubj"):
            if is_time_word(i):
                continue
            ks = [norm(k[2] if k[2] != "_" else k[1], lang) for k in kids[i] if k[7].startswith("case")]
            cs = feats(r).get("Case", "")
            static = any(k in c["SLOC"] for k in ks) or cs in c["SCASE"]
            direc = any(k in c["DLOC"] for k in ks) or cs in c["DCASE"]
            if lang == "ko":
                ps = ko_particles(r[2])
                static = static or bool(ps & c["KO_S"])
                direc = direc or bool(ps & c["KO_D"])
            strong = up == "PROPN" or is_place_word(i)
            if rel.split(":")[0] not in ("obl", "nmod") and not (lang == "ko" and (static or direc)):
                continue
            if static:
                place_b = True; hits["P:static"] += 1
            if direc and strong:
                place_b = True; hits["P:dir+strong"] += 1
            if (static or direc) and strong:
                place_n = True
    return time, place_b, place_n, quant


def load(root, tbs, lang, hits):
    out = []
    for tb in tbs:
        # train/dev/test only: Turkish-BOUN r2.18 also ships a "finetuning" file that repeats train
        for p in sorted(glob.glob(os.path.join(root, "data", "ud", "r2.18", tb, "*-ud-*.conllu"))):
            if not re.search(r"-ud-(train|dev|test)\.conllu$", p):
                continue
            for meta, rows in read(p):
                if all(r[1] == "_" for r in rows):
                    continue
                sid = meta.get("sent_id", "%s:%d" % (os.path.basename(p), len(out)))
                out.append((tb, sid, len(rows)) + screen(rows, lang, hits))
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n; d = 1 + z * z / n
    m = (p + z * z / (2 * n)) / d; h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (max(0.0, m - h), min(1.0, m + h))


def english_truth(root):
    """Final Arm A / A3 / A3b class and A3b cell weight for each of the 4,000 coded sentences."""
    def tsv(p):
        lines = open(os.path.join(root, p), encoding="utf-8").read().splitlines()
        h = lines[0].split("\t")
        return [dict(zip(h, l.split("\t"))) for l in lines[1:] if l]
    weight = {"C-T": 1.0, "C-N": 1.0, "F-T": 2696 / 1005, "F-N": 9052 / 1188, "R-T": 1561 / 562, "R-N": 17017 / 1045}
    truth = {}
    sets = [("arm-a-model/p65_model-items_map.tsv", "arm-a-model/p65_model-codes_coder1.tsv",
             "arm-a-model/p65_model-codes_coder2.tsv", "arm-a-model/p65_model-adjudication.tsv")]
    for tag in ("a3", "a3b"):
        d = "arm-%s-model/p65_%s-" % (tag, tag)
        sets.append((d + "items_map.tsv", d + "codes_coder1.tsv", d + "codes_coder2.tsv", d + "adjudication.tsv"))
    armA_cell = {r["item"]: r["cell"] for r in tsv("arm-a3-model/p65_a3-armA-cells.tsv")}
    for mp, c1, c2, adj in sets:
        m = {r["item"]: r for r in tsv(mp)}
        k1 = {r["item"]: r["class"] for r in tsv(c1)}
        k2 = {r["item"]: r["class"] for r in tsv(c2)}
        ad = {r["item"]: r["class"] for r in tsv(adj)}
        for it, r in m.items():
            if it not in k1:  # gold items are not in the map; anything else missing is an error
                raise SystemExit("no code for " + it)
            final = k1[it] if k1[it] == k2[it] else ad[it]
            cell = r.get("cell") or armA_cell[it]
            truth[(r["treebank"], r["sent_id"])] = (final, weight[cell], cell)
    return truth


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--seed", type=int, default=20261130)
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    outdir = os.path.join(a.root, "wave3", "pilot")
    os.makedirs(outdir, exist_ok=True)

    # ---------- English validation ----------
    hits = collections.Counter()
    en = load(a.root, ["UD_English-EWT", "UD_English-GUM"], "en", hits)
    flags = {("en_ewt" if tb.endswith("EWT") else "en_gum", sid): (t, pb, pn) for tb, sid, n, t, pb, pn, q in en}
    truth = english_truth(a.root)
    miss = [k for k in truth if k not in flags]
    print("ENGLISH VALIDATION (Arm A + A3 + A3b final classes, n %d; matched %d; unmatched %d)"
          % (len(truth), len(truth) - len(miss), len(miss)))
    if miss:
        raise SystemExit("unmatched sentence ids: %s" % miss[:5])
    items = [(truth[k][0], truth[k][1], truth[k][2]) + flags[k] for k in truth]
    pool_w = sum(w for _, w, *_ in items)
    print("  weighted pool %.0f (A3b eligible population 30,526: weight check)" % pool_w)

    def metrics(its, which):
        ix = {"time": 3, "broad": 4, "narrow": 5}
        def flag(x):
            return x[3] and x[ix[which]] if which != "time" else x[3]
        both = lambda x: x[0] != "NA"
        dirl = lambda x: x[0] in ("TP", "PT")
        sw = lambda f: sum(x[1] for x in its if f(x))
        F = sw(flag); B = sw(both); D = sw(dirl)
        return dict(flag_share=F / pool_w, rec_both=sw(lambda x: both(x) and flag(x)) / B,
                    rec_dir=sw(lambda x: dirl(x) and flag(x)) / D,
                    prec_both=sw(lambda x: both(x) and flag(x)) / F, ppv_dir=sw(lambda x: dirl(x) and flag(x)) / F,
                    rec_TP=sw(lambda x: x[0] == "TP" and flag(x)) / sw(lambda x: x[0] == "TP"),
                    rec_PT=sw(lambda x: x[0] == "PT" and flag(x)) / sw(lambda x: x[0] == "PT"))
    cells = collections.defaultdict(list)
    for x in items:
        cells[x[2]].append(x)
    rng = random.Random(a.seed + 1)
    res = {}
    for which in ("broad", "narrow"):
        m = metrics(items, which)
        bs = collections.defaultdict(list)
        for _ in range(a.boot):
            s = [rng.choice(v) for v in cells.values() for _ in v]
            mm = metrics(s, which)
            for k, v in mm.items():
                bs[k].append(v)
        res[which] = (m, {k: (sorted(v)[int(0.025 * a.boot)], sorted(v)[int(0.975 * a.boot) - 1]) for k, v in bs.items()})
        print("  screen TIME and %s PLACE:" % which.upper())
        for k in ("flag_share", "rec_both", "prec_both", "rec_dir", "ppv_dir", "rec_TP", "rec_PT"):
            lo, hi = res[which][1][k]
            print("    %-10s %.3f  (95%% cell bootstrap %.3f to %.3f)" % (k, m[k], lo, hi))
    # unweighted confusion on the coded set, as a readable check
    for which, ix in (("broad", 4), ("narrow", 5)):
        cc = collections.Counter((x[0], bool(x[3] and x[ix])) for x in items)
        print("  unweighted coded-set counts, %s: %s" % (which, ", ".join("%s/%s %d" % (k[0], "flag" if k[1] else "noflag", v)
                                                                          for k, v in sorted(cc.items()))))
    tmiss = collections.Counter(x[0] for x in items if x[0] in ("TP", "PT") and not x[3])
    print("  directional items with NO time flag (time-screen misses, unweighted): %s" % dict(tmiss))
    print("  English census: %d sentences" % len(en))

    # ---------- per language ----------
    print("\nPER LANGUAGE (seed %d, %d-sentence draw; census = whole treebank)" % (a.seed, a.n))
    print("  D = N x r x PPV_dir(English); PPV_dir broad %.4f, narrow %.4f (English, weighted)"
          % (res["broad"][0]["ppv_dir"], res["narrow"][0]["ppv_dir"]))
    print("  columns: language, verdict, N | draw: screen-positive k/500 = r [Wilson 95%] | census r_broad r_narrow r_time "
          "r_time+quantity | D_broad from draw [95%] | D_broad census | D_narrow census | TOTAL directional = D_broad census / rec_dir_broad(English)")
    lexhits = {}
    for name, lang, tbs, verdict in LANGS:
        hits = collections.Counter()
        S = load(a.root, tbs, lang, hits)
        lexhits[name] = hits
        N = len(S)
        rng = random.Random("%d:%s" % (a.seed, name))
        draw = rng.sample(sorted(S, key=lambda x: (x[0], x[1])), min(a.n, N))
        with open(os.path.join(outdir, "p65_wave3_yield-draw_%s.tsv" % name), "w", encoding="utf-8") as f:
            f.write("treebank\tsent_id\ttokens\ttime\tplace_broad\tplace_narrow\tquantity\n")
            for x in draw:
                f.write("\t".join(map(str, x[:3])) + "\t" + "\t".join(str(int(v)) for v in x[3:]) + "\n")
        kd = sum(1 for x in draw if x[3] and x[4]); lo, hi = wilson(kd, len(draw))
        rb = sum(1 for x in S if x[3] and x[4]) / N
        rn = sum(1 for x in S if x[3] and x[5]) / N
        rt = sum(1 for x in S if x[3]) / N
        rq = sum(1 for x in S if x[3] and x[6]) / N
        pb, pn = res["broad"][0]["ppv_dir"], res["narrow"][0]["ppv_dir"]
        print("  %-14s %-9s %7d | %3d/%d = %.3f [%.3f-%.3f] | %.3f %.3f %.3f %.3f | %5.0f [%.0f-%.0f] | %5.0f | %5.0f | %5.0f"
              % (name, verdict, N, kd, len(draw), kd / len(draw), lo, hi, rb, rn, rt, rq,
                 N * kd / len(draw) * pb, N * lo * pb, N * hi * pb, N * rb * pb, N * rn * pn,
                 N * rb * pb / res["broad"][0]["rec_dir"]))
    print("\nLEXICON CHECK (entries matched at least once per language / entries listed; zero-hit entries listed)")
    for name, lang, tbs, verdict in LANGS:
        h = lexhits[name]
        used = {k.split(":", 2)[2] for k in h if k.startswith("T:lex:")}
        listed = CFG[lang]["TIME"]
        dead = sorted(listed - used)
        print("  %-14s time lex %d/%d used; zero-hit: %s" % (name, len(listed & used), len(listed), " ".join(dead[:25])))
        print("  %-14s top time cues: %s" % ("", ", ".join("%s %d" % kv for kv in h.most_common(8) if kv[0].startswith("T"))))


if __name__ == "__main__":
    main()
