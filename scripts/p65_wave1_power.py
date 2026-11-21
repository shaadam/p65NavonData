"""p65 wave 1, Appendix D.6: power for each test, in directional items per pair (and per language).

Run: python3 -I scripts/p65_wave1_power.py [--quick]
Writes wave1-math/p65_wave1_power-results_2026-11-16.txt and wave1-math/p65_wave1_power-table_2026-11-16.tsv.

Every simulated test is also run with the effect set to zero (or the null true): that row is the
negative control, and it must reject near alpha = .05. A control far from .05 means the code or the
reference distribution is wrong, and the power numbers beside it are void.

Anchor: Arm A3 share 0.74, logit gap 1.046 (time over place). Six dimensions: time, place, size,
colour, quantity, manner, with theta = (2.09, 1.046, 0, 0, 0, 0) for the Navon scenario (other four tied).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy import stats
from scipy.special import expit, logit
import p65_wave1_bt as bt

QUICK = "--quick" in sys.argv
R = 300 if QUICK else 2000
R_FIT = 150 if QUICK else 600
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "wave1-math")
lines, rows = [], []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); lines.append(s)
def row(test, scenario, unit, n, power, note=""):
    rows.append((test, scenario, unit, str(n), f"{power:.3f}", note))

G = logit(0.74)                                  # 1.046
THETA_NAV = np.array([2 * G, G, 0, 0, 0, 0])
ALPHA = 0.05

# ---------------- P1: direction of one pair (F1); exact, equal-tailed binomial = 95% CI excludes .5
def reject_region(n):
    x = np.arange(n + 1)
    lo = stats.binom.cdf(x, n, 0.5) <= ALPHA / 2
    hi = stats.binom.sf(x - 1, n, 0.5) <= ALPHA / 2
    return lo | hi
def power_dir(n, p):
    x = np.arange(n + 1)
    return float(np.sum(stats.binom.pmf(x, n, p)[reject_region(n)]))
def min_n(p, target=0.80, nmax=5000):
    # smallest n from which power stays >= target for the next 20 n (guards the sawtooth)
    for n in range(5, nmax):
        if all(power_dir(m, p) >= target for m in range(n, n + 20)):
            return n
    return None
say("P1 direction of one pair (F1), exact equal-tailed binomial, alpha .05, power .80")
ctrl = max(power_dir(n, 0.5) for n in range(5, 400))
say(f"   control: max rejection at true share 0.5 over n=5..399 = {ctrl:.4f} (must be <= .05)")
P1 = {}
for p in (0.60, 0.65, 0.70, 0.74, 0.80):
    n = min_n(p); P1[p] = n
    say(f"   true share {p:.2f} (logit {logit(p):+.2f}): n = {n} directional items"
        f"  [x5.7 = {int(np.ceil(n * 5.7))} if drawn like Arm A3]")
    row("F1 direction", f"share {p:.2f}", "items per pair", n, power_dir(n, p),
        "0.65 = Arm C's 0.35 (14 of 40) read the other way" if p == 0.65 else "")

# ---------------- P2: transitivity (F2): resolve all three pairs of a triad
say("\nP2 transitivity (F2): all three pairs of a triad resolved (each 95% CI clear of .5)")
for p in (0.65, 0.74, 0.80):
    pik = expit(2 * logit(p))
    for n in range(5, 2000):
        if all(power_dir(m, p) ** 2 * power_dir(m, pik) >= 0.8 for m in range(n, n + 20)):
            break
    say(f"   BT triad adjacent {p:.2f}, non-adjacent {pik:.3f}: n = {n} per pair "
        f"(a cyclic triad with all three shares {p:.2f} is detected with prob {power_dir(n, p) ** 3:.2f} at this n)")
    row("F2 transitivity", f"adjacent {p:.2f}", "items per pair", n, power_dir(n, p) ** 2 * power_dir(n, pik))

# ---------------- P3: additivity (F3) on one triad, 1-df LR (BT vs saturated)
say("\nP3 additivity (F3), one triad, LR on 1 df; Monte Carlo", R, "reps per cell, seed 20261120")
crit1 = stats.chi2.ppf(0.95, 1)
def triad_wins(s_ij, s_jk, s_ik, n, rng, err=0.0):
    w = np.zeros((3, 3))
    for (i, j), s in (((0, 1), s_ij), ((1, 2), s_jk), ((0, 2), s_ik)):
        s = err + (1 - 2 * err) * s
        y = rng.binomial(n, s); w[i, j] = y; w[j, i] = n - y
    return w
def lr3(w):
    return 2 * (bt.ll_sat(w) - bt.fit_bt(w)[1])
from scipy.optimize import minimize
def lr3_err(w, e):
    """LR with a known direction-flip rate e built into both likelihoods: q = e + (1-2e) s."""
    P, y, n = bt.pair_counts(w)
    def ll(q):
        q = np.clip(q, 1e-12, 1 - 1e-12)
        return float(np.sum(y * np.log(q) + (n - y) * np.log1p(-q)))
    l_sat = ll(np.clip(y / n, e, 1 - e))
    X = np.array([[1, 0], [1, 1], [0, 1]], float)   # bt.pairs(3) order (0,1),(0,2),(1,2); gaps g1=t0-t1, g2=t1-t2
    f = lambda g: -ll(e + (1 - 2 * e) * expit(X @ g))
    g0 = logit(np.clip((y[[0, 2]] / n[[0, 2]] - e) / (1 - 2 * e), 0.02, 0.98))
    l_bt = -minimize(f, g0, method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 4000}).fun
    return 2 * max(l_sat - l_bt, 0.0)
scen3 = [("null: BT 0.74/0.74/0.89 (CONTROL)", 0.74, 0.74, expit(2 * G), 0.0),
         ("no chaining: 0.74/0.74/0.74", 0.74, 0.74, 0.74, 0.0),
         ("half chaining: 0.74/0.74/0.83", 0.74, 0.74, expit(1.5 * G), 0.0),
         ("null BT but coder flips 5%", 0.74, 0.74, expit(2 * G), 0.05),
         ("null BT, coder flips 5%, error in likelihood", 0.74, 0.74, expit(2 * G), -0.05)]
for label, a, b, c, err in scen3:
    for n in (50, 100, 200, 300, 500, 1000):
        rng = np.random.default_rng(20261120 + n)
        rej = 0
        for _ in range(R):
            if err >= 0:
                w = triad_wins(a, b, c, n, rng, err)
                stat = lr3(w)
            else:   # simulate with flips, then fit both models with the known flip rate in the likelihood
                w = triad_wins(a, b, c, n, rng, -err)
                stat = lr3_err(w, -err)
            rej += stat > crit1
        pw = rej / R
        say(f"   {label:<40} n={n:>5}: rejection {pw:.3f}")
        row("F3 additivity (triad, 1 df)", label, "items per pair", n, pw)
say("   error-in-likelihood rows: both models fitted with q = e + (1-2e) s at the known e; saturated q clipped to [e, 1-e].")

# ---------------- P3b: omnibus BT fit, six dimensions, 10 df
say("\nP3b additivity omnibus, D=6, LR on 10 df;", R_FIT, "reps, seed 20261121")
crit10 = stats.chi2.ppf(0.95, 10)
def garner_wins(n, rng):
    D = 6; w = np.zeros((D, D))
    for i, j in bt.pairs(D):
        s = 0.74 if i in (0, 1) else 0.5          # time and place beat everything at 0.74, no chaining
        y = rng.binomial(n, s); w[i, j] = y; w[j, i] = n - y
    return w
for label, gen in (("null: Navon BT (CONTROL)", lambda n, r: bt.simulate_wins(THETA_NAV, n, r)),
                   ("Garner rival: every time/place pair 0.74, no chaining", garner_wins)):
    for n in (30, 50, 100, 200):
        rng = np.random.default_rng(20261121 + n)
        rej = sum(2 * (bt.ll_sat(w) - bt.fit_bt(w)[1]) > crit10
                  for w in (gen(n, rng) for _ in range(R_FIT)))
        say(f"   {label:<55} n={n:>4}: rejection {rej / R_FIT:.3f}")
        row("F3 additivity (6 dims, 10 df)", label, "items per pair", n, rej / R_FIT)

# ---------------- P4: rank-one convergence across three criteria (F4), 8 df
say("\nP4 convergence (F4), D=6, C=3, LR on 8 df;", R_FIT, "reps, seed 20261122")
crit8 = stats.chi2.ppf(0.95, 8)
th_swap = THETA_NAV.copy(); th_swap[[0, 1]] = th_swap[[1, 0]]
th_flat = THETA_NAV.copy(); th_flat[0] = th_flat[1] = 1.5 * G
scen4 = [("null: one scale, k = 1, 0.6, 1.5 (CONTROL)", [THETA_NAV] * 3, (1, 0.6, 1.5)),
         ("criterion 3 swaps time and place", [THETA_NAV, THETA_NAV, th_swap], (1, 1, 1)),
         ("criterion 3 ties time and place", [THETA_NAV, THETA_NAV, th_flat], (1, 1, 1)),
         ("criterion 3 reverses every pair (rank one!)", [THETA_NAV] * 3, (1, 1, -1))]
for label, ths, ks in scen4:
    for n in (20, 40, 60, 100, 200):
        rng = np.random.default_rng(20261122 + n)
        rej = 0; neg = 0
        for _ in range(R_FIT):
            wl = [bt.simulate_wins(t, n, rng, k=k) for t, k in zip(ths, ks)]
            th, k, l1 = bt.fit_rank1(wl)
            rej += 2 * (bt.ll_sepbt(wl) - l1) > crit8
            neg += k[2] < 0
        say(f"   {label:<45} n={n:>4}: LR rejection {rej / R_FIT:.3f}; fitted k3<0 {neg / R_FIT:.3f}")
        row("F4 rank one (8 df)", label, "items per pair per criterion", n, rej / R_FIT)

# ---------------- P5: languages, time-place pair, theta(d, lang) = theta(d) + u
say("\nP5 languages: per-language time-place logit = 1.046 + v, v ~ N(0, s^2), s = tau*sqrt(2);", R,
    "reps, seed 20261123")
for s in (0.0, 0.5, 1.0):
    keep = stats.norm.cdf(G / s) if s > 0 else 1.0
    for L in (4, 8, 12):
        for n in (50, 100, 200, 300):
            rng = np.random.default_rng(20261123 + 100 * L + n + int(10 * s))
            het = mean_rej = 0; widths = []
            for _ in range(R):
                lg = G + s * rng.standard_normal(L)
                y = rng.binomial(n, expit(lg))
                tab = np.vstack([y, n - y]).T
                if np.all(tab.sum(0) > 0):
                    het += stats.chi2_contingency(tab, correction=False)[1] < ALPHA
                el = np.log((y + 0.5) / (n - y + 0.5))
                t = stats.ttest_1samp(el, 0.0)
                mean_rej += t.pvalue < ALPHA
                widths.append(2 * stats.t.ppf(0.975, L - 1) * el.std(ddof=1) / np.sqrt(L))
            say(f"   s={s:.1f} (new language keeps order with prob {keep:.2f}) L={L:>2} n={n:>3}: "
                f"heterogeneity rejected {het / R:.3f}; mean>0 {mean_rej / R:.3f}; "
                f"median 95% CI width of mean logit {np.median(widths):.2f}")
            row("Languages: heterogeneity (L-1 df)", f"s={s:.1f}, L={L}", "items per language (time-place)", n, het / R,
                "CONTROL (s=0)" if s == 0 else "")
            row("Languages: mean direction", f"s={s:.1f}, L={L}", "items per language (time-place)", n, mean_rej / R)

with open(os.path.join(OUT, "p65_wave1_power-results_2026-11-16.txt"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(os.path.join(OUT, "p65_wave1_power-table_2026-11-16.tsv"), "w") as fh:
    fh.write("test\tscenario\tunit\tn\tpower_or_rejection\tnote\n")
    for r in rows:
        fh.write("\t".join(r) + "\n")
