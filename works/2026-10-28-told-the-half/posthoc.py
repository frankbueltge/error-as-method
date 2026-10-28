"""POST-HOC, written after results.json was read (Session 160). Not a prediction; nothing here decides a row.

1. The shape of the half: on the diverging keys, how many shifts s are (about) none (s <= 0.1), whole (s >= 0.9),
   or between? Tonight's P and T, and experiment 40's P re-read from its committed results.json (read only; that
   night's record is not changed).
2. Where the describers stayed: of the keys with s <= 0.1, on how many is the people's median the scale's neutral
   point (4 of 1-7 tonight, 5 of 1-9 in experiment 40)? Against the same count on the keys with s >= 0.9.
3. What the doubling did, by kind of key: X's error against P's where s was none, between, whole.
4. Who read the told note which way: each T maker's HOW line, printed for hand coding.
"""
import json, statistics as st
from pathlib import Path
HERE = Path(__file__).parent
r = json.loads((HERE / "results.json").read_text())
D = [k for k in r["rows"] if k["diverges"]]

def shape(s):
    return {"none (<=0.1)": sum(x <= 0.1 for x in s), "between": sum(0.1 < x < 0.9 for x in s),
            "whole (>=0.9)": sum(x >= 0.9 for x in s), "n": len(s), "mean": round(st.mean(s), 3)}

out = {"tonight_P": shape([k["s_P"] for k in D]), "tonight_T": shape([k["s_T"] for k in D])}

prev = json.loads((HERE.parent / "2026-10-26-without-a-tongue" / "results.json").read_text())["keys"]
pd = [k for k in prev if abs(k["median"]["A"] - k["median"]["people"]) >= 0.5]
ps = [(k["median"]["P"] - k["median"]["A"]) / (k["median"]["people"] - k["median"]["A"]) for k in pd]
out["experiment40_P"] = shape(ps)

def at_mid(keys, s, mid):
    none = [k for k, x in zip(keys, s) if x <= 0.1]; whole = [k for k, x in zip(keys, s) if x >= 0.9]
    return {"none_at_midpoint": f"{sum(k == mid for k in [kk for kk in none])} of {len(none)}",
            "whole_at_midpoint": f"{sum(k == mid for k in [kk for kk in whole])} of {len(whole)}"}

out["midpoint_tonight"] = at_mid([k["people_q"][2] for k in D], [k["s_P"] for k in D], 4.0)
out["midpoint_experiment40"] = at_mid([k["median"]["people"] for k in pd], ps, 5.0)
out["stayed_tonight"] = [k["phrase"] for k in D if k["s_P"] <= 0.1]
out["whole_tonight"] = [k["phrase"] for k in D if k["s_P"] >= 0.9]

def errs(sel):
    ks = [k for k in D if sel(k["s_P"])]
    return {"n": len(ks), "err_P": round(st.mean(k["err_P"] for k in ks), 3) if ks else None,
            "err_X": round(st.mean(k["err_X"] for k in ks), 3) if ks else None}
out["doubling_by_kind"] = {"none": errs(lambda x: x <= 0.1), "between": errs(lambda x: 0.1 < x < 0.9),
                           "whole": errs(lambda x: x >= 0.9)}
out["T_how"] = {m: v for m, v in r["summary"]["how"].items() if m[0] == "T"}
(HERE / "posthoc.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
print(json.dumps(out, indent=1, ensure_ascii=False))
