# p65 wave 3 Indonesian pilot P01: S1 disagreement read (2026-11-17, Eastern)

Registration `p65_wave3_registration_FROZEN_2026-11-16.md` Section 9 S1: after an S1 stop the per-language notes
(Section 4.1, here `wave3/main/p65_codebook-v2-TP-x_id.md` "Indonesian notes") may be revised once, using
**disagreement content only, never direction counts**. This file is that read. It names constructions and causes.
It carries no tally by direction and no final label; the adjudication file is not quoted.

## What was read

`wave3/main/codes/P01_adjudication-sheet.tsv` (the 12 items of 495 where the two coders differed, with the previous
sentence and the two codes, coder order shuffled by the checker) and `P01_adjudication.tsv` (the adjudicator's rule
citations, read to see which rule each split turned on). `run.log` gives the gate numbers: P-kappa 0.937, D-kappa 0.215
on 50 both-present items, raw presence agreement 0.988.

Six of the twelve splits are on presence (one coder NA, the other a pair label) and six on the pair label among
items both coders found present. On the 50 both-present items 44 agree. The D-kappa is low at that raw agreement
because the pair labels are concentrated in few classes, so chance agreement is high and every split costs a lot of
kappa. All six pair-label splits are PAR against a directional label; none is a flip between the two directions.
So the failure is the boundary between 1.3 step 2 (two settings, PAR) and step 3 (one asserted value, one restrictor),
and the Indonesian notes say nothing about how that boundary shows in Indonesian grammar. Below, by construction.

## Pair-label splits (step 2 versus step 3)

| cause | construction | items | codebook gap or coder error |
|---|---|---|---|
| C1. Locative or existential predicate with a bare time adverb | `kini` / `saat ini` with `dapat ditemukan di X`, and the fronted existential `di X terdapat Y`. One coder read the time adverb and the place as two settings; the other read the place as the sentence's asserted value, as the anchor "... sudah ada di rumah" asserts one. | 2 (P0471, P0148) | gap: the notes never say that `ada / terdapat / berada / terletak / ditemukan + di` is a predicate that asserts a place, nor that the existential `di X terdapat Y` is one |
| C2. Fronted time span or fronted place with the other dimension inside the predicate | `Di antara tahun A dan B, ... di luar studio ...`; `Di Bogor biasanya dijual setelah direbus ...`. The fronted phrase reads as a frame (R3 instance-picking) to one coder and as a parallel setting to the other. Two Indonesian traits sharpen it: `di` marks the time span as well as the place, and `setelah + passive verb` is a time clause that looks like a step of the process. | 2 (P0293, P0124) | gap: no note on fronting (Indonesian fronts freely; position decides nothing) and none on `di antara ... dan` with years or `setelah/sebelum + verb` as time clauses. Partly the general step 2/3 boundary, which English coders also meet |
| C3. Modifiers inside a named referent, `yang` relative clause | `acara televisi pertama X untuk wilayah Tokyo, X yang mulai ditayangkan 11 Oktober 2011`: date inside a `yang` clause on a show's name; `untuk wilayah` a coverage area. One coder applied R2 (identifies the referent); the other read the clause's date as asserted. | 1 (P0254) | gap: R2 has no Indonesian form (`yang` clause on a name; bare date inside it) |
| C4. Duration as the predicate's value, place picking the instance | `masa pendidikan di SMAN 2 Kota Ternate ditempuh dalam waktu tiga tahun`: `dalam waktu + duration` is the asserted length; `di + school name` and `di Indonesia` locate which schools. One coder took the duration as a setting. | 1 (P0172) | gap: `dalam waktu`, `selama` + duration not in the notes (only `selama` as an opener); `di + institution name` as a location not addressed (the table's "institutions as positions" pulls the other way) |

Three of the six (P0471, P0172, P0148) are treebank units holding two sentences in the `sentence` column. Coders may
pair an expression in one sentence with one in the other; PR2 says the whole target is inventoried, but the notes do
not say the two-sentence unit is one target. One line fixes that.

## Presence splits (NA against a pair label)

| cause | construction | items | gap or error |
|---|---|---|---|
| P1. `dari` or `sejak` + time noun | `Dari tahun tersebut` (from that year). The notes cover `dari` with a place only. Same item: `di Hollywood` as place or industry (PR12, already in the rules). | 1 (P0333) | gap (`dari` + time); PR12 part is coder judgement |
| P2. Bare day name or date, no preposition | `..., Rabu, mengatakan` (newswire parenthetical weekday); same item `di Bursa Efek Jakarta` inside `dalam keterbukaan informasi` (an institution within a filing event: PR5 and the table). | 1 (P0109) | gap (bare time nouns; `di` + institution inside an event phrase) |
| P3. `bila` conditional against temporal | `Suatu kehormatan bila generasi muda ...`: "if" or "when"; `tanah air` a recipient (PR3). | 1 (P0233) | gap (`bila / jika / kalau / apabila` not in the subordinator list) |
| P4. Preposition inside a title | `Cintaku di Rumah Susun` (film title) with `terkenal di Indonesia pada tahun 1987`. One coder found no place; the title's `di` and the country of fame both in play. | 1 (P0469) | gap (a `di` / `pada` inside a proper name or title is part of the name) |
| P5. Place inside a definition | `putaran bumi disekeliling matahari` (the earth's path round the sun) inside a definition of the second, with `Pada tahun 1956` and `pada saat itu`. One coder read the orbit as not a literal location. | 1 (P0419) | gap (`di sekeliling / di sekitar / sepanjang` + physical noun is place, in a definition as elsewhere); PR12 judgement |
| P6. `di` + time noun and a locating phrase inside a noun phrase | `di dekade terakhir` (di + time noun, already in the notes) and `sepertiga di daerah perkotaan` (PR3's "locating phrase inside a noun phrase", already in PR3). | 1 (P0149) | coder error against existing text; one Indonesian example of PR3's noun-phrase case would help |

## What the revision may say (construction rules, no direction)

1. Predicate type: `ada / terdapat / berada / terletak / ditemukan + di` and the fronted existential assert a place
   (1.3 "asserts a value"); a phrase that only frames an action verb is a setting (anchor PAR), unless the sentence
   asserts that phrase (contrast or focus). Fronting decides nothing.
2. R2 in Indonesian: a time or place phrase inside a proper or definite noun phrase, including a `yang` clause on a
   name, identifies the referent.
3. Time: `dari, sejak, mulai, sampai, hingga, antara/di antara ... dan, dalam (waktu), selama` + time noun or
   duration; bare day names, dates, years, clock times; `setelah / sebelum / sesudah / ketika / saat + verb` as time
   clauses; `bila / jika / kalau / apabila` conditional unless settled.
4. Place: `di sekeliling / di sekitar / sepanjang / di atas / di dalam` + physical noun; `di` + institution name as a
   location when something is or happens there, not when the institution acts or frames a filing or decision; a
   preposition inside a title or proper name is part of the name.
5. The `sentence` column is one target even when it holds two sentences.

Examples in the revised notes come from the three anchors and constructed phrases, never from pilot items.
