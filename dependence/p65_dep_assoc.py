"""P65 unit 3: logical dependence as a variable: direction (TP/PT) x dependent (0/1) x language.

Copy of definitional/p65_defdep_assoc.py (branch claude/p65-definitional-dependence-2026-11-18), with the input
file and column changed (definitional -> a dependence column given on the command line) and, appended, the
registered statistic s0 (TP share among non-dependent, exact Clopper-Pearson 95%) and the verdict table
(docs/p65_unit3-dependence_registration_2026-11-19.md).
Usage: python3 -I p65_dep_assoc.py COLUMN [FINAL_TSV] [TAG]
"""
import csv, math, random
from fractions import Fraction
from math import comb
import numpy as np
from scipy.optimize import brentq

import sys
D = "/Users/as/_Claude/Claude/worktrees/p65-stats-fix/dependence/"
COL = sys.argv[1]
FIN = sys.argv[2] if len(sys.argv) > 2 else D + "p65_dep_final.tsv"
TAG = sys.argv[3] if len(sys.argv) > 3 else COL
rows = list(csv.DictReader(open(FIN), delimiter="\t", quoting=csv.QUOTE_NONE))
data = [(r["corpus"], int(r[COL]), 1 if r["final"] == "TP" else 0) for r in rows]
assert len(data) == 243


def table(dat, lang):
    """2x2 for one language: a=def&PT, b=def&TP, c=nondef&PT, d=nondef&TP.
    Odds ratio reported = odds(TP | def) / odds(TP | nondef) = (b*c)/(a*d)."""
    t = {(g, y): 0 for g in (0, 1) for y in (0, 1)}
    for l, g, y in dat:
        if lang is None or l == lang:
            t[(g, y)] += 1
    return t


def fisher(t):
    # x = TP count among definitional; margins fixed
    n1 = t[(1, 0)] + t[(1, 1)]; n0 = t[(0, 0)] + t[(0, 1)]; m = t[(1, 1)] + t[(0, 1)]
    lo, hi = max(0, m - n0), min(n1, m)
    p = {x: Fraction(comb(n1, x) * comb(n0, m - x), comb(n1 + n0, m)) for x in range(lo, hi + 1)}
    obs = p[t[(1, 1)]]
    return sum(v for v in p.values() if v <= obs), p


def strat_support(tabs):
    """Exact conditional distribution of S = sum of TP-among-def over strata: coefficient c_s with
    P(S=s | psi) = c_s psi^s / sum c_u psi^u."""
    poly = {0: 1}
    for t in tabs:
        n1 = t[(1, 0)] + t[(1, 1)]; n0 = t[(0, 0)] + t[(0, 1)]; m = t[(1, 1)] + t[(0, 1)]
        new = {}
        for s, c in poly.items():
            for x in range(max(0, m - n0), min(n1, m) + 1):
                new[s + x] = new.get(s + x, 0) + c * comb(n1, x) * comb(n0, m - x)
        poly = new
    return poly


def cond_mle_ci(poly, s_obs):
    ks = sorted(poly)
    def mean(lpsi):
        w = np.array([math.log(poly[k]) + k * lpsi for k in ks]); w = np.exp(w - w.max()); w /= w.sum()
        return float(np.dot(w, ks))
    def tail_ge(lpsi):
        w = np.array([math.log(poly[k]) + k * lpsi for k in ks]); w = np.exp(w - w.max()); w /= w.sum()
        return float(sum(wi for wi, k in zip(w, ks) if k >= s_obs))
    def tail_le(lpsi):
        w = np.array([math.log(poly[k]) + k * lpsi for k in ks]); w = np.exp(w - w.max()); w /= w.sum()
        return float(sum(wi for wi, k in zip(w, ks) if k <= s_obs))
    if s_obs == ks[0]: mle = 0.0
    elif s_obs == ks[-1]: mle = math.inf
    else: mle = math.exp(brentq(lambda l: mean(l) - s_obs, -30, 30))
    lo = math.exp(brentq(lambda l: tail_ge(l) - 0.025, -30, 30)) if s_obs > ks[0] else 0.0
    hi = math.exp(brentq(lambda l: tail_le(l) - 0.025, -30, 30)) if s_obs < ks[-1] else math.inf
    tot = sum(poly.values()); pobs = Fraction(poly[s_obs], tot)
    p2 = sum(Fraction(v, tot) for v in poly.values() if Fraction(v, tot) <= pobs)
    return mle, lo, hi, p2


def mh(tabs):
    # Robins-Breslow-Greenland on OR = (b c)/(a d) with exposure def, outcome TP.
    R = S = PR = PSQS = QS = 0.0
    for t in tabs:
        a, b, c, d = t[(1, 0)], t[(1, 1)], t[(0, 0)], t[(0, 1)]
        n = a + b + c + d
        # cast as standard 2x2: exposed=def, outcome=TP: A=def&TP=b, B=def&PT=a, C=nondef&TP=d, Dd=nondef&PT=c
        A, B, C, Dd = b, a, d, c
        Ri, Si = A * Dd / n, B * C / n
        Pi, Qi = (A + Dd) / n, (B + C) / n
        R += Ri; S += Si; PR += Pi * Ri; PSQS += Pi * Si + Qi * Ri; QS += Qi * Si
    or_ = R / S
    var = PR / (2 * R * R) + PSQS / (2 * R * S) + QS / (2 * S * S)
    se = math.sqrt(var)
    return or_, math.exp(math.log(or_) - 1.96 * se), math.exp(math.log(or_) + 1.96 * se)


def design(dat, inter):
    X = []; y = []
    for l, g, yy in dat:
        idl = 1.0 if l == "id" else 0.0
        row = [1.0, float(g), idl] + ([float(g) * idl] if inter else [])
        X.append(row); y.append(yy)
    return np.array(X), np.array(y, float)


def firth_ll(beta, X, y):
    eta = X @ beta; p = 1 / (1 + np.exp(-eta))
    W = p * (1 - p); I = X.T @ (X * W[:, None])
    return float(np.sum(y * eta - np.log1p(np.exp(eta))) + 0.5 * np.linalg.slogdet(I)[1])


def firth(X, y, fixed=None, tol=1e-10):
    """Firth via modified score Newton; fixed=(j, value) holds beta_j fixed (profile)."""
    k = X.shape[1]; beta = np.zeros(k)
    if fixed: beta[fixed[0]] = fixed[1]
    free = [j for j in range(k) if not fixed or j != fixed[0]]
    for _ in range(200):
        eta = X @ beta; p = 1 / (1 + np.exp(-eta)); W = p * (1 - p)
        I = X.T @ (X * W[:, None]); Iinv = np.linalg.inv(I)
        h = W * np.einsum("ij,jk,ik->i", X, Iinv, X)
        U = X.T @ (y - p + h * (0.5 - p))
        Ifr = I[np.ix_(free, free)]
        step = np.linalg.solve(Ifr, U[free])
        mx = np.max(np.abs(step))
        if mx > 5: step *= 5 / mx
        # step-halving on penalised likelihood
        old = firth_ll(beta, X, y); t = 1.0
        while True:
            nb = beta.copy(); nb[free] += t * step
            if firth_ll(nb, X, y) >= old - 1e-12 or t < 1e-6: break
            t /= 2
        beta = nb
        if np.max(np.abs(t * step)) < tol: break
    eta = X @ beta; p = 1 / (1 + np.exp(-eta)); W = p * (1 - p)
    cov = np.linalg.inv(X.T @ (X * W[:, None]))
    return beta, cov, firth_ll(beta, X, y)


def profile_ci(X, y, j, beta, llmax):
    crit = 3.841458820694124 / 2
    f = lambda v: firth(X, y, fixed=(j, v))[2] - (llmax - crit)
    lo = brentq(f, beta[j] - 15, beta[j]); hi = brentq(f, beta[j], beta[j] + 15)
    return lo, hi


def lrt_p(X, y, j, llmax):
    from scipy.stats import chi2
    ll0 = firth(X, y, fixed=(j, 0.0))[2]
    return float(chi2.sf(2 * (llmax - ll0), 1))


out = []
P = out.append
P(f"TABLE direction x dependent x language (column {COL}, file {FIN.split('/')[-1]})")
tabs = {}
for lang in ("en", "id", None):
    t = table(data, lang); tabs[lang] = t
    name = lang or "pooled"
    P(f"  {name:6s} dependent: TP {t[(1,1)]:3d} PT {t[(1,0)]:3d} (n {t[(1,1)]+t[(1,0)]:3d}) | "
      f"non-dependent: TP {t[(0,1)]:3d} PT {t[(0,0)]:3d} (n {t[(0,1)]+t[(0,0)]:3d}) | "
      f"total TP {t[(1,1)]+t[(0,1)]} PT {t[(1,0)]+t[(0,0)]}")

P("\nFISHER exact, two-sided, OR = odds(TP|dependent)/odds(TP|non-dependent); conditional MLE and exact 95% interval")
for lang in ("en", "id", None):
    t = tabs[lang]; pf, _ = fisher(t)
    poly = strat_support([t])
    try:
        mle, lo, hi, _ = cond_mle_ci(poly, t[(1, 1)])
    except Exception:
        mle = lo = hi = float("nan")
    den = t[(1, 0)] * t[(0, 1)]
    sor = (t[(1, 1)] * t[(0, 0)]) / den if den else float("inf")
    P(f"  {lang or 'pooled(collapsed)':18s} p = {float(pf):.5f}  (exact {pf.numerator}/{pf.denominator}) "
      f"sample OR {sor:.4f}  cond. MLE {mle:.4f} [{lo:.4f}, {hi:.4f}]")

poly = strat_support([tabs["en"], tabs["id"]]); s_obs = tabs["en"][(1, 1)] + tabs["id"][(1, 1)]
try:
    mle, lo, hi, p2 = cond_mle_ci(poly, s_obs)
except Exception:
    mle = lo = hi = p2 = float("nan")  # boundary (separation): reported as undefined
P(f"\nEXACT CONDITIONAL common OR across language strata: S_obs = {s_obs}; MLE {mle:.4f} [{lo:.4f}, {hi:.4f}]; "
  f"two-sided p (prob <= obs) = {float(p2):.6f}")
try:
    mor, mlo, mhi = mh([tabs["en"], tabs["id"]])
except ZeroDivisionError:
    mor = mlo = mhi = float("inf")  # a zero cell in every stratum: undefined
P(f"MANTEL-HAENSZEL common OR {mor:.4f} [{mlo:.4f}, {mhi:.4f}] (Robins-Breslow-Greenland)")

P("\nFIRTH logistic, outcome TP=1. Coefficients (log-odds), Wald SE, profile-penalised 95% interval, LR p")
fits = {}
for inter in (False, True):
    X, y = design(data, inter)
    beta, cov, ll = firth(X, y); fits[inter] = (beta, cov, ll)
    names = ["intercept", "dependent", "indonesian"] + (["dep x indonesian"] if inter else [])
    P(f"  model {'with' if inter else 'without'} interaction: penalised loglik {ll:.6f}")
    for j, nm in enumerate(names):
        try:
            lo_, hi_ = profile_ci(X, y, j, beta, ll)
        except Exception:
            lo_, hi_ = float("nan"), float("nan")
        pj = lrt_p(X, y, j, ll)
        P(f"    {nm:18s} b {beta[j]: .4f} SE {math.sqrt(cov[j,j]):.4f}  OR {math.exp(beta[j]):8.4f} "
          f"[{math.exp(lo_):.4f}, {math.exp(hi_):.4f}]  LR p {pj:.5f}")
b, cov, _ = fits[False]
from scipy.special import expit
P("\nPREDICTED TP share (Firth main-effects model)")
for nm, idl in (("en", 0), ("id", 1)):
    for g in (0, 1):
        x = np.array([1, g, idl]); eta = x @ b; se = math.sqrt(x @ cov @ x)
        P(f"  {nm} {'dependent    ' if g else 'non-dependent'} {expit(eta):.4f} "
          f"(Wald 95% {expit(eta-1.96*se):.4f}-{expit(eta+1.96*se):.4f})")

# Negative control: shuffle definitional labels within language
rng = random.Random(6518); R = 2000
ors = []; ps = []; extreme = 0; extreme_hi = 0
obs_s = s_obs
for _ in range(R):
    sh = []
    for lang in ("en", "id"):
        sub = [d for d in data if d[0] == lang]; labs = [d[1] for d in sub]; rng.shuffle(labs)
        sh += [(l, g2, yy) for (l, _, yy), g2 in zip(sub, labs)]
    st = [table(sh, "en"), table(sh, "id")]
    pl = strat_support(st); s = st[0][(1, 1)] + st[1][(1, 1)]
    try:
        m_, _, _, pp = cond_mle_ci(pl, s)
    except Exception:
        m_, pp = float("nan"), float("nan")
    ors.append(m_); ps.append(float(pp))
    if s <= obs_s: extreme += 1
    if s >= obs_s: extreme_hi += 1
ors.sort(); ps.sort()
P(f"\nNEGATIVE CONTROL: dependence labels shuffled within language, {R} permutations, seed 6518")
P(f"  median conditional OR {ors[R//2]:.3f} (observed {mle:.3f}); share of shuffles with p < 0.05: "
  f"{sum(p < 0.05 for p in ps)/R:.4f}; share with S <= observed {obs_s}: {extreme/R:.4f}; share with S >= observed: {extreme_hi/R:.4f} (one-sided permutation p each way)")
P(f"  CONTROL FIRES iff median OR in [0.5, 2] and share p<0.05 <= 0.10: "
  f"{'FIRED (association removed)' if 0.5 <= ors[R//2] <= 2 and sum(p < 0.05 for p in ps)/R <= 0.10 else 'DID NOT FIRE'}")
from scipy.stats import beta as _beta
def cp(k, n):
    if n == 0: return float("nan"), float("nan"), float("nan")
    lo = 0.0 if k == 0 else float(_beta.ppf(0.025, k, n - k + 1))
    hi = 1.0 if k == n else float(_beta.ppf(0.975, k + 1, n - k))
    return k / n, lo, hi
P("\nSHARES (raw counts, exact Clopper-Pearson 95%): TP share among dependent / non-dependent")
for lang in ("en", "id", None):
    t = tabs[lang]
    for g, nm in ((1, "dependent"), (0, "non-dependent")):
        k, n = t[(g, 1)], t[(g, 1)] + t[(g, 0)]; s, lo, hi = cp(k, n)
        P(f"  {lang or 'pooled':6s} {nm:13s} TP {k:3d} of {n:3d}  share {s:.3f} [{lo:.3f}, {hi:.3f}]")
t = tabs[None]; k0, n0 = t[(0, 1)], t[(0, 1)] + t[(0, 0)]; s0, lo0, hi0 = cp(k0, n0)
OV = 195 / 243
if n0 < 10: v = ("NOT TESTABLE", "NOT TESTABLE")
elif hi0 < 0.5: v = ("NOT SUPPORTED as stated (non-dependent lean place over time)", "NOT SUPPORTED")
elif lo0 <= 0.5 <= hi0 and lo0 <= OV <= hi0: v = ("UNDECIDED", "UNDECIDED")
elif lo0 <= 0.5 <= hi0: v = ("SUPPORTED", "NOT SUPPORTED")
elif lo0 > 0.5 and lo0 <= OV <= hi0: v = ("NOT SUPPORTED", "SUPPORTED")
elif lo0 > 0.5 and hi0 < OV: v = ("PARTLY (falls, stays above half)", "PARTLY (stays above half, falls)")
else: v = ("OTHER (above overall share)", "OTHER (above overall share)")
P(f"\nVERDICT (pooled, column {COL}): s0 = {k0}/{n0} = {s0:.3f} [{lo0:.3f}, {hi0:.3f}] vs overall {OV:.3f}")
P(f"  logical dependence: {v[0]}")
P(f"  Navon's hierarchy:  {v[1]}")
txt = "\n".join(out); print(txt)
open(D + f"p65_dep_assoc_run_{TAG}_2026-11-19.txt", "w").write(txt + "\n")
