"""p65 wave 1, Appendix D: ATTACK-stage numerical checks. Fixed seeds. Every block prints its control.

Run: python3 -I scripts/p65_wave1_attack_checks.py
(-I isolates; the script adds its own directory to sys.path for p65_wave1_bt.)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
import numpy as np
from scipy.special import expit, logit
from scipy import stats
if not hasattr(stats, "binom_test"):  # scipy >= 1.12 (deposit cold run, 2026-11-17): same test, new name
    stats.binom_test = lambda k, n, p=0.5, alternative="two-sided": stats.binomtest(int(k), int(n), p, alternative=alternative).pvalue
import mpmath as mp
import p65_wave1_bt as bt

mp.mp.dps = 40
out = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    out.append(s)

# ---------------------------------------------------------------------------------------------
say("A1. F3 worked example, exact. Shares 0.8 and 0.8 imply time-over-colour = 16/17 under BT.")
p = Fraction(4, 5)
odds = (p / (1 - p)) ** 2          # odds multiply under BT
pik = odds / (1 + odds)
say("   implied share =", pik, "=", float(pik))
say("   Thurstone (probit) version:", float(mp.ncdf(2 * mp.sqrt(2) * mp.erfinv(2 * mp.mpf('0.8') - 1))))
say("   control (no chaining, Garner-like): non-adjacent share 0.8 -> logit defect",
    float(mp.log(mp.mpf(4)) - 2 * mp.log(mp.mpf(4))))

# ---------------------------------------------------------------------------------------------
say("\nA2. Coder direction-flip error attenuates logits subadditively (proved in D.3; Wolfram W4).")
for e in (0.0, 0.02, 0.05, 0.10):
    q = lambda s: e + (1 - 2 * e) * s
    a, c = 0.8, float(pik)
    lhs = logit(q(c)); rhs = 2 * logit(q(a))
    say(f"   err={e:.2f}: observed adjacent {q(a):.3f}, observed non-adjacent {q(c):.3f}, "
        f"predicted-from-observed {expit(rhs):.3f}, logit defect {lhs - rhs:+.3f}")
say("   control: err=0 row must show defect 0.000 (it can fail if the code mis-specifies q).")

# ---------------------------------------------------------------------------------------------
say("\nA3. Mixtures. (a) common order, criterion-specific sharpness, pair-specific weights -> SST can fail, WST cannot.")
th = np.array([2.0, 1.0, 0.0])   # i, j, k
kA, kB = 5.0, 0.1
P_ij = expit(kA * (th[0] - th[1]))         # pair ij coded only from sharp criterion
P_jk = expit(kA * (th[1] - th[2]))
P_ik = expit(kB * (th[0] - th[2]))         # pair ik coded only from diffuse criterion
say(f"   P_ij={P_ij:.4f} P_jk={P_jk:.4f} P_ik={P_ik:.4f}; WST holds: {P_ik > 0.5}; SST holds: {P_ik >= max(P_ij, P_jk)}")
say("   (b) Condorcet: three equal-weight sources with cyclic orders, sharp k -> pooled cycle.")
orders = [np.array([2, 1, 0]), np.array([0, 2, 1]), np.array([1, 0, 2])]  # theta for (T, P, C)
for k in (2.0, 5.0, 50.0):
    pooled = lambda i, j: np.mean([expit(k * (o[i] - o[j])) for o in orders])
    t = (pooled(0, 1), pooled(1, 2), pooled(2, 0))
    tri = (t[0] + t[1] - (1 - t[2]))
    say(f"   k={k:>4}: P(T>P)={t[0]:.3f} P(P>C)={t[1]:.3f} P(C>T)={t[2]:.3f}  cycle={min(t) > 0.5};"
        f" triangle P_TP+P_PC-P_TC={tri:.3f} (<=1 required for any mixture of orders)")
say("   control: a single source (orders[0] alone) must show no cycle:",
    not all(expit(5 * (orders[0][i] - orders[0][j])) > 0.5 for i, j in ((0, 1), (1, 2), (2, 0))))

say("\n   (c) common order, pair-INDEPENDENT weights: is logit of a logistic mixture subadditive on x>=0?")
rng = np.random.default_rng(20261116)
worst = -np.inf
nviol = 0
nmp = 0
N = 20000
for _ in range(N):
    m = rng.integers(2, 5)
    w = rng.dirichlet(np.ones(m))
    k = np.exp(rng.uniform(np.log(0.05), np.log(20), m))
    x, y = rng.uniform(0, 4, 2)
    f = lambda z: logit(np.clip(np.sum(w * expit(k * z)), 1e-15, 1 - 1e-15))
    d = f(x + y) - f(x) - f(y)
    if d > -1e-6:   # float cannot be trusted near 0 or near shares of 1: re-evaluate at 40 digits
        def fm_(z):
            s_ = mp.fsum(mp.mpf(float(a)) / (1 + mp.e ** (-mp.mpf(float(b)) * z)) for a, b in zip(w, k))
            return mp.log(s_ / (1 - s_))
        X_, Y_ = mp.mpf(float(x)), mp.mpf(float(y))
        d = float(fm_(X_ + Y_) - fm_(X_) - fm_(Y_))
        nmp += 1
    if d > worst:
        worst, wcase = d, (w.copy(), k.copy(), x, y)
    nviol += d > 0
say(f"   {N} random mixtures (seed 20261116): max of f(x+y)-f(x)-f(y) = {worst:.2e}; violations {nviol} (after {nmp} near-zero cases re-evaluated at 40 digits)")
ww, kk, xx, yy = wcase
def fm(z):
    s_ = mp.fsum(mp.mpf(float(a)) / (1 + mp.e ** (-mp.mpf(float(b)) * z)) for a, b in zip(ww, kk))
    return mp.log(s_ / (1 - s_))
dmp = fm(mp.mpf(float(xx)) + mp.mpf(float(yy))) - fm(mp.mpf(float(xx))) - fm(mp.mpf(float(yy)))
say(f"   worst case re-evaluated at 40 digits: weights {np.round(ww, 4)}, sharpness {np.round(kk, 4)},"
    f" x={xx:.4f}, y={yy:.4f}: defect {mp.nstr(dmp, 12)} (positive = superadditive = counterexample)")
# control: the same search on a function that is NOT subadditive must find violations
nviol_c = 0
for _ in range(2000):
    x, y = rng.uniform(0.1, 4, 2)
    fc = lambda z: z ** 1.5
    nviol_c += (fc(x + y) - fc(x) - fc(y)) > 1e-9
say(f"   control (superadditive z^1.5 through the same search): violations {nviol_c}/2000 (must be > 0)")

# ---------------------------------------------------------------------------------------------
say("\nA4. MLE existence. Navon's strong form ('time never changes over anything') puts a zero in a row.")
w = np.array([[0, 30, 20], [10, 0, 25], [0, 5, 0]], float)   # dim 0 never loses to dim 2
theta, ll, div = bt.fit_bt(w, ridge=0.0, iters=200)
say(f"   one-way zero (0 beats 2 in all 20): theta={np.round(theta, 2)}, diverged={div}"
    "  (Ford: MLE exists iff the win graph is strongly connected; here 2 cannot reach 0 directly but"
    " can via 1 -> finite)")
w2 = np.array([[0, 30, 20], [0, 0, 25], [0, 5, 0]], float)   # dim 0 never loses to anyone
theta2, ll2, div2 = bt.fit_bt(w2, ridge=1e-9, iters=200)
say(f"   dim 0 never loses at all: theta={np.round(theta2, 2)}, diverged={div2} (must diverge)")
say("   control: the first case is strongly connected (2 beat 1 five times, 1 beat 0 ten times) so must NOT diverge:",
    not div)

# ---------------------------------------------------------------------------------------------
say("\nA5. Rank-one convergence test: null distribution of the LR statistic, D=6, C=3, df=(C-1)(D-2)=8.")
D, C = 6, 3
df = (C - 1) * (D - 2)
theta_nav = np.array([2.1, 1.05, 0.0, 0.0, 0.0, 0.0])
def lr_rank1(wl):
    _, _, l1 = bt.fit_rank1(wl)
    return 2 * (bt.ll_sepbt(wl) - l1)
for label, ks, th_true in (("true rank one (k=1,0.6,1.5)", (1.0, 0.6, 1.5), theta_nav),
                           ("true rank ZERO (no hierarchy)", (1.0, 1.0, 1.0), np.zeros(D)),
                           ("CONTROL: criterion 3 swaps time and place", None, None)):
    rng = np.random.default_rng(20261117)
    stats_ = []
    for rep in range(400):
        if ks is None:
            th3 = theta_nav.copy(); th3[[0, 1]] = th3[[1, 0]]
            wl = [bt.simulate_wins(theta_nav, 60, rng), bt.simulate_wins(theta_nav, 60, rng),
                  bt.simulate_wins(th3, 60, rng)]
        else:
            wl = [bt.simulate_wins(th_true, 60, rng, k=k) for k in ks]
        stats_.append(lr_rank1(wl))
    s = np.array(stats_)
    say(f"   {label}: mean LR {s.mean():.2f} (chi2 mean {df}), rejection at chi2_8 .95 = "
        f"{np.mean(s > stats.chi2.ppf(0.95, df)):.3f}")
say("   reading: rank one exact -> size near .05; rank zero -> conservative; control must reject often.")

# ---------------------------------------------------------------------------------------------
say("\nA6. Rank-one blind spot: criterion 3 reverses EVERY pair (k_3 = -1). Rank one still holds.")
rng = np.random.default_rng(20261118)
rej = []
ksig = []
for rep in range(300):
    wl = [bt.simulate_wins(theta_nav, 60, rng, k=k) for k in (1.0, 0.6, -1.0)]
    th, k, l1 = bt.fit_rank1(wl)
    rej.append(2 * (bt.ll_sepbt(wl) - l1) > stats.chi2.ppf(0.95, df))
    ksig.append(k[2] < 0)
say(f"   LR rejection {np.mean(rej):.3f} (stays near alpha: the rank test cannot see a reversal);"
    f" fitted k_3 < 0 in {np.mean(ksig):.3f} of runs (the sign check sees it)")

# ---------------------------------------------------------------------------------------------
say("\nA7. Empirical anchors from the arms (inputs to the power table).")
s_A3, lo, hi, nA3 = 0.74, 0.56, 0.89, 155
say(f"   Arm A3 time-over-place 0.74 -> logit gap theta_T - theta_P = {logit(s_A3):.3f} (interval {logit(lo):.2f} to {logit(hi):.2f})")
se_srs = np.sqrt(s_A3 * (1 - s_A3) / nA3)
se_obs = (hi - lo) / (2 * 1.96)
say(f"   design effect of the weighted A3 estimate: SE observed {se_obs:.4f} vs simple random {se_srs:.4f}"
    f" -> deff {(se_obs / se_srs) ** 2:.1f}, effective n {nA3 / (se_obs / se_srs) ** 2:.0f} of {nA3}")
k_C, n_C = 14, 41
say(f"   Arm C time-over-space 14 of 41 = {k_C / n_C:.3f} (logit {logit(k_C / n_C):+.3f});"
    f" exact two-sided p {stats.binom_test(k_C, n_C, 0.5):.4f};"
    f" one-sided p (share >= .5 as H0) {stats.binom_test(k_C, n_C, 0.5, alternative='less'):.4f}")
k_C2 = 14; n_C2 = 42
say(f"   second coding 14 of 42: two-sided p {stats.binom_test(k_C2, n_C2, 0.5):.4f};"
    f" one-sided {stats.binom_test(k_C2, n_C2, 0.5, alternative='less'):.4f}")
say("   control: 20 of 41 must give a large p:", round(stats.binom_test(20, 41, 0.5), 3))

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wave1-math",
                       "p65_wave1_attack-checks_2026-11-16.txt"), "w") as fh:
    fh.write("\n".join(out) + "\n")
