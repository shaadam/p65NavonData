"""P65 unit 3: copy items, build blind file (243 items + 6 plants, shuffled seed 20261119) and id map."""
import csv, random, shutil, hashlib
SRC = "/Users/as/_Claude/Claude/worktrees/p65-definitional-dependence-2026-11-18/definitional/p65_defdep_items.tsv"
D = "/Users/as/_Claude/Claude/worktrees/p65-stats-fix/dependence/"
assert hashlib.sha256(open(SRC, "rb").read()).hexdigest() == "d9f2dbcda9b66ec19a129f1d1c2f33348000209baa8f7712a3d18b8271234681"
shutil.copyfile(SRC, D + "p65_dep_items.tsv")
items = list(csv.DictReader(open(D + "p65_dep_items.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE))
assert len(items) == 243
plants = [
 ("PL1", "PLACE-STATED", "We looked everywhere for him.", "At nine he was still at his aunt's house.", "S"),
 ("PL2", "PLACE-STATED", "The road climbs steeply.", "Even in midwinter the old fort sits on the ridge above the town.", "N"),
 ("PL3", "PLACE-STATED", "Kotanya kecil.", "Sampai sekarang pun danau itu terletak di sebelah utara kota.", "N"),
 ("PL4", "TIME-STATED", "The call came from abroad.", "In Sydney it was already Saturday morning.", "S"),
 ("PL5", "TIME-STATED", "Kami menelepon keluarga di rumah.", "Di Jayapura waktu itu sudah pukul sembilan malam.", "S"),
 ("PL6", "TIME-STATED", "The conference had three days of talks.", "In the main hall the keynote was on the Tuesday.", "N"),
]
with open(D + "p65_dep_plants.tsv", "w") as f:
    f.write("pid\tframe\tprevious_sentence\tsentence\texpected\n")
    for p in plants: f.write("\t".join(p) + "\n")
rows = [(it["item"], "PLACE-STATED" if it["final"] == "TP" else "TIME-STATED",
         it["previous_sentence"], it["sentence"]) for it in items]
rows += [(p[0], p[1], p[2], p[3]) for p in plants]
random.Random(20261119).shuffle(rows)
clean = lambda s: s.replace("\t", " ").replace("\n", " ")
with open(D + "p65_dep_blind.tsv", "w") as b, open(D + "p65_dep_blind_map.tsv", "w") as m:
    b.write("did\tframe\tprevious_sentence\tsentence\n"); m.write("did\titem\n")
    for i, r in enumerate(rows, 1):
        did = f"D{i:04d}"
        b.write(f"{did}\t{r[1]}\t{clean(r[2])}\t{clean(r[3])}\n"); m.write(f"{did}\t{r[0]}\n")
print(len(rows), "rows written")
