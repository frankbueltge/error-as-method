#!/usr/bin/env python3
"""Build the instant corpus for Session 68.

Instants are integer epoch seconds and nothing else. No runtime is consulted here, and no
string is produced here: the corpus exists before any runtime sees it, so that a property of
the draw can never be reported as a property of a runtime (Session 67, correction C4).

Twelve instants are CHOSEN for the boundaries they stress and are labelled as such.
Two hundred are DRAWN by SplitMix64 seeded with the session number, uniform over
1900-01-01T00:00:00Z .. 2100-01-01T00:00:00Z. The two are kept apart in the output.
"""
import json
import datetime as dt

SEED = 68
N_DRAWN = 200
LO = -2208988800   # 1900-01-01T00:00:00Z
HI = 4102444800    # 2100-01-01T00:00:00Z

MASK = (1 << 64) - 1


def splitmix64(state):
    """Vigna's SplitMix64. Same generator Session 67 used, seeded with this session's number."""
    while True:
        state = (state + 0x9E3779B97F4A7C15) & MASK
        z = state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
        yield z ^ (z >> 31)


def utc(y, mo, d, h=0, mi=0, s=0):
    return int(dt.datetime(y, mo, d, h, mi, s, tzinfo=dt.timezone.utc).timestamp())


CHOSEN = [
    ("epoch",                    0,
     "the zero of the scale itself"),
    ("pre-epoch",                -1,
     "one second before it; a sign change in every implementation that stores it as an integer"),
    ("dst-spring-forward",       utc(2026, 3, 29, 1, 30),
     "Europe/Berlin 03:30 CEST; the local clock skipped 02:00..03:00 the same morning"),
    ("dst-fall-back-first",      utc(2026, 10, 25, 0, 30),
     "Europe/Berlin 02:30 CEST, the FIRST of the two local 02:30s that day"),
    ("dst-fall-back-second",     utc(2026, 10, 25, 1, 30),
     "Europe/Berlin 02:30 CET, the SECOND; the same local text as the line above"),
    ("leap-day",                 utc(2024, 2, 29, 12, 0),
     "29 February, a date three of the four parsers must special-case"),
    ("y2038",                    2147483647,
     "the last instant a signed 32-bit time_t can hold"),
    ("y2038-plus-one",           2147483648,
     "the first it cannot"),
    ("year-1900",                LO,
     "the low end of the drawn range; before the epoch by 70 years"),
    ("year-2100",                HI,
     "the high end; a year that is not a leap year despite being divisible by four"),
    ("day-month-ambiguous",      utc(2026, 1, 2, 0, 0),
     "2 January: both fields are <= 12, so day-first and month-first readings both parse"),
    ("noon-berlin-local",        1787479200,
     "2026-08-23 12:00:00 local in Europe/Berlin; 10:00 UTC. The night's own date."),
]


def main():
    gen = splitmix64(SEED)
    span = HI - LO
    drawn = []
    for i in range(N_DRAWN):
        drawn.append(LO + (next(gen) % span))

    corpus = {
        "seed": SEED,
        "generator": "SplitMix64 (Vigna), as used by Session 67",
        "range": {"lo": LO, "hi": HI,
                  "meaning": "1900-01-01T00:00:00Z .. 2100-01-01T00:00:00Z"},
        "chosen": [{"label": lab, "epoch": e, "why": why} for lab, e, why in CHOSEN],
        "drawn": drawn,
        "note": ("chosen and drawn are kept apart deliberately. Any count reported over 'drawn' "
                 "is a property of a uniform draw over bit-range, not of the runtimes; any count "
                 "over 'chosen' is a property of instants picked because they were expected to "
                 "stress something."),
    }
    with open("corpus.json", "w") as fh:
        json.dump(corpus, fh, indent=1)
    print(f"corpus.json: {len(CHOSEN)} chosen + {len(drawn)} drawn = "
          f"{len(CHOSEN) + len(drawn)} instants")


if __name__ == "__main__":
    main()
