#!/usr/bin/env python3
"""Experiment 38, Drawn in Twenty Seconds: the draw, the people's pools and the shown six.

Seed 156 draws 12 of the 345 Quick, Draw! categories. For each, the simplified ndjson file
(CC BY 4.0) is sampled by byte ranges at 8 seeded offsets, 262,144 bytes each; partial lines at
the edges are dropped. Only drawings the game recognised are kept (declared before any maker ran:
an unrecognised drawing is often an abandoned one, and keeping them would inflate the people's
spread in the direction this experiment's hypothesis expects). The pool is capped at 1,500.

From each pool, seed 156 draws the SHOWN six people (arm H). They are removed from the pool, so
the null distributions in score.py never contain a drawing a maker has seen.

Writes plan.json (categories, files, byte ranges, counts) and pools/<category>.json, then the
contact sheets for arm H (sheets/H-<n>.png). Arm F's sheets are written by sheets.py after arm S.

    python3 -I prepare.py
"""
import hashlib
import json
import os
import random
import urllib.parse
import urllib.request

from render import contact_sheet

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://storage.googleapis.com/quickdraw_dataset/full/simplified/"
SEED = 156
N_CATS = 12
OFFSETS = 8
CHUNK = 262144
CAP = 1500


def url_of(cat):
    return BASE + urllib.parse.quote(cat + ".ndjson")


def size_of(url):
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=60) as r:
        return int(r.headers["Content-Length"])


def fetch(url, start, length):
    req = urllib.request.Request(url, headers={"Range": f"bytes={start}-{start + length - 1}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def main():
    cats = [c.strip() for c in open(os.path.join(HERE, "sources", "categories.txt")) if c.strip()]
    rng = random.Random(SEED)
    chosen = rng.sample(cats, N_CATS)
    os.makedirs(os.path.join(HERE, "pools"), exist_ok=True)
    plan = {"seed": SEED, "categories": [], "note": __doc__.strip().split("\n\n")[1]}
    for cat in chosen:
        url = url_of(cat)
        size = size_of(url)
        starts = sorted(rng.randrange(0, size - CHUNK) for _ in range(OFFSETS))
        seen, rows, hashes = set(), [], []
        n_lines = n_rec = 0
        for s in starts:
            raw = fetch(url, s, CHUNK)
            hashes.append(hashlib.sha256(raw).hexdigest())
            lines = raw.split(b"\n")[1:-1]  # drop the partial edges
            for ln in lines:
                try:
                    d = json.loads(ln)
                except ValueError:
                    continue
                n_lines += 1
                if d["key_id"] in seen:
                    continue
                seen.add(d["key_id"])
                if d.get("recognized"):
                    n_rec += 1
                    rows.append({"key_id": d["key_id"], "countrycode": d["countrycode"],
                                 "drawing": d["drawing"]})
        rng.shuffle(rows)
        rows = rows[:CAP]
        shown = rows[:6]
        pool = rows[6:]
        with open(os.path.join(HERE, "pools", cat.replace(" ", "_") + ".json"), "w") as fh:
            json.dump({"category": cat, "shown": shown, "pool": pool}, fh, separators=(",", ":"))
        plan["categories"].append({
            "category": cat, "url": url, "file_bytes": size, "range_starts": starts,
            "range_length": CHUNK, "range_sha256": hashes, "complete_lines": n_lines,
            "recognised": n_rec, "kept_pool": len(pool),
            "shown_key_ids": [r["key_id"] for r in shown]})
        print(f"{cat:20s} {size:>11,d} bytes  lines {n_lines:5d}  recognised {n_rec:5d}  pool {len(pool)}")
    with open(os.path.join(HERE, "plan.json"), "w") as fh:
        json.dump(plan, fh, indent=1)
    # arm H: the same six people for every H maker; the order of categories differs by maker
    order_rng = random.Random(SEED + 1)
    briefs = {}
    for arm in ("S", "F", "H"):
        for n in range(1, 7):
            order = list(range(N_CATS))
            order_rng.shuffle(order)
            briefs[f"{arm}{n}"] = order
    with open(os.path.join(HERE, "orders.json"), "w") as fh:
        json.dump(briefs, fh, indent=1)
    os.makedirs(os.path.join(HERE, "sheets"), exist_ok=True)
    for i, c in enumerate(plan["categories"]):
        pool = json.load(open(os.path.join(HERE, "pools", c["category"].replace(" ", "_") + ".json")))
        contact_sheet([r["drawing"] for r in pool["shown"]],
                      os.path.join(HERE, "sheets", f"H-{i + 1:02d}.png"))


if __name__ == "__main__":
    main()
