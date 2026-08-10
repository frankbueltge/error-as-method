#!/usr/bin/env python3
"""
Two Exacts — where the cut falls, and who errs.

One list of numbers. Eight summation apparatuses. Three norms.
Nothing here is simulated: every difference below is real IEEE-754 rounding,
produced by running the sum, not by staging an accident.

Deterministic: stdlib only, seed 20260810, no wall-clock, no Math.random.
Same seed -> same data.json, byte for byte.

Reference for the arithmetic:
  Goldberg, D. (1991). What Every Computer Scientist Should Know About
  Floating-Point Arithmetic. ACM Computing Surveys 23(1), 5-48.
  https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html
  IEEE 754-2019, https://doi.org/10.1109/IEEESTD.2019.8766229
  Neumaier, A. (1974). ZAMM 54(1), 39-51. https://doi.org/10.1002/zamm.19740540106
  Python's math.fsum (Shewchuk's exact accumulation):
  https://docs.python.org/3/library/math.html#math.fsum
"""

import json
import math
import random
import struct
from fractions import Fraction
from pathlib import Path

SEED = 20260810


# --------------------------------------------------------------------------
# the apparatuses — eight ways to add the same numbers
# --------------------------------------------------------------------------

def naive_lr(xs):
    s = 0.0
    for x in xs:
        s += x
    return s


def naive_rl(xs):
    s = 0.0
    for x in reversed(xs):
        s += x
    return s


def sorted_asc(xs):
    return naive_lr(sorted(xs, key=abs))


def sorted_desc(xs):
    return naive_lr(sorted(xs, key=abs, reverse=True))


def pairwise(xs):
    if len(xs) <= 8:
        return naive_lr(xs)
    h = len(xs) // 2
    return pairwise(xs[:h]) + pairwise(xs[h:])


def neumaier(xs):
    """Kahan-Babuska-Neumaier compensated summation."""
    s = 0.0
    c = 0.0
    for x in xs:
        t = s + x
        if abs(s) >= abs(x):
            c += (s - t) + x
        else:
            c += (x - t) + s
        s = t
    return s + c


def fsum(xs):
    """Correctly rounded sum of the stored doubles."""
    return math.fsum(xs)


def _f32(x):
    return struct.unpack("f", struct.pack("f", x))[0]


def fp32_lr(xs):
    """Left-to-right, every operand and every partial sum rounded to binary32."""
    s = _f32(0.0)
    for x in xs:
        s = _f32(s + _f32(x))
    return float(s)


APPARATUSES = [
    ("naive_lr", "left to right, float64", naive_lr),
    ("naive_rl", "right to left, float64", naive_rl),
    ("sorted_asc", "smallest magnitude first", sorted_asc),
    ("sorted_desc", "largest magnitude first", sorted_desc),
    ("pairwise", "recursive halving (block 8)", pairwise),
    ("neumaier", "compensated (Kahan-Babuska-Neumaier)", neumaier),
    ("fsum", "exactly rounded over the stored doubles", fsum),
    ("fp32_lr", "left to right, binary32 throughout", fp32_lr),
]


# --------------------------------------------------------------------------
# the data — each item exists twice: as written, and as stored
# --------------------------------------------------------------------------

def ledger(n=2000):
    """Money. Written in base ten with two places; stored in base two."""
    rng = random.Random(SEED)
    written = []
    for _ in range(n):
        cents = rng.randint(-9_999_99, 9_999_99)
        written.append(f"{cents // 100}.{abs(cents) % 100:02d}"
                       if cents >= 0 else f"-{abs(cents) // 100}.{abs(cents) % 100:02d}")
    exact = [Fraction(w) for w in written]
    return written, exact


def cancellation(n=2000):
    """Large opposed magnitudes with a small residue: the sum is nearly nothing."""
    rng = random.Random(SEED + 1)
    written = []
    for _ in range(n // 2):
        big = rng.randint(1, 9_999_999_99) / Fraction(100)
        written.append(str(big))
        written.append(str(-big))
    for _ in range(n - len(written)):
        written.append(str(rng.randint(-999_99, 999_99) / Fraction(100)))
    rng.shuffle(written)
    exact = [Fraction(w) for w in written]
    return written, exact


def harmonic(n=6000):
    """1/k. Written as a rational; stored as the nearest double."""
    written = [f"1/{k}" for k in range(1, n + 1)]
    exact = [Fraction(1, k) for k in range(1, n + 1)]
    return written, exact


DATASETS = [
    ("ledger", "2000 signed amounts of money, two decimal places", ledger),
    ("cancellation", "2000 terms, opposed magnitudes up to 1e8, small residue", cancellation),
    ("harmonic", "1/k for k = 1..6000", harmonic),
]


# --------------------------------------------------------------------------
# the run
# --------------------------------------------------------------------------

def frac_to_float(f):
    """Nearest double to an exact rational (no intermediate overflow)."""
    return f.numerator / f.denominator if abs(f.numerator) < 2 ** 900 else float(f)


def measure(name, note, build):
    written, exact = build()
    stored = [float(f) for f in exact]

    sum_written = sum(exact, Fraction(0))          # exact, the object as written
    sum_stored = sum(Fraction(x) for x in stored)  # exact, the object as stored
    representation_gap = abs(sum_written - sum_stored)

    results = {}
    for key, desc, fn in APPARATUSES:
        v = fn(stored)
        results[key] = {"desc": desc, "value": v, "repr": repr(v)}

    golden = Fraction(results["naive_lr"]["value"])

    norms = {
        "as_written": {
            "label": "as written",
            "note": "the exact sum of the source literals — the object before any machine touched it",
            "value": sum_written,
        },
        "as_stored": {
            "label": "as stored",
            "note": "the exact sum of the float64 values actually in memory — the machine's object",
            "value": sum_stored,
        },
        "golden": {
            "label": "the frozen value",
            "note": "whatever left-to-right float64 produced, held fixed by a regression test",
            "value": golden,
        },
    }

    for norm_key, norm in norms.items():
        ref = norm["value"]
        for key in results:
            err = abs(Fraction(results[key]["value"]) - ref)
            results[key].setdefault("err", {})[norm_key] = frac_to_float(err)
        order = sorted(results, key=lambda k: (results[k]["err"][norm_key], k))
        norm["ranking"] = order
        norm["zero_error"] = [k for k in results if results[k]["err"][norm_key] == 0.0]
        norm["floor"] = frac_to_float(min(
            abs(Fraction(results[k]["value"]) - ref) for k in results))
        norm["value"] = float(ref)
        norm["value_exact"] = f"{ref.numerator}/{ref.denominator}"

    return {
        "name": name,
        "note": note,
        "n": len(stored),
        "sum_written": float(sum_written),
        "sum_stored": float(sum_stored),
        "representation_gap": frac_to_float(representation_gap),
        "apparatuses": results,
        "norms": norms,
    }


def findings(datasets):
    """Facts computed from the run, not asserted about it."""
    out = []
    for d in datasets:
        n = d["name"]
        st, wr, go = d["norms"]["as_stored"], d["norms"]["as_written"], d["norms"]["golden"]

        out.append({
            "dataset": n,
            "id": "golden_inverts",
            "claim": "under the frozen value, the apparatuses that err are exactly the accurate ones",
            "zero_error_under_golden": go["zero_error"],
            "nonzero_under_golden": [k for k in d["apparatuses"] if k not in go["zero_error"]],
            "fsum_error_vs_golden": d["apparatuses"]["fsum"]["err"]["golden"],
        })

        # NOTE. The first version of this claim read "against the object as written
        # there is a floor no summation can cross". The run refuted it: on the ledger
        # the best distance (pairwise, 1.63e-11) is BELOW the representation gap
        # (2.18e-11), because pairwise's own rounding error runs opposite to the gap
        # and overshoots it. The offset is inherited, not reducible by accuracy —
        # but it can be undershot by luck. Corrected wording kept; the discard is in
        # the journal for 2026-08-10.
        out.append({
            "dataset": n,
            "id": "offset",
            "claim": "the distance to the object as written is the distance to the object as "
                     "stored combined, with sign, with a representation gap fixed before any "
                     "addition happened; no summation reduces that gap, and landing nearer to "
                     "the written object is cancellation, not accuracy",
            "best_distance_under_written": wr["floor"],
            "representation_gap": d["representation_gap"],
            "best_under_written": wr["ranking"][0],
            "best_under_stored": st["ranking"][0],
            "check_fsum": {
                "err_as_stored": d["apparatuses"]["fsum"]["err"]["as_stored"],
                "err_as_written": d["apparatuses"]["fsum"]["err"]["as_written"],
                "gap_plus_own": d["representation_gap"] + d["apparatuses"]["fsum"]["err"]["as_stored"],
            },
        })

        better_than_fsum = [k for k in d["apparatuses"]
                            if d["apparatuses"][k]["err"]["as_written"]
                            < d["apparatuses"]["fsum"]["err"]["as_written"]]
        out.append({
            "dataset": n,
            "id": "sloppy_can_win",
            "claim": "against the object as written, apparatuses less accurate about the "
                     "stored object can land closer than the exactly rounded one",
            "beat_fsum_under_as_written": better_than_fsum,
            "fsum_err_as_written": d["apparatuses"]["fsum"]["err"]["as_written"],
            "fsum_err_as_stored": d["apparatuses"]["fsum"]["err"]["as_stored"],
        })

        out.append({
            "dataset": n,
            "id": "ranking_moves",
            "claim": "the ranking of the apparatuses is not a property of the apparatuses",
            "as_written": wr["ranking"],
            "as_stored": st["ranking"],
            "golden": go["ranking"],
            "same_order_written_stored": wr["ranking"] == st["ranking"],
        })
    return out


def main():
    datasets = [measure(name, note, build) for name, note, build in DATASETS]
    data = {
        "title": "Two Exacts",
        "seed": SEED,
        "generated_by": "cut.py (stdlib only; same seed, same file)",
        "python": "3.11",
        "apparatus_order": [k for k, _, _ in APPARATUSES],
        "datasets": datasets,
        "findings": findings(datasets),
    }
    out = Path(__file__).with_name("data.json")
    out.write_text(json.dumps(data, indent=1, sort_keys=False) + "\n")
    print(f"wrote {out}")

    # the work is self-contained: the run is carried inside index.html as a JSON
    # island, so the page loads nothing from anywhere.
    page = Path(__file__).with_name("index.html")
    if page.exists():
        head, sep, rest = page.read_text().partition('<script type="application/json" id="run">')
        if sep:
            _, close, tail = rest.partition("</script>")
            page.write_text(head + sep + "\n" + json.dumps(data, separators=(",", ":"))
                            + "\n" + close + tail)
            print(f"inlined the run into {page}")

    for d in datasets:
        print(f"\n=== {d['name']}  (n={d['n']})")
        print(f"    sum as written : {d['sum_written']!r}")
        print(f"    sum as stored  : {d['sum_stored']!r}")
        print(f"    representation gap: {d['representation_gap']:.3e}")
        for norm_key in ("as_written", "as_stored", "golden"):
            nm = d["norms"][norm_key]
            print(f"  -- norm: {nm['label']:16s} floor={nm['floor']:.6e} "
                  f"zero={nm['zero_error']}")
            for k in nm["ranking"]:
                print(f"       {k:12s} err={d['apparatuses'][k]['err'][norm_key]:.6e}")


if __name__ == "__main__":
    main()
