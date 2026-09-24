#!/usr/bin/env python3
"""power.py -- what twenty hand-read occurrences can decide, computed before any of them exists.

Session 95's open thread 4: "Compute the MDE before the night, not after."  This file is that
rule taken up on its first occasion.  It uses nothing but the standard library and no data: the
only inputs are the sample size and the falsification bar written into S95.NOTPARTY
(works/FALSIFIERS.md) -- "falsified if that top carrier is a genuine party in more than half of
twenty of its occurrences".

It prints and writes `power.json`:
  * for every true party share p on a grid, the chance that twenty draws put more than ten on the
    party side -- i.e. the chance the row is falsified if the truth is p;
  * for every count k that could come back, the exact (Clopper-Pearson) 95 % interval on p;
  * the band of true shares inside which the verdict is closer to a coin than to a finding.

Drawing twenty occurrences of one word out of a frame holding many more is sampling without
replacement; the binomial here is the with-replacement approximation and is conservative (the
true intervals are slightly narrower).  Stated, not corrected.
"""
import json
from math import comb
from pathlib import Path

N = 20
BAR = 10                                  # falsified if YES > BAR


def pmf(k, n, p):
    return comb(n, k) * p ** k * (1 - p) ** (n - k)


def p_falsified(p, n=N, bar=BAR):
    return sum(pmf(k, n, p) for k in range(bar + 1, n + 1))


def cdf(k, n, p):
    return sum(pmf(i, n, p) for i in range(0, k + 1))


def bisect(f, lo, hi, target, it=80):
    """f increasing on [lo, hi]; the x with f(x) == target."""
    for _ in range(it):
        mid = (lo + hi) / 2
        if f(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def clopper_pearson(k, n, alpha=0.05):
    lo = 0.0 if k == 0 else bisect(lambda p: 1 - cdf(k - 1, n, p), 0.0, 1.0, alpha / 2)
    hi = 1.0 if k == n else bisect(lambda p: -cdf(k, n, p), 0.0, 1.0, -alpha / 2)
    return lo, hi


def main():
    grid = [round(0.05 * i, 2) for i in range(1, 20)]
    curve = {"%.2f" % p: round(p_falsified(p), 4) for p in grid}
    intervals = {k: [round(x, 4) for x in clopper_pearson(k, N)] for k in range(N + 1)}
    # the band where the verdict is neither reliably 'survives' nor reliably 'falsified'
    lo = bisect(p_falsified, 0.0, 1.0, 0.2)
    hi = bisect(p_falsified, 0.0, 1.0, 0.8)
    # the counts that exclude 0.5 at 95 % on their own
    decisive_low = [k for k, (a, b) in intervals.items() if b < 0.5]
    decisive_high = [k for k, (a, b) in intervals.items() if a > 0.5]
    out = {
        "n": N, "bar": "falsified if YES > %d" % BAR,
        "p_falsified_by_true_share": curve,
        "clopper_pearson_95_by_count": intervals,
        "coin_band_20_to_80_percent": [round(lo, 4), round(hi, 4)],
        "counts_that_exclude_half_low": decisive_low,
        "counts_that_exclude_half_high": decisive_high,
    }
    # self-check derived from the formula, not from memory (F-155): p = 0.5 is symmetric, so the
    # chance of more than ten is (1 - P(exactly ten)) / 2, with P(ten) = C(20,10) / 2**20.
    expect = (1 - comb(20, 10) / 2 ** 20) / 2
    assert abs(p_falsified(0.5) - expect) < 1e-12, (p_falsified(0.5), expect)
    Path(__file__).with_name("power.json").write_text(json.dumps(out, indent=1) + "\n")
    print("P(falsified | p):")
    for p, v in curve.items():
        print("  p = %s  ->  %.4f" % (p, v))
    print("coin band (20 %% .. 80 %% chance of falsifying): p in [%.4f, %.4f]" % (lo, hi))
    print("counts whose 95 % interval lies wholly below 0.5:", decisive_low)
    print("counts whose 95 % interval lies wholly above 0.5:", decisive_high)
    for k in (5, 8, 10, 11, 12, 15):
        print("  k = %2d  ->  95 %% CI %s" % (k, intervals[k]))


if __name__ == "__main__":
    main()
