#!/usr/bin/env python3
"""Build seeds.json — the doubles every runtime is asked to render and to parse.

Two parts, and the split matters for what can be claimed afterwards.

  named    : twelve doubles chosen by hand for what they are known to stress
             (the classic 0.1+0.2, the 2^53 boundary, negative zero, the
             smallest subnormal, the largest finite double).
  drawn    : 500 doubles drawn from a fixed, documented pseudo-random source
             over whole 64-bit patterns, so the negative result below is not a
             property of a hand-picked list. Seed 67 = the session number;
             SplitMix64, the constants as published by Steele, Lea and Flood
             (OOPSLA 2014, doi:10.1145/2660193.2660195). Non-finite patterns
             are skipped; nothing else is.

A seed is a BIT PATTERN, never a decimal string: the point of the night is
what each runtime does when it turns a double into text, so the input must not
already be text.
"""
import json
import math
import struct

MASK = (1 << 64) - 1

NAMED = [
    ("point_one", 0.1),
    ("one_tenth_plus_two_tenths", 0.1 + 0.2),
    ("one_third", 1 / 3),
    ("pi", math.pi),
    ("1e21", 1e21),
    ("1e-7", 1e-7),
    ("two53", float(2 ** 53)),
    ("two53_plus_two", float(2 ** 53 + 2)),
    ("neg_zero", -0.0),
    ("min_subnormal", 5e-324),
    ("max_double", 1.7976931348623157e308),
    ("big_int_as_double", 123456789012345678.0),
]


def splitmix64(state):
    state = (state + 0x9E3779B97F4A7C15) & MASK
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
    return state, (z ^ (z >> 31)) & MASK


def main(n_drawn=500, seed=67):
    out = [{"name": n, "kind": "named", "bits": struct.pack(">d", v).hex()}
           for n, v in NAMED]
    state, drawn, tried = seed, 0, 0
    while drawn < n_drawn:
        state, r = splitmix64(state)
        tried += 1
        x = struct.unpack(">d", r.to_bytes(8, "big"))[0]
        if not math.isfinite(x):
            continue
        out.append({"name": "drawn_%03d" % drawn, "kind": "drawn",
                    "bits": "%016x" % r})
        drawn += 1
    json.dump(out, open("seeds.json", "w"), indent=1)
    print("named %d · drawn %d · draws rejected as non-finite %d · total %d"
          % (len(NAMED), drawn, tried - drawn, len(out)))


if __name__ == "__main__":
    main()
