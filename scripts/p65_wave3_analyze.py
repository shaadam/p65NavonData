"""p65 wave 3 first-preprint analysis (registration Section 6.5, 5.2, 5.3, 6.3; S5): Indonesian census.
Prints directions. Run ONCE on frozen labels (real mode), after every batch is DONE. Smoke-tested first on synthetic codes.

  python3 -I scripts/p65_wave3_analyze.py --selftest        constants vs registration text, planted H2 sets, synthetic pipeline
  python3 -I scripts/p65_wave3_analyze.py --real [--allow-partial]
Bars are NAMED CONSTANTS; the selftest asserts each against the registration text (and a control that must fail when
the text is changed).
"""
import argparse, collections, csv, math, os, random, re, sys
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p65_wave3_check as ck

# ---- the bars (registration text in the comment) --------------------------------------------------------------------
D_KAPPA_BAR = 0.60          # 5.2 "Bar 0.60"
S1_FIRST = 0.40             # 9 S1
S1_SECOND = 0.60            # 9 S1
MIN_BOTH_PRESENT_FOR_GATE = 100   # 5.2 "at least 100 both-present items"
RULE_Y_EXPLORATORY_BELOW = 60     # 3 rule Y
RULE_Y_FULL = 100                 # 3 rule Y
FLIP_MAX = 0.15             # 5.3 "e above 0.15"
MIN_LANGUAGES = 6           # 5.2 "at least six"
ALPHA = 0.05                # 6.3
GOLD_MISS_RECODE = 2        # S2 (checker)
CAP_USD, CENTRAL_USD = 165, 110   # 2.3
ENGLISH_A3B = (0.823, 0.728, 0.906)   # 0: share, 95% document interval
CONSTANT_TEXT = {  # name -> (value, regex that must match the registration text)
    "D_KAPPA_BAR": (D_KAPPA_BAR, r"\*\*Bar 0\.60\*\*"),
    "S1_FIRST": (S1_FIRST, r"S1_FIRST = 0\.40"),
    "S1_SECOND": (S1_SECOND, r"S1_SECOND = 0\.60"),
    "MIN_BOTH_PRESENT_FOR_GATE": (MIN_BOTH_PRESENT_FOR_GATE, r"at least 100 both-present items"),
    "RULE_Y_EXPLORATORY_BELOW": (RULE_Y_EXPLORATORY_BELOW, r"below 60 is coded anyway"),
    "RULE_Y_FULL": (RULE_Y_FULL, r"unless the main run reaches 100"),
    "FLIP_MAX": (FLIP_MAX, r"e above 0\.15"),
    "MIN_LANGUAGES": (MIN_LANGUAGES, r"at least six"),
    "ALPHA": (ALPHA, r"α = \.05"),
    "GOLD_MISS_RECODE": (GOLD_MISS_RECODE, r"Five constructed gold items per batch"),
    "CAP_USD": (CAP_USD, r"cap\s+\$165"),
    "CENTRAL_USD": (CENTRAL_USD, r"central \$110"),
}


def logit(p): return math.log(p / (1 - p))
def expit(x): return 1 / (1 + math.exp(-x))


def e_from_d(d):
    d = min(d, 0.5); return (1 - math.sqrt(1 - 2 * d)) / 2


def cp(k, n, alpha=ALPHA):
    if n == 0: return (0.0, 1.0)
    lo = 0.0 if k == 0 else stats.beta.ppf(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - alpha / 2, k + 1, n - k)
    return lo, hi


def share_logit_ci(k, n):
    """k time-over-place among n directional; 95% interval on the logit scale (sentence the unit)."""
    k = min(max(k, 0.5), n - 0.5)  # half-count guard at the edges
    m = logit(k / n); se = math.sqrt(1 / k + 1 / (n - k))
    return k / n, expit(m - 1.96 * se), expit(m + 1.96 * se), m, se


def correct(q, e): return min(1.0, max(0.0, (q - e) / (1 - 2 * e)))   # Proposition D.7 inverted: q = e + (1-2e)P


def analyze(c1, c2, final, flags, gold=()):
    """c1, c2, final: item -> label (gold already excluded). flags: item -> (screen_time, screen_place_broad)."""
    out = {}
    pk, dk, nb, raw = ck.agreement(c1, c2)
    out.update(P_kappa=pk, D_kappa=dk, n_both=nb, raw_presence=raw)
    tp = sum(1 for v in final.values() if v == "TP"); pt = sum(1 for v in final.values() if v == "PT")
    n = tp + pt; out.update(tp=tp, pt=pt, n_dir=n)
    out["gate"] = ("undecided" if nb < MIN_BOTH_PRESENT_FOR_GATE else ("pass" if dk >= D_KAPPA_BAR else "fail"))
    bd = [i for i in c1 if c1[i] in ck.DIRECTIONAL and c2[i] in ck.DIRECTIONAL]
    dd = sum(c1[i] != c2[i] for i in bd); d = dd / len(bd) if bd else 0.0
    e = e_from_d(d); e_hi = e_from_d(cp(dd, len(bd))[1]) if bd else 0.5
    out.update(flip_d=d, flip_e=e, flip_e_upper=e_hi, flip_ok=(e <= FLIP_MAX), n_both_dir=len(bd))
    q, lo, hi, m, se = share_logit_ci(tp, n)
    out.update(share=q, share_lo=lo, share_hi=hi, logit=m, logit_se=se)
    out["p_two_sided"] = (stats.binomtest(tp, n, 0.5).pvalue if hasattr(stats, 'binomtest') else stats.binom_test(tp, n, 0.5)) if n else float("nan")
    out["share_corrected"] = (correct(q, e), correct(lo, e), correct(hi, e))
    out["share_corrected_e_upper"] = correct(q, min(e_hi, 0.49))
    s_en = (logit(ENGLISH_A3B[2]) - logit(ENGLISH_A3B[1])) / (2 * 1.96)
    diff = m - logit(ENGLISH_A3B[0]); sd = math.sqrt(se ** 2 + s_en ** 2)
    out["diff_vs_english_logit"] = (diff, diff - 1.96 * sd, diff + 1.96 * sd)
    out["rule_y"] = "exploratory" if n < RULE_Y_EXPLORATORY_BELOW else ("insufficient-for-own-test" if n < RULE_Y_FULL else "full")
    fl = {i: bool(flags[i][0] and flags[i][1]) for i in final if i in flags}
    sc = {}
    for lab in ("TP", "PT"):
        its = [i for i in fl if final[i] == lab]
        sc[lab] = (sum(fl[i] for i in its) / len(its)) if its else float("nan")
    fd = [i for i in fl if fl[i]]
    sc["precision"] = (sum(final[i] in ck.DIRECTIONAL for i in fd) / len(fd)) if fd else float("nan")
    out["screen"] = sc
    return out


def h2_cochran(logits, ses, alpha=ALPHA):
    """H2: chi-square heterogeneity (Cochran Q) on L-1 df across per-language logit shares. Returns (Q, p, reject)."""
    w = [1 / s ** 2 for s in ses]; mbar = sum(wi * x for wi, x in zip(w, logits)) / sum(w)
    q = sum(wi * (x - mbar) ** 2 for wi, x in zip(w, logits)); p = 1 - stats.chi2.cdf(q, len(logits) - 1)
    return q, p, p < alpha


def h1_t(logits, alpha=ALPHA):
    """H1: delta > 0, one-sided t-test on per-language logit shares."""
    t, p2 = stats.ttest_1samp(logits, 0.0); p = p2 / 2 if t > 0 else 1 - p2 / 2
    return t, p, p < alpha


def planted_language(rng, share, n):
    k = sum(rng.random() < share for _ in range(n)); return logit(max(k, 0.5) / n if k < n else (n - .5) / n), \
        math.sqrt(1 / max(k, .5) + 1 / max(n - k, .5))


def planted_sets(seed=1, L=8, n=100, reps=300):
    rng = random.Random(seed); out = {}
    for name, sd in (("homogeneous", 0.0), ("heterogeneous", 1.0)):
        rej = 0
        for _ in range(reps):
            ls, ss = zip(*[planted_language(rng, expit(1.0 + rng.gauss(0, sd)), n) for _ in range(L)])
            rej += h2_cochran(ls, ss)[2]
        out[name] = rej / reps
    return out


def synthetic(seed, share=0.74, n_items=6628, e=0.05):
    """Synthetic census: truth labels, coder noise, adjudication = truth. Returns c1, c2, final, flags."""
    rng = random.Random(seed); c1, c2, fin, fl = {}, {}, {}, {}
    for i in range(n_items):
        u = rng.random(); t = ("NA" if u < 0.95 else ("TP" if rng.random() < share else "PT") if u < 0.99 else "PAR")
        def code(x):
            if x in ck.DIRECTIONAL and rng.random() < e: x = "PT" if x == "TP" else "TP"
            if x != "NA" and rng.random() < 0.05: x = "NA"
            return x
        k = f"i{i}"; c1[k], c2[k] = code(t), code(t); fin[k] = t if c1[k] != c2[k] else c1[k]; fl[k] = (1, 1 if t != "NA" or rng.random() < .3 else 0)
    return c1, c2, fin, fl


def selftest(reg_path):
    text = open(reg_path, encoding="utf-8").read()
    for name, (val, rx) in CONSTANT_TEXT.items():
        assert re.search(rx, text), f"constant {name} = {val}: its text {rx!r} not found in {os.path.basename(reg_path)}"
    mutated = text.replace("**Bar 0.60**", "**Bar 0.50**")
    assert not re.search(CONSTANT_TEXT["D_KAPPA_BAR"][1], mutated), "constants control cannot fail"
    print(f"constants OK: {len(CONSTANT_TEXT)} bars found in the registration text; control (Bar 0.60 -> 0.50) is detected")
    # numeric sanity of the constant values against the text of the numbers the code uses
    assert (D_KAPPA_BAR, S1_FIRST, S1_SECOND, FLIP_MAX, ALPHA) == (0.60, 0.40, 0.60, 0.15, 0.05)
    res = planted_sets()
    print(f"planted H2 (8 languages x 100 items, 300 sets): rejection rate homogeneous {res['homogeneous']:.3f}, "
          f"heterogeneous {res['heterogeneous']:.3f}")
    assert res["heterogeneous"] >= 0.80 and res["homogeneous"] <= 0.10, "H2 smoke test failed"
    assert res["heterogeneous"] - res["homogeneous"] > 0.5, "NON-DISCRIMINATING: H2 does not separate planted sets"
    # a single planted set each, as the registration words it
    rng = random.Random(7)
    het = [planted_language(rng, s, 150) for s in (0.95, 0.9, 0.7, 0.5, 0.3, 0.8, 0.2, 0.6)]
    hom = [planted_language(rng, 0.74, 150) for _ in range(8)]
    assert bool(h2_cochran(*zip(*het))[2]) and not bool(h2_cochran(*zip(*hom))[2])
    t, p, rej = h1_t([1.0, 1.2, 0.8, 1.1, 0.9, 1.3]); assert rej
    t, p, rej = h1_t([0.1, -0.2, 0.05, -0.1, 0.0, 0.1]); assert not rej
    print("H1 control OK: positive set rejects, null set does not; H2 planted single sets OK")
    c1, c2, fin, fl = synthetic(11)
    r = analyze(c1, c2, fin, fl)
    assert abs(r["share"] - 0.74) < 0.12 and r["flip_e"] < 0.10 and r["gate"] in ("pass", "fail", "undecided")
    c1b, c2b, finb, flb = synthetic(12, share=0.50); rb = analyze(c1b, c2b, finb, flb)
    assert rb["p_two_sided"] > 0.01 or rb["n_dir"] < 60
    c1n, c2n, finn, fln = synthetic(13, share=0.74, e=0.40); rn = analyze(c1n, c2n, finn, fln)
    assert rn["D_kappa"] < D_KAPPA_BAR and rn["gate"] != "pass", "gate control: heavy flipping must not pass"
    assert abs(correct(0.1 + 0.8 * 0.8, 0.1) - 0.8) < 1e-9
    import tempfile
    with tempfile.TemporaryDirectory() as td:   # amendment 3: the S1 second-pilot label is read from the run state file
        lp = os.path.join(td, "S1_LABEL.txt")
        assert label_of(lp) == "confirmatory", "no label file: confirmatory"
        open(lp, "w").write("P02: D-kappa 0.123 below S1_SECOND 0.60: exploratory\n")
        assert label_of(lp) == "exploratory"
    print(f"synthetic pipeline OK: share {r['share']:.3f} (truth 0.74), D-kappa {r['D_kappa']:.3f}, gate {r['gate']}, flip e {r['flip_e']:.3f}; "
          f"null set p {rb['p_two_sided']:.3f}; noisy-coder control D-kappa {rn['D_kappa']:.3f} gate {rn['gate']}")


def label_of(path):
    """Amendment 3: the runner writes wave3/main/S1_LABEL.txt after the second pilot P02 (registration 9 S1). 'exploratory'
    when P02's D-kappa was below S1_SECOND, else 'confirmatory'; no file (no second pilot) means confirmatory."""
    if not os.path.exists(path):
        return "confirmatory"
    return "exploratory" if "exploratory" in open(path, encoding="utf-8").read() else "confirmatory"


def real(allow_partial):
    # P02 (the S1 second pilot) is not a census batch: its sentences are analysed from their M batch codes only
    done = [u for u in ["P01"] + [f"M{i:02d}" for i in range(1, 17)] if os.path.exists(os.path.join(ck.CODES, f"{u}_DONE"))]
    label = label_of(os.path.join(ck.MAIN, "S1_LABEL.txt"))
    if len(done) < 17 and not allow_partial:
        raise SystemExit(f"only {len(done)} of 17 batches DONE; use --allow-partial to analyse complete batches only")
    c1, c2, fin, fl = {}, {}, {}, {}
    gk = ck.gold_key()
    for u in done:
        a, b = ck.load_merged(u, "coder1"), ck.load_merged(u, "coder2")
        adj = {r["item"]: r["final"] for r in ck.read_tsv(os.path.join(ck.CODES, f"{u}_adjudication.tsv"))}
        mp = {r["item"]: r for r in ck.read_tsv(os.path.join(ck.BATCHES, f"{u}_map.tsv"))}
        for i in a:
            if i in gk: continue
            c1[i], c2[i] = a[i], b[i]; fin[i] = a[i] if a[i] == b[i] else adj[i]
            fl[i] = (int(mp[i]["screen_time"]), int(mp[i]["screen_place"]))
    r = analyze(c1, c2, fin, fl)
    if label == "exploratory":
        r = {k: v for k, v in r.items()}; r["gate"] = f"exploratory (S1_SECOND: second pilot D-kappa below {S1_SECOND}); {r.get('gate')}"
    print(f"RESULT LABEL: {label.upper()} (registration 9 S1, wave3/main/S1_LABEL.txt)")
    print(f"batches analysed: {len(done)} ({len(c1)} sentences)")
    for k, v in r.items(): print(f"[{label}]", k, v)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--real", action="store_true")
    ap.add_argument("--allow-partial", action="store_true")
    ap.add_argument("--registration", default=None)
    a = ap.parse_args()
    reg = a.registration or next(p for p in (os.path.join(ROOT, "p65_wave3_registration_FROZEN_2026-11-16.md"),
                                             os.path.join(ROOT, "p65_wave3_registration_DRAFT_2026-11-16.md")) if os.path.exists(p))
    selftest(reg) if a.selftest else real(a.allow_partial) if a.real else print(__doc__)
