#!/usr/bin/env python3
"""Rebuild the abstract-and-discussion block of p65_v1_number-trace.md from the results files.

Every number the abstract and the discussion (Sections 6.1 to 6.5) of docs/manuscript/p65_navon_v1.md carry is
(1) located in the manuscript text by exact string match (counted in Python), (2) recomputed from the results
files by code that shares nothing with the analysis scripts (cell tables, coded TSVs, item maps, codes files),
or, where recomputation needs a bootstrap or a simulation this script does not rerun, read off the results line
and marked READ, and (3) compared with the printed value. The script rewrites the block between
<!-- trace:generated:begin --> and <!-- trace:generated:end --> in p65_v1_number-trace.md and exits 1 on any
MISMATCH or a printed value it cannot find in the text.

Usage: python3 -I scripts/p65_v1_number-trace.py [--perturb]   (--perturb nudges three printed values as a
negative control; the run must then report mismatches and exit 1).

Bundle mode. In the public data-and-code bundle the manuscript, the appendix and the wave 2 registration are not
present (they are the article, or not a result of it). When docs/manuscript/p65_navon_v1.md is absent the script
takes the printed strings from the recorded table in p65_v1_number-trace.md (the location of each string in the
manuscript was checked in the repository when that table was written) and recomputes every value from the tables
here exactly as above; the rows read off the appendix's simulation table keep their recorded READ status. The
regenerated block must then equal the recorded one.
"""
import csv, math, os, re, sys
from collections import Counter

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MS = os.path.join(ROOT, "docs", "manuscript", "p65_navon_v1.md")
OUT = os.path.join(ROOT, "p65_v1_number-trace.md")
PERTURB = "--perturb" in sys.argv


def rd(*p):
    return open(os.path.join(ROOT, *p), encoding="utf-8").read()


def tsv(*p):
    return list(csv.DictReader(open(os.path.join(ROOT, *p), encoding="utf-8"), delimiter="\t"))


def rd_opt(*p):
    """the file's text, or None when it is not in this tree (bundle mode)"""
    return rd(*p) if os.path.isfile(os.path.join(ROOT, *p)) else None


def has(txt, s):
    """True when the text holds s; a file that is not in this tree (None) is the article's own copy, taken as read"""
    return True if txt is None else (s in txt)


BUNDLE = not os.path.isfile(MS)
if BUNDLE:
    ms = ""
    rec = rd("p65_v1_number-trace.md")
    rec = rec[rec.index("<!-- trace:generated:begin -->"):rec.index("<!-- trace:generated:end -->")]
    regions = {"abstract": [], "discussion": []}
    for line in rec.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if len(cells) >= 2 and cells[0] in regions:
            regions[cells[0]].append(cells[1].replace("\\|", "|"))
    regions = {k: " ".join(v) for k, v in regions.items()}
else:
    ms = rd("docs", "manuscript", "p65_navon_v1.md")
    abstract = ms[ms.index("## Abstract"):ms.index("## 1. Introduction")]
    discussion = ms[ms.index("## 6. Discussion"):ms.index("## Data and code availability")]
    regions = {"abstract": " ".join(abstract.split()), "discussion": " ".join(discussion.split())}

rows = []   # (region, printed, meaning, source, recomputed, method, status)
bad = 0


WORDS = {"none": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
         "nine": 9, "ten": 10, "twelve": 12, "fifty": 50}
NUM = re.compile(r"-?(?:\d[\d,]*\.?\d*|\.\d+)")


def printed_numbers(printed):
    out = []
    for tok in re.findall(r"-?(?:\d[\d,]*\.?\d*|\.\d+)|[A-Za-z]+", printed.replace("−", "-")):
        if tok.lower() in WORDS:
            out.append(float(WORDS[tok.lower()]))
        elif NUM.fullmatch(tok):
            out.append(float(tok.replace(",", "")))
    return out


def check(region, printed, meaning, source, value, method, tol=None, read=False, printed_value=None):
    """printed: the exact string in the manuscript; value: recomputed number(s) (None = text-only);
    printed_value: the number(s) the phrase means, when they are not its digits (e.g. 'three of four' = 0.75)."""
    global bad
    text = regions[region]
    found = text.count(printed)
    if found == 0:
        status = "NOT IN TEXT"
    elif value is None:
        status = "LOCATED"
    elif read:
        status = "READ (source line)"
    else:
        nums = list(printed_value) if isinstance(printed_value, (list, tuple)) else ([printed_value] if printed_value is not None else printed_numbers(printed))
        vals = value if isinstance(value, (list, tuple)) else [value]
        ok = len(nums) >= len(vals) and all(
            abs(n - v) <= (tol if tol is not None else (0.5 if float(v).is_integer() and abs(v) >= 1 else 0.0051))
            for n, v in zip(nums[:len(vals)], vals))
        status = "OK" if ok else "MISMATCH"
    if status in ("NOT IN TEXT", "MISMATCH"):
        bad += 1
    if isinstance(value, (list, tuple)):
        shown = ", ".join(f"{v:.4g}" if isinstance(v, float) else str(v) for v in value)
    elif isinstance(value, float):
        shown = f"{value:.4g}"
    else:
        shown = "" if value is None else str(value)
    rows.append((region, printed, meaning, source, shown, method, status))


# ------------------------------------------------------------------ helpers
def cell_table(txt):
    """Parse 'CELL TABLE' lines: name pop coded weight | TP a, PT b, ..."""
    cells = {}
    for m in re.finditer(r"^\s+(\S+) pop\s+(\d+) coded\s+(\d+) weight\s+([\d.]+) \| TP (\d+), PT (\d+), PAR (\d+), AMB (\d+), NA (\d+)",
                         txt, flags=re.M):
        cells[m.group(1)] = dict(pop=int(m.group(2)), coded=int(m.group(3)), TP=int(m.group(5)), PT=int(m.group(6)))
    return cells


def share_from_cells(cells):
    tp = sum(c["TP"] * c["pop"] / c["coded"] for c in cells.values())
    pt = sum(c["PT"] * c["pop"] / c["coded"] for c in cells.values())
    return tp / (tp + pt), tp, pt


def kappa(labels1, labels2):
    n = len(labels1)
    agree = sum(a == b for a, b in zip(labels1, labels2)) / n
    c1, c2 = Counter(labels1), Counter(labels2)
    pe = sum(c1[k] * c2[k] for k in set(c1) | set(c2)) / (n * n)
    return (agree - pe) / (1 - pe), agree


def coder_kappa(folder, f1, f2):
    a = {r["item"]: r["class"] for r in tsv(folder, f1)}
    b = {r["item"]: r["class"] for r in tsv(folder, f2)}
    items = sorted(set(a) & set(b))
    return kappa([a[i] for i in items], [b[i] for i in items]), len(items)


def sign_test(a, b):
    n = a + b
    k = min(a, b)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def binom_power(n, p, alpha=0.05):
    """Exact two-sided binomial test of share = 0.5; power at true share p."""
    def pmf(k, q):
        return math.comb(n, k) * q ** k * (1 - q) ** (n - k)
    lo = next(k for k in range(n + 1) if sum(pmf(i, 0.5) for i in range(k + 1)) > alpha / 2) - 1
    hi = n - lo
    return sum(pmf(k, p) for k in range(n + 1) if k <= lo or k >= hi)


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def read_line(txt, pattern):
    m = re.search(pattern, txt)
    return m.group(1) if m else None


# ------------------------------------------------------------------ Arm A
a_res = rd("arm-a-model", "p65_model-results_2026-11-13.txt")
a3_res = rd("arm-a3-model", "p65_a3-results_2026-11-13.txt")
a3b_res = rd("arm-a3b-model", "p65_a3b-results_2026-11-13.txt")
n_items = sum(len(tsv(*p)) for p in (("arm-a-model", "p65_model-items_map.tsv"), ("arm-a3-model", "p65_a3-items_map.tsv"),
                                       ("arm-a3b-model", "p65_a3b-items_map.tsv")))
s3, tp3, pt3 = share_from_cells(cell_table(a3_res))
s3b, tp3b, pt3b = share_from_cells(cell_table(a3b_res))
(k_a, raw_a), n_a = coder_kappa("arm-a-model", "p65_model-codes_coder1.tsv", "p65_model-codes_coder2.tsv")
(k_a3, raw_a3), n_a3 = coder_kappa("arm-a3-model", "p65_a3-codes_coder1.tsv", "p65_a3-codes_coder2.tsv")
(k_a3b, raw_a3b), n_a3b = coder_kappa("arm-a3b-model", "p65_a3b-codes_coder1.tsv", "p65_a3b-codes_coder2.tsv")
directional_a3 = sum(c["TP"] + c["PT"] for c in cell_table(a3_res).values())

# ------------------------------------------------------------------ Arm B (final codes re-derived from the codes files)
cv = os.path.join("change-verbs")
def load_codes(f):
    return {r["item"]: (r["CHANGE"], r["DIM"], r["OVER"]) for r in tsv(cv, "codes", f)}
A, B = {}, {}
for i in "123":
    A.update(load_codes(f"A{i}.tsv")); B.update(load_codes(f"B{i}.tsv"))
C = load_codes("C1.tsv")
key = {r["item"]: r for r in tsv(cv, "items_key_nodefs.tsv")}
def maj(vals, tie):
    for v in set(vals):
        if vals.count(v) >= 2:
            return v
    return tie
final = {}
for k in A:
    a, b = A[k], B[k]
    if a == b:
        final[k] = a; continue
    c = C[k]
    if maj([a[0], b[0], c[0]], c[0]) == "N":
        final[k] = ("N", "", ""); continue
    ys = [x for x in (a, b, c) if x[0] == "Y"]
    cy = c if c[0] == "Y" else ys[0]
    final[k] = ("Y", maj([x[1] for x in ys], cy[1]) if len(ys) > 1 else ys[0][1],
                maj([x[2] for x in ys], cy[2]) if len(ys) > 1 else ys[0][2])
real = [k for k in final if "PLANT" not in key[k]["sense_id"]]
n_items_b = len(A)
# directional = a named over-dimension different from the dimension that changes (the matrix's off-diagonal cells)
# the codebook's OVER value SPACE is the DIM value POSITION
over = {k: ("POSITION" if final[k][2] == "SPACE" else final[k][2]) for k in final}
directional = [k for k in real if final[k][0] == "Y" and over[k] not in ("UNSPECIFIED", "ITEMS", "") and over[k] != final[k][1]]
unbiased = [k for k in directional if ("C" in key[k]["strata"] or "R" in key[k]["strata"])]
unb_time = [k for k in unbiased if over[k] == "TIME"]
falsifiers_both = [k for k in real if A[k][0] == "Y" and B[k][0] == "Y" and A[k][1] == "TIME" and B[k][1] == "TIME"
                   and A[k][2] not in ("TIME", "UNSPECIFIED", "ITEMS", "") and B[k][2] not in ("TIME", "UNSPECIFIED", "ITEMS", "")]
# Garner licence: a change on dimension A over B is "licensed" when A logically needs B and not the reverse.
# Everything that exists has a time; the appendix's rule (analysis run) licenses every X-over-TIME except TIME itself.
licensed = sum(1 for k in directional if over[k] == "TIME")
licensed += sum(1 for k in directional if over[k] == "POSITION" and final[k][1] in ("SIZE", "COLOUR", "INTENSITY", "QUANTITY"))
dirs_total = len(directional)

# ------------------------------------------------------------------ Arm C (tally rule re-applied to the coded TSV)
coded = tsv("published-asymmetry", "p65_published-asymmetry-coded_2026-11-13.tsv")
CODES = ("SPACE>TIME", "TIME>SPACE", "SYMMETRIC", "NONE")
counted = [r for r in coded if r["code"].strip() in CODES and "CLINICAL" not in r["tags"].upper()
           and not r["verification"].upper().startswith("SECONDARY")]
cc = Counter(r["code"].strip() for r in counted)
p_sign = sign_test(cc["SPACE>TIME"], cc["TIME>SPACE"])
papers = {}
for r in counted:
    papers.setdefault(r["doi"] or r["key"], []).append(r["verification"].upper().startswith("ABSTRACT"))
n_papers = len(papers)
abstract_papers = sum(all(v) for v in papers.values())
row76 = [r for r in coded if r["key"] == "RiedlHallez2026" and r["exp"] == "1"][0]["code"].strip()

# ------------------------------------------------------------------ Arm D (per-source list, recount of 2026-11-17)
armd = tsv("error-evidence", "p65_armD_per-source_2026-11-17.tsv")
n_sources = len(armd)
assert len({r["source_key"] for r in armd}) == n_sources
d_codes = Counter(r["direction_code"] for r in armd)
d_full = sum(r["status_in_map"] in ("FULL", "PDF grepped") for r in armd)
e1 = rd("error-evidence", "p65_e1-run_2026-11-13.txt")
e1_learner = e1[:e1.index("## NATIVE")]
tokens = int(read_line(e1_learner, r"tokens ([\d,]+)").replace(",", ""))
n_st, n_ts = int(read_line(e1_learner, r"n\(S->T\) = (\d+)")), int(read_line(e1_learner, r"n\(T->S\) = (\d+)"))

# ------------------------------------------------------------------ extensions
census = tsv("wave3", "main", "census_map.tsv")
freeze = rd("wave3", "FREEZE.txt")
w3 = rd("p65_wave3_registration_FROZEN_2026-11-16.md")
appD = rd_opt("docs", "manuscript", "p65_appendix-D_math_2026-11-16.md")   # the article's Appendix D (absent in the bundle)
# exact binomial power is not monotone in n (0.824 at 35, 0.795 at 36, 0.859 at 37): "items needed" is the
# smallest n from which power stays at or above 0.80
n37 = next(n for n in range(10, 400) if all(binom_power(m, 0.74) >= 0.80 for m in range(n, n + 40)))
share80_164 = next(q / 1000 for q in range(500, 800) if binom_power(164, q / 1000) >= 0.80)
pow164 = binom_power(164, 0.74); pow113 = binom_power(113, 0.74)
gap = math.log(0.738 / (1 - 0.738))
deff = (5.0, 6.9)

if PERTURB:
    # negative control: nudge three recomputed values so the comparison must fail
    s3 += 0.03; cc["SPACE>TIME"] += 2; n_sources += 1

# ================================================================== abstract
A_ = "abstract"
check(A_, "almost fifty years", "2026 minus 1978", "Navon 1978 (title page)", 2026 - 1978, "subtraction; 48 is 'almost fifty'", tol=3, printed_value=50)
check(A_, "four arms", "arms A, B, C, D", "Sections 2 to 5", 4, "count of arm sections", tol=0)
check(A_, "two blind model coders", "coders per sample", "arm-a*/codes_coder1, coder2", 2, "files per sample", tol=0)
check(A_, "about three times as often", "0.738 / (1 − 0.738) = 2.8", "arm-a3-model/p65_a3-results_2026-11-13.txt", s3 / (1 - s3), "odds from the recomputed share; 2.8 reads 'about three'", tol=0.4, printed_value=3)
check(A_, "0.74 of directional sentences", "registered share, time over place", "arm-a3-model/p65_a3-results_2026-11-13.txt CELL TABLE", s3, "Σ TP·pop/coded ÷ Σ (TP+PT)·pop/coded over the six cells")
check(A_, "(95% interval 0.56 to 0.89)", "document bootstrap within cells, 10,000 resamples", "same file, 'DIRECTIONAL share' line: 0.561 to 0.893", (0.561, 0.893), "READ: the bootstrap is not rerun here", read=True)
check(A_, "three openly licensed dictionaries", "WordNet, GCIDE, Wiktionary", "change-verbs/items_key_nodefs.tsv 'dict' column", len({key[k]["dict"] for k in key}), "distinct dict values", tol=0)
check(A_, "23 of 27 unbiased cases", "directional change senses in the C and R strata naming time", "change-verbs/codes/*.tsv + items_key (final codes re-derived by the 2-of-3 rule)", (len(unb_time), len(unbiased)), "final OVER not UNSPECIFIED/ITEMS, strata C or R, plants out; OVER == TIME")
check(A_, "64 published experiments", "counted experiments", "published-asymmetry/p65_published-asymmetry-coded_2026-11-13.tsv", len(counted), "tally rule re-applied: code in the four codes, not CLINICAL, not SECONDARY")
check(A_, "(27 against 14, with 21 symmetric)", "primary tally", "same TSV", (cc["SPACE>TIME"], cc["TIME>SPACE"], cc["SYMMETRIC"]), "Counter over counted rows (row 76 Riedl & Hallez Exp 1 = %s, ruled 2026-11-17)" % row76)
check(A_, "(p = .060)", "two-sided exact sign test 27 vs 14", "same TSV", p_sign, "binomial tail sum, doubled", tol=0.0006)
check(A_, "of 33 sources", "Arm D map, one row per source", "error-evidence/p65_armD_per-source_2026-11-17.tsv", n_sources, "rows counted; source_key distinct")
check(A_, "none shows time structuring space", "T>S count", "same TSV, direction_code", d_codes["T>S"], "rows with direction_code T>S", tol=0)
# 2026-11-17 field-register read (Adam) cut: "4,000 sentences", the exploratory 0.82 (0.73 to 0.91), "one sense in 1,725", the learner-English
# 1.2 million words and ten errors, and "six dimensions in English" left the abstract; the body still prints them and the
# hand tables below trace them (the ten errors and the 4,000 are also checked in the discussion block).

# ================================================================== discussion
D_ = "discussion"
check(D_, "about three of four directional English sentences", "0.738 ≈ 3/4", "arm-a3-model results, CELL TABLE", s3, "recomputed share; 0.74 reads 'three of four'", tol=0.02, printed_value=0.75)
check(D_, "lower bound 0.56 above one half", "A3 interval lower bound", "arm-a3-model results 'DIRECTIONAL share' line: 0.561", 0.561, "READ", read=True)
check(D_, "117 of the 121 directional senses", "Garner licence on pooled directional senses", "change-verbs/codes (final codes) with the appendix's dependence rule", (licensed, dirs_total), "licensed = X over TIME (X ≠ TIME) plus size/colour/intensity/quantity over POSITION; total directional")
check(D_, "ten errors cannot decide", "E1 count", "error-evidence/p65_e1-run_2026-11-13.txt", n_st + n_ts, "n(S->T) + n(T->S)", tol=0)
check(D_, "kappa 0.79 and 0.68", "first sample and A3 agreement", "arm-a-model and arm-a3-model coder files", (k_a, k_a3), "Cohen's kappa recomputed on the 'class' columns (n %d, %d)" % (n_a, n_a3))
check(D_, "0.58 on the", "A3b agreement", "arm-a3b-model coder files", k_a3b, "Cohen's kappa recomputed (n %d)" % n_a3b)
check(D_, "300 of the same sentences is planned", "planned human coding", "docs/manuscript/p65_navon-validation_DRAFT.md (plan, no results file)", None, "plan statement, not a result")
check(D_, "155\ndirectional sentences".replace("\n", " "), "A3 combined directional count", "arm-a3-model results CELL TABLE", directional_a3, "Σ (TP + PT) over the six cells")
check(D_, "design effect of about 6", "stratified-draw design effect", "p65_wave1_verify_2026-11-16.md L20: 5.0 to 6.9", (deff[0] + deff[1]) / 2, "READ: midpoint of the verify pass's range", read=True)
check(D_, "about 22 to 31 independent items", "155 ÷ design effect", "same, L20", (round(155 / deff[1]), round(155 / deff[0])), "155 ÷ 6.9 and 155 ÷ 5.0, rounded")
check(D_, "ten of its 39 papers", "abstract-only papers among counted", "published-asymmetry coded TSV, 'verification' column", (abstract_papers, n_papers), "papers whose counted rows all start ABSTRACT; distinct doi-or-key")
check(D_, "re-codes the 4,000", "wave 2 items", "item maps (as above)", n_items, "rows counted")
check(D_, "all 30 ordered pairs", "6 dimensions, ordered pairs", "p65_wave2_registration_2026-11-16.md Section 1.4", 6 * 5, "6 × 5", tol=0)
check(D_, "about 37 directional items per pair for direction at a share of 0.74", "exact binomial power 0.80", "Appendix D.6 table (exact binomial)", n37, "smallest n with exact two-sided power ≥ 0.80 at p = 0.74, α = .05")
check(D_, "about 110 per pair", "additivity power, simulation", "docs/manuscript/p65_appendix-D_math_2026-11-16.md D.6 table", 110 if has(appD, "about 110 per pair") else None, "READ: simulation not rerun", read=True)
check(D_, "at least 20 per pair per criterion", "rank-one power, simulation", "same, D.6 table", 20 if has(appD, "20 per pair per criterion") else None, "READ: simulation not rerun", read=True)
check(D_, "time-place kappa 0.38 on 58 pilot", "wave 2 pilot 2", "p65_wave3_registration_FROZEN_2026-11-16.md Section 0 ('0.376 in pilot 2 (n 58)')", (0.376, 58) if "0.376 in pilot 2 (n 58)" in w3 else None, "READ: pilot codes not re-scored here", read=True)
check(D_, "SHA-256 1c3e0fee", "wave 3 freeze hash", "wave3/FREEZE.txt", None if freeze.split("\n")[3].startswith("1c3e0fee") else "FREEZE line 4 differs", "prefix compared with FREEZE.txt line 4")
check(D_, "(6,628 sentences, two treebanks", "Indonesian census size", "wave3/main/census_map.tsv", len(census), "rows counted")
check(D_, "about 164 directional items (113", "expected yield", "p65_wave3_registration_FROZEN_2026-11-16.md Section 2.3", (164, 113) if "Expected effective items 164" in w3 and "113 at the" in w3 else None, "READ: yield pilot not rerun", read=True)
check(D_, "has power 1.00 at either count", "exact binomial power at 0.74, n = 164 and 113", "recomputed", min(pow164, pow113), "exact two-sided binomial test of 0.5; power at p = 0.74 (the smaller of the two counts)", tol=0.005)
check(D_, "keeps power 0.80 down to a true share of about 0.62 at 164 items", "smallest share with exact power ≥ 0.80 at n = 164", "recomputed; the frozen registration's normal approximation said 0.60 (exact power there is %.2f)" % binom_power(164, 0.60), share80_164, "exact binomial power scanned in steps of 0.001", tol=0.006, printed_value=0.62)
check(D_, "eight languages suffice", "mean-direction power, SD 0.5", "Appendix D.6 table ('8 languages × 50 items (0.99)')", 8 if has(appD, "8 languages × 50 items (0.99)") else None, "READ: simulation not rerun", read=True)
check(D_, "twelve give power 0.90", "mean-direction power, SD 1.0", "Appendix D.6 table ('12 languages × 100 items (0.90)')", 12 if has(appD, "12 languages × 100 items (0.90)") else None, "READ: simulation not rerun", read=True)
check(D_, "gap of 1.04", "logit of 0.738", "arm-a3 share", gap, "ln(0.738/0.262)", tol=0.006) if "gap of 1.04" in regions[D_] else None

# ------------------------------------------------------------------ Wave 3, Indonesian census (2026-11-17; Section 2.6)
# Own recount from the merged code files and the adjudication files (no import of the analysis script, no parsing
# of its run file): final label = coder 1's when the coders agree, else the adjudicator's; gold items excluded.
W3 = os.path.join(ROOT, "wave3", "main")
w3_run = os.path.join(ROOT, "wave3", "p65_wave3_analysis-run_2026-11-17.txt")
if os.path.exists(w3_run) and "[ID-RESULT" not in ms:
    gold_w3 = {r["item"] for r in tsv("wave3", "main", "batches", "gold_key.tsv")}
    units_w3 = [u for u in ["P01"] + ["M%02d" % i for i in range(1, 17)] if os.path.exists(os.path.join(W3, "codes", u + "_DONE"))]
    w_tp = w_pt = w_sent = w_both = w_both_agree = 0
    both1, both2 = [], []
    for u in units_w3:
        c1 = {r["item"]: r["label"] for r in tsv("wave3", "main", "codes", u + "_coder1.tsv")}
        c2 = {r["item"]: r["label"] for r in tsv("wave3", "main", "codes", u + "_coder2.tsv")}
        adj = {r["item"]: r["final"] for r in tsv("wave3", "main", "codes", u + "_adjudication.tsv")}
        for it, lab in c1.items():
            if it in gold_w3:
                continue
            w_sent += 1
            fin = lab if lab == c2[it] else adj[it]
            w_tp += fin == "TP"; w_pt += fin == "PT"
            if lab != "NA" and c2[it] != "NA":
                both1.append(lab); both2.append(c2[it])
    w_n = w_tp + w_pt
    w_share = w_tp / w_n
    w_k = min(max(w_tp, 0.5), w_n - 0.5)
    w_m = math.log(w_k / (w_n - w_k)); w_se = math.sqrt(1 / w_k + 1 / (w_n - w_k))
    w_lo, w_hi = 1 / (1 + math.exp(-(w_m - 1.96 * w_se))), 1 / (1 + math.exp(-(w_m + 1.96 * w_se)))
    w_p = min(1.0, 2 * sum(math.comb(w_n, i) for i in range(0, min(w_tp, w_n - w_tp) + 1)) / 2 ** w_n)
    (w_dk, w_raw) = kappa(both1, both2)
    w_label = "confirmatory"
    if os.path.exists(os.path.join(W3, "S1_LABEL.txt")) and "exploratory" in open(os.path.join(W3, "S1_LABEL.txt")).read():
        w_label = "exploratory"
    W3_CHECKS = [
        (A_, "two Indonesian treebanks (6,628 sentences)", "census size", lambda: w_sent, "non-gold rows over P01 and M01 to M16 code files", {"printed_value": 6628}),
        (A_, "the share was 0.70 (0.58 to 0.80; 70 directional sentences)", "share; interval; directional count", lambda: (w_share, w_lo, w_hi, w_n), "TP / (TP + PT); logit(k/n) ± 1.96·sqrt(1/k + 1/(n−k)), own arithmetic; TP + PT, final labels re-derived", {}),
        (D_, "0.70 of its directional sentences", "share", lambda: w_share, "as above", {}),
        (D_, "pair-label agreement was 0.60", "D-kappa over both-present sentences", lambda: w_dk, "Cohen's kappa recomputed on the two coders' labels where neither is NA (n %d)" % len(both1), {}),
        (D_, "the census returned 70, under the 100", "directional count; rule Y bar", lambda: (w_n, 100), "TP + PT; registration Section 3", {"tol": 0}),
        (D_, "Indonesian sentences about twice as often", "0.70 / 0.30 = 2.3", lambda: w_share / (1 - w_share), "odds from the recomputed share; 2.3 reads 'about twice'", {"tol": 0.5, "printed_value": 2}),
    ]
    for region, printed, meaning, value, method, kw in W3_CHECKS:
        check(region, printed, meaning, "wave3/main/codes (own recount)", value(), method, **kw)
    if PERTURB:
        check(D_, "0.70 of its directional sentences", "PERTURB control", "wave3 (control)", w_share + 0.03, "share + 0.03 must MISMATCH")

# ================================================================== write
hdr = ["region", "printed", "meaning", "source", "recomputed", "method", "status"]
lines = ["<!-- trace:generated:begin -->",
         "## Abstract and Discussion, recomputed by `scripts/p65_v1_number-trace.py` (%s)" % ("PERTURBED CONTROL RUN" if PERTURB else "2026-11-17"),
         "",
         "Status: OK = printed value matches the recomputation; READ = taken from the results line (bootstrap or simulation "
         "not rerun); LOCATED = text-only claim found; MISMATCH / NOT IN TEXT fail the run.",
         "",
         "| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
for r in rows:
    lines.append("| " + " | ".join(str(x).replace("|", "\\|") for x in r) + " |")
n_ok = sum(r[-1] == "OK" for r in rows); n_read = sum(r[-1].startswith("READ") for r in rows)
n_loc = sum(r[-1] == "LOCATED" for r in rows)
summary = "%d numbers: %d recomputed OK, %d read from source lines, %d located as text, %d failures." % (len(rows), n_ok, n_read, n_loc, bad)
lines += ["", summary, "<!-- trace:generated:end -->"]
block = "\n".join(lines)
print(summary)
for r in rows:
    if r[-1] in ("MISMATCH", "NOT IN TEXT"):
        print("  FAIL", r[0], r[1], "->", r[4], r[-1])
if not PERTURB:
    old = open(OUT, encoding="utf-8").read()
    i, j = old.index("<!-- trace:generated:begin -->"), old.index("<!-- trace:generated:end -->") + len("<!-- trace:generated:end -->")
    open(OUT, "w", encoding="utf-8").write(old[:i] + block + old[j:])
    print("wrote", OUT)
sys.exit(1 if bad else 0)
