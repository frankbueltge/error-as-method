"""Session 161: write face-data.js for index.html from the committed rooms, people.json and results.json."""
import json, re
from pathlib import Path
HERE = Path(__file__).parent
plan = json.load(open(HERE / "plan.json")); people = json.load(open(HERE / "people.json"))
res = json.load(open(HERE / "results.json"))
def read(letter):
    out = {}
    for i in range(1, 7):
        m = f"{letter}{i}"; order = plan["orders"][m]
        for line in (HERE / "rooms" / f"{m}.txt").read_text().splitlines():
            mm = re.match(r"\s*(\d+)\s*:\s*(.*)$", line)
            if mm and 1 <= int(mm.group(1)) <= 32:
                k = order[int(mm.group(1)) - 1]
                if letter == "A": out.setdefault(k, []).append(int(mm.group(2)))
                else: out.setdefault(k, []).append(float(re.search(r"p50=(-?[\d.]+)", mm.group(2)).group(1)))
    return out
A, S, F = read("A"), read("S"), read("F")
rows = []
for k in plan["keys"]:
    key = k["key"]; r = people[key]["ratings"]
    rows.append({"key": key, "sentence": k["sentence"], "cond": k["cond"], "n": people[key]["n"],
                 "hist": [r.count(v) for v in range(1, 8)], "pmed": people[key]["median"], "pmean": people[key]["mean"],
                 "A": A[key], "S": S[key], "F": F[key]})
order = {"insitu": 0, "extrap": 1}
rows.sort(key=lambda x: (order[x["cond"].split("/")[2]], x["pmed"], x["key"]))
data = {"rows": rows, "pred": res["predictions"],
        "between": {"S": round(res["S"]["between_share"], 3), "F": round(res["F"]["between_share"], 3)},
        "mae": {"S": round(res["S"]["mae_f1"], 3), "F": round(res["F"]["mae_f1"], 3)},
        "onstep": round(res["F"]["F_p50_on_step_share"], 3), "mult5": round(res["F"]["F_mult5_share"], 3)}
(HERE / "face-data.js").write_text("window.FACE = " + json.dumps(data, separators=(",", ":")) + ";\n")
print(len(rows), "rows")
