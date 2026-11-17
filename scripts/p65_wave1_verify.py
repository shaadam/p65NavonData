"""p65 wave 1 VERIFY (independent of scripts/p65_wave1_{bt,attack_checks,power,figs}.py; imports none of them).

Routes differ from the agent's on purpose:
  - LR-test power by the analytic noncentral chi-square (expected-data LR as noncentrality), then spot Monte Carlo
    with my own fitting code and different seeds;
  - direction power through Clopper-Pearson intervals (beta quantiles), strict "all larger n" criterion;
  - df count by numerical Jacobian rank, identifiability by exhaustive graph enumeration;
  - languages by the noncentral t and an own simulation, with a null control the agent did not run.
Run: python3 -I scripts/p65_wave1_verify.py
Writes wave1-math/p65_wave1_verify-run_2026-11-16.txt
"""
import itertools, os, sys
import numpy as np
from scipy import stats, optimize
if not hasattr(stats, "binomtest"):  # scipy < 1.7 (deposit cold run, 2026-11-17): same test, old name
    class _BT:
        def __init__(self, k, n, p=0.5, alternative="two-sided"): self.pvalue = stats.binom_test(k, n, p, alternative=alternative)
    stats.binomtest = _BT
from scipy.special import expit, logit
from scipy.sparse.csgraph import connected_components
import sympy as sp
import mpmath as mp

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wave1-math", "p65_wave1_verify-run_2026-11-16.txt")
LOG = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)

# ======================= PART 1: proofs =======================
say("V1 Davidson / Rao-Kupper ties (sympy)")
pi, pj, nu, th = sp.symbols("pi pj nu theta", positive=True)
Pd_ij = pi / (pi + pj + nu * sp.sqrt(pi * pj)); Pd_ji = pj / (pi + pj + nu * sp.sqrt(pi * pj))
say("   Davidson conditional - BT simplifies to:", sp.simplify(Pd_ij / (Pd_ij + Pd_ji) - pi / (pi + pj)))
Pr_ij = pi / (pi + th * pj); Pr_ji = pj / (pj + th * pi)
odds = sp.simplify((Pr_ij / Pr_ji) / (pi / pj))
say("   Rao-Kupper conditional odds / BT odds =", sp.factor(odds), " (=1 only if theta=1 or pi=pj)")
r = sp.symbols("r", positive=True)
hx = sp.log(r * (1 + th * r) / (r + th))   # conditional logit as function of r = pi/pj
# additivity defect for RK-conditional table: strengths 1, e, e^2, theta=2
f = sp.lambdify((r, th), hx)
d = f(np.e ** 2, 2.0) - 2 * f(np.e, 2.0)
say(f"   RK (theta=2) conditional table, unit gaps: logit-additivity defect {d:+.4f} (nonzero: not BT, so dropping ties misfits)")
say(f"   CONTROL RK theta=1: defect {f(np.e**2,1.0)-2*f(np.e,1.0):+.2e} (must be 0)")

say("\nV2 identifiability iff comparison graph connected: all 1024 graphs on 5 nodes")
D = 5; E = list(itertools.combinations(range(D), 2)); bad = 0
for mask in range(1 << len(E)):
    edges = [E[k] for k in range(len(E)) if mask >> k & 1]
    J = np.zeros((len(edges), D))
    for row, (i, j) in enumerate(edges): J[row, i] = 1; J[row, j] = -1
    rank = np.linalg.matrix_rank(J) if edges else 0
    A = np.zeros((D, D))
    for i, j in edges: A[i, j] = A[j, i] = 1
    ncomp = connected_components(A, directed=False)[0]
    bad += (rank == D - 1) != (ncomp == 1)
say(f"   mismatches between 'rank D-1 (identified up to a constant)' and 'connected': {bad} of 1024")
say("   CONTROL: same loop testing 'rank D-1 iff every node has degree>=1' gives mismatches:",
    sum(1 for mask in range(1 << len(E)) if (
        (np.linalg.matrix_rank(np.array([[1 if x == i else -1 if x == j else 0 for x in range(D)] for (i, j) in [E[k] for k in range(len(E)) if mask >> k & 1]])) if mask else 0) == D - 1)
        != all(any(v in E[k] for k in range(len(E)) if mask >> k & 1) for v in range(D))))

say("\nV3 Ford: finite MLE vs strongly connected win graph (random 4-node tables, own optimiser)")
def bt_ll(theta, W):
    dif = theta[:, None] - theta[None, :]
    return float(np.sum(W * np.log(expit(dif) + 1e-300)))
def fit_bt(W, box=40.0):
    Dn = W.shape[0]
    fun = lambda t: -bt_ll(np.concatenate([[0.0], t]), W)
    res = optimize.minimize(fun, np.zeros(Dn - 1), method="L-BFGS-B", bounds=[(-box, box)] * (Dn - 1))
    return np.concatenate([[0.0], res.x]), -res.fun
rng = np.random.default_rng(9101); tally = {}
for _ in range(600):
    W = rng.integers(0, 3, size=(4, 4)) * (rng.random((4, 4)) < 0.6); np.fill_diagonal(W, 0)
    comp = ((W + W.T) > 0).astype(int)
    conn = connected_components(comp, directed=False)[0] == 1
    sc = connected_components((W > 0).astype(int), directed=True, connection="strong")[0] == 1
    t1, l1 = fit_bt(W, 40.0); t2, l2 = fit_bt(W, 80.0)
    finite = abs(l2 - l1) < 1e-6 and np.max(np.abs(t1)) < 39   # box doubling does not improve, interior
    tally[(conn, sc, finite)] = tally.get((conn, sc, finite), 0) + 1
for k, v in sorted(tally.items()):
    say(f"   comparison-connected={k[0]!s:5} win-strongly-connected={k[1]!s:5} interior finite maximiser={k[2]!s:5}: {v}")
say("   reading: iff holds when the comparison graph is connected; a disconnected graph whose components are each")
say("   strongly connected has finite (non-unique) maximisers while the win graph is not strongly connected.")

say("\nV4 coder flips (mpmath 40 digits)")
mp.mp.dps = 40
def g(x, e): return mp.log((e + (1 - 2 * e) / (1 + mp.e ** (-x))) / (1 - e - (1 - 2 * e) / (1 + mp.e ** (-x))))
for e in (mp.mpf("0.05"), mp.mpf(0)):
    x = mp.log(4)  # logit 0.80
    obs_adj = e + (1 - 2 * e) * mp.mpf("0.8"); obs_far = e + (1 - 2 * e) * mp.mpf(16) / 17
    pred = 1 / (1 + mp.e ** (-2 * mp.log(obs_adj / (1 - obs_adj))))
    say(f"   e={float(e):.2f}: observed adj {float(obs_adj):.4f}, far {float(obs_far):.4f}, additive prediction {float(pred):.4f},"
        f" shortfall g(2x)-2g(x) = {float(g(2*x,e)-2*g(x,e)):+.4f} logit" + ("  (CONTROL, must be 0)" if e == 0 else ""))
t, a = sp.symbols("t a", real=True)
h = (sp.Rational(1, 4) - t**2) / (sp.Rational(1, 4) - a**2 * t**2)
say("   h'(t) - 8(a^2-1)t/(4a^2t^2-1)^2 simplifies to:", sp.simplify(sp.diff(h, t) - 8*(a**2-1)*t/(4*a**2*t**2-1)**2))
xs = np.linspace(0, 8, 401); ee = 0.05
gg = np.log((ee + (1-2*ee)*expit(xs)) / (1 - ee - (1-2*ee)*expit(xs)))
say(f"   max second difference of g on [0,8] (must be <=0 for concavity): {np.max(np.diff(gg, 2)):.2e}")
gs = lambda x, e: np.log((e+(1-2*e)*expit(x))/(1-e-(1-2*e)*expit(x)))
say(f"   CONTROL (mixed signs x=2,y=-1 not covered by the proposition): g(1)-g(2)-g(-1) = {gs(1,.05)-gs(2,.05)-gs(-1,.05):+.4f}")

say("\nV5 rank-one df by Jacobian rank")
def jac_rank(Dn, C, theta, k, separate=False):
    prs = list(itertools.combinations(range(Dn), 2))
    if separate:
        return C * (Dn - 1)
    J = np.zeros((len(prs) * C, Dn + C))
    for c in range(C):
        for p_, (i, j) in enumerate(prs):
            rr = c * len(prs) + p_
            J[rr, i] += k[c]; J[rr, j] -= k[c]; J[rr, Dn + c] = theta[i] - theta[j]
    return np.linalg.matrix_rank(J)
ok = True
for Dn in range(3, 8):
    for C in range(2, 5):
        rk = jac_rank(Dn, C, rng.normal(size=Dn), rng.uniform(0.5, 2, C))
        df = C * (Dn - 1) - rk
        ok &= df == (C - 1) * (Dn - 2)
        if (Dn, C) == (6, 3): say(f"   D=6 C=3: rank-one model rank {rk}, separate {C*(Dn-1)}, df {df}; (C-1)(D-1) would be {(C-1)*(Dn-1)}")
say("   (C-1)(D-2) matches the Jacobian count for D=3..7, C=2..4:", ok)
say("   CONTROL all-equal theta: rank drops to", jac_rank(6, 3, np.zeros(6), np.ones(3)), "(k unidentified)")
TH = np.array([2, 1, 0, 0, 0, 0]) * logit(0.74)
prs6 = list(itertools.combinations(range(6), 2))
M = np.array([[k_ * (TH[i] - TH[j]) for k_ in (1, 0.6, -1)] for i, j in prs6])
sv = np.linalg.svd(M, compute_uv=False); say(f"   reversed third criterion: singular values {np.round(sv,4)} -> rank one")
TS = TH.copy(); TS[[0, 1]] = TS[[1, 0]]
M2 = np.column_stack([M[:, 0], M[:, 1], [TS[i] - TS[j] for i, j in prs6]])
say(f"   CONTROL swap: singular values {np.round(np.linalg.svd(M2, compute_uv=False),4)} -> rank two")

say("\nV6 SST, product rule, Thurstone defect, triangle bound, circular triads")
viol = 0
for _ in range(2000):
    tt = rng.normal(size=3) * 2
    P = expit(tt[:, None] - tt[None, :])
    viol += abs(logit(P[0, 2]) - logit(P[0, 1]) - logit(P[1, 2])) > 1e-9
    viol += abs(P[0,1]*P[1,2]*P[2,0] - P[1,0]*P[2,1]*P[0,2]) > 1e-12
say("   BT tables violating additivity or product rule:", viol, "of 4000 checks")
say(f"   16/17 = {16/17:.4f}; probit far share {stats.norm.cdf(2*stats.norm.ppf(0.8)):.4f}; Thurstone defect at unit gaps "
    f"{logit(stats.norm.cdf(2)) - 2*logit(stats.norm.cdf(1)):+.4f}")
orders = list(itertools.permutations(range(3))); worst = -1
for _ in range(5000):
    w = rng.dirichlet(np.ones(6) * 0.3)
    P = np.zeros((3, 3))
    for wt, o in zip(w, orders):
        pos = {v: q for q, v in enumerate(o)}
        for i in range(3):
            for j in range(3):
                if i != j and pos[i] < pos[j]: P[i, j] += wt
    for i, j, k_ in itertools.permutations(range(3)):
        worst = max(worst, P[i, j] + P[j, k_] - P[i, k_])
say(f"   max of P_ij+P_jk-P_ik over 5000 mixtures of linear orders: {worst:.6f} (bound 1)")
say(f"   CONTROL table cycling at 0.9 each way: 0.9+0.9-0.1 = {0.9+0.9-0.1:.2f} > 1 (fires)")
bad = 0
for bits in itertools.product([0, 1], repeat=10):
    Wt = np.zeros((5, 5), int)
    for b, (i, j) in zip(bits, itertools.combinations(range(5), 2)):
        if b: Wt[i, j] = 1
        else: Wt[j, i] = 1
    cyc = sum(1 for i, j, k_ in itertools.combinations(range(5), 3)
              if (Wt[i,j] and Wt[j,k_] and Wt[k_,i]) or (Wt[j,i] and Wt[k_,j] and Wt[i,k_]))
    s = Wt.sum(1); bad += cyc != 10 - sum(int(x)*(int(x)-1)//2 for x in s)
say("   Kendall-Babington Smith formula vs brute force, all 1024 tournaments on 5: mismatches", bad)
say(f"   A3a example: sigma(5)={expit(5):.4f}, sigma(0.2)={expit(0.2):.4f}")
say(f"   Arm C: P(X<=14|41,.5)={stats.binom.cdf(14,41,.5):.4f} two-sided {stats.binomtest(14,41).pvalue:.4f}; "
    f"14/42 one-sided {stats.binom.cdf(14,42,.5):.4f} two-sided {stats.binomtest(14,42).pvalue:.4f}")
say(f"   language keep-order: Phi(1.046/0.5)={stats.norm.cdf(logit(.74)/.5):.3f}, Phi(1.046/1)={stats.norm.cdf(logit(.74)):.3f}")
say(f"   A3 source share 0.738 -> gap {logit(.738):.3f}; interval 0.561-0.893 -> logit {logit(.561):.3f} to {logit(.893):.3f}")
se_obs = (0.893 - 0.561) / 3.92; se_srs = np.sqrt(.738 * .262 / 155)
se_lo = (0.738 - 0.561) / 1.96; se_hi = (0.893 - 0.738) / 1.96
se_lg = (logit(.893) - logit(.561)) / 3.92; se_lg_srs = 1 / np.sqrt(155 * .738 * .262)
say(f"   design effect: share-scale symmetric {(se_obs/se_srs)**2:.2f}; lower half {(se_lo/se_srs)**2:.2f}; upper half "
    f"{(se_hi/se_srs)**2:.2f}; logit scale {(se_lg/se_lg_srs)**2:.2f}")

# ======================= PART 2: power =======================
say("\nW1 direction (Clopper-Pearson interval excludes .5), strict criterion: power >= .80 for every n' in [n, 1500]")
def cp_excl(x, n):
    lo = stats.beta.ppf(0.025, x, n - x + 1) if x > 0 else 0.0
    hi = stats.beta.ppf(0.975, x + 1, n - x) if x < n else 1.0
    return lo > 0.5 or hi < 0.5
REJ = {}
def rej(n):
    if n not in REJ: REJ[n] = np.array([cp_excl(x, n) for x in range(n + 1)])
    return REJ[n]
def pw(n, p): return float(stats.binom.pmf(np.arange(n + 1), n, p)[rej(n)].sum())
def nstrict(fun, nmax=1500):
    ok_from = None
    for n in range(nmax, 4, -1):
        if fun(n) >= 0.8: ok_from = n
        else: break
    first = next(n for n in range(5, nmax) if fun(n) >= 0.8)
    return first, ok_from
for p in (0.60, 0.65, 0.66, 0.70, 0.74, 0.80):
    f1, fs = nstrict(lambda n: pw(n, p))
    za, zb = 1.959964, 0.841621
    napx = ((za * 0.5 + zb * np.sqrt(p * (1 - p))) / (p - 0.5)) ** 2
    say(f"   share {p:.2f}: first n reaching .80 = {f1}; strict n = {fs}; normal approx {napx:.1f}")
say(f"   CONTROL size: max rejection at .5 over n=5..300 = {max(pw(n,.5) for n in range(5,301)):.4f}")
say(f"   CONTROL fires: power at n=37 with share 0.70 = {pw(37,.70):.3f} (<.80, so '37 suffices' is falsifiable)")

say("\nW2 transitivity triad resolved")
for p in (0.65, 0.74, 0.80):
    pik = expit(2 * logit(p))
    f1, fs = nstrict(lambda n: pw(n, p) ** 2 * pw(n, pik), 800)
    say(f"   adjacent {p:.2f}, far {pik:.3f}: first {f1}, strict {fs}; cycle caught at strict n: {pw(fs,p)**3:.3f}")

# --- LR machinery (own code)
def ll_bin(y, n, q):
    q = np.clip(q, 1e-12, 1 - 1e-12); return float(np.sum(y * np.log(q) + (n - y) * np.log(1 - q)))
def fit_pairs(y, n, prs, Dn, e=0.0, starts=1):
    def nll(tf):
        tt = np.concatenate([[0.0], tf]); s = expit(np.array([tt[i] - tt[j] for i, j in prs]))
        return -ll_bin(y, n, e + (1 - 2 * e) * s)
    best = None
    for st in range(starts):
        x0 = np.zeros(Dn - 1) if st == 0 else rng.normal(size=Dn - 1)
        r_ = optimize.minimize(nll, x0, method="BFGS")
        if best is None or r_.fun < best.fun: best = r_
    return -best.fun
def sat_ll(y, n, e=0.0):
    q = np.clip(y / n, e, 1 - e); return ll_bin(y, n, q)
TRI = [(0, 1), (1, 2), (0, 2)]
def lr_triad(y, n, e=0.0): return 2 * (sat_ll(y, n, e) - fit_pairs(y, n, TRI, 3, e))
def ncx_power(lam, df): return 1 - stats.ncx2.cdf(stats.chi2.ppf(0.95, df), df, max(lam, 1e-12))

say("\nW3 additivity, one triad, 1 df: analytic noncentral chi-square (expected-data LR) and own Monte Carlo")
G = logit(0.74)
scen = {"null BT 0.74/0.74/0.89": (0.74, 0.74, expit(2*G), 0.0),
        "no chaining 0.74x3": (0.74, 0.74, 0.74, 0.0),
        "half chaining far 0.83": (0.74, 0.74, expit(1.5*G), 0.0),
        "BT + 5% flips, ignored": (0.74, 0.74, expit(2*G), 0.05)}
for name, (a_, b_, c_, e) in scen.items():
    s = np.array([a_, b_, c_]); q = e + (1 - 2 * e) * s
    out = []
    for n in (100, 110, 200, 500, 1000):
        nn = np.full(3, float(n)); lam = lr_triad(q * nn, nn)
        out.append(f"n={n}: {ncx_power(lam,1):.3f}")
    say(f"   {name:<26} analytic " + "; ".join(out))
def mc_triad(s, n, e_gen, e_fit, R, seed):
    r_ = np.random.default_rng(seed); q = e_gen + (1 - 2 * e_gen) * np.array(s); nn = np.full(3, n); k = 0
    crit = stats.chi2.ppf(0.95, 1)
    for _ in range(R):
        y = r_.binomial(n, q).astype(float); k += lr_triad(y, nn, e_fit) > crit
    return k / R
say(f"   MC (seed 7001, 1500 reps) null BT n=200: {mc_triad((0.74,0.74,expit(2*G)),200,0,0,1500,7001):.3f}  [CONTROL]")
say(f"   MC no chaining n=100: {mc_triad((0.74,0.74,0.74),100,0,0,1500,7002):.3f}; n=110: {mc_triad((0.74,0.74,0.74),110,0,0,1500,7003):.3f}")
say(f"   MC half chaining n=500: {mc_triad((0.74,0.74,expit(1.5*G)),500,0,0,1500,7004):.3f}")
say(f"   MC flips ignored n=500: {mc_triad((0.74,0.74,expit(2*G)),500,.05,0,1500,7005):.3f}; n=1000: {mc_triad((0.74,0.74,expit(2*G)),1000,.05,0,1500,7006):.3f}")
say(f"   MC flips in likelihood n=1000: {mc_triad((0.74,0.74,expit(2*G)),1000,.05,.05,1500,7007):.3f}  [CONTROL]")

say("\nW4 additivity omnibus D=6, 10 df (Garner rival: pairs involving time or place at 0.74, rest 0.5)")
P6 = list(itertools.combinations(range(6), 2))
def lr_omni(y, n): return 2 * (sat_ll(y, n) - fit_pairs(y, n, P6, 6))
sg = np.array([0.74 if i in (0, 1) else 0.5 for i, j in P6])
for n in (100, 110, 200):
    nn = np.full(15, float(n)); say(f"   analytic n={n}: {ncx_power(lr_omni(sg*nn, nn),10):.3f}")
r_ = np.random.default_rng(7101); crit10 = stats.chi2.ppf(.95, 10)
sn = expit(np.array([TH[i] - TH[j] for i, j in P6]))
k1 = sum(lr_omni(r_.binomial(100, sg).astype(float), np.full(15, 100.)) > crit10 for _ in range(400)) / 400
k0 = sum(lr_omni(r_.binomial(100, sn).astype(float), np.full(15, 100.)) > crit10 for _ in range(400)) / 400
say(f"   MC 400 reps n=100: Garner {k1:.3f}; Navon null {k0:.3f} [CONTROL]")

say("\nW5 rank one, D=6, C=3, 8 df (rank-one null with free-sign k, k1 = 1)")
def fit_r1(Y, n):
    def nll(par):
        tt = np.concatenate([[0.0], par[:5]]); kk = np.concatenate([[1.0], par[5:]])
        tot = 0.0
        for c in range(3):
            s = expit(kk[c] * np.array([tt[i] - tt[j] for i, j in P6])); tot -= ll_bin(Y[c], n, s)
        return tot
    best = None
    for k0_ in ([1, 1], [1, -1], [-1, 1], [0.5, 0.5]):
        x0 = np.concatenate([-np.arange(1, 6) * 0.3, k0_])
        r2 = optimize.minimize(nll, x0, method="BFGS")
        if best is None or r2.fun < best.fun: best = r2
    return -best.fun, best.x[6]
def lr_r1(Y, n):
    sep = sum(fit_pairs(Y[c], n, P6, 6) for c in range(3)); r1, k3 = fit_r1(Y, n)
    return 2 * (sep - r1), k3
TSW = TH.copy(); TSW[[0, 1]] = TSW[[1, 0]]; TFL = TH.copy(); TFL[0] = TFL[1] = 1.5 * G
sc4 = {"null k=1,.6,1.5": ([TH]*3, (1, .6, 1.5)), "swap": ([TH, TH, TSW], (1, 1, 1)),
       "tie": ([TH, TH, TFL], (1, 1, 1)), "reverse": ([TH]*3, (1, 1, -1))}
def shares4(v):
    ths, ks = v; return np.array([expit(ks[c] * np.array([ths[c][i] - ths[c][j] for i, j in P6])) for c in range(3)])
for name, v in sc4.items():
    S = shares4(v); res = []
    for n in (20, 40):
        lam, _ = lr_r1(S * n, n); res.append(f"n={n}: {ncx_power(lam,8):.3f} (lambda {lam:.2f})")
    say(f"   analytic {name:<16} " + "; ".join(res))
crit8 = stats.chi2.ppf(.95, 8)
for name, n, R_, seed in (("null k=1,.6,1.5", 40, 250, 7201), ("tie", 40, 250, 7202), ("swap", 20, 150, 7203), ("reverse", 40, 250, 7204)):
    r_ = np.random.default_rng(seed); S = shares4(sc4[name]); rj = neg = 0
    for _ in range(R_):
        Y = r_.binomial(n, S).astype(float); G2, k3 = lr_r1(Y, n); rj += G2 > crit8; neg += k3 < 0
    say(f"   MC {name:<16} n={n} reps={R_}: rejection {rj/R_:.3f}; fitted k3<0 {neg/R_:.3f}")

say("\nW6 languages, time-place logit 1.046 + v, v ~ N(0, s^2)")
def nct_power(L, n, s, mu=G):
    var = s**2 + 1 / (n * expit(mu) * (1 - expit(mu)))
    delta = mu / np.sqrt(var / L); c = stats.t.ppf(.975, L - 1)
    return 1 - stats.nct.cdf(c, L - 1, delta) + stats.nct.cdf(-c, L - 1, delta)
for s in (0.5, 1.0):
    for L in (4, 8, 12):
        say(f"   noncentral t s={s} L={L:>2}: " + "; ".join(f"n={n} {nct_power(L,n,s):.3f}" for n in (50, 100, 300, 10**6)))
def mc_lang(L, n, s, mu, R, seed):
    r_ = np.random.default_rng(seed); het = mn = 0
    for _ in range(R):
        y = r_.binomial(n, expit(mu + s * r_.standard_normal(L)))
        p_ = y.sum() / (L * n); chi = np.sum((y - n*p_)**2 / (n*p_*(1-p_)))   # 2xL Pearson, own formula
        het += stats.chi2.sf(chi, L - 1) < .05
        el = np.log((y + .5) / (n - y + .5)); tst = el.mean() / (el.std(ddof=1) / np.sqrt(L))
        mn += 2 * stats.t.sf(abs(tst), L - 1) < .05
    return het / R, mn / R
for (L, n, s) in ((8, 50, .5), (8, 100, .5), (4, 200, .5), (4, 300, .5), (12, 100, 1.), (8, 300, 1.)):
    h_, m_ = mc_lang(L, n, s, G, 2000, 7300 + L * 10 + n)
    say(f"   MC L={L:>2} n={n} s={s}: heterogeneity {h_:.3f}; mean direction {m_:.3f}")
h0, _ = mc_lang(8, 100, 0.0, G, 2000, 7401); _, m0 = mc_lang(8, 100, 0.5, 0.0, 2000, 7402); _, m0b = mc_lang(4, 50, 1.0, 0.0, 2000, 7403)
say(f"   CONTROL heterogeneity at s=0 L=8 n=100: {h0:.3f}; CONTROL mean-direction at true mean 0, L=8 n=100 s=0.5: {m0:.3f}; L=4 n=50 s=1: {m0b:.3f}")

with open(OUT, "w") as fh: fh.write("\n".join(LOG) + "\n")
