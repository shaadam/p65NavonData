"""p65 wave 1: Bradley-Terry fitting helpers shared by the Appendix D checks and power simulations.

Data layout: for one criterion, `wins[i, j]` = number of directional items in which dimension i is
stated over dimension j (i dominates j). Pairs with i < j are the comparison units.

Models
- sat:      every pair has its own share (no scale).                       params: D(D-1)/2 per criterion
- bt:       share(i over j) = logistic(theta_i - theta_j), theta_0 = 0.       params: D-1 per criterion
- rank1:    across C criteria, logit share_c(i over j) = k_c (theta_i - theta_j), k_0 = 1.  params: (D-1)+(C-1)
- sepbt:    a separate bt per criterion.                                      params: C(D-1)

All log-likelihoods are binomial, conditional on the number of directional items per pair (the
Davidson-ties and Poisson-log-linear arguments in Appendix D justify conditioning).
"""
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, gammaln

def pairs(D):
    return [(i, j) for i in range(D) for j in range(i + 1, D)]

def _binom_ll(y, n, p):
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return float(np.sum(y * np.log(p) + (n - y) * np.log1p(-p)))

def pair_counts(wins):
    D = wins.shape[0]
    P = pairs(D)
    y = np.array([wins[i, j] for i, j in P], float)
    n = np.array([wins[i, j] + wins[j, i] for i, j in P], float)
    return P, y, n

def ll_sat(wins):
    P, y, n = pair_counts(wins)
    m = n > 0
    p = np.where(m, y / np.where(m, n, 1), 0.5)
    return _binom_ll(y[m], n[m], p[m])

def _design(D):
    P = pairs(D)
    X = np.zeros((len(P), D - 1))
    for r, (i, j) in enumerate(P):
        if i > 0:
            X[r, i - 1] += 1
        if j > 0:
            X[r, j - 1] -= 1
    return X

def fit_bt(wins, ridge=1e-6, iters=100):
    """Newton-Raphson for theta (theta_0 = 0). A tiny ridge keeps the step defined when the MLE
    does not exist (a dimension never loses, or never wins); callers check `diverged`."""
    D = wins.shape[0]
    P, y, n = pair_counts(wins)
    X = _design(D)
    th = np.zeros(D - 1)
    for _ in range(iters):
        eta = X @ th
        p = expit(eta)
        g = X.T @ (y - n * p) - ridge * th
        H = (X * (n * p * (1 - p))[:, None]).T @ X + ridge * np.eye(D - 1)
        step = np.linalg.solve(H, g)
        th = th + step
        if np.max(np.abs(step)) < 1e-10:
            break
    theta = np.concatenate([[0.0], th])
    ll = _binom_ll(y, n, expit(X @ th))
    return theta, ll, bool(np.max(np.abs(th)) > 15)

def fit_rank1(wins_list):
    """wins_list: C arrays D x D. logit share_c = k_c (theta_i - theta_j), theta_0 = 0, k_0 = 1."""
    C = len(wins_list)
    D = wins_list[0].shape[0]
    X = _design(D)
    data = [pair_counts(w)[1:] for w in wins_list]

    def nll(par):
        th = par[:D - 1]
        k = np.concatenate([[1.0], par[D - 1:]])
        tot = 0.0
        gr_th = np.zeros(D - 1)
        gr_k = np.zeros(C)
        eta0 = X @ th
        for c, (y, n) in enumerate(data):
            p = expit(k[c] * eta0)
            p = np.clip(p, 1e-12, 1 - 1e-12)
            tot -= np.sum(y * np.log(p) + (n - y) * np.log1p(-p))
            r = y - n * p
            gr_th -= k[c] * (X.T @ r)
            gr_k[c] = -np.sum(r * eta0)
        return tot, np.concatenate([gr_th, gr_k[1:]])

    # start: theta from criterion 0, k_c from regression of separate fits
    th0, _, _ = fit_bt(wins_list[0])
    starts = []
    ks = []
    for w in wins_list[1:]:
        thc, _, _ = fit_bt(w)
        denom = np.dot(th0, th0)
        ks.append(np.dot(thc, th0) / denom if denom > 1e-9 else 0.0)
    starts.append(np.concatenate([th0[1:], ks]))
    # second start: pooled theta, unit k (guards against a poor criterion-0 start)
    pooled = sum(wins_list)
    thp, _, _ = fit_bt(pooled)
    starts.append(np.concatenate([thp[1:], np.ones(C - 1)]))
    best = None
    for s in starts:
        r = minimize(nll, s, jac=True, method="BFGS", options={"gtol": 1e-8, "maxiter": 2000})
        if best is None or r.fun < best.fun:
            best = r
    th = np.concatenate([[0.0], best.x[:D - 1]])
    k = np.concatenate([[1.0], best.x[D - 1:]])
    return th, k, -best.fun

def ll_sepbt(wins_list):
    return sum(fit_bt(w)[1] for w in wins_list)

def simulate_wins(theta, n_per_pair, rng, k=1.0, err=0.0):
    """Binomial directional counts for every pair; err = probability a coder flips the direction."""
    D = len(theta)
    w = np.zeros((D, D))
    for i, j in pairs(D):
        p = expit(k * (theta[i] - theta[j]))
        p = err + (1 - 2 * err) * p
        y = rng.binomial(n_per_pair, p)
        w[i, j] = y
        w[j, i] = n_per_pair - y
    return w

def circular_triads(wins):
    """Kendall & Babington Smith count on the majority tournament (ties in a pair: pair skipped,
    returned separately)."""
    D = wins.shape[0]
    beats = np.zeros((D, D), int)
    tied = 0
    for i, j in pairs(D):
        if wins[i, j] > wins[j, i]:
            beats[i, j] = 1
        elif wins[j, i] > wins[i, j]:
            beats[j, i] = 1
        else:
            tied += 1
    cyc = 0
    for a in range(D):
        for b in range(a + 1, D):
            for c in range(b + 1, D):
                if any(beats[x, y] + beats[y, x] == 0 for x, y in ((a, b), (b, c), (a, c))):
                    continue  # a tied pair: the triad is neither cyclic nor transitive
                s = beats[a, b] + beats[b, c] + beats[c, a]
                if s in (0, 3):
                    cyc += 1
    return cyc, tied
