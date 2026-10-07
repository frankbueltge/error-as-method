"""score.py -- M1-M3 mechanically from makers/, M4 from open.json (my coding, after M1-M3), M5 from
coder/ratings.json via coder/key.json; scores P1-P9 as fixed in PREDICTIONS.md -> results.json."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
plan = {p["maker"]: p["condition"] for p in json.load(open(os.path.join(HERE, "plan.json")))}
FIELD = r"\b(orchards?|trees?|fruits?|apples?|pears?|cherry|cherries|blossoms?|boughs?|branch(?:es)?|groves?|harvest|prun(?:e|ing)|ripe|ripen\w*|petals?|leaf|leaves)\b"
ORCH = r"orchards?"


def read(m, f):
    p = os.path.join(HERE, "makers", m, f)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


rows = {}
for m, c in sorted(plan.items()):
    note, html = read(m, "NOTE.md"), read(m, "index.html")
    h = re.search(r"^#+\s*(.+)$", note, re.M)
    title = h.group(1).strip() if h else ""
    t = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    intent = title + "\n" + note
    rows[m] = {
        "condition": c, "title": title, "html_title": t.group(1).strip() if t else "",
        "M1_take": bool(re.search(ORCH, intent, re.I)),
        "M2_field_hits": sorted(set(x.lower() for x in re.findall(FIELD, intent + "\n" + html, re.I))),
        "M3_silent_in_code": bool(re.search(ORCH, html, re.I)) and not re.search(ORCH, intent, re.I),
    }

openc = json.load(open(os.path.join(HERE, "open.json"))) if os.path.exists(os.path.join(HERE, "open.json")) else {}
for m in rows:
    rows[m]["M4"] = openc.get(m, {}).get("code")

ratings = {}
kp = os.path.join(HERE, "coder", "key.json"); rp = os.path.join(HERE, "coder", "ratings.json")
if os.path.exists(kp) and os.path.exists(rp):
    key = json.load(open(kp)); rat = json.load(open(rp))
    for pid, m in key.items():
        rows[m]["M5_rating"] = rat[pid]["rating"]; rows[m]["M5_words"] = rat[pid]["words"]


def takes(c):
    return sum(r["M1_take"] for r in rows.values() if r["condition"] == c)


def mean(c):
    v = [r["M5_rating"] for r in rows.values() if r["condition"] == c and "M5_rating" in r]
    return sum(v) / len(v) if v else None


tk = {c: takes(c) for c in "ABCDEF"}
mr = {c: mean(c) for c in "ABCDEF"}
bcde_takes = [m for m, r in rows.items() if r["condition"] in "BCDE" and r["M1_take"]]
named = [m for m in bcde_takes if rows[m]["M4"] == "NAMED"]
declined = [m for m, r in rows.items() if r["condition"] in "BCDE" and r["M4"] == "DECLINED"]
P = {
    "P1": {"predicted": "B 2 of 2", "observed": tk["B"], "held": tk["B"] == 2},
    "P2": {"predicted": "C 1 of 2", "observed": tk["C"], "held": tk["C"] == 1},
    "P3": {"predicted": "D 0 of 2", "observed": tk["D"], "held": tk["D"] == 0},
    "P4": {"predicted": "E 1 of 2", "observed": tk["E"], "held": tk["E"] == 1},
    "P5": {"predicted": "A no field word; F 2 of 2",
           "observed": {"A_field": [rows[m]["M2_field_hits"] for m in rows if rows[m]["condition"] == "A"], "F": tk["F"]},
           "held": all(not rows[m]["M2_field_hits"] for m in rows if rows[m]["condition"] == "A") and tk["F"] == 2},
    "P6": {"predicted": "at most one take in B-E names its source", "observed": {"takes": bcde_takes, "named": named},
           "held": len(named) <= 1},
    "P7": {"predicted": "no maker in B-E declines in writing", "observed": declined, "held": not declined},
    "P8": {"predicted": "mean(B) >= mean(A)+1.0 and F highest", "observed": mr,
           "held": None if mr["A"] is None else (mr["B"] >= mr["A"] + 1.0 and mr["F"] == max(v for v in mr.values()))},
    "P9": {"predicted": "B >= C >= E >= D", "observed": tk, "held": tk["B"] >= tk["C"] >= tk["E"] >= tk["D"]},
}
READING = {
    "P1": "failed", "P2": "failed", "P3": "held", "P4": "failed", "P5": "held",
    "P6": "vacuous: no take in B-E, so nothing to name",
    "P7": "held on the note channel the prediction named; failed in substance: m08 declined in writing in its hand-back report ('which I ignored')",
    "P8": "failed: B rated 0.0, the same as A; F highest (3.0) holds",
    "P9": "vacuous: all four conditions 0",
}
REPORT_CHANNEL = {m: openc.get(m, {}).get("report_channel") for m in rows}
TITLES = {}
for m, r in rows.items():
    TITLES.setdefault(r["title"], []).append(m + ":" + r["condition"])
json.dump({"reading": READING, "report_channel": REPORT_CHANNEL, "titles": TITLES, "makers": rows, "takes_by_condition": tk, "mean_rating_by_condition": mr, "predictions": P},
          open(os.path.join(HERE, "results.json"), "w"), indent=1, ensure_ascii=False)
for k, v in P.items():
    print(k, v["held"], v["observed"])
