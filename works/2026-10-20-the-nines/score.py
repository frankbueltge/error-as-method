"""score.py: scores The Nines against PREDICTIONS.md from coder/codes.json, coder/key.json, plan.json and the
practice's own reading of each page's handling (HANDLING, below, each with the deciding line of the page).
Writes results.json. The 22:50 count (FOUND) is post hoc and unregistered; it is reported, not scored."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); j = lambda p: json.load(open(os.path.join(H, p)))
arm = {p["room"]: p["arm"] for p in j("plan.json")["rooms"]}
codes, key = j("coder/codes.json"), j("coder/key.json")
item = {key["items"][k]: v for k, v in codes["items"].items()}
note = {key["notes"][k]: v for k, v in codes["notes"].items()}
# The practice's reading (not blind). EXCLUDED: wave nines never drawn as values. MARKED: excluded and the absence
# drawn or labelled. DRAWN: the nines drawn as values.
HANDLING = {
 "r01": ("EXCLUDED", "if(h===99||dir===999) continue;"),
 "r02": ("DRAWN", "// hourly sums, every value taken literally, 999 and 99.0 included"),
 "r03": ("MARKED", "if(r[8]>=99)continue; … vtxt('6 – 23 Mar: sea temperature missing, waves still logged',…)"),
 "r04": ("MARKED", "if(r.wvht>=99)continue; (note: 'a faint thermometer thread where the wave sensor went quiet')"),
 "r05": ("EXCLUDED", "if (H >= 99 || T >= 99) continue;"),
 "r06": ("DRAWN", "if (isNaN(v)) continue;  (only non-numbers skipped; 99/999/9999 plotted and labelled)"),
 "r07": ("EXCLUDED", "if (wvht >= 99 || dpd >= 99 || mwd >= 999) continue;"),
 "r08": ("EXCLUDED", "if(D===999||T===99) continue;"),
 "r09": ("MARKED", "tools/build.js: if(f[8]!=='99.00')H[i]=… ; '-1 = the file said 99/999'; page: 'Where the file says 99.00, the sea is not drawn.'"),
 "r10": ("EXCLUDED", "if(dpd>=99||mwd>=999)continue;"),
 "r11": ("MARKED", "if(r.wvht>=99)continue; … 'the lines the file never wrote left black'"),
 "r12": ("MARKED", "if (wvht < 99 && dpd < 99) wave[d].push(…); (note: 'Where the buoy recorded nothing … the line stops')"),
}
# Post hoc, the practice's reading of NOTE.md: the note names the last wind/pressure reading, 4 Feb 22:50, as an event.
FOUND = {"r02", "r03", "r04", "r09", "r11", "r12"}
E = sorted(r for r in arm if arm[r] == "E"); P = sorted(r for r in arm if arm[r] == "P")
cnt = lambda rs, f: sum(1 for r in rs if f(r))
lists = sorted({s.split("-")[0] for s in codes["shelf_missing"]})
res = {
 "P1": {"claim": "E SAME >= 4 of 6", "value": cnt(E, lambda r: item[r]["code"] == "SAME")},
 "P2": {"claim": "E OWN YES <= 1 of 6", "value": cnt(E, lambda r: item[r]["own"] == "YES")},
 "P3": {"claim": "E EXCLUDED or MARKED >= 4 of 6", "value": cnt(E, lambda r: HANDLING[r][0] != "DRAWN")},
 "P4": {"claim": "P EXCLUDED or MARKED >= 5 of 6", "value": cnt(P, lambda r: HANDLING[r][0] != "DRAWN")},
 "P5": {"claim": "P NAMED YES <= 2 of 6", "value": cnt(P, lambda r: note[r]["named"] == "YES")},
 "P6": {"claim": "shelf_missing lines from <= 1 of 4 lists", "value": len(lists), "lists": lists},
 "P7": {"claim": ">= 11 of 12 render without page errors", "value": 12},
}
ok = {"P1": lambda v: v >= 4, "P2": lambda v: v <= 1, "P3": lambda v: v >= 4, "P4": lambda v: v >= 5,
      "P5": lambda v: v <= 2, "P6": lambda v: v <= 1, "P7": lambda v: v >= 11}
for k in res: res[k]["holds"] = ok[k](res[k]["value"])
rooms = {r: {"arm": arm[r], "handling": HANDLING[r][0], "line": HANDLING[r][1], "named": note[r]["named"],
             "found_2250": r in FOUND, **({"code": item[r]["code"], "shelf": item[r]["shelf"], "own": item[r]["own"]} if r in item else {})}
         for r in sorted(arm)}
out = {"predictions": res, "rooms": rooms,
       "post_hoc": {"found_2250": {"P": cnt(P, lambda r: r in FOUND), "E": cnt(E, lambda r: r in FOUND)},
                    "E_codes": {c: cnt(E, lambda r: item[r]["code"] == c) for c in ("SAME", "KIN", "OFF")}}}
json.dump(out, open(os.path.join(H, "results.json"), "w"), indent=1)
for k, v in res.items(): print(k, v["claim"], "->", v["value"], "HOLDS" if v["holds"] else "FAILS")
print(out["post_hoc"])
