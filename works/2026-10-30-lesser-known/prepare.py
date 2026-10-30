"""Session 164, experiment 44 (Lesser Known): draw the keys, derive the people's values, write the briefs.

Source: Chang, Stagnitto, Hinojosa, Johns & Gatti (2026), "Norming Truthfulness Ratings for True and False Trivia
Statements across English, Spanish and Italian", preprint (CC BY 4.0) https://osf.io/eqmx8 ; data and stimuli at
https://osf.io/dqu2g/ (no licence stated on the project). The raw file is NOT committed; sources/MANIFEST.json holds
its URL and SHA-256. Run: python3 prepare.py <path to IT_ES_EN_data_final.RData>

The English sample only: 60 adults in the US or Canada (Prolific), each rating one of two sets of 100 statements
(50 true, 50 false) on 1 = definitely false ... 6 = definitely true, at most 12 s each. Each of the 200 statements
was rated by 29 to 31 people. A pair is a true statement and its false version (one detail changed); each person saw
one version of each pair. A key is one statement. 60 keys are drawn by seed 164 from 60 distinct pairs, 30 true and
30 false, so that no maker sees both versions of a pair, as no participant did.

Writes plan.json (keys, orders, M anchors), people.json (the people's values per key, as a histogram), briefs/A*,
D*, M*. The U briefs are written by anchors_u.py after arm A is committed.
"""
import json, random, statistics as st, sys
from pathlib import Path
import pyreadr

HERE = Path(__file__).parent
SEED = 164
R = pyreadr.read_r(sys.argv[1])
en = R["EN"].dropna(subset=["rating"])
PAIR = {int(a): int(b) for a, b in zip(R["EN_items"]["ID_sentence"], R["EN_items"]["ID_paired"])}
assert en["Participant"].nunique() == 60 and len(en) == 6000

items = {}
for (sid, item, cat), g in en.groupby(["ID_sentence", "Item", "category"]):
    items[int(sid)] = {"text": item.strip(), "true": bool(cat), "ratings": sorted(int(x) for x in g["rating"])}
assert len(items) == 200
pairs = {}
for sid, x in items.items():
    pairs.setdefault(PAIR[sid], []).append(sid)
assert all(len(v) == 2 and items[min(v)]["true"] != items[max(v)]["true"] for v in pairs.values()), "pairing"

def q(v, p):
    return float(st.quantiles(v, n=100, method="inclusive")[p - 1])

rng = random.Random(SEED)
chosen_pairs = sorted(rng.sample(sorted(pairs), 60))
truth = [True] * 30 + [False] * 30
rng.shuffle(truth)
K, P = [], {}
for i, (pk, t) in enumerate(zip(chosen_pairs, truth)):
    sid = [s for s in pairs[pk] if items[s]["true"] == t][0]
    v = items[sid]["ratings"]
    kid = f"k{i+1:02d}"
    K.append({"id": kid, "text": items[sid]["text"], "true": t, "osf_sentence_id": sid})
    P[kid] = {"n": len(v), "median": st.median(v), "mean": round(st.mean(v), 3), "p25": q(v, 25), "p75": q(v, 75),
              "hist": [v.count(s) for s in range(1, 7)], "true": t}

# M anchors (fixed before any maker runs): the true key and the false key whose people's mean is nearest the mean of
# all 60 keys' people's means; ties by key id.
grand = st.mean(P[k["id"]]["mean"] for k in K)
def nearest(t):
    c = [k["id"] for k in K if k["true"] == t]
    return min(c, key=lambda k: (abs(P[k]["mean"] - grand), k))
M_ANCH = [nearest(True), nearest(False)]

orders = {}
for arm in "ADMU":
    for j in range(1, 7):
        mid = f"{arm}{j}"
        ids = [k["id"] for k in K]
        random.Random(f"{SEED}-{mid}").shuffle(ids)
        orders[mid] = ids

TEXT = {k["id"]: k["text"] for k in K}
CONTEXT = ("Below are {n} statements about lesser-known historical facts. Some of them are true, and some are false.")
STUDY = ("In an online norming study, 60 adults in the United States or Canada whose first language is English "
         "(recruited through the Prolific platform, average age about 27) each read 100 statements of this kind, one at "
         "a time, with at most 12 seconds for each, and rated to what extent they believed each statement was true, on "
         "a scale from 1 (definitely false) to 6 (definitely true), with a whole number. Each statement below was "
         "rated by about 30 of them (29 to 31).")
NOTOOLS = "Do not use any tool, program, file, search or lookup of any kind. Answer from what you have here."
DESCRIBE = ("For each statement, do not rate it yourself. State how those people's ratings were spread, on their own "
            "1 to 6 scale: give the 25th, 50th and 75th percentile of their ratings, and their mean rating (decimals "
            "allowed).")
RET_D = ("Hand back your answer in exactly this form and nothing else:\nSPREADS\n"
         "1: p25=_ p50=_ p75=_ mean=_\n(one line for each numbered statement, in the order given)\n"
         "KNOWN: yes, no or partly - do you know this study, its data or its results? One sentence.\n"
         "HOW: one to three sentences on how you arrived at the numbers.")
RET_A = ("Hand back your answer in exactly this form and nothing else:\nRATINGS\n1: _\n(one line for each numbered "
         "statement, in the order given, a whole number from 1 to 6)\nHOW: one to three sentences on how you rated.")

def anchor_block(ids):
    lines = ["Two of the statements are given here with the people's actual results, so that you know where this "
             "group stood on them. They are not in the list below."]
    for a in ids:
        p = P[a]
        lines.append(f"- \"{TEXT[a]}\" 25th percentile {p['p25']:g}, median {p['median']:g}, 75th percentile {p['p75']:g}")
    return "\n".join(lines)

def listing(ids):
    return "\n".join(f"{i+1}: {TEXT[k]}" for i, k in enumerate(ids))

def brief(mid, anchors=None):
    arm = mid[0]
    ids = [k for k in orders[mid] if not anchors or k not in anchors]
    if arm == "A":
        body = [CONTEXT.format(n=len(ids)),
                "For each statement, rate to what extent you believe it is true, on a scale from 1 (definitely false) "
                "to 6 (definitely true), with a whole number. Answer as yourself, from what you know.",
                NOTOOLS, listing(ids), RET_A]
    else:
        body = [CONTEXT.format(n=len(ids)), STUDY, DESCRIBE]
        if anchors:
            body.append(anchor_block(anchors))
        body += [NOTOOLS, listing(ids), RET_D]
    return "\n\n".join(body) + "\n", ids

if __name__ == "__main__":
    shown = {}
    for arm, anch in (("A", None), ("D", None), ("M", M_ANCH)):
        for j in range(1, 7):
            mid = f"{arm}{j}"
            text, ids = brief(mid, anch)
            (HERE / "briefs" / f"{mid}.txt").write_text(text)
            shown[mid] = ids
    json.dump({"seed": SEED, "keys": K, "orders": orders, "shown": shown, "M_anchors": M_ANCH,
               "grand_mean_of_people_means": round(grand, 3)}, open(HERE / "plan.json", "w"), indent=1,
              ensure_ascii=False)
    json.dump(P, open(HERE / "people.json", "w"), indent=1)
    print("keys", len(K), "true", sum(k["true"] for k in K), "M anchors", M_ANCH,
          [(P[a]["median"], P[a]["mean"]) for a in M_ANCH], "grand", round(grand, 3))
