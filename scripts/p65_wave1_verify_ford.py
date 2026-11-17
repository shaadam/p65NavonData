"""p65 wave1 verify: Ford condition by Zermelo/Hunter MM iteration (own route). Divergence = log-spread still growing.
Replaces V3 of p65_wave1_verify.py, whose box-optimiser detector was NON-DISCRIMINATING (stopped on tiny gradients)."""
import numpy as np
from scipy.sparse.csgraph import connected_components
def spread(W, iters):
    D = len(W); N = W + W.T; w = W.sum(1).astype(float); p = np.ones(D)
    out = {}
    for it in range(1, max(iters) + 1):
        den = np.array([sum(N[i, j] / (p[i] + p[j]) for j in range(D) if N[i, j]) for i in range(D)])
        p = np.where(den > 0, np.maximum(w, 1e-300) / np.where(den > 0, den, 1), p); p /= np.exp(np.mean(np.log(p)))
        if it in iters:
            lp = np.log(p); comp = connected_components((N > 0).astype(int), directed=False)[1]
            out[it] = max(np.ptp(lp[comp == c]) for c in set(comp))
    return out
rng = np.random.default_rng(9102); tally = {}
for _ in range(300):
    W = rng.integers(0, 3, size=(4, 4)) * (rng.random((4, 4)) < 0.6); np.fill_diagonal(W, 0)
    N = W + W.T
    conn = connected_components((N > 0).astype(int), directed=False)[0] == 1
    sc = connected_components((W > 0).astype(int), directed=True, connection="strong")[0] == 1
    s = spread(W, (300, 3000))
    finite = s[3000] - s[300] < 0.05 and s[3000] < 50
    tally[(conn, sc, finite)] = tally.get((conn, sc, finite), 0) + 1
for k, v in sorted(tally.items()):
    print(f"comparison-connected={k[0]!s:5} win-strongly-connected={k[1]!s:5} finite={k[2]!s:5}: {v}")
W = np.array([[0,2,1],[1,0,0],[0,3,0]])   # 0>1,0>2,1>0,2>1 : strongly connected
print("CONTROL SC table spread", spread(W,(300,3000)))
W = np.array([[0,2,1],[0,0,1],[0,1,0]])   # node 0 never loses
print("CONTROL never-loses table spread", spread(W,(300,3000)))
