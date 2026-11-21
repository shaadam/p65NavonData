# Coding brief: does the stated value need the other dimension?

You will see sentences in English and Indonesian, each with the sentence before it. Every sentence pairs a literal
time expression with a literal place expression, and one of the two restricts the other. Each row tells you which
way round it is, in the column `frame`:

- `PLACE-STATED`: the sentence states where something is (a location, a position, a place reached as a state), and
  the time expression says when that holds.
- `TIME-STATED`: the sentence states a time value (a clock time, a date, a season, daylight, the timing of
  something), and the place expression says where that holds.

Do not re-decide the frame. Your one question is about the **stated value** (the place in a PLACE-STATED row, the
time in a TIME-STATED row):

**Does the stated value, by the kind of thing it is, have no fixed value unless the other dimension is given?**

Every sentence of this kind restricts the stated value to the other dimension; that is what the frame means, so the
restriction alone is never a reason to say yes. The question is whether the stated value *could* be given without
the other dimension at all, for this kind of thing.

Write one of three codes.

**S (strict: needs it by its kind).**
- PLACE-STATED: the thing located is, by its kind, somewhere only for a time: a person, an animal, a vehicle, a
  movable object, a crowd, an event, a visit or stay, weather. "The train is in Boston at nine." "By six the
  children were home." "At nine he was still at his aunt's house." Its place has no value until a time is given.
- TIME-STATED: the time value is local by the nature of time-keeping or of the sky: a clock reading, a date, a
  weekday, a season, daylight or darkness, the sun's position, or the time at which a moving thing (a train, a
  bus, a ship) passes or reaches that stop. "It is nine o'clock in Boston." "In Sydney it was already Saturday
  morning." "In the southern hemisphere it is winter in July." Its time has no value until a place is given.

**B (broad: differs with it, but only by practice or by history).**
- PLACE-STATED: the thing located is normally fixed (a building, a shop, a business, an institution, a town), but
  the sentence or the sentence before it shows it was, or will be, elsewhere at another time. "In 2019 the bakery
  was still on Main Street." (it later moved)
- TIME-STATED: the time is set by a custom, rule or schedule of that place, and would differ elsewhere by practice,
  not by time-keeping: "In Spain dinner is at ten." "Here the school year starts in August." "At the museum the
  doors open at nine."

**N (no: the stated value stands without the other dimension).**
- PLACE-STATED: the thing located is fixed by its kind or by its identity, and the time phrase does not change
  where it is: a mountain, a lake, a river, a city, a region, a landmark, ruins. "Even in midwinter the old fort
  sits on the ridge above the town." "Sampai sekarang pun danau itu terletak di sebelah utara kota." Also N when the
  located thing is a fixed feature and the time phrase only says when it can be seen or reached.
- TIME-STATED: the time of a single event or state, which the place merely locates or picks out: "In the main hall
  the keynote was on the Tuesday." "At the conference the vote came on the last day." The event has one time; the
  place says which event, not what time it is there.

Minimal pairs (same frame, different code):
- PLACE-STATED: "At noon the ferry is at the pier." S / "At noon the lighthouse is at the end of the pier." N
- PLACE-STATED: "In 1990 the bakery was on Main Street, before it moved." B / "In 1990 the cathedral was on Main
  Street." N
- TIME-STATED: "In Jakarta it is already evening." S / "In Jakarta the opening ceremony was on a Monday." N
- TIME-STATED: "At this stop the last bus leaves at 11:40." S / "In this town the shops close at six." B

Rules of thumb. Ask what kind of thing carries the stated value, not whether the sentence happens to be true only
then or there. If you could write the stated value on a map or a calendar once and for all, it is N. If it changes
with the other dimension by nature (movement, time zones, seasons, the sun), it is S. If it changes only by human
practice or history, it is B. Decide from the sentence and the one before it; do not consult the wider text.
Indonesian sentences are coded from the Indonesian only.

**Output.** One row per item, tab-separated, header exactly:

    did	code	confidence	note

- `code`: S, B or N.
- `confidence`: 3 sure, 2 fairly sure, 1 unsure.
- `note`: at most a dozen words naming the stated value and what carries it.

Code every row of the file you are given, in its order, and nothing else.
