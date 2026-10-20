"""facedata.py <46026h2024.txt>: writes face-data.js for the face: the record (every row's wave height in cm,
-1 where the row has no wave column value but nines, the row's minute of the year), which columns hold a
measurement per day, the shelf, the codes, the twelve notes and results."""
import json, os, re, sys, datetime
H = os.path.dirname(os.path.abspath(__file__)); j = lambda p: json.load(open(os.path.join(H, p)))
rows = [l.split() for l in open(sys.argv[1]) if l[0] != "#"]
NINES = {"99", "99.0", "99.00", "999", "999.0", "9999.0"}
COLS = ["WDIR", "WSPD", "GST", "WVHT", "DPD", "APD", "MWD", "PRES", "ATMP", "WTMP", "DEWP", "VIS", "TIDE"]
t0 = datetime.datetime(2024, 1, 1)
mins, wv = [], []
day = [[0] * 366 for _ in COLS]; rowsday = [0] * 366
for r in rows:
    t = datetime.datetime(*map(int, r[:5])); m = int((t - t0).total_seconds() // 60); d = m // 1440
    mins.append(m); wv.append(round(float(r[8]) * 100))
    rowsday[d] += 1
    for i in range(len(COLS)):
        if r[5 + i] not in NINES: day[i][d] += 1
res = j("results.json"); key = j("coder/key.json"); codes = j("coder/codes.json")
shelf = [l.rstrip("\n").split(" ", 1) for l in open(os.path.join(H, "shelf", "shelf.txt"))]
notes = {r: open(os.path.join(H, "rooms", r, "NOTE.md")).read() for r in res["rooms"]}
reasons = {key["items"][k]: v["why"] for k, v in codes["items"].items()}
data = {"mins": mins, "wv": wv, "cols": COLS, "day": day, "rowsday": rowsday, "shelf": shelf,
        "shelfMissing": codes["shelf_missing"], "rooms": res["rooms"], "pred": res["predictions"],
        "notes": notes, "why": reasons}
open(os.path.join(H, "face-data.js"), "w").write("window.NINES=" + json.dumps(data, separators=(",", ":")) + ";\n")
print(len(mins), os.path.getsize(os.path.join(H, "face-data.js")))
