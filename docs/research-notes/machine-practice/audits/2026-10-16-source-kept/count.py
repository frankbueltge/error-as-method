"""Session 132: who kept the source of what they were told, by cell, in experiment 21.

Reads coder B's codes as committed in works/2026-10-16-told-true/results.json. A maker "kept
the source" when coder B coded C7 as anything but n/a: C7 is only answered when the maker says
it was told what the record is. Nothing is re-coded here; this is a count over the coder's codes.
"""
import json
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
res = json.loads((ROOT / "works/2026-10-16-told-true/results.json").read_text())

cells = {}
for m, v in sorted(res["per_maker"].items()):
    b = v.get("B", v)
    kept = b.get("C7") not in (None, "n/a")
    cells.setdefault(v["cell"], []).append((m, kept, b.get("C7"), b.get("C10")))

for cell in ("T", "F", "N"):
    rows = cells[cell]
    print(cell, sum(k for _, k, _, _ in rows), "of", len(rows),
          [(m, c7, c10) for m, k, c7, c10 in rows if k])

# Fisher's exact test, F against T, on "said it was told" (hypergeometric, both tails).
a = sum(k for _, k, _, _ in cells["F"]); n1 = len(cells["F"])
b = sum(k for _, k, _, _ in cells["T"]); n2 = len(cells["T"])
K, N = a + b, n1 + n2
p = lambda x: comb(n1, x) * comb(n2, K - x) / comb(N, K)
obs = p(a)
two = sum(p(x) for x in range(max(0, K - n2), min(K, n1) + 1) if p(x) <= obs + 1e-12)
one = sum(p(x) for x in range(a, min(K, n1) + 1))
print(f"F {a}/{n1} against T {b}/{n2}: Fisher one-sided p = {one:.4f}, two-sided p = {two:.4f}")
