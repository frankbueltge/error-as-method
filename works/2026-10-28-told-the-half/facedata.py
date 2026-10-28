"""Session 160: write face-data.js for index.html from results.json and the T rooms' HOW lines (no new numbers)."""
import json
from pathlib import Path
HERE = Path(__file__).parent
r = json.loads((HERE / "results.json").read_text())
rows = []
for k in r["rows"]:
    rows.append({"p": k["phrase"], "f": k["foundation"].split("/")[0], "n": k["n_people"],
                 "ppl": k["people_q"][2], "pq": [k["people_q"][1], k["people_q"][3]], "A": k["A"], "a": k["A_q"][2],
                 "P": k["P_p50s"], "T": k["T_p50s"], "d": k["diverges"]})
out = {"rows": rows, "how": {m: v for m, v in r["summary"]["how"].items() if m[0] == "T"},
       "sP": r["summary"]["HALFWAY_mean_s_P"], "sT": r["summary"]["mean_s_T"]}
(HERE / "face-data.js").write_text("window.FACE = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n")
print(len(rows), "rows")
