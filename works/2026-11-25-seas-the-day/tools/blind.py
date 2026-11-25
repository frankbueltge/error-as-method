"""Make the blind coding sheet: the SCORE sample's 200 names and every maker's final names, shuffled
together by seed 1870, with no arm or source. The coder sees only a running number and a name.

Usage: python3 -I blind.py MAKERS_DIR OUTDIR
Writes OUTDIR/blind-sheet.txt (for the coder) and OUTDIR/blind-key.json (kept from the coder).
"""
import json, os, random, sys

here = os.path.dirname(os.path.abspath(__file__))


def main(makers, out):
    rows = json.load(open(os.path.join(here, "..", "people", "people.json")))["rows"][:200]
    items = [{"src": "people", "id": r["draw"], "name": r["name"].strip().upper()} for r in rows]
    for m in sorted(os.listdir(makers)):
        p = os.path.join(makers, m, "names.txt")
        if not os.path.exists(p):
            continue
        for k, line in enumerate(l for l in open(p) if l.strip()):
            items.append({"src": m, "id": k, "name": line.strip().upper()})
    random.Random(1870).shuffle(items)
    for i, it in enumerate(items):
        it["n"] = i
    with open(os.path.join(out, "blind-sheet.txt"), "w") as f:
        for it in items:
            f.write(f"{it['n']}\t{it['name']}\n")
    json.dump(items, open(os.path.join(out, "blind-key.json"), "w"), indent=1)
    print(len(items), "items")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
