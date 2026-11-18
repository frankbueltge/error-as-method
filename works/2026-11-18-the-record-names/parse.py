"""Parse the makers' hand-backs into labels and claims.

python3 -I parse.py  ->  labels.json : one entry per (round, maker, object) with heading, paragraph and claims.
Assignment of makers to objects is the one committed in predictions.md.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).parent
LETTERS = json.loads((HERE / "objects" / "letters.json").read_text())
out = []
for rnd in (1, 2):
    for f in sorted((HERE / "makings").glob(f"r{rnd}-m*.txt")):
        maker = f.stem.split("-")[1]
        text = f.read_text()
        changed = dict(re.findall(r"^changed object-(\w):\s*(.*)$", text, re.M))
        for block in re.split(r"^=== object-(\w) ===\s*$", text, flags=re.M)[1:]:
            pass
        parts = re.split(r"^=== object-(\w) ===\s*$", text, flags=re.M)
        for i in range(1, len(parts), 2):
            obj, body = parts[i], parts[i + 1]
            lines = [l.strip() for l in body.strip().splitlines()]
            claims, prose = [], []
            for l in lines:
                if l.startswith("{") and '"claim"' in l:
                    claims.append(json.loads(l))
                elif l and not l.startswith("changed object-"):
                    prose.append(l)
            out.append({"round": rnd, "maker": maker, "object": obj, "objectID": LETTERS[obj],
                        "heading": prose[0] if prose else "", "paragraph": " ".join(prose[1:]),
                        "claims": claims, "changed": changed.get(obj)})
(HERE / "labels.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(len(out), "labels;", sum(len(x["claims"]) for x in out), "claims")
for rnd in (1, 2):
    sub = [x for x in out if x["round"] == rnd]
    print("round", rnd, len(sub), "labels", sum(len(x["claims"]) for x in sub), "claims")
