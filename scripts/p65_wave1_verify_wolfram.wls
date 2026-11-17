(* p65 wave 1 VERIFY, independent symbolic checks (not a copy of p65_wave1_wolfram_checks.wls).
   Run: scripts/wolfram-run.sh --timeout 120 -- -file scripts/p65_wave1_verify_wolfram.wls *)
pr[tag_, v_] := Print[tag, " -> ", v];
(* V-W1: coder-flip map in logit coordinates, second derivative sign, by direct differentiation in x *)
gx[x_, e_] := Log[(e + (1 - 2 e) LogisticSigmoid[x])/(1 - e - (1 - 2 e) LogisticSigmoid[x])];
d2 = FullSimplify[D[gx[x, e], {x, 2}], 0 < e < 1/2 && x >= 0];
pr["V-W1 g''(x) <= 0 for x>=0, 0<e<1/2", Resolve[ForAll[{x, e}, x >= 0 && 0 < e < 1/2, d2 <= 0], Reals]];
pr["V-W1c g''(x) <= 0 for ALL real x (must be False: convex for x<0)", Resolve[ForAll[{x, e}, 0 < e < 1/2, d2 <= 0], Reals]];
pr["V-W1d shortfall e=1/20 shares .8", N[gx[2 Log[4], 1/20] - 2 gx[Log[4], 1/20], 15]];
(* V-W2: Rao-Kupper conditional odds ratio to BT odds *)
rk = (pi/(pi + th pj))/(pj/(pj + th pi));
pr["V-W2 RK conditional odds / (pi/pj)", Factor[Simplify[rk/(pi/pj)]]];
pr["V-W2c at th=1 (must be 1)", Simplify[(rk/(pi/pj)) /. th -> 1]];
(* V-W3: Thurstone defect at unit gaps *)
pr["V-W3 Thurstone defect", N[Log[CDF[NormalDistribution[], 2]/(1 - CDF[NormalDistribution[], 2])] - 2 Log[CDF[NormalDistribution[], 1]/(1 - CDF[NormalDistribution[], 1])], 15]];
(* V-W4: Ford sufficiency sketch: loglik -> -Infinity along a nonconstant direction when the max set has a loss *)
ll[t_] := Log[LogisticSigmoid[t]];
pr["V-W4 Limit log sigma(-t) as t->Infinity (must be -Infinity)", Limit[Log[LogisticSigmoid[-t]], t -> Infinity]];
