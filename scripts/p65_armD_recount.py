#!/usr/bin/env python3
"""p65 Arm D recount: count the error-evidence sources from the per-source list.

Reads error-evidence/p65_armD_per-source_2026-11-17.tsv (one row per published source named in
p65_error-evidence-map_2026-11-13.md) and prints:
  (i)  N = number of distinct sources (duplicate source_key is an error, not a count);
  (ii) per-code counts under the map's own rule: one primary code per source, a source may carry a
       second code (double_coded = Y), in which case it is counted once in N and once per code;
  (iii) the same counts with the primary code only (no double counting);
  (iv) the headline check: number of sources coded T>S.
Negative controls (run with --control): a planted duplicate row must raise DUPLICATE, and a planted
T>S row must move the T>S count off zero. If either control fails to fire the counter is
non-discriminating and the run exits 2.
"""
import csv
import io
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, "error-evidence", "p65_armD_per-source_2026-11-17.tsv")
CODES = ["S>T", "DISSOC", "MIXED", "T>S", "NONE", "unknown"]


def load(text):
    rows = list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    return rows


def count(rows):
    keys = [r["source_key"] for r in rows]
    dups = [k for k, c in Counter(keys).items() if c > 1]
    if dups:
        raise ValueError("DUPLICATE source_key: " + ", ".join(dups))
    bad = [r["source_key"] for r in rows if r["direction_code"] not in CODES]
    if bad:
        raise ValueError("unknown direction code on: " + ", ".join(bad))
    n = len(rows)
    primary = Counter(r["direction_code"] for r in rows)
    with_double = Counter(primary)
    n_double = 0
    for r in rows:
        if r["double_coded"].strip().upper() == "Y":
            sec = r["secondary_code"].strip()
            if sec not in CODES:
                raise ValueError("double-coded row without a valid secondary code: " + r["source_key"])
            with_double[sec] += 1
            n_double += 1
    return n, primary, with_double, n_double


def report(label, rows):
    n, primary, wd, nd = count(rows)
    print("%s: N = %d distinct sources" % (label, n))
    print("  primary code only : " + " · ".join("%s %d" % (c, primary.get(c, 0)) for c in CODES)
          + "  (sum %d)" % sum(primary.values()))
    print("  with double codes : " + " · ".join("%s %d" % (c, wd.get(c, 0)) for c in CODES)
          + "  (sum %d = N %d + %d double-coded)" % (sum(wd.values()), n, nd))
    print("  headline: sources coded T>S = %d" % primary.get("T>S", 0))
    return n, primary, wd


def main():
    text = open(TSV, encoding="utf-8").read()
    rows = load(text)
    n, primary, wd = report("RECOUNT", rows)
    if "--control" in sys.argv:
        ok = True
        # Control 1: planted duplicate (Kemmerer 2005 twice) must raise.
        planted = rows + [dict(rows[0])]
        try:
            count(planted)
            print("CONTROL 1 (planted duplicate): DID NOT FIRE -> counter non-discriminating")
            ok = False
        except ValueError as e:
            print("CONTROL 1 (planted duplicate): FIRED -> %s" % e)
        # Control 2: planted T>S source must move the headline count.
        fake = dict(rows[0]); fake["source_key"] = "PLANTED T>S"; fake["direction_code"] = "T>S"
        fake["double_coded"] = "N"; fake["secondary_code"] = ""
        n2, p2, _, _ = count(rows + [fake])
        if p2.get("T>S", 0) == primary.get("T>S", 0) + 1 and n2 == n + 1:
            print("CONTROL 2 (planted T>S row): FIRED -> T>S %d -> %d, N %d -> %d"
                  % (primary.get("T>S", 0), p2["T>S"], n, n2))
        else:
            print("CONTROL 2 (planted T>S row): DID NOT FIRE"); ok = False
        if not ok:
            sys.exit(2)
    # Comparison with the map's stated counts.
    stated = {"S>T": 12, "DISSOC": 7, "MIXED": 9, "T>S": 0, "NONE": 15, "unknown": 2}
    print("MAP STATES: 42 sources; " + " · ".join("%s %d" % (c, stated[c]) for c in CODES)
          + "  (sum %d; 43 net of the 2 double-coded)" % sum(stated.values()))
    print("DIFFERENCE (map minus recount, with double codes): "
          + " · ".join("%s %+d" % (c, stated[c] - wd.get(c, 0)) for c in CODES))


if __name__ == "__main__":
    main()
