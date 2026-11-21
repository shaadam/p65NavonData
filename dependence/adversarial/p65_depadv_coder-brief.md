# Coding brief: which of two facts needs the other?

Each row describes one fact about the world in three short fields, given in random order, with no sentence:

- `entity`: the person, thing or event involved;
- two expressions, labelled `expr_1` and `expr_2`: one says when, the other says where (which is which is for you
  to see; the order means nothing).

Answer two questions, each by the **kind** of thing involved, not by whether the fact happens to be true only then
or there.

**Q-PLACE. Does where the entity is have no fixed value until a time is given?**
Yes when the entity is, by its kind, somewhere only for a time: a person, an animal, a vehicle, a movable object, a
crowd, an event, a visit or stay, weather. No when the entity is fixed by its kind or identity: a mountain, a lake,
a river, a city, a region, a building, a shop, an institution, a landmark, ruins, a fixed installation, a feature
of a script or a text. If the entity is a time of day, a date or a duration rather than a thing that has a place,
answer No.

**Q-TIME. Does the time value have no fixed value until a place is given?**
Yes when the time expression is local by the nature of time-keeping or of the sky: a clock reading, a calendar day
or date, a weekday, daylight or darkness, morning or evening, a season, the sun's position; or the time at which a
moving thing (a train, a bus, a ship) passes, leaves or reaches a stop, or takes to travel between places. No when
the time expression is a year, a decade, a century, a period of history, a duration ("for years", "since 2011"), an
age, a frequency, or a time relative to an event or to now ("after the war", "now", "still", "until then"), or
when it is set only by a custom, rule or schedule of a place (opening hours, school terms).

Write one code per row:

- `P`: Q-PLACE yes, Q-TIME no.
- `T`: Q-PLACE no, Q-TIME yes.
- `BOTH`: both yes.
- `NEITHER`: both no.

Examples:
- entity "the delivery van"; "for most of the morning"; "outside the bakery" -> P
- entity "the time of day"; "in Jakarta"; "already evening" -> T
- entity "the ferry"; "at the pier"; "at 6:15" -> BOTH
- entity "the volcano"; "for ten thousand years"; "in the north of the island" -> NEITHER

Indonesian rows are coded from the Indonesian. Decide from the three fields only.

**Output.** One row per item, tab-separated, header exactly:

    bid	code	confidence	note

- `code`: P, T, BOTH or NEITHER.
- `confidence`: 3 sure, 2 fairly sure, 1 unsure.
- `note`: at most a dozen words.

Code every row of the file you are given, in its order, and nothing else.
