#!/usr/bin/env python3
"""p65_wave3_ud_fetch.py -- fetch the wave 3 Universal Dependencies treebanks at a pinned release tag and
checksum them.

Source: the official UD release tag (default r2.18, the release Arm A's English codes were made on) of each
treebank repository under github.com/UniversalDependencies, downloaded as the tag's tarball from
codeload.github.com. Only *.conllu, README* and LICENSE* members are extracted (tarfile 'data' filter).

The treebank text is NOT committed (several licences are NC or ShareAlike, and the repo should hold codes and
sentence IDs only). It lands in data/ud/<tag>/<repo>/, which .gitignore excludes. This script and the checksum
file wave3/p65_wave3_ud-checksums_<tag>.tsv are committed instead.

Checksums are taken on the extracted files, not the tarball: GitHub does not guarantee byte-stable archives.

Usage:
  python3 -I scripts/p65_wave3_ud_fetch.py --root <repo>            # fetch, write checksum file
  python3 -I scripts/p65_wave3_ud_fetch.py --root <repo> --check    # re-hash local files against the committed file
  (needs network access to codeload.github.com)
"""
import argparse, hashlib, io, os, re, sys, tarfile, urllib.request

REPOS = [  # wave 3 recommended eight (+ Kenet as Turkish fallback), reserves, English validation
    "UD_Hindi-HDTB", "UD_Finnish-TDT", "UD_Chinese-GSD", "UD_Chinese-HK", "UD_Japanese-GSD",
    "UD_Turkish-BOUN", "UD_Turkish-Kenet", "UD_Arabic-PADT", "UD_Indonesian-GSD", "UD_Indonesian-CSUI",
    "UD_Naija-NSC", "UD_Korean-Kaist", "UD_Persian-PerDT", "UD_English-EWT", "UD_English-GUM",
]
KEEP = re.compile(r"^[^/]+/([^/]+\.conllu|README[^/]*|LICENSE[^/]*)$")  # top-level files only


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def licence(readme):
    m = re.search(r"^License:\s*(.*)$", readme, re.M)
    return m.group(1).strip() if m else "NOT STATED IN README"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--tag", default="r2.18")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    data = os.path.join(a.root, "data", "ud", a.tag)
    ck = os.path.join(a.root, "wave3", "p65_wave3_ud-checksums_%s.tsv" % a.tag)
    if a.check:
        bad = n = 0
        for line in open(ck, encoding="utf-8"):
            if line.startswith("repo\t"):
                continue
            repo, fn, size, digest, lic = line.rstrip("\n").split("\t")
            p = os.path.join(data, repo, fn)
            n += 1
            if not os.path.exists(p) or sha(p) != digest:
                bad += 1
                print("MISMATCH", repo, fn)
        print("checked %d files, %d mismatches" % (n, bad))
        sys.exit(1 if bad else 0)
    rows = []
    for repo in REPOS:
        url = "https://codeload.github.com/UniversalDependencies/%s/tar.gz/refs/tags/%s" % (repo, a.tag)
        raw = None
        for attempt in range(6):  # the proxy drops long chunked transfers; retry whole archive
            try:
                raw = urllib.request.urlopen(url, timeout=300).read()
                break
            except Exception as e:
                print(repo, "attempt", attempt + 1, "failed:", repr(e)[:80])
        if raw is None:
            sys.exit("could not fetch " + repo)
        out = os.path.join(data, repo)
        os.makedirs(out, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
            members = [m for m in tf.getmembers() if m.isfile() and KEEP.search(m.name)]
            for m in members:  # written by basename only: no path from the archive is trusted
                with open(os.path.join(out, os.path.basename(m.name)), "wb") as g:
                    g.write(tf.extractfile(m).read())
        readmes = [f for f in os.listdir(out) if f.startswith("README")]
        lic = licence(open(os.path.join(out, readmes[0]), encoding="utf-8", errors="replace").read()) if readmes else "NO README"
        for fn in sorted(os.listdir(out)):
            p = os.path.join(out, fn)
            rows.append((repo, fn, str(os.path.getsize(p)), sha(p), lic))
        print(repo, "archive sha256", hashlib.sha256(raw).hexdigest(), "files", len(members), "licence", lic)
    os.makedirs(os.path.dirname(ck), exist_ok=True)
    with open(ck, "w", encoding="utf-8") as f:
        f.write("repo\tfile\tbytes\tsha256\tlicence\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    print("wrote", ck, len(rows), "files")


if __name__ == "__main__":
    main()
