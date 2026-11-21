# Coding brief: is one expression fixed by the other?

Each row gives two short expressions, `expr_1` and `expr_2`, in random order. One says **when**, the other says
**where** (which is which is for you to see; the order means nothing). There is no sentence. Some rows are in
Indonesian; code them from the Indonesian.

Your one question: **does meaning or convention fix one expression by the other?** "Fixed by" means you could work
out, or identify, the value of one expression from the other using only definitions, time-keeping conventions or
the sky, not facts about the world (schedules, customs, where something happened to be).

**The time is fixed by the place (code TBP)** when either:

- the time is a clock time, date, weekday, part of day or season whose reading differs from place to place only
  because of time zones, the date line or the hemispheres, and the place is a city, region, country, time zone or
  hemisphere that sets which reading applies ("already Saturday morning" / "in Sydney"; "12:30 Central Time" /
  "Central Time"); or
- the time is defined by the sun's position (noon, midnight as solar midnight, sunrise, sunset, dawn, dusk) and the
  place is where that position is read off; or
- the time *is* reaching, leaving or being at the place named ("once there" / "there"; "on arrival" / "at the
  station"; "until the X stop" / "on the bus").

**The place is fixed by the time (code PBT)** when the place is identified through a time: a clock-face position
("the two o'clock position"), a place named by when it happens or is reached ("the Tuesday market"), or a position
of the sun or sky that a time defines.

**BOTH** when each holds. **NEITHER** otherwise. A year, a decade, a historical period, a duration ("for two
nights", "since 2011"), "now", "then", "yesterday", or a time relative to an event ("after the war") is never fixed
by a place. A room, a building, a shop, "here", "at home" does not set a time-keeping reading. A time that merely
tends to go with a place (dinner at ten in Spain, opening hours) is NEITHER.

Examples:
- "already evening" / "in Jakarta" -> TBP
- "the six o'clock position" / "at six" -> PBT
- "at noon" / "at its highest point in the sky" -> BOTH
- "in 1990" / "in the old town" -> NEITHER
- "on Monday" / "at the office" -> NEITHER

**Output.** One row per item, tab-separated, header exactly:

    bid	code	confidence	note

- `code`: TBP, PBT, BOTH or NEITHER.
- `confidence`: 3 sure, 2 fairly sure, 1 unsure.
- `note`: at most a dozen words.

Code every row of the file you are given, in its order, and nothing else.
