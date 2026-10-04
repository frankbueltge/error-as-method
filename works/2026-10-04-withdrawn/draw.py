"""Draw the hand sample (P5): 60 NOTICE rows, random.seed(104), ids sorted ascending.
Prints only id and comment; writes sample.json. Run before code.py exists."""
import json, random
rows = [r for r in json.load(open("notices.json")) if "withdr" in r["comment"].lower()]
rows.sort(key=lambda r: r["id"])
random.seed(104)
sample = random.sample(rows, 60)
json.dump([{"n": i + 1, "id": r["id"], "comment": r["comment"]} for i, r in enumerate(sample)],
          open("sample.json", "w"), ensure_ascii=False, indent=1)
for i, r in enumerate(sample):
    print(f"{i+1:2d} | {r['comment']}")
