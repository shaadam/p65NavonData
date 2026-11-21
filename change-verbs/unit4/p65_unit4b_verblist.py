"""Unit 4b: the spatial-extent change-verb list, drawn from WordNet 3.1 by a fixed rule (registration addendum B in
docs/p65_unit4-spatial-change-verbs_registration_2026-11-19.md). No corpus sentence is read.

Rule: a WordNet 3.1 verb synset qualifies when (1) its lexicographer file is verb.change (30), verb.motion (38) or
verb.stative (42), and (2) its definition (the gloss before any quoted example) contains, as a whole word, one of the
spatial-extent words in EXTENT. A single-word lemma of a qualifying synset is listed when (3) that synset is one of the
lemma's two most frequent verb senses (the first two offsets in index.verb, WordNet's frequency order), so a common
verb does not enter through a rare sense; lowercased; minus the 76 lemmas unit 4 already coded. Also writes every WordNet 3.1 verb sense of every listed lemma (the dictionary side of the test).

Usage: python3 -I p65_unit4b_verblist.py <wn3.1 dict dir> <out dir>
"""
import os
import re
import sys

EXTENT = """wide wider widen widening width broad broader broaden breadth narrow narrower narrowing deep deeper deepen
depth shallow shallower thick thicker thickness steep steeper slope slopes sloping slant slanting incline inclined angle
taper tapering height tall taller elevation upward downward""".split()
UNIT4 = set("""alternate ameliorate amortize anneal temper normalize bioaccumulate break checker chisel co-vary
convalesce crash creep dawn daypart decrease depreciate develop drip-feed evanesce fade fleet pass explode filter
fine flit gather glean graduate grizzle grow interchange iterate knit lull marinate mature mellow migrate mushroom
overfish overprint phase plateau proliferate pulse refract reoxidize rust scaffold scrape scratch shade shawshank
shift shoot sink slug soil stale step superannuate time-change track turn uptalk vanish fly vaporize vary wear wipe
wizen melt""".split())
assert len(UNIT4) == 76


def synsets(path):
    for line in open(path, encoding="utf-8"):
        if line.startswith("  "):
            continue
        head, _, gloss = line.partition("| ")
        f = head.split()
        off, lex, n = f[0], int(f[1]), int(f[3], 16)
        lemmas = [re.sub(r"\(.*\)$", "", f[4 + 2 * i]).lower() for i in range(n)]
        definition = gloss.split('; "')[0].split(' "')[0].strip()
        yield off, lex, lemmas, definition, gloss.strip()


def main():
    wn, out = sys.argv[1], sys.argv[2]
    pat = re.compile(r"\b(" + "|".join(EXTENT) + r")\b", re.I)
    allsyn = list(synsets(os.path.join(wn, "data.verb")))
    hit = [s for s in allsyn if s[1] in (30, 38, 42) and pat.search(s[3])]
    top2 = {}
    for line in open(os.path.join(wn, "index.verb"), encoding="utf-8"):
        if line.startswith(" "):
            continue
        f = line.split()
        p = int(f[3])
        top2[f[0]] = f[4 + p + 2:][:2]
    lemmas = sorted({l for s in hit for l in s[2] if "_" not in l and "-" not in l and s[0] in top2.get(l, [])} - UNIT4)
    hit = [s for s in hit if any(l in lemmas and s[0] in top2.get(l, []) for l in s[2])]
    with open(os.path.join(out, "p65_unit4b_verblist.tsv"), "w", encoding="utf-8") as fh:
        fh.write("lemma\tqualifying_synsets\n")
        for l in lemmas:
            fh.write(l + "\t" + "; ".join(f"{s[0]} ({s[3]})" for s in hit if l in s[2]) + "\n")
    with open(os.path.join(out, "p65_unit4b_wn-senses.tsv"), "w", encoding="utf-8") as fh:
        fh.write("sense_id\tlemma\tsynset\tlexfile\tgloss\n")
        k = 0
        for l in lemmas:
            for s in allsyn:
                if l in s[2]:
                    k += 1
                    fh.write(f"WN{k:04d}\t{l}\t{s[0]}\t{s[1]}\t{s[4]}\n")
    print(f"qualifying synsets {len(hit)}; lemmas {len(lemmas)}; senses written {k}")
    print(" ".join(lemmas))
    ask = "widen narrow slope taper rise fall deepen thin thicken broaden".split()
    print("coordinator examples in list:", [a for a in ask if a in lemmas], "not in list:", [a for a in ask if a not in lemmas])


if __name__ == "__main__":
    main()
