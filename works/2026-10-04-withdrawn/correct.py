"""Post-hoc correction, Session 104, written AFTER results.json was seen. Not a verdict.
code.py removed stop-words before punctuation, so 'withdrawn.' (with a full stop) survived and a
notice reading 'This paper has been withdrawn.' was coded as giving a reason (hand row 11).
PREDICTIONS.md lists both removals without an order; the intent was plainly to strip both.
This file strips punctuation first, then stop-words, and reports both runs side by side."""
import json, re
import code as pre
def bare2(comment):
    c = re.sub(r"[\W\d_]+", " ", comment.lower())
    return int(all(w in pre.STOP for w in c.split()))
rows = json.load(open("notices.json"))
coded = {c["id"]: c for c in json.load(open("coded.json"))}
for r in rows:
    coded[r["id"]]["bare_corrected"] = bare2(r["comment"])
N = list(coded.values())
b2 = sum(c["bare_corrected"] for c in N)
nb2 = [c for c in N if not c["bare_corrected"]]
hand = json.load(open("hand.json"))
agree = sum(coded[h["id"]]["bare_corrected"] == h["bare"] for h in hand)
out = {"status": "post hoc; written after results.json; not a verdict on P1 or P4",
       "bare_corrected": b2, "bare_corrected_pct": round(100 * b2 / len(N), 2),
       "error_pct_of_not_bare_corrected": round(100 * sum(c["error"] for c in nb2) / len(nb2), 2),
       "other_pct_of_not_bare_corrected": round(100 * sum(c["other"] for c in nb2) / len(nb2), 2),
       "hand_agreement_bare_corrected_of_60": agree,
       "disagreeing_rows": [h["n"] for h in hand if coded[h["id"]]["bare_corrected"] != h["bare"]]}
json.dump(list(coded.values()), open("coded.json", "w"), indent=0)
json.dump(out, open("correction.json", "w"), indent=1)
print(json.dumps(out, indent=1))
