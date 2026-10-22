"""facedata.py: writes face-data.js for index.html from the rooms, the shelves, results.json and the
material names below (the practice's short labels; the makers' own words are quoted from their files)."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); J = lambda p: json.load(open(os.path.join(H, p)))
res = J("results.json"); plan = J("plan.json"); desc = J("coder/describe.json")
skey = {v: k for k, v in J("coder/shelf-key.json").items()}; keyA = {v: k for k, v in J("coder/key.json").items()}
A = {c["id"]: c for c in J("coder/codes-A.json")}
LABEL = {"r01": "New York 311 noise complaints, per day", "r02": "Diameters of 139,688 asteroids (JPL)",
 "r03": "Defra payments over £25,000, 2025", "r04": "Measles in Cambridge, fortnightly, 1944–66",
 "r05": "US weekly price of gasoline, 1990–2026", "r06": "Billboard Hot 100 issue dates, 1958–2026",
 "r07": "Prices paid for houses, England and Wales", "r08": "Billboard Hot 100 chart weeks, 1958–2026",
 "r09": "Curiosity rover weather reports, by Earth date", "r10": "Lake Michigan-Huron water level, monthly, 1918–2026",
 "r11": "Publication dates of every xkcd comic", "r12": "Diameters of 139,688 asteroids (JPL)",
 "r13": "New York 311 residential noise, per hour", "r14": "US influenza-like illness, weekly, 2002–26",
 "r15": "Bank of England Bank Rate, monthly, 1694–2026", "r16": "Days of ice on Lake Mendota, 1852–2026"}
WHAT = {"PLOT": "Draws one column as a line, in file order. The neutral control.",
        "CYCLES": "A periodogram: how strongly every period recurs in evenly spaced values.",
        "GAPS": "Finds where a record breaks its own most common interval.",
        "DIGITS": "Sets a column's first digits beside Benford's law."}
NAME = {"P": "PLOT", "C": "CYCLES", "G": "GAPS", "D": "DIGITS"}
def sec(text, head):
    m = re.split(r"^#+\s*%s\s*$" % head, text, flags=re.M | re.I)
    return m[1].split("\n#")[0].strip() if len(m) > 1 else ""
def lines(s): return [re.sub(r"^\s*\d+\.\s*", "", l).strip() for l in s.splitlines() if re.match(r"^\s*\d+\.", l)]
def showed(n):
    parts = re.split(r"^#{2,3}\s+.*$", n, flags=re.M)
    t = " ".join(parts[-1].split()) if len(parts) > 1 else " ".join(n.split()[-160:])
    return t if len(t) <= 1400 else t[:1400].rsplit(" ", 1)[0] + " […]"
arms = []
for a in ["PLOT", "CYCLES", "GAPS", "DIGITS"]:
    rooms = [r["room"] for r in plan["rooms"] if NAME[r["arm"]] == a]
    hits = set()
    cards = []
    for r in rooms:
        c = open(os.path.join(H, "rooms", r, "CHOICE.md")).read(); n = open(os.path.join(H, "rooms", r, "NOTE.md")).read()
        code = A[keyA[r]][skey[a]]; own = code["code"]
        if code["line"]: hits.add(code["line"])
        paras = [p.strip() for p in re.split(r"\n\s*\n", n) if p.strip() and not p.strip().startswith(("#", "-", "*", "|", "`"))]
        cards.append({"room": r, "material": LABEL[r], "own": own,
                      "ownLabel": {"SAME": "on its shelf", "KIN": "kin on its shelf", "OFF": "off its shelf"}[own],
                      "met": res["rooms"][r]["met"].replace("_", " ").lower(), "first": lines(sec(c, "First to mind")),
                      "expected": " ".join(sec(c, "Expected").split()), "showed": showed(n),
                      "url": re.search(r"https?://\S+", desc[r]).group(0)})
    shelf = [l.strip() for l in open(os.path.join(H, "coder", skey[a] + ".txt")) if l.strip()]
    arms.append({"name": a.replace("DIGITS", "FIRST DIGITS"), "what": WHAT[a], "rooms": cards, "shelf": [{"line": l, "hit": l in hits} for l in shelf]})
P = res
text = open(os.path.join(H, "face-text.html")).read()
open(os.path.join(H, "face-data.js"), "w").write("window.FACE = " + json.dumps({"arms": arms, "text": text}, ensure_ascii=False, indent=0) + ";\n")
print("ok", [(a["name"], sum(s["hit"] for s in a["shelf"])) for a in arms])
