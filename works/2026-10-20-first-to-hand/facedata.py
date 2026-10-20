"""facedata.py: builds face-data.js from the shelf, the rooms' CHOICE.md, NOTE.md titles, the blind codes and plan.json.
The mapping of first-to-mind lines and choices to items (FIRST, CHOSEN) is the practice's reading, written by hand."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); J = lambda p: json.load(open(os.path.join(H, p)))
groups = J("shelf/groups.json"); res = J("results.json"); plan = J("plan.json")
def short(line):
    m = re.match(r"(.*?)\s+—\s+(.*?)\s*\(", line); return (m.group(2) if m else line).strip(), (m.group(1) if m else "")
shelf = []
for g in groups:
    ds, pub = short(g["lines"][0]); shelf.append({"key": g["key"], "label": ds, "pub": pub, "n": g["n"]})
OFF_SHELF = [{"key": "meteorites", "label": "Meteorite landings", "pub": "Meteoritical Society / NASA"},
             {"key": "oldfaithful", "label": "Old Faithful eruptions", "pub": "(GeyserTimes)"},
             {"key": "lakeice", "label": "Lake ice-on / ice-off dates", "pub": "(Lake Mendota)"},
             {"key": "shiplogs", "label": "Ship logbook weather (CLIWOC)", "pub": "CLIWOC"},
             {"key": "kyoto", "label": "Kyoto cherry full-bloom dates", "pub": "Aono and Katata (via Our World in Data)"}]
# first to mind, slot by slot, as each CHOICE.md lists them (the practice's mapping to keys)
FIRST = {"r01": ["usgs-eq", "maunaloa", "volcano"], "r02": ["maunaloa", "usgs-eq", "silso"], "r03": ["usgs-eq", "maunaloa", "silso"],
         "r04": ["maunaloa", "usgs-eq", "silso"], "r05": ["maunaloa", "usgs-eq", "silso"], "r06": ["osm", "silso", "oldfaithful"],
         "r07": ["silso", "shiplogs", "osm"], "r08": ["silso", "oldfaithful", "lakeice"], "r09": ["maunaloa", "usgs-eq", "meteorites"],
         "r10": ["volcano", "silso", "lakeice"], "r11": ["silso", "oldfaithful", "lakeice"], "r12": ["oldfaithful", "silso", "lakeice"]}
# the item each room chose; r06 and r07 both chose lighthouse lights (r06 from NGA, after OSM's servers failed)
CHOSEN = {"r01": "maunaloa", "r02": "silso", "r03": "silso", "r04": "silso", "r05": "silso", "r06": "lights", "r07": "lights",
          "r08": "oldfaithful", "r09": "kyoto", "r10": "silso", "r11": "oldfaithful", "r12": "oldfaithful"}
rooms = []
for p in plan["rooms"]:
    r = p["room"]; d = os.path.join(H, "rooms", r)
    title = open(os.path.join(d, "NOTE.md")).readline().lstrip("# ").strip()
    rooms.append({"room": r, "arm": p["arm"], "title": title, "first": FIRST[r], "chosen": CHOSEN[r],
                  "code": res["rooms"][r]["code"], "shelf_line": res["rooms"][r]["shelf_line"], "domain": res["rooms"][r]["domain"],
                  "choice": open(os.path.join(d, "CHOICE.md")).read(), "note": open(os.path.join(d, "NOTE.md")).read()})
line = [{"id": k, "code": v["code"], "domain": v["domain"]} for k, v in sorted(res["line"].items())]
out = {"shelf": shelf, "offshelf": OFF_SHELF, "rooms": rooms, "line": line,
       "scores": {k: res[k] for k in ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]}}
open(os.path.join(H, "face-data.js"), "w").write("window.FTH = " + json.dumps(out, ensure_ascii=False) + ";\n")
print(len(shelf), "shelf;", len(rooms), "rooms;", os.path.getsize(os.path.join(H, "face-data.js")), "bytes")
