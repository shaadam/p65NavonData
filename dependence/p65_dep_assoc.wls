(* P65 unit 3, dependence as a variable: route 2 (Wolfram), shares no code with p65_dep_assoc.py.
   Adapted from definitional/p65_defdep_assoc.wls: input file and column changed; Clopper-Pearson s0 added.
   Recount from item file; Fisher exact by exact enumeration of hypergeometric in rationals;
   exact conditional common OR across strata; Firth penalised logistic by direct maximisation
   of loglik + 1/2 log det I (FindMaximum), profile interval by FindRoot.
   Negative control: definitional labels shuffled within language (seed 6518, 500 draws)
   must remove the association. *)
dir = "/Users/as/_Claude/Claude/worktrees/p65-stats-fix/dependence/";
raw = Import[dir <> "p65_dep_final-numeric.tsv", "TSV"]; hdr = First[raw]; rows = Rest[raw];
ci = Position[hdr, "corpus"][[1, 1]]; fi = Position[hdr, "final"][[1, 1]]; di = Position[hdr, "dependent"][[1, 1]];
dat = {#[[ci]], ToExpression[ToString[#[[di]]]], Boole[#[[fi]] === "TP"]} & /@ rows;
Print["n = ", Length[dat]];
cell[d_, l_, g_, y_] := Count[d, {c_, g, y} /; (l === All || c === l)];
Do[Print["TABLE ", l, " def TP ", cell[dat, l, 1, 1], " PT ", cell[dat, l, 1, 0], " | nondef TP ", cell[dat, l, 0, 1], " PT ", cell[dat, l, 0, 0]], {l, {"en", "id", All}}];

(* hypergeometric weights for x = TP among def *)
weights[d_, l_] := Module[{n1 = cell[d, l, 1, 1] + cell[d, l, 1, 0], n0 = cell[d, l, 0, 1] + cell[d, l, 0, 0], m = cell[d, l, 1, 1] + cell[d, l, 0, 1]},
  Table[x -> Binomial[n1, x] Binomial[n0, m - x], {x, Max[0, m - n0], Min[n1, m]}]];
fisherP[w_, xo_] := Module[{tot = Total[w[[All, 2]]], po}, po = (xo /. w)/tot; Total[Select[w[[All, 2]]/tot, # <= po &]]];
Do[With[{w = weights[dat, l], xo = cell[dat, l, 1, 1]}, Print["FISHER ", l, " p = ", N[fisherP[w, xo], 8], " exact ", fisherP[w, xo]]], {l, {"en", "id", All}}];

conv[ws_] := Normal[Merge[Flatten[Outer[(#1[[1]] + #2[[1]]) -> #1[[2]] #2[[2]] &, ws[[1]], ws[[2]], 1]], Total]];
condOR[w_, so_] := Module[{s, mle, lo, hi, pd, g1, g2, g3},
  pd[psi_?NumericQ] := Module[{z = Total[#[[2]] psi^#[[1]] & /@ w]}, {Total[#[[1]] #[[2]] psi^#[[1]] & /@ w]/z,
     Total[If[#[[1]] >= so, #[[2]] psi^#[[1]], 0] & /@ w]/z, Total[If[#[[1]] <= so, #[[2]] psi^#[[1]], 0] & /@ w]/z}];
  g1[q_?NumericQ] := pd[Exp[q]][[1]]; g2[q_?NumericQ] := pd[Exp[q]][[2]]; g3[q_?NumericQ] := pd[Exp[q]][[3]];
  mle = Exp[lp /. FindRoot[g1[lp] == so, {lp, -2}, WorkingPrecision -> 30]];
  lo = Exp[lp /. FindRoot[g2[lp] == 1/40, {lp, -4}, WorkingPrecision -> 30]];
  hi = Exp[lp /. FindRoot[g3[lp] == 1/40, {lp, -1}, WorkingPrecision -> 30]];
  N[{mle, lo, hi}, 6]];
wS = conv[{weights[dat, "en"], weights[dat, "id"]}]; sObs = cell[dat, "en", 1, 1] + cell[dat, "id", 1, 1];
Print["EXACT CONDITIONAL common OR (MLE, lo, hi) ", condOR[wS, sObs], " p = ", N[fisherP[wS, sObs], 8]];
Print["en cond OR ", condOR[weights[dat, "en"], cell[dat, "en", 1, 1]]];

(* Firth by direct maximisation *)
xrow[{c_, g_, y_}, int_] := Join[{1, g, Boole[c === "id"]}, If[int, {g Boole[c === "id"]}, {}]];
pll[b_List, int_, d_] := Module[{X = xrow[#, int] & /@ d, yv = d[[All, 3]], eta, p},
  eta = X.b; p = LogisticSigmoid[eta];
  Total[yv eta - Log[1 + Exp[eta]]] + 1/2 Log[Det[Transpose[X].(X (p (1 - p)))]]];
firth[int_, d_] := Module[{k = If[int, 4, 3], bs, sol},
  bs = Array[bb, k]; sol = FindMaximum[pll[bs, int, d], Transpose[{bs, ConstantArray[0., k]}], AccuracyGoal -> 10, PrecisionGoal -> 10];
  {sol[[1]], bs /. sol[[2]]}];
profCI[int_, d_, j_, {llmax_, bhat_}] := Module[{k = Length[bhat], others, f},
  others = Delete[Array[cc, k], j];
  f[v_?NumericQ] := Module[{bs = Insert[others, v, j]}, First[FindMaximum[pll[bs, int, d], Transpose[{others, Delete[bhat, j]}]]]];
  Exp[{v /. FindRoot[f[v] == llmax - Quantile[ChiSquareDistribution[1], 0.95]/2, {v, bhat[[j]] - 1}],
       v /. FindRoot[f[v] == llmax - Quantile[ChiSquareDistribution[1], 0.95]/2, {v, bhat[[j]] + 1}]}]];
Do[Module[{fit = firth[int, dat]},
  Print["FIRTH ", If[int, "with", "without"], " interaction: loglik ", fit[[1]], " b ", fit[[2]], " OR ", Exp[fit[[2]]]];
  Do[Print["   coef ", j, " OR ", Exp[fit[[2, j]]], " profile 95% ", Quiet[profCI[int, dat, j, fit]]], {j, 2, If[int, 4, 3]}];
  If[! int, Print["   predicted TP non-def en ", LogisticSigmoid[fit[[2, 1]]], " id ", LogisticSigmoid[fit[[2, 1]] + fit[[2, 3]]],
     " | def en ", LogisticSigmoid[fit[[2, 1]] + fit[[2, 2]]], " id ", LogisticSigmoid[Total[fit[[2]]]]]]], {int, {False, True}}];

(* negative control *)
SeedRandom[6518];
shuf[] := Join @@ (Function[l, Module[{sub = Select[dat, #[[1]] === l &]}, Transpose[{sub[[All, 1]], RandomSample[sub[[All, 2]]], sub[[All, 3]]}]]] /@ {"en", "id"});
ctrl = Table[Module[{d = shuf[], w, s}, w = conv[{weights[d, "en"], weights[d, "id"]}]; s = cell[d, "en", 1, 1] + cell[d, "id", 1, 1];
   {s, N[fisherP[w, s]]}], {500}];
Print["CONTROL shuffled within language, 500 draws: share p<0.05 = ", N[Count[ctrl[[All, 2]], p_ /; p < 0.05]/500],
  "; share S <= ", sObs, " = ", N[Count[ctrl[[All, 1]], s_ /; s <= sObs]/500], "; median S = ", N[Median[ctrl[[All, 1]]]],
  " (null expectation of S ~ ", N[Total[(cell[dat, #, 1, 1] + cell[dat, #, 1, 0]) (cell[dat, #, 1, 1] + cell[dat, #, 0, 1])/Count[dat, {#, _, _}] & /@ {"en", "id"}]], ")"];
Print["CONTROL ", If[Count[ctrl[[All, 2]], p_ /; p < 0.05]/500 <= 0.10, "FIRED (association removed)", "DID NOT FIRE"]];

(* s0: TP share among non-dependent, exact Clopper-Pearson via Beta quantiles *)
cpI[k_, n_] := {N[k/n], If[k == 0, 0., Quantile[BetaDistribution[k, n - k + 1], 0.025]], If[k == n, 1., Quantile[BetaDistribution[k + 1, n - k], 0.975]]};
Do[Print["SHARE ", l, " non-dep TP ", cell[dat, l, 0, 1], "/", cell[dat, l, 0, 1] + cell[dat, l, 0, 0], " ", cpI[cell[dat, l, 0, 1], cell[dat, l, 0, 1] + cell[dat, l, 0, 0]],
  " | dep TP ", cell[dat, l, 1, 1], "/", cell[dat, l, 1, 1] + cell[dat, l, 1, 0], " ", cpI[cell[dat, l, 1, 1], cell[dat, l, 1, 1] + cell[dat, l, 1, 0]]], {l, {"en", "id", All}}];
