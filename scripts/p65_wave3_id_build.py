"""p65 wave 3, first preprint: Indonesian census draw, batches, gold items. NEVER calls a model; no direction is read.

Registration Section 2.2a: every sentence of Indonesian GSD + CSUI (UD r2.18; train, dev, test; 6,628). The yield pilot's
500 (seed 20261130, string seed 20261130:Indonesian) is batch P01. The other 6,128 are ONE uniform permutation (string
seed 20261131:Indonesian), batches of 400: M01..M16 (M16 holds 128). Gold (S2): five constructed Indonesian items per
batch (TP, PT, PAR, and two NA), distinct wordings per batch, inserted and shuffled in with Random(20261135) used batch
by batch in order; keyed in gold_key.tsv. Blind ids run consecutively through a stage including the gold slots.
Coders see item, previous sentence (previous sentence of the treebank file), sentence. English translations in the
treebank are never read (registration 4.3).
Amendment 3 (2026-11-17, S1 second pilot, registration Section 9): batch P02 = 300 sentences drawn from the census minus
P01 (string seed 20261132:Indonesian, the registration's `20261132:<language>` in the form the other seeds use), plus
an 18th gold set, shuffled in by the same Random(20261135) continued after the 17 batches. P02 ids continue the P
stage (P0506 on). The M batches are untouched: a P02 sentence is also coded in its M batch, and the analysis reads the M
codes only (P02 serves S1). census_map.tsv is unchanged; P02_map.tsv carries the P02 mapping.

Text is not committed (registration Section 1): *_blind/_coder*_input.tsv are git-ignored and rebuilt from data/ud;
batches_sha256.tsv commits their hashes. Committed: census_map.tsv, *_map.tsv, gold_key.tsv, batches_sha256.tsv.

  python3 -I scripts/p65_wave3_id_build.py             dry run: counts, checks, writes nothing
  python3 -I scripts/p65_wave3_id_build.py --build     write wave3/main/batches and census_map.tsv
  python3 -I scripts/p65_wave3_id_build.py --selftest  controls
"""
import argparse, collections, csv, glob, hashlib, importlib.util, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "wave3", "main")
TBS = ["UD_Indonesian-GSD", "UD_Indonesian-CSUI"]
SEED_PILOT, SEED_MAIN, SEED_GOLD = "20261130:Indonesian", "20261131:Indonesian", 20261135
SEED_PILOT2, N_PILOT2 = "20261132:Indonesian", 300   # amendment 3, registration 9 S1
BATCH, N_GOLD, N_PILOT, N_CENSUS = 400, 5, 500, 6628
CHECKSUMS = os.path.join(ROOT, "wave3", "p65_wave3_ud-checksums_r2.18.tsv")

# ---- gold: 17 distinct wordings per kind, all constructed (not corpus sentences) ------------------------------------
TP = [("pukul delapan", "para kru", "studio"), ("pukul enam", "para pilot", "lapangan terbang"),
      ("senja", "para pendaki", "penginapan"), ("siang hari", "para petani", "pasar"),
      ("pagi hari", "para perawat", "klinik"), ("pukul tiga", "para penyelam", "dermaga"),
      ("malam hari", "para gembala", "kandang"), ("pukul sepuluh", "para mahasiswa", "asrama"),
      ("waktu makan siang", "para penjaga", "gerbang"), ("pukul lima", "para juru masak", "dapur"),
      ("tengah malam", "para nelayan", "pelabuhan"), ("pukul tujuh", "para guru", "sekolah"),
      ("subuh", "para pedagang", "terminal"), ("pukul empat", "para pekerja", "pabrik"),
      ("sore hari", "para petugas", "kantor pos"), ("pukul sembilan", "para tamu", "hotel"),
      ("menjelang malam", "para pemain", "stadion"),
      ("pukul dua siang", "para montir", "bengkel")]                       # 18th set: P02 (amendment 3)
PT = [("Kairo", "Rabu malam"), ("Mumbai", "lewat tengah malam"), ("Tokyo", "Kamis pagi"), ("Lima", "siang hari"),
      ("Oslo", "malam hari"), ("Perth", "Senin malam"), ("Nairobi", "sore hari"), ("Seoul", "Jumat subuh"),
      ("Dublin", "pukul enam lewat tiga puluh"), ("Cusco", "Minggu sore"), ("Sydney", "Selasa pagi"),
      ("Madrid", "pukul dua dini hari"), ("Dakar", "pukul lima pagi"), ("Hanoi", "Sabtu malam"),
      ("Quito", "Rabu siang"), ("Manila", "Jumat sore"), ("Warsawa", "pukul sebelas malam"), ("Lisboa", "Kamis sore")]
PAR = [("Kami makan siang", "taman", "Minggu"), ("Mereka sarapan", "teras", "Sabtu"),
       ("Dia membaca buku", "perpustakaan", "Selasa"), ("Anak-anak bermain bola", "pantai", "Senin"),
       ("Ayah menunggu bus", "pojok jalan", "Rabu"), ("Kami menonton pertandingan", "kafe", "Minggu"),
       ("Mereka berenang", "danau", "Jumat"), ("Saya menelepon ibu", "stasiun", "Minggu"),
       ("Band itu berlatih", "garasi", "Selasa"), ("Kami piknik", "bukit", "Sabtu"),
       ("Nenek memetik bunga", "kebun", "Kamis"), ("Para tetangga berkumpul", "balai desa", "Jumat"),
       ("Adik menggambar", "halaman", "Senin"), ("Kakek memancing", "sungai", "Rabu"),
       ("Kami berdiskusi", "kantin", "Kamis"), ("Dia berlari", "lapangan", "Sabtu"),
       ("Mereka menjahit", "bengkel", "Selasa"), ("Paman memperbaiki sepeda", "gudang", "Jumat")]
NAP = [("Truk-truk bongkar muatan", "gerbang belakang"), ("Kapal-kapal menunggu", "dermaga"),
       ("Para turis berfoto", "alun-alun"), ("Bus-bus berhenti", "terminal utara"),
       ("Mobil-mobil parkir", "halaman belakang"), ("Kuda-kuda merumput", "padang"),
       ("Tenda-tenda berdiri", "lapangan"), ("Para pelari berkumpul", "gerbang"),
       ("Sepeda-sepeda bersandar", "pagar"), ("Kursi-kursi ditata", "aula"),
       ("Perahu-perahu tertambat", "teluk"), ("Toko-toko berjajar", "gang sempit"),
       ("Burung-burung bertengger", "atap"), ("Para siswa antre", "kantin"),
       ("Kereta-kereta menunggu", "peron"), ("Pedagang menggelar dagangan", "pasar"),
       ("Para penari berlatih", "panggung"), ("Lampu-lampu menyala", "lorong")]
NAT = [("Senin", "para siswa", "tugas itu"), ("Selasa", "para penerjemah", "naskah itu"),
       ("Rabu", "kakak", "lukisannya"), ("Kamis", "para teknisi", "pekerjaan itu"),
       ("Jumat", "Ibu", "laporan keuangan"), ("Sabtu", "para pelukis", "mural itu"),
       ("Minggu", "kami", "resep baru"), ("Senin", "para editor", "buku itu"),
       ("Selasa", "para penulis", "cerita pendek itu"), ("Rabu", "adik", "pekerjaan rumahnya"),
       ("Kamis", "para peneliti", "analisis itu"), ("Jumat", "Ayah", "anyaman itu"),
       ("Sabtu", "para siswa", "ujian itu"), ("Minggu", "mereka", "teka-teki itu"),
       ("Senin", "para dokter", "pemeriksaan itu"), ("Selasa", "kami", "daftar belanja"),
       ("Rabu", "para pelajar", "presentasi itu"), ("Kamis", "para tukang", "pagar itu")]
N_BATCHES = 17   # P01 + M01..M16


def gold_sets():
    sets = []
    for k in range(N_BATCHES + 1):   # + P02 (amendment 3)
        t, g, p = TP[k]; c, w = PT[k]; s, l, h = PAR[k]; sp, lp = NAP[k]; d, o, ob = NAT[k]
        sets.append([(f"Pada {t} {g} sudah kembali di {p}.", "TP"), (f"Di {c} sudah {w}.", "PT"),
                     (f"{s} di {l} pada hari {h}.", "PAR"), (f"{sp} di {lp}.", "NA"),
                     (f"Pada hari {d} {o} menyelesaikan {ob}.", "NA")])
    return sets


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def read_census():
    """[(key, treebank, sent_id, text, previous_text)] in sorted file order; previous within the same file only."""
    out = []
    for tb in TBS:
        for p in sorted(glob.glob(os.path.join(ROOT, "data", "ud", "r2.18", tb, "*-ud-*.conllu"))):
            if not re.search(r"-ud-(train|dev|test)\.conllu$", p):
                continue
            prev = ""
            for blk in open(p, encoding="utf-8").read().split("\n\n"):
                if not blk.strip():
                    continue
                sid = re.search(r"^# sent_id = (.*)$", blk, re.M).group(1)
                txt = re.search(r"^# text = (.*)$", blk, re.M).group(1)
                forms = [l.split("\t")[1] for l in blk.split("\n") if l and l[0].isdigit() and len(l.split("\t")) == 10]
                if all(f == "_" for f in forms):
                    continue
                out.append((f"{tb}|{sid}", tb, sid, txt, prev))
                prev = txt
    return out


def pilot_keys():
    p = os.path.join(ROOT, "wave3", "pilot", "p65_wave3_yield-draw_Indonesian.tsv")
    return [f"{r['treebank']}|{r['sent_id']}" for r in csv.DictReader(open(p, encoding="utf-8"), delimiter="\t")]


def reproduce_pilot(census, seed=SEED_PILOT):
    univ = sorted(census, key=lambda x: (x[1], x[2]))
    return [x[0] for x in random.Random(seed).sample(univ, N_PILOT)]


def screen_flags():
    spec = importlib.util.spec_from_file_location("yp", os.path.join(ROOT, "scripts", "p65_wave3_yield_pilot.py"))
    yp = importlib.util.module_from_spec(spec); spec.loader.exec_module(yp)
    S = yp.load(ROOT, TBS, "id", collections.Counter())
    return {f"{x[0]}|{x[1]}": (int(x[3]), int(x[4])) for x in S}


def pilot2_draw(census, pilot, seed=SEED_PILOT2):
    """Amendment 3: the S1 second pilot, 300 from the census minus P01, same universe order as reproduce_pilot."""
    ps = set(pilot)
    univ = sorted((x for x in census if x[0] not in ps), key=lambda x: (x[1], x[2]))
    return [x[0] for x in random.Random(seed).sample(univ, N_PILOT2)]


def main_order(census, pilot):
    ps = set(pilot)
    rest = sorted((x for x in census if x[0] not in ps), key=lambda x: (x[1], x[2]))
    random.Random(SEED_MAIN).shuffle(rest)
    return rest


def checks(census, pilot):
    assert len(census) == N_CENSUS, len(census)
    assert len({x[0] for x in census}) == N_CENSUS
    assert len(pilot) == N_PILOT and len(set(pilot)) == N_PILOT and set(pilot) <= {x[0] for x in census}
    assert reproduce_pilot(census) == pilot, "pilot draw not reproduced from its registered seed"
    assert reproduce_pilot(census, "20261130:Other") != pilot, "pilot-reproduction control cannot fail"
    gs = gold_sets()
    texts = [g[0] for s in gs for g in s]
    assert len(set(texts)) == len(texts) == (N_BATCHES + 1) * N_GOLD, "gold wordings not all distinct"
    assert not set(texts) & {x[3] for x in census}, "a gold sentence equals a corpus sentence"
    return gs


def verify_checksums():
    bad = 0
    for line in open(CHECKSUMS, encoding="utf-8"):
        r = line.rstrip("\n").split("\t")
        if r[0] in TBS and r[1].endswith(".conllu"):
            if sha(os.path.join(ROOT, "data", "ud", "r2.18", r[0], r[1])) != r[3]:
                bad += 1
    assert bad == 0, f"{bad} treebank files differ from the committed r2.18 checksums"


def build(out, write):
    verify_checksums()
    census = read_census(); pilot = pilot_keys(); gs = checks(census, pilot)
    by = {x[0]: x for x in census}
    main = main_order(census, pilot)
    stages = [("P", [by[k] for k in pilot])] + [("M", main)]
    batches = [("P01", "P", [by[k] for k in pilot])] + \
              [(f"M{i + 1:02d}", "M", main[i * BATCH:(i + 1) * BATCH]) for i in range((len(main) + BATCH - 1) // BATCH)]
    assert len(batches) == N_BATCHES and sum(len(b[2]) for b in batches) == N_CENSUS
    p2 = pilot2_draw(census, pilot)
    assert len(p2) == N_PILOT2 and not set(p2) & set(pilot) and set(p2) <= {x[0] for x in main}
    batches.append(("P02", "P", [by[k] for k in p2]))   # after the 17, so the gold Random(20261135) continues in order
    print(f"census {len(census)} (pilot {len(pilot)} + main {len(main)}), batches {[(b[0], len(b[2])) for b in batches][:3]} "
          f"... {batches[-2][0]} {len(batches[-2][2])}, second pilot {batches[-1][0]} {len(batches[-1][2])}; "
          f"gold {N_GOLD} per batch = {(N_BATCHES + 1) * N_GOLD}")
    if not write:
        print("dry run: nothing written"); return
    flags = screen_flags()
    bd = os.path.join(out, "batches"); os.makedirs(bd, exist_ok=True)
    rng = random.Random(SEED_GOLD)
    nid = {"P": 0, "M": 0}; rank = {"P": 0, "M": 0}
    gold_rows, cm, hashes = [], [], []
    for bi, (name, pre, rows) in enumerate(batches):
        items = [("S", x) for x in rows] + [("G", g) for g in gs[bi]]
        rng.shuffle(items)
        blind, mp = [], []
        for kind, x in items:
            nid[pre] += 1; iid = f"{pre}{nid[pre]:04d}"
            if kind == "S":
                rank[pre] += 1
                fl = flags[x[0]]
                blind.append((iid, x[4], x[3]))
                mp.append((iid, "sentence", x[0], f"{pre}{rank[pre]:04d}", name, str(fl[0]), str(fl[1])))
                if name != "P02":   # P02 sentences keep their M-batch row in census_map.tsv (amendment 3)
                    cm.append((x[0], x[1], x[2], "pilot" if pre == "P" else "main", name, iid, str(fl[0]), str(fl[1])))
            else:
                blind.append((iid, "", x[0])); mp.append((iid, "gold", "", "", name, "", ""))
                gold_rows.append((iid, name, x[1], x[0]))
        for fn in (f"{name}_blind.tsv", f"{name}_coder1_input.tsv", f"{name}_coder2_input.tsv"):
            p = os.path.join(bd, fn)
            with open(p, "w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh, delimiter="\t", lineterminator="\n")
                w.writerow(["item", "previous_sentence", "sentence"]); w.writerows(blind)
            hashes.append((fn, sha(p)))
        with open(os.path.join(bd, f"{name}_map.tsv"), "w", encoding="utf-8") as fh:
            fh.write("item\tkind\tsource_key\trank\tbatch\tscreen_time\tscreen_place\n")
            for r in mp:
                fh.write("\t".join(r) + "\n")
    with open(os.path.join(bd, "gold_key.tsv"), "w", encoding="utf-8") as fh:
        fh.write("item\tbatch\tkey\ttext\n")
        for iid, name, key, txt in gold_rows:
            fh.write(f"{iid}\t{name}\t{key}\t{txt}\n")
    with open(os.path.join(out, "census_map.tsv"), "w", encoding="utf-8") as fh:
        fh.write("source_key\ttreebank\tsent_id\tset\tbatch\titem\tscreen_time\tscreen_place\n")
        for r in cm:
            fh.write("\t".join(r) + "\n")
    with open(os.path.join(bd, "batches_sha256.tsv"), "w", encoding="utf-8") as fh:
        for fn, h in hashes:
            fh.write(f"{h}\t{fn}\n")
    print(f"built {len(batches)} batches (17 + P02), {sum(nid.values())} items incl. {len(gold_rows)} gold, in {bd}")


def selftest():
    c = [("a|1", "a", "1", "x", ""), ("a|2", "a", "2", "y", "")]
    assert [x[0] for x in main_order(c, ["a|1"])] == ["a|2"]
    gs = gold_sets()
    assert len(gs) == N_BATCHES + 1 and all(len(s) == N_GOLD for s in gs)
    assert [g[1] for g in gs[0]] == ["TP", "PT", "PAR", "NA", "NA"]
    # amendment 3 (S1 second pilot): 300 drawn from the census minus P01, reproducible from the registered string seed,
    # a wrong seed must not reproduce it; an 18th gold set exists and all 90 wordings are distinct
    c = [(f"a|{i}", "a", f"{i:04d}", f"t{i}", "") for i in range(1000)]
    pil = [f"a|{i}" for i in range(0, 1000, 2)]
    d = pilot2_draw(c, pil)
    assert len(d) == N_PILOT2 == 300 and len(set(d)) == 300 and not set(d) & set(pil), "second pilot overlaps P01 or wrong size"
    assert d == pilot2_draw(c, pil) and d != pilot2_draw(c, pil, "20261132:Other"), "second pilot draw not reproducible / control"
    assert len(gs) == N_BATCHES + 1 and len({g[0] for s_ in gs for g in s_}) == (N_BATCHES + 1) * N_GOLD
    print("selftest OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true"); ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    selftest() if a.selftest else build(a.out, a.build)
