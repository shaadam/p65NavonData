(* p65 wave 1, Appendix D symbolic checks. Run through
   scripts/wolfram-run.sh --timeout 120 -- -file <this file>
   Each claim W* is paired with a negative control W*c that MUST come out False
   (a control that came out True would mean the check cannot discriminate). *)

pr[tag_, val_] := Print[tag, " -> ", val];
assum = pi > 0 && pj > 0 && nu > 0 && eta > 1;

(* W1: Davidson (1970) ties model. Conditional on a non-tie, P(i beats j) is exactly Bradley-Terry. *)
dav = (pi/(pi + pj + nu Sqrt[pi pj])) / ((pi + pj)/(pi + pj + nu Sqrt[pi pj]));
pr["W1  Davidson conditional == BT", FullSimplify[dav - pi/(pi + pj) == 0, assum]];

(* W1c: control. Rao-Kupper (1967) ties model: conditional on non-tie is NOT BT when eta > 1. *)
rkI = pi/(pi + eta pj); rkJ = pj/(pj + eta pi);
pr["W1c Rao-Kupper conditional == BT (must be False)",
   FullSimplify[rkI/(rkI + rkJ) - pi/(pi + pj) == 0, assum]];
pr["W1c' witness pi=2,pj=1,eta=2", rkI/(rkI + rkJ) - pi/(pi + pj) /. {pi -> 2, pj -> 1, eta -> 2}];

(* W2: BT logit additivity: logit P(i,k) == logit P(i,j) + logit P(j,k). *)
bt[a_, b_] := Exp[a]/(Exp[a] + Exp[b]);
logit[p_] := Log[p/(1 - p)];
pr["W2  BT logit additive", FullSimplify[logit[bt[ti, tk]] - logit[bt[ti, tj]] - logit[bt[tj, tk]] == 0,
   Element[{ti, tj, tk}, Reals]]];
(* W2c: control. Probit-scale (Thurstone Case V) probabilities are NOT logit-additive. *)
th[a_, b_] := CDF[NormalDistribution[0, 1], a - b];
pr["W2c Thurstone logit additive at (1,0,-1) (must be False)",
   N[logit[th[1, -1]] - logit[th[1, 0]] - logit[th[0, -1]], 20] == 0];
pr["W2c' size of the defect", N[logit[th[1, -1]] - logit[th[1, 0]] - logit[th[0, -1]], 20]];

(* W3: product rule (Luce): P_ij P_jk P_ki == P_ji P_kj P_ik under BT. *)
pij = pi/(pi + pj); pjk = pj/(pj + pk); pki = pk/(pk + pi);
pr["W3  BT product rule", FullSimplify[pij pjk pki == (1 - pij) (1 - pjk) (1 - pki), pi > 0 && pj > 0 && pk > 0]];
(* W3c: control through the SAME FullSimplify path: replace one pair by a non-BT share (strengths squared
   for pair k,i only). The product-rule identity must then fail (not return True). Replaces the earlier
   W3c (0.8^3 == 0.2^3), which never touched the computation and was NON-DISCRIMINATING (verify, 2026-11-16). *)
pkiBad = pk^2/(pk^2 + pi^2);
pr["W3c product rule with one non-BT pair (must NOT be True)",
   FullSimplify[pij pjk pkiBad == (1 - pij) (1 - pjk) (1 - pkiBad), pi > 0 && pj > 0 && pk > 0]];
pr["W3c' witness pi=2,pj=1,pk=1", (pij pjk pkiBad - (1 - pij) (1 - pjk) (1 - pkiBad)) /. {pi -> 2, pj -> 1, pk -> 1}];

(* W4: misclassification attenuation. Observed share q = e + (1-2e) s, s = logistic(x).
   With t = s - 1/2 and a = 1-2e, g'(x) is proportional to h(t) = (1/4 - t^2)/(1/4 - a^2 t^2).
   Claim: dh/dt <= 0 on 0 <= t < 1/2 for 0 < a < 1 (so g is concave on x >= 0, g(0) = 0, hence subadditive). *)
h = (1/4 - t^2)/(1/4 - a^2 t^2);
dh = Together[D[h, t]];
pr["W4  dh/dt closed form", dh];
pr["W4  dh/dt <= 0 for 0<=t<1/2, 0<a<1",
   Resolve[ForAll[{t, a}, 0 <= t < 1/2 && 0 < a < 1, dh <= 0], Reals]];
(* W4c: control: the opposite claim (dh/dt >= 0 everywhere, i.e. superadditivity) must be refuted. *)
pr["W4c dh/dt >= 0 everywhere (must be False)",
   Resolve[ForAll[{t, a}, 0 <= t < 1/2 && 0 < a < 1, dh >= 0], Reals]];
(* W4d: direct subadditivity witness at e = 0.05, x = y = ln 4 (shares 0.8). *)
g[x_, e_] := logit[e + (1 - 2 e) LogisticSigmoid[x]];
pr["W4d g(2 ln4) - 2 g(ln4) at e=0.05 (negative = subadditive)", N[g[2 Log[4], 1/20] - 2 g[Log[4], 1/20], 20]];
pr["W4e same at e=0 (must be 0: no error, exact additivity)", FullSimplify[g[2 Log[4], 0] - 2 g[Log[4], 0]]];

(* W5: parameter count for the rank-one convergence test.
   Saturated-across-criteria BT: C(D-1) free; rank-one: (D-1) + (C-1). Difference must equal (C-1)(D-2). *)
pr["W5  df identity", Simplify[c (d - 1) - ((d - 1) + (c - 1)) == (c - 1) (d - 2)]];
(* W5c control: the tempting wrong count (C-1)(D-1) is not an identity. *)
pr["W5c wrong df (must be False)", Simplify[c (d - 1) - ((d - 1) + (c - 1)) == (c - 1) (d - 1)]];
(* W6: additivity (BT within one criterion) vs saturated pairs: D(D-1)/2 - (D-1) == (D-1)(D-2)/2 *)
pr["W6  BT goodness-of-fit df", Simplify[d (d - 1)/2 - (d - 1) == (d - 1) (d - 2)/2]];
pr["W6  values D=3,6", {(3 - 1) (3 - 2)/2, (6 - 1) (6 - 2)/2}];
