"""FREQ: how many valid recreational vessels in the register bear exactly a name.

Same API and frame as sample.py; the count is found by exponential search and bisection on
single-row pages, so no full listing is downloaded. Names are upper-cased and inner whitespace
collapsed; nothing else is changed (an apostrophe stays an apostrophe).

Usage: python3 -I freq.py NAMES.txt OUT.json   (one name per line; OUT is updated, not overwritten)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample import get  # noqa: E402
from features import norm  # noqa: E402


def count(name):
    q = {"service": "Recreational", "doc_status": "Valid", "vessel_name": norm(name)}
    has = lambda off: get(off, 1, q)["count"] > 0
    if not has(0):
        return 0
    lo, hi = 0, 1
    while has(hi):
        lo, hi = hi, hi * 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if has(mid):
            lo = mid
        else:
            hi = mid
    return hi


def main(src, out):
    res = json.load(open(out)) if os.path.exists(out) else {}
    for line in open(src):
        n = norm(line)
        if n and n not in res:
            res[n] = count(n)
            json.dump(res, open(out, "w"), indent=1, sort_keys=True)
    print(len(res), "names counted")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
