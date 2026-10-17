"""score.py: scores experiment 23 (Told Where) against PREDICTIONS.md from coder H's and coder D's answers.
Rules as fixed in PREDICTIONS.md: a maker MENTIONS THE PLACE if coder H lists a `where` claim naming Fort Peck, Montana,
the USA, the Great Plains or 634 m, or if its NOTE.md does; it HOLDS THE PLACE APART if such a claim has standing `given`
or `against`; it HOLDS THE KIND APART if a `what` claim on sunlight or solar radiation has standing `given` or `against`;
it FAVOURS LIGHT if its favoured `what` claim names sunlight, sun, solar radiation, irradiance or daylight.
Coder D's pages p01-p24 map to makers by random.Random(1330).shuffle of m01..m24. Writes results.json."""
import json, os, re, random
H = os.path.dirname(os.path.abspath(__file__))
J = lambda *p: json.load(open(os.path.join(H, *p)))
plan = {p["maker"]: p["cell"] for p in J("plan.json")["makers"]}
A = J("coder", "H", "answers.json"); D = J("coder", "D", "answers.json")
PLACE = re.compile(r"fort\s*peck|montana|u\.?s\.?a\b|united states|great plains|\b634\b", re.I)
LIGHT = re.compile(r"sun|solar|irradian|daylight|light|radiation|insolation", re.I)
order = ["m%02d" % i for i in range(1, 25)]; sh = order[:]; random.Random(1330).shuffle(sh)
page = {m: "p%02d" % (i + 1) for i, m in enumerate(sh)}
per = {}
for m in order:
    cl = A[m]["claims"]; note = open(os.path.join(H, "makers", m, "NOTE.md"), encoding="utf-8").read()
    wh = [c for c in cl if c["topic"] == "where" and PLACE.search(c["claim"] + " " + " ".join(q["text"] for q in c["quotes"]))]
    kd = [c for c in cl if c["topic"] == "what" and LIGHT.search(c["claim"])]
    fav = [c for c in cl if c["topic"] == "what" and c["favoured"] == "yes"]
    d = D[page[m]]
    per[m] = {"cell": plan[m], "page": page[m],
              "favours_light": any(LIGHT.search(c["claim"]) for c in fav), "favoured_what": [c["claim"] for c in fav],
              "mentions_place": bool(wh) or bool(PLACE.search(note)), "place_in_note": bool(PLACE.search(note)),
              "place_standing": [c["standing"] for c in wh], "holds_place_apart": any(c["standing"] in ("given", "against") for c in wh),
              "kind_standing": [c["standing"] for c in kd], "holds_kind_apart": any(c["standing"] in ("given", "against") for c in kd),
              "page_light": "light" in d["K1_cats"], "page_place": d["L1"] == "yes", "page_given": d["L2"] == "yes",
              "page_title": d["K4"], "page_place_quote": d.get("L1_quote", ""), "page_given_quote": d.get("L2_quote", "")}
cells = {c: [m for m in order if plan[m] == c] for c in ("N", "K", "P", "KP")}
n = lambda c, k: sum(per[m][k] for m in cells[c])
P_mention = [m for m in cells["P"] if per[m]["mentions_place"]]
P_apart = [m for m in P_mention if per[m]["holds_place_apart"]]
KP_split = [m for m in cells["KP"] if per[m]["holds_place_apart"] and not per[m]["holds_kind_apart"]]
counts = {c: {k: n(c, k) for k in ("favours_light", "mentions_place", "holds_place_apart", "holds_kind_apart", "page_light", "page_place", "page_given")} for c in cells}
void = len(P_mention) < 4
a = (not void) and len(P_apart) < 3; b = n("K", "holds_kind_apart") >= 3
row = {"void": void, "P_mentioning": len(P_mention), "P_holding_place_apart": len(P_apart), "K_holding_kind_apart": n("K", "holds_kind_apart"),
       "clause_a_fires": a, "clause_b_fires": b, "verdict": "void" if void else ("falsified" + (" by (a)" if a else "") + (" and (b)" if a and b else (" by (b)" if b else "")) if (a or b) else "held")}
pg = sum(per[m]["page_given"] for m in order)
preds = {"P1": n("N", "favours_light") >= 4, "P2": n("K", "favours_light") == 6, "P3": n("K", "holds_kind_apart") <= 2,
         "P4": len(P_mention) >= 4, "P5": len(P_apart) >= 3, "P6": len(KP_split) >= 3,
         "P7": n("P", "favours_light") >= 4 and abs(n("P", "favours_light") - n("N", "favours_light")) <= 1,
         "P8": n("P", "page_place") >= 4 and n("KP", "page_place") >= 4 and n("N", "page_place") + n("K", "page_place") == 0,
         "P9": pg <= 2}
out = {"cells": cells, "per_maker": per, "counts": counts, "S132.CHECKABLE": row, "KP_place_apart_kind_not": KP_split,
       "pages_marking_given": pg, "predictions": preds, "predictions_held": "%d of %d" % (sum(preds.values()), len(preds))}
json.dump(out, open(os.path.join(H, "results.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({"counts": counts, "row": row, "KP_split": KP_split, "preds": preds}, indent=1))
