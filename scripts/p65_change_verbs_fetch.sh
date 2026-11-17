#!/bin/sh
# Fetch the three openly licensed dictionaries for the criterion-(b) test and print sha256.
# Usage: sh p65_change_verbs_fetch.sh <new empty dir>. Files are NOT committed (licence/size).
set -e
D="$1"; mkdir -p "$D/wn" "$D/gcide" "$D/wikt"
curl -sSL -o "$D/wn/wn3.1.dict.tar.gz" https://wordnetcode.princeton.edu/wn3.1.dict.tar.gz
curl -sSL -o "$D/gcide/gcide-0.53.tar.xz" https://ftp.gnu.org/gnu/gcide/gcide-0.53.tar.xz
curl -sSL -o "$D/wikt/kaikki-English-verb.jsonl" https://kaikki.org/dictionary/English/pos-verb/kaikki.org-dictionary-English-by-pos-verb.jsonl
date -u +%Y-%m-%dT%H:%MZ
shasum -a 256 "$D/wn/wn3.1.dict.tar.gz" "$D/gcide/gcide-0.53.tar.xz" "$D/wikt/kaikki-English-verb.jsonl"
