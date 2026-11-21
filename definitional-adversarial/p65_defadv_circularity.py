"""P65 definitional adversarial, step 1: is the registered definitional label conditioned on direction?

Reads the registered final codes (other branch, read only) and asks:
 (a) how the subtypes split by direction (TZ is defined as 'a clock or calendar value stated as holding at a place',
     i.e. the place-over-time frame; SUN and ARR are defined on a time restricting an asserted location, the
     time-over-place frame);
 (b) a null world: each item carries a latent convention tie independent of direction; the registered rule is
     applied as written (TZ only fires on a PT frame, SUN/ARR only on a TP frame, EXPR on either). How often does the
     registered analysis (exact conditional common OR across language, two-sided) report OR < 1 with p < 0.05?
 (c) negative control: the same latent ties, but the label fires regardless of frame (a direction-blind rule).
     The analysis must then report OR < 1, p < 0.05 near the nominal rate (<= 0.05 one tail). If it does not,
     the simulation is broken.
Usage: python3 -I p65_defadv_circularity.py
"""
import csv, math, random
from math import comb
from fractions import Fraction
D = "/Users/as/_Claude/Claude/worktrees/p65-definitional-dependence-2026-11-18/definitional/"
O = "/Users/as/_Claude/Claude/worktrees/p65-stats-fix/definitional-adversarial/"
fin = list(csv.DictReader(open(D + "p65_defdep_final.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE))
assert len(fin) == 243
out = []; P = out.append

def tabs(dat):
    t = {l: {(g, y): 0 for g in (0, 1) for y in (0, 1)} for l in ("en", "id")}
    for l, g, y in dat: t[l][(g, y)] += 1
    return [t["en"], t["id"]]

def poly_of(ts):
    poly = {0: 1}
    for t in ts:
        n1 = t[(1, 0)] + t[(1, 1)]; n0 = t[(0, 0)] + t[(0, 1)]; m = t[(1, 1)] + t[(0, 1)]
        new = {}
        for s, c in poly.items():
            for x in range(max(0, m - n0), min(n1, m) + 1):
                new[s + x] = new.get(s + x, 0) + c * comb(n1, x) * comb(n0, m - x)
        poly = new
    return poly

def exact(dat):
    """two-sided exact conditional p and direction of the conditional OR (sign of S - E[S | psi=1])."""
    ts = tabs(dat); poly = poly_of(ts); s = sum(t[(1, 1)] for t in ts)
    tot = sum(poly.values()); pobs = poly[s]
    p = sum(v for v in poly.values() if v <= pobs) / tot
    mean = sum(k * v for k, v in poly.items()) / tot
    ndef = sum(t[(1, 0)] + t[(1, 1)] for t in ts)
    return p, s - mean, ndef

def mh_or(dat):
    R = S = 0.0
    for t in tabs(dat):
        A, B, C, Dd = t[(1, 1)], t[(1, 0)], t[(0, 1)], t[(0, 0)]; n = A + B + C + Dd
        R += A * Dd / n; S += B * C / n
    return R / S if S else float("inf")

# (a) subtype by direction
P("(a) REGISTERED DEFINITIONAL CODES, subtype x direction (primary rule)")
from collections import Counter
c = Counter((r["subtype"], r["final"]) for r in fin if r["definitional"] == "1")
for k in sorted(c): P(f"  {k[0]:5s} {k[1]}: {c[k]}")
obs = [(r["corpus"], int(r["definitional"]), int(r["final"] == "TP")) for r in fin]
p, d, n = exact(obs); P(f"  all definitional: n {n}, exact conditional p {p:.6f}, MH OR {mh_or(obs):.4f}")
nontz = [(r["corpus"], int(r["definitional"] == "1" and r["subtype"] != "TZ"), int(r["final"] == "TP"))
         for r in fin if not (r["definitional"] == "1" and r["subtype"] == "TZ")]
p2, d2, n2 = exact(nontz)
P(f"  TZ rows removed (n {len(nontz)}), definitional non-TZ: n {n2}, TP {sum(1 for l,g,y in nontz if g and y)}, "
  f"exact conditional p {p2:.4f}, MH OR {mh_or(nontz):.4f}")

# (b), (c) null worlds
nTP = sum(1 for r in fin if r["final"] == "TP"); nPT = 243 - nTP
q_tz = c[("TZ", "PT")] / nPT                       # labelled TZ rate among PT rows
q_sa = (c.get(("ARR", "TP"), 0) + c.get(("SUN", "TP"), 0)) / nTP
q_e = sum(v for (s, _), v in c.items() if s == "EXPR") / 243
P(f"\n(b) NULL WORLD: latent ties independent of direction; rates q_TZ {q_tz:.4f}, q_SUN/ARR {q_sa:.4f}, "
  f"q_EXPR {q_e:.4f}; direction kept as observed (TP {nTP}, PT {nPT}), language kept")
rng = random.Random(20261119); R = 5000
def sim(directional):
    hits = 0; ors = []; ns = []
    for _ in range(R):
        dat = []
        for r in fin:
            tp = r["final"] == "TP"
            ltz = rng.random() < q_tz; lsa = rng.random() < q_sa; le = rng.random() < q_e
            if directional: g = (ltz and not tp) or (lsa and tp) or le
            else: g = ltz or lsa or le
            dat.append((r["corpus"], int(g), int(tp)))
        if sum(g for _, g, _ in dat) == 0: ors.append(float("nan")); ns.append(0); continue
        p, d, n = exact(dat); ns.append(n)
        o = mh_or(dat); ors.append(o)
        if p < 0.05 and d < 0: hits += 1
    good = sorted(o for o in ors if o == o)
    return hits / R, good[len(good) // 2], sorted(ns)[R // 2]
h, mo, mn = sim(True)
P(f"  registered (directional) rule: share of {R} runs reporting OR < 1 with p < 0.05: {h:.4f}; "
  f"median MH OR {mo:.4f}; median n definitional {mn}")
h2, mo2, mn2 = sim(False)
P(f"\n(c) NEGATIVE CONTROL, same latent ties, label fires regardless of frame:")
P(f"  share reporting OR < 1 with p < 0.05: {h2:.4f}; median MH OR {mo2:.4f}; median n definitional {mn2}")
P(f"  CONTROL {'FIRED (no false association, <= 0.05)' if h2 <= 0.05 else 'DID NOT FIRE: simulation suspect'}")
txt = "\n".join(out); print(txt)
open(O + "p65_defadv_circularity_run_2026-11-19.txt", "w").write(txt + "\n")
