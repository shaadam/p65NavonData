# p65 wave 3 codebook v2-TP-x, Indonesian (first preprint)

Last updated: 2026-11-17 (Eastern; Indonesian notes revised once under S1, amendment 2). Registration: `p65_wave3_registration_FROZEN_2026-11-16.md` Section 4. Built from
codebook v3.1 (`wave2/p65_codebook-v3.1_sec1.md`, sha d0cacc9b...ecc): the time and place rows of its table, presence rules
PR1 to PR6 and PR12, and the directional rule of 1.3 with R1 to R3, copied word for word. PR7 to PR11 (quantity, manner,
size, colour) are not used. One pair only: time and place.

## Task and labels

For each target sentence (read with the sentence before it, PR1) decide whether time and place are BOTH literally present
(PR1 to PR6, PR12, table below). If not, the label is **NA**. If both are present give one label:
- **TP**: time over place (i = time, j = place in 1.3): a place-value is asserted and the time expression narrows when it holds.
- **PT**: place over time (i = place, j = time): a time-value is asserted and the place expression narrows where it holds.
- **PAR**: the two expressions each locate or describe the event, neither restricting the other (1.3 step 2).
- **AMB**: still torn after steps 1 to 4 of 1.3.

Where 1.3 below says `i>j` and `j>i` for the pair, read `time>place` as TP and `place>time` as PT.

### Table (v3.1 1.1, time and place rows)

| dimension | counts | does not count |
|---|---|---|
| time | when something holds or happens: dates, clock times, parts of the day, seasons, "now", "then", "currently", "when/while" clauses (A3b adjudicator rule, adopted). Durations ("for three hours", "it takes a week") are time. | frequency words ("always", "often", "never", "usually"): neither time nor quantity in v3 (A3b adjudicator rule, kept so the time-place series stays continuous) |
| place | where something is or happens: locations, positions, "here", "there" (deictic, literal), directions, distance between places | institutions used as positions ("in office") |

### Presence rules (v3.1 1.1.1; time and place only)

Work in two steps for this sentence: decide whether time is present, decide whether place is present, then label the pair.

**PR1. The target sentence only.** An expression counts only if its words are in the target sentence. The
previous sentence is read only to find what a word in the target sentence refers to ("there", "it", "then"). It
never supplies an expression of its own.
- Example (counts): P019, "so probably just sit in there, read some ultrasounds and get out early". "in there"
  is a place in the target sentence; the previous sentence ("today I got pulled to ultrasound") only says what
  "there" is.
- Counter-example: P155, "That Tuesday, I remember I had been getting a little bit more symptomatic." "That 40
  minutes" and "in the car" are in the previous sentence, so neither counts. Only time ("That Tuesday") is present,
  and the sentence gets no pair.

**PR2. Inventory over the whole sentence, then every pair.** An expression counts wherever it stands in the
sentence: in any clause, inside a noun phrase, in a quotation or a parenthesis. Two dimensions present anywhere
in the sentence form a pair even when they sit in different clauses. A dimension on the inventory is present for
every pair it forms, never for some of them only.
- Example: P200, "The magician behind the counter was wise enough not to sell it to me, but instead sold me two
  books which I still own today". The inventory is place ("behind the counter"), quantity ("two books") and time
  ("today"), so all three pairs are labelled, place-quantity included, though the two expressions are in
  different clauses.
- Counter-example: P115, "The USI art gallery celebrated the Thursday opening with its display of Warhol's
  Polaroids, gelatin silver prints and several colored screen prints." The inventory is time, colour and quantity.
  "The USI art gallery" fails PR3, so place is not on the inventory and forms no pair.

**PR3. Time and place must locate something.** A time or place expression counts when it says when or where a
state, event or thing is: an adverbial ("in the park", "yesterday"), a predicate ("is in the garage"), or a
locating phrase inside a noun phrase ("all events in the city", "a cat in Devon"). A time or place noun that is
itself the subject, object or possessor, the thing the sentence talks about, does not count.
- Example: P194, "its stalked eyes gleaming at you on either side of its metallic front". "on either side of its
  metallic front" says where the eyes are: place.
- Counter-example: P113, "France eventually did conquer Mexico". "Mexico" is what was conquered, not where
  anything happened: no place. Likewise a place as subject (P003 "the expanding outer east bay areas started out
  as...", P159 "the Bay Area has been fairly mixed") or an institution acting (P115 "The USI art gallery
  celebrated").

**PR4. Motion, people and "of" phrases.** The source, goal or path of literal movement counts as place, including
a direction particle on a motion verb ("move away", "ooze out", "go back", "come down"). Residence or origin
counts ("formerly of Algoa Bay", "a man from Ohio"), and so does "at X's" meaning X's premises ("over at
Jerry's"). These do not count: a person as the goal of custom or contact ("going to Nick" for haircuts, "talk to
Bart"); membership, title, rule or capture ("citizens of these United States", "Emperor of these U.S.", "the
taking of Mecca"); the thing an action affects ("damage is made to the bark").
- Example: P049, "I would be able to cancel the 12 month membership if I was to move away". "move away" is the
  direction of a literal move: place.
- Counter-example: P056, "I have been going to Nick for 5 months now". "to Nick" names a barber as the goal of
  custom, not a location: no place.

**PR5. Events used as settings.** A phrase that sets a sentence at an event ("in the interview", "at the
meeting") counts as time only if it carries a temporal word (during, before, after, while, since, until) or a
date or clock time, and as place only if it also names a location. Otherwise it counts as neither.
- Example: P098, "in a 2011 radio interview". The phrase carries a date: time.
- Counter-example: P052, "In the very interview in which they admitted 9/11, ...". No temporal word, no date in
  the phrase, no location: neither time nor place. ("9/11" here names the attacks, not the interview's date.)

**PR6. Ages and travel times.** An age that describes a person or thing is not time ("a sixteen-year-old
daughter", "a 20 something gay black male"). An age that says when an event happens or ends is time ("aged 31
when...", "lived to the age of 36"). A duration used as a distance is place, as the table already says of
distance ("a five-minute walk from", "two hours away").
- Example: P110, "a cat in Devon, England who reportedly live to the age of 36". The age marks when the life
  ended: time.
- Counter-example: P131, "My sixteen-year-old daughter pulls up her T-shirt sleeve". The age describes the
  daughter: not time. Also P201, "a five-minute walk from Tokyo's ill-famed red-light district": a distance, so
  place, not time.

**PR12. When in doubt, not present.** When a literal reading and a non-literal reading both fit, and neither the
sentence nor the previous one settles which, the expression is not present.
- Example: P083, "10% of the knowledge that some of the other EXPERIENCED vets do in this area". "in this area"
  can be the locality or the field of practice, and the context does not settle it: no place.
- Counter-example: P053, "the confidentiality agreement, which may be in Bart's files". Only the literal reading
  (where the document is kept) fits: place counts.

### 1.3 The directional rule, for every ordered pair

**i over j** when the sentence *asserts a value on dimension j* (a state, property, amount, manner, location or
time value), and an *expression on dimension i narrows the occasion, circumstance or instance for which that value
holds*. Test paraphrase: "[j-value] holds, given [i-value]" fits, and the reverse does not. This is protocol v2's
TP/PT rule, unchanged for time and place, written for any pair.

Decision steps, in order (v2's steps, generalised):
1. Both dimensions literal? If not, no label.
2. Do the two expressions each locate or describe an event or action, with neither restricting the truth of the
   other? **PAR.** ("We met in the park yesterday": time-place PAR. "She drove slowly through town": place-manner PAR.)
3. Is a j-value asserted, with the i-expression narrowing when, where, for which instance, or under what condition
   it holds? **i>j.**
4. The reverse? **j>i.**
5. Still torn: **AMB.**

Three rules for cases v2 left open:
- **R1, one asserted value with two restrictors.** Each restrictor is over the asserted dimension, and the two
  restrictors are PAR to each other. "At noon in Paris the sky is red": time>colour, place>colour, time-place PAR.
- **R2, modifiers inside a referring noun phrase.** A modifier inside a definite or proper noun phrase identifies a
  referent ("the red car is in the garage"). It does not restrict, so the pair gets PAR, not colour>place. A
  modifier on a generic or bare-plural subject restricts and counts ("Large ships dock at the outer pier":
  size>place). This rule is new. Its agreement is reported separately (Section 5.2), and if coders split on it
  the affected items are flagged.
- **R3, instance picking (A3 adjudicator rule, kept).** When a sentence asserts a j-value and the i-expression
  picks which instance or occasion, that is i>j ("In Spain dinner is at ten": place>time).

(In 1.3, R1 needs a third dimension and does not arise here; it is kept so the text is the v3.1 text.)

## Indonesian notes (translation of the rules, not new rules; written from the grammar and the registration's Section 4.1, before any wave 3 code; none mentions direction)

- **di** before a place noun (di rumah, di Jakarta, di atas, di dalam, di sebelah) marks place. **di** before a time
  noun (di tahun 2010, di pagi hari) is time. The head decides (registration 4.1). **di-** written attached to a verb
  (dibangun, diberikan) is the passive prefix, not a preposition: it marks neither time nor place.
- **pada** before a time noun (pada hari Senin, pada tahun 1998, pada pukul enam) is time. Before a person or an abstract
  noun (pada saya, pada kenyataannya) it is neither time nor place.
- **ke** (to) and **dari** (from) with a place are goal and source of movement and count as place (PR4); with a person they do not.
- **saat, ketika, sewaktu, waktu, selama, sebelum, setelah, sesudah, sejak, hingga** open time expressions; **sekarang,
  kini, kemarin, besok, tadi, nanti** are time. Frequency words (selalu, sering, jarang) are not time (table).
- **di sini, di situ, di sana** are deictic place and count when they locate something (PR3).
- A place name that is the subject, object or possessor does not count (PR3); one inside a locating phrase does
  ("harga di Jakarta", the price in Jakarta, locates the price inside the noun phrase: place).
- Reduplication (hari-hari, kota-kota) does not change the dimension.

Revised once under registration Section 9 S1 (2026-11-17, `wave3/p65_wave3_amendment-2_2026-11-17.md`), from the content
of the pilot's disagreements only. These say how a rule already above shows in Indonesian grammar; none mentions direction.
- **Other markers of time.** `dari`, `sejak`, `mulai`, `sampai`, `hingga`, `antara ... dan`, `di antara ... dan`, `dalam
  (waktu)`, `selama` before a time noun or a duration are time, as `di` and `pada` are: the head decides ("sejak pukul
  enam", "dalam waktu dua jam"). A day name, date, year or clock time standing with no preposition, including as a
  parenthetical ("..., Rabu, ..."), is time when it says when something holds or happens (PR3).
- **Time clauses.** `setelah`, `sebelum`, `sesudah`, `ketika`, `saat`, `sewaktu`, `sambil` before a verb or clause, including a
  passive verb ("setelah dimasak", after being cooked), open a time clause (table: "when/while" clauses). `bila`, `jika`,
  `kalau`, `apabila` are conditional ("if") unless the sentence settles a temporal reading; unsettled, PR12.
- **Other markers of place.** `di sekeliling`, `di sekitar`, `sepanjang`, `di atas`, `di dalam`, `di luar` before a
  physical thing or location are place, in a definition or description as anywhere else. `di` before the name of an
  institution (a school, a company, an exchange) is place when it says where something is or happens; when the
  institution acts, or frames a filing or decision ("dalam rapat di ..."), it is not (table: institutions as positions; PR5).
- **Names and titles.** A `di` or `pada` inside a proper name or a title (a film, a song, an organisation) is part of the
  name and marks neither time nor place.
- **Locative and existential predicates (1.3 "asserts a value").** `ada di`, `terdapat di`, `berada di`, `terletak di`,
  `ditemukan di`, and the fronted existential `di X ada / terdapat Y`, are predicates whose value is a place: the anchor
  "Pada pukul enam anak-anak sudah ada di rumah" asserts where the children are. A time or place phrase that only frames an
  action verb is a setting (1.3 step 2): "Kemarin kami bertemu di taman". A framing phrase becomes the asserted value only
  when the sentence asserts it (contrast or focus: `hanya`, `bukan ... melainkan`, `selain`). A duration on a verb ("ditempuh
  dalam waktu tiga tahun", takes three years) states how long and is a time value.
- **Fronting.** Indonesian puts a time or place phrase first freely ("Di Tokyo sudah tengah malam"; "Kemarin kami bertemu
  di taman"). Position decides nothing; decide by what the predicate asserts (1.3 steps 2 and 3).
- **R2 in Indonesian.** A time or place phrase inside a proper or definite noun phrase identifies its referent and does not
  restrict: a `yang` relative clause on a name or title ("film X yang dirilis pada tahun 1990"), an apposition, or a
  coverage phrase ("untuk wilayah Jawa"). The same phrase on a bare or generic noun counts.
- **The target.** The `sentence` column is one target even when the treebank unit holds two sentences; PR1 and PR2 apply to
  all of it, and the `previous_sentence` column is the previous sentence only.

## Anchors (English authoritative; translations in `wave3/p65_wave3_id_anchors_2026-11-16.md`)

- TP: "By six the children were home." / Pada pukul enam anak-anak sudah ada di rumah.
- PT: "In Tokyo it was already midnight." / Di Tokyo sudah tengah malam.
- PAR: "We met in the park yesterday." / Kemarin kami bertemu di taman.
