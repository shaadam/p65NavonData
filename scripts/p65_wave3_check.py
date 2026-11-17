"""p65 wave 3 (Indonesian) batch checker: DIRECTION-BLIND. Every printed line passes say(), which refuses any text
containing '>' or the direction labels TP / PT. Counts of directional items are printed pooled only.

  merge UNIT ROLE      concatenate the role's part files, validate, write codes/UNIT_ROLE.tsv, print format and gold score
  sheet UNIT           write codes/UNIT_adjudication-sheet.tsv (rows where the two coders differ, gold excluded)
  validate-adj UNIT    check codes/UNIT_adjudication.tsv against the sheet
  gate [UNIT]          S1 on the pilot P01 (bar S1_FIRST 0.40), or on the second pilot P02 (bar S1_SECOND 0.60 on D-kappa;
                       amendment 3): P-kappa and D-kappa, printed as numbers only
  selftest             planted controls
Importable: LABELS, kappa, read_codes, parts_for.
"""
import csv, math, os, random, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.environ.get("P65_W3_MAIN") or os.path.join(ROOT, "wave3", "main")
BATCHES, CODES = os.path.join(MAIN, "batches"), os.path.join(MAIN, "codes")
LABELS = ("TP", "PT", "PAR", "AMB", "NA")
DIRECTIONAL = ("TP", "PT")
N_PARTS, GOLD_MISS_RECODE = 5, 2
S1_FIRST = 0.40
S1_SECOND = 0.60   # registration 9 S1: second pilot's D-kappa below this -> every result exploratory (amendment 3)
SHEET_SEED = "20261122"
BAD = re.compile(r">|\bTP\b|\bPT\b")


def say(*a):
    t = " ".join(str(x) for x in a)
    assert not BAD.search(t), "direction-blindness: refused to print: " + t[:40]
    print(t)


def read_tsv(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))


def ids_of(unit, role):
    return [r["item"] for r in read_tsv(os.path.join(BATCHES, f"{unit}_{role}_input.tsv"))]


def parts_for(unit, role):
    ids = ids_of(unit, role); per = math.ceil(len(ids) / N_PARTS)
    return [(f"{unit}_{role}_part{j + 1}.tsv", ids[j * per:(j + 1) * per]) for j in range(N_PARTS) if j * per < len(ids)]


def read_codes(path, ids):
    """Validated rows {item: row}. Raises ValueError on any format defect."""
    with open(path, newline="", encoding="utf-8") as f:
        lines = f.read().rstrip("\n").split("\n")
    if lines[0].split("\t") != ["item", "label", "phrase_time", "phrase_place", "confidence", "note"]:
        raise ValueError("header")
    out = {}
    for ln in lines[1:]:
        c = ln.split("\t")
        if len(c) == 5:  # amendment 1 (2026-11-17): coders drop the trailing EMPTY note column; pad it, loosen nothing else
            c.append("")
        if len(c) != 6 or c[1] not in LABELS or c[4] not in ("1", "2", "3"):
            raise ValueError("row " + c[0])
        out[c[0]] = dict(item=c[0], label=c[1], conf=c[4])
    if [l.split("\t")[0] for l in lines[1:]] != list(ids):
        raise ValueError("ids differ from the range, in order")
    return out


def gold_key():
    return {r["item"]: r["key"] for r in read_tsv(os.path.join(BATCHES, "gold_key.tsv"))}


def gold_missed(codes, gk):
    return sum(1 for i, k in gk.items() if i in codes and codes[i]["label"] != k)


def merge(unit, role):
    allids, rows = ids_of(unit, role), {}
    for fn, ids in parts_for(unit, role):
        rows.update(read_codes(os.path.join(CODES, fn), ids))
    assert list(rows) == allids
    with open(os.path.join(CODES, f"{unit}_{role}.tsv"), "w", encoding="utf-8") as f:
        f.write("item\tlabel\tconfidence\n")
        for i in allids:
            f.write(f"{i}\t{rows[i]['label']}\t{rows[i]['conf']}\n")
    gm = gold_missed(rows, gold_key())
    return rows, gm


def load_merged(unit, role):
    return {r["item"]: r["label"] for r in read_tsv(os.path.join(CODES, f"{unit}_{role}.tsv"))}


def sheet(unit):
    c1, c2 = load_merged(unit, "coder1"), load_merged(unit, "coder2")
    gk = gold_key()
    inp = {r["item"]: r for r in read_tsv(os.path.join(BATCHES, f"{unit}_coder1_input.tsv"))}
    diff = [i for i in c1 if i not in gk and c1[i] != c2[i]]
    rng = random.Random(f"{SHEET_SEED}:{unit}")
    rng.shuffle(diff)
    with open(os.path.join(CODES, f"{unit}_adjudication-sheet.tsv"), "w", encoding="utf-8") as f:
        f.write("row\titem\tprevious_sentence\tsentence\tcode_A\tcode_B\n")
        for n, i in enumerate(diff, 1):
            a, b = (c1[i], c2[i]) if rng.random() < 0.5 else (c2[i], c1[i])
            f.write(f"{n}\t{i}\t{inp[i]['previous_sentence']}\t{inp[i]['sentence']}\t{a}\t{b}\n")
    return len(diff), len(c1) - len([i for i in c1 if i in gk])


def validate_adj(unit):
    sh = read_tsv(os.path.join(CODES, f"{unit}_adjudication-sheet.tsv"))
    p = os.path.join(CODES, f"{unit}_adjudication.tsv")
    lines = open(p, encoding="utf-8").read().rstrip("\n").split("\n")
    if lines[0].split("\t") != ["row", "item", "final", "rule"]:
        raise ValueError("header")
    rows = [l.split("\t") for l in lines[1:]]
    if len(rows) != len(sh) or any(len(r) != 4 or r[2] not in LABELS or r[0] != s["row"] or r[1] != s["item"]
                                   for r, s in zip(rows, sh)):
        raise ValueError("adjudication rows differ from the sheet")
    return len(rows)


def kappa(xs, ys):
    n = len(xs)
    if n == 0:
        return float("nan")
    po = sum(a == b for a, b in zip(xs, ys)) / n
    cx, cy = collections.Counter(xs), collections.Counter(ys)
    pe = sum(cx[c] * cy[c] for c in set(cx) | set(cy)) / n / n
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def agreement(c1, c2, exclude=()):
    """(P-kappa over present-or-not on all items, D-kappa over items both coders found present, n_both, raw presence agreement)."""
    its = [i for i in c1 if i not in exclude]
    p1 = ["NA" if c1[i] == "NA" else "P" for i in its]; p2 = ["NA" if c2[i] == "NA" else "P" for i in its]
    both = [i for i in its if c1[i] != "NA" and c2[i] != "NA"]
    pk = kappa(p1, p2); dk = kappa([c1[i] for i in both], [c2[i] for i in both])
    return pk, dk, len(both), sum(a == b for a, b in zip(p1, p2)) / max(1, len(its))


def gate(unit="P01", bar=S1_FIRST):
    """P01: both kappas against S1_FIRST (stop on failure). P02: D-kappa against S1_SECOND (label, never a stop)."""
    c1, c2 = load_merged(unit, "coder1"), load_merged(unit, "coder2")
    pk, dk, nb, raw = agreement(c1, c2, exclude=set(gold_key()))
    ok = (dk >= bar) if unit == "P02" else (pk >= bar and dk >= bar)
    verdict = ("PASS" if ok else "STOP") if unit == "P01" else ("confirmatory" if ok else "exploratory")
    say(f"S1 pilot {unit}: P-kappa {pk:.3f}, D-kappa {dk:.3f} on {nb} both-present items, raw presence agreement {raw:.3f}; "
        f"bar {bar}: {verdict}")
    return ok


def selftest():
    # direction-blindness control: a printed direction must be refused; a clean line must pass
    for bad in ("TP 3", "a > b", "x PT"):
        try:
            say(bad); raise SystemExit("control failed: direction line printed")
        except AssertionError:
            pass
    say("clean line passes")
    assert kappa(list("aabb"), list("aabb")) == 1.0 and abs(kappa(list("aabb"), list("abab"))) < 1e-9
    c1 = {"a": "TP", "b": "NA", "c": "PT", "d": "PAR"}; c2 = {"a": "TP", "b": "NA", "c": "PAR", "d": "PAR"}
    pk, dk, nb, raw = agreement(c1, c2)
    assert pk == 1.0 and nb == 3 and raw == 1.0 and 0 < dk < 1
    assert kappa(list("aabbab"), list("bbaabb")) < S1_FIRST, "S1 control: discordant coders must fall below the bar"
    gk = {"g1": "TP", "g2": "NA"}
    assert gold_missed({"g1": {"label": "TP"}, "g2": {"label": "PT"}}, gk) == 1
    # amendment 3: the second-pilot bar is 0.60 and the gate function takes the unit and bar
    assert S1_SECOND == 0.60
    assert kappa(list("aabbab"), list("ababba")) < S1_SECOND < kappa(list("aabbab"), list("aabbaa")), "S1_SECOND control"
    assert gate.__code__.co_argcount == 2, "gate(unit, bar) missing"
    say("selftest OK: blindness control refuses directions; kappa, agreement and gold score checked; second-pilot bar 0.60")


def main(argv):
    cmd = argv[1]
    if cmd == "selftest":
        return selftest()
    if cmd == "merge":
        try:
            rows, gm = merge(argv[2], argv[3])
        except (ValueError, OSError, AssertionError) as e:
            say("FORMAT FAIL:", e); return 2
        say(f"{argv[2]} {argv[3]}: {len(rows)} rows, format ok, gold missed {gm}/5 "
            f"({'RECODE' if gm >= GOLD_MISS_RECODE else 'ok'})")
        return 3 if gm >= GOLD_MISS_RECODE else 0
    if cmd == "sheet":
        n, tot = sheet(argv[2]); say(f"{argv[2]}: sheet {n} rows of {tot} sentences"); return 0
    if cmd == "validate-adj":
        try:
            say(f"{argv[2]}: adjudication ok, {validate_adj(argv[2])} rows"); return 0
        except (ValueError, OSError) as e:
            say("ADJUDICATION FAIL:", e); return 2
    if cmd == "gate":
        u = argv[2] if len(argv) > 2 else "P01"
        return 0 if gate(u, S1_SECOND if u == "P02" else S1_FIRST) else 4


if __name__ == "__main__":
    sys.exit(main(sys.argv))
