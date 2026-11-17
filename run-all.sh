#!/bin/sh
# run-all.sh -- cold run of the p65 preprint v1 data and code bundle. Unzip into an empty folder and run `sh run-all.sh`.
# Every step prints its exit code; the run stops at the first failing registered analysis. Outputs land in
# out/ next to the recorded copies they are compared with. Needs Python 3.8 or later; numpy, scipy (1.6 or later), sympy
# and mpmath for the appendix checks (steps 10 to 12); scipy for step 13. PYTHON=/path/to/python3 overrides the interpreter.
set -u
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
T0=$(date +%s)
mkdir -p out
A=arm-a-model; B=arm-a3-model; C=arm-a3b-model
fail=0
step() { printf '\n== %s\n' "$1"; }
# byte comparison, except that numpy 2 prints a scalar as np.float64(x) where numpy 1 printed x, and an
# interpreter may print an OpenMP warning line on start-up; same_prefix allows notes appended by hand after the run
same() { "$PY" -I -c '
import re, sys
f = lambda p: re.sub(r"np\.float64\(([^()]*)\)", r"\1", "\n".join(l for l in open(p, encoding="utf-8").read().splitlines() if not l.startswith("OMP: Warning")))
a, b = f(sys.argv[1]), f(sys.argv[2])
print("   %s %s" % ("output equals the recorded copy" if a == b else "DIFFERS from the recorded copy", sys.argv[2]))
sys.exit(0 if a == b else 1)' "$1" "$2" || fail=1; }
same_prefix() { "$PY" -I -c '
import re, sys
f = lambda p: re.sub(r"np\.float64\(([^()]*)\)", r"\1", "\n".join(l for l in open(p, encoding="utf-8").read().splitlines() if not l.startswith("OMP: Warning")))
a, b = f(sys.argv[1]), f(sys.argv[2])
ok = b.startswith(a)
print("   %s %s" % ("output equals the recorded copy up to the notes appended after the run" if ok else "DIFFERS from the recorded copy", sys.argv[2]))
sys.exit(0 if ok else 1)' "$1" "$2" || fail=1; }
same_nodefs() { "$PY" -I -c '
import re, sys
f = lambda p: [re.sub(r" :: \".*$", "", l) for l in open(p, encoding="utf-8").read().splitlines()]
a, b = f(sys.argv[1]), f(sys.argv[2])
d = sum(x != y for x, y in zip(a, b)) + abs(len(a) - len(b))
print("   %s: %d differing lines against %s after dropping the quoted definitions" % ("output equals the recorded copy" if d == 0 else "DIFFERS", d, sys.argv[2]))
sys.exit(1 if d else 0)' "$1" "$2" || fail=1; }

same_rounded() { "$PY" -I -c '
import re, sys
# step 13: scipy prints the exact binomial p to a last digit that differs between scipy 1.6 and 1.17 (0.0010932449729686143
# against ...8613), so every float is compared after rounding to 10 significant digits; integers and words must match exactly
f = lambda p: re.sub(r"-?\d+\.\d+(?:e-?\d+)?", lambda m: "%.10g" % float(m.group(0)), "\n".join(l for l in open(p, encoding="utf-8").read().splitlines() if not l.startswith("OMP: Warning")))
a, b = f(sys.argv[1]), f(sys.argv[2])
print("   %s %s" % ("output equals the recorded copy to 10 significant digits" if a == b else "DIFFERS from the recorded copy", sys.argv[2]))
sys.exit(0 if a == b else 1)' "$1" "$2" || fail=1; }

step "1. number trace: every abstract and discussion number recomputed from the tables and compared with the printed value recorded in the trace"
cp p65_v1_number-trace.md out/number-trace_recorded.md
"$PY" -I scripts/p65_v1_number-trace.py > out/number-trace.log 2>&1; rc=$?; echo "   exit $rc (0 = every number matched)"; [ $rc -eq 0 ] || fail=1
tail -1 out/number-trace.log
"$PY" -I -c '
import re, sys
g = lambda p: re.search(r"<!-- trace:generated:begin -->(.*)<!-- trace:generated:end -->", open(p, encoding="utf-8").read(), re.S).group(1)
a, b = g("p65_v1_number-trace.md"), g("out/number-trace_recorded.md")
norm = lambda s: re.sub(r"\(\d{4}-\d{2}-\d{2}\)", "(date)", s)
print("   regenerated trace block %s the recorded one (dates aside)" % ("equals" if norm(a) == norm(b) else "DIFFERS FROM"))
sys.exit(0 if norm(a) == norm(b) else 1)' || fail=1

step "2. number trace, negative control (--perturb nudges three values; must exit 1 with mismatches)"
"$PY" -I scripts/p65_v1_number-trace.py --perturb > out/number-trace-perturb.log 2>&1; rc=$?; echo "   exit $rc (1 = control fired)"; [ $rc -eq 1 ] || fail=1
cp out/number-trace_recorded.md p65_v1_number-trace.md

step "3. corpus arm, first sample (registered analysis)"
"$PY" -I scripts/p65_navon_arm_a_analyze.py --map $A/p65_model-items_map.tsv --c1 $A/p65_model-codes_coder1.tsv --c2 $A/p65_model-codes_coder2.tsv --adj $A/p65_model-adjudication.tsv > out/arm-a_results.txt 2>&1; echo "   exit $?"
same out/arm-a_results.txt $A/p65_model-results_2026-11-13.txt

step "4. corpus arm, registered extension (the registered estimate 0.74)"
"$PY" -I scripts/p65_navon_arm_a3_analyze.py --armA-map $A/p65_model-items_map.tsv --armA-c1 $A/p65_model-codes_coder1.tsv --armA-c2 $A/p65_model-codes_coder2.tsv --armA-adj $A/p65_model-adjudication.tsv --armA-cells $B/p65_a3-armA-cells.tsv --cells $B/p65_a3-cells.tsv --map $B/p65_a3-items_map.tsv --c1 $B/p65_a3-codes_coder1.tsv --c2 $B/p65_a3-codes_coder2.tsv --adj $B/p65_a3-adjudication.tsv > out/arm-a3_results.txt 2>&1; echo "   exit $?"
same out/arm-a3_results.txt $B/p65_a3-results_2026-11-13.txt

step "5. corpus arm, exploratory extension (0.82)"
"$PY" -I $C/p65_navon_arm_a3b_analyze.py --armA-map $A/p65_model-items_map.tsv --armA-c1 $A/p65_model-codes_coder1.tsv --armA-c2 $A/p65_model-codes_coder2.tsv --armA-adj $A/p65_model-adjudication.tsv --armA-cells $B/p65_a3-armA-cells.tsv --a3-cells $B/p65_a3-cells.tsv --a3-map $B/p65_a3-items_map.tsv --a3-c1 $B/p65_a3-codes_coder1.tsv --a3-c2 $B/p65_a3-codes_coder2.tsv --a3-adj $B/p65_a3-adjudication.tsv --map $C/p65_a3b-items_map.tsv --c1 $C/p65_a3b-codes_coder1.tsv --c2 $C/p65_a3b-codes_coder2.tsv --adj $C/p65_a3b-adjudication.tsv > out/arm-a3b_results.txt 2>&1; echo "   exit $?"
same out/arm-a3b_results.txt $C/p65_a3b-results_2026-11-13.txt

step "6. dictionary arm (registered analysis and its transpose control; definitions are not redistributed, so the item key is read with a blank definition column)"
"$PY" -I -c '
rows = [r for r in open("change-verbs/items_key_nodefs.tsv", encoding="utf-8").read().split("\n") if r]
open("out/items_key_blankdefs.tsv", "w", encoding="utf-8").write("\n".join(r + "\t" + ("definition" if i == 0 else "") for i, r in enumerate(rows)) + "\n")'
"$PY" -I scripts/p65_change_verbs_analyze.py change-verbs/codes out/items_key_blankdefs.tsv > out/change-verbs_analysis-run.txt 2>&1; echo "   exit $?"
same_nodefs out/change-verbs_analysis-run.txt change-verbs/p65_analysis-run_2026-11-14.txt
"$PY" -I scripts/p65_change_verbs_analyze.py change-verbs/codes out/items_key_blankdefs.tsv --control-transpose > out/change-verbs_transpose-control.txt 2>&1; echo "   transpose control exit $?"
same_nodefs out/change-verbs_transpose-control.txt change-verbs/p65_analysis-transpose-control_2026-11-14.txt

step "7. dictionary arm, independent recount (own code) and its planted-error control"
"$PY" -I verify/p65v_recount.py change-verbs/codes change-verbs/items_key_nodefs.tsv > out/change-verbs_recount.txt 2>&1; echo "   exit $?"
same out/change-verbs_recount.txt verify/p65v_recount-run_2026-11-14.txt
"$PY" -I verify/p65v_recount.py change-verbs/codes change-verbs/items_key_nodefs.tsv --plant-wrong > out/change-verbs_recount-control.txt 2>&1; echo "   control exit $?"
same out/change-verbs_recount-control.txt verify/p65v_recount-control_2026-11-14.txt

step "8. interference arm: registered tally (primary and two-tailed coding columns) and the random-effects summary"
"$PY" -I scripts/p65_published_asymmetry_tally.py published-asymmetry/p65_published-asymmetry-coded_2026-11-13.tsv code > out/arm-c_tally_primary.txt 2>&1; echo "   exit $?"
same out/arm-c_tally_primary.txt published-asymmetry/p65_tally_primary.txt
"$PY" -I scripts/p65_published_asymmetry_tally.py published-asymmetry/p65_published-asymmetry-coded_2026-11-13.tsv code_2tailed > out/arm-c_tally_2tailed.txt 2>&1; echo "   exit $?"
same out/arm-c_tally_2tailed.txt published-asymmetry/p65_tally_2tailed.txt
"$PY" -I scripts/p65_published_asymmetry_meta.py > out/arm-c_meta.txt 2>&1; echo "   exit $?"
same out/arm-c_meta.txt published-asymmetry/p65_meta_random-effects.txt

step "9. error-evidence arm: per-source recount with its two planted controls"
"$PY" -I scripts/p65_armD_recount.py --control > out/arm-d_recount.txt 2>&1; echo "   exit $?"
same out/arm-d_recount.txt error-evidence/p65_armD_recount-run_2026-11-17.txt

step "10. appendix mathematics: attack-stage numerical checks (fixed seeds)"
"$PY" -I scripts/p65_wave1_attack_checks.py > out/wave1_attack-checks.txt 2>&1; echo "   exit $?"
same out/wave1_attack-checks.txt wave1-math/p65_wave1_attack-checks_2026-11-16.txt

step "11. appendix mathematics: power table (about two minutes; rewrites wave1-math/p65_wave1_power-*)"
cp wave1-math/p65_wave1_power-results_2026-11-16.txt out/wave1_power-results_recorded.txt
"$PY" -I scripts/p65_wave1_power.py > out/wave1_power.log 2>&1; echo "   exit $?"
same wave1-math/p65_wave1_power-results_2026-11-16.txt out/wave1_power-results_recorded.txt

step "12. appendix mathematics: independent verify pass (own routes; rewrites wave1-math/p65_wave1_verify-run_*) and the Ford-condition detector"
cp wave1-math/p65_wave1_verify-run_2026-11-16.txt out/wave1_verify-run_recorded.txt
"$PY" -I scripts/p65_wave1_verify.py > out/wave1_verify.log 2>&1; echo "   exit $?"
same_prefix wave1-math/p65_wave1_verify-run_2026-11-16.txt out/wave1_verify-run_recorded.txt
"$PY" -I scripts/p65_wave1_verify_ford.py > out/wave1_verify-ford.txt 2>&1; echo "   exit $?"
same out/wave1_verify-ford.txt wave1-math/p65_wave1_verify-ford_2026-11-16.txt

step "13. Indonesian census: analysis self-test on synthetic codes (bars read off the registration text), then the registered analysis from the deposited codes"
"$PY" -I scripts/p65_wave3_analyze.py --selftest > out/wave3_selftest.txt 2>&1; echo "   selftest exit $?"
"$PY" -I scripts/p65_wave3_analyze.py --real > out/wave3_analysis-run.txt 2>&1; echo "   exit $?"
same_rounded out/wave3_analysis-run.txt wave3/p65_wave3_analysis-run_2026-11-17.txt

T1=$(date +%s)
printf '\n== cold run finished in %d s; ' $((T1 - T0))
if [ $fail -eq 0 ]; then echo "every step exited as expected and every output equals its recorded copy"; else echo "AT LEAST ONE STEP FAILED (see above)"; fi
exit $fail
