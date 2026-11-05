"""Session 170 (experiment 48, Laughed Off): keys, contact sets and the stage-1 and stage-2 briefs.

Reads Silvia & Bui's dad-joke ratings (https://osf.io/vnw2p, CC BY-NC 4.0) from a download directory holding the joke-level
and person-level CSV files, checks their SHA-256 against sources/MANIFEST.json, and writes:
  people.json   per key used tonight: the joke's text, its survey position, its number of raters, and the mean of their 1-5
                funniness ratings (the authors' funny_joke_5mean, re-computed here from the person-level file and asserted equal)
  plan.json     the 72 keys, which 24 are contact keys, the shuffled pairing, each maker's arrangement
  briefs/*.txt  the briefs for arms A, D (stage 1) and B, S (stage 2). Arm V's briefs are written by stage2.py from the A
                rooms, by the rule fixed in PREDICTIONS.md.
The people's value for a joke: the mean of every 1-5 funniness rating it received (1 = Not at all, 5 = Extremely).
Run: python3 prepare.py <download dir>
"""
import csv, hashlib, json, random, statistics as st, sys
from pathlib import Path

SEED = 170
HERE = Path(__file__).parent
DL = Path(sys.argv[1])
MAN = json.loads((HERE / "sources" / "MANIFEST.json").read_text())
for f in MAN["files"]:
    assert hashlib.sha256((DL / f["name"]).read_bytes()).hexdigest() == f["sha256"], f["name"]

J = list(csv.DictReader(open(DL / "Joke_Aesthetics_Joke_Level_240_OSF.csv", encoding="utf-8-sig")))
P = list(csv.DictReader(open(DL / "Joke_Aesthetics_Person_Level_OSF.csv", encoding="utf-8-sig")))
meta = {}
for j in J:
    s = int(j["serial_survey_id"])
    v = [float(p[f"j_{s}_funny"]) for p in P if p[f"j_{s}_funny"] not in ("", "NA")]
    assert abs(st.mean(v) - float(j["funny_joke_5mean"])) < 1e-9 and len(v) == int(float(j["funny_joke_completed"])), s
    meta[s] = dict(text=" ".join(j["full_joke"].split()), survey_position=s, raters=len(v), mean=round(st.mean(v), 4),
                   sd=round(st.pstdev(v), 4), joke_type=j["joke_type"])
assert len(meta) == 240

rng = random.Random(SEED)
keys = rng.sample(sorted(meta), 72)
contact, scored = keys[:24], keys[24:]
kid = {f: f"k{i+1:02d}" for i, f in enumerate(keys)}


def rank(x):
    o = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0] * len(x); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and x[o[j + 1]] == x[o[i]]: j += 1
        for t in range(i, j + 1): r[o[t]] = (i + j) / 2
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = rank(a), rank(b); ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    return num / (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5


# Arm S: the first derangement from seed 170 upward whose Spearman rho with the true means lies within +-0.1 (rule of exp. 45-47).
s = SEED
while True:
    r2 = random.Random(s); perm = contact[:]; r2.shuffle(perm)
    if all(a != b for a, b in zip(contact, perm)):
        rho = spearman([meta[f]["mean"] for f in contact], [meta[f]["mean"] for f in perm])
        if abs(rho) <= 0.1: break
    s += 1
shuffle_seed, shuffle_rho = s, rho
told = {"B": {f: f for f in contact}, "S": dict(zip(contact, perm))}

arr_s = [random.Random(SEED * 10 + a).sample(scored, 48) for a in range(3)]
arr_c = [random.Random(SEED * 100 + a).sample(contact, 24) for a in range(2)]
arr_all = [random.Random(SEED * 1000 + a).sample(keys, 72) for a in range(3)]  # arm A rates all 72 (V is built from it)

ROOMS = "/home/user/error-as-method/works/2026-11-05-laughed-off/rooms"
OBJ = 'Below are short jokes of the kind sometimes called "dad jokes": short, clean jokes that try to be funny with puns and wordplay.'
PEOPLE = ("In a study whose data were released in October 2026, 541 adults recruited through an online research panel each "
          "read about 25 such jokes and rated how funny they found each one, from 1 = not at all funny to 5 = extremely funny. "
          "Each joke was rated by about 45 of them. For each joke, the people's value is the mean of their ratings.")
ANSWER_A = ("For each of the {n} numbered jokes, rate it yourself: how funny do you find it, from 1 (not at all) to 5 "
            "(extremely), with a whole number.")
ANSWER_D = ("For each of the 48 numbered jokes, do not rate it yourself. State those people's value for it: their mean "
            "funniness rating on the 1 to 5 scale (decimals allowed).")
RULE = ("Use no tool, program, search or lookup of any kind, except one: when you are done, write your answer, and nothing "
        "else, to the file {p} with your file-writing tool, then hand back the same text. Answer from what is written here.")
FORM_A = "Your answer is exactly {n} lines in the form\n1: <rating>\n2: <rating>\n... and then one more line:\nHOW: <one sentence on how you rated>"
FORM_D = ("Your answer is exactly 48 lines in the form\n1: mean <number>\n2: mean <number>\n... and then two more lines:\n"
          "HOW: <one sentence on how you arrived at the numbers>\nKNOWN: <yes, no or partly> - did you know this study or its data before today?")


def contact_block(tm, a):
    order = arr_c[a]
    lines = [f"T{i+1}. {meta[f]['text']} -> mean {meta[tm[f]]['mean']:.2f}" for i, f in enumerate(order)]
    return ("First, here are 24 other jokes from the same study, labelled T1 to T24, each with those people's value on the "
            "1 to 5 scale:\n" + "\n".join(lines) + "\n\n")


def brief(mid, arm, a, c, tm=None):
    rule = RULE.format(p=f"{ROOMS}/{mid}.txt")
    if arm == "A":
        objs = "The 72 jokes:\n" + "\n".join(f"{j+1}. {meta[f]['text']}" for j, f in enumerate(arr_all[a]))
        return OBJ + "\n\n" + objs + "\n\n" + ANSWER_A.format(n=72) + "\n\n" + rule + "\n\n" + FORM_A.format(n=72) + "\n"
    objs = "The 48 jokes:\n" + "\n".join(f"{j+1}. {meta[f]['text']}" for j, f in enumerate(arr_s[a]))
    return (OBJ + "\n\n" + PEOPLE + "\n\n" + (contact_block(tm, c) if tm else "") + objs + "\n\n" + ANSWER_D + "\n\n" + rule +
            "\n\n" + FORM_D + "\n")


if __name__ == "__main__":
    plan = {"seed": SEED, "keys": [{"id": kid[f], "survey_position": f, "role": "contact" if f in contact else "scored"} for f in keys],
            "shuffle": {"seed": shuffle_seed, "rho_with_true_means": round(shuffle_rho, 4),
                        "told_S": {kid[f]: kid[g] for f, g in told["S"].items()}},
            "arrangements_all": [[kid[f] for f in o] for o in arr_all],
            "arrangements_scored": [[kid[f] for f in o] for o in arr_s],
            "arrangements_contact": [[kid[f] for f in o] for o in arr_c], "makers": {}}
    for arm in "ADBS":
        for i in range(1, 7):
            a, c = (i - 1) % 3, (i - 1) % 2
            mid = f"{arm}{i}"
            (HERE / "briefs" / f"{mid}.txt").write_text(brief(mid, arm, a, c, told.get(arm)))
            plan["makers"][mid] = {"arrangement": a + 1, "contact_arrangement": (c + 1) if arm in "BS" else None}
    (HERE / "plan.json").write_text(json.dumps(plan, indent=1))
    (HERE / "people.json").write_text(json.dumps(
        {"_source": MAN["source"], "_licence": "CC BY-NC 4.0; jokes and derived means reproduced with attribution, non-commercial",
         "_derivation": "the people's value for a joke is the mean of every 1-5 funniness rating it received (1 = Not at all, 5 = Extremely)",
         **{kid[f]: {**meta[f], "role": "contact" if f in contact else "scored"} for f in keys}}, indent=1, ensure_ascii=False))
    print("shuffle seed", shuffle_seed, "rho", round(shuffle_rho, 3))
    sm = [meta[f]["mean"] for f in scored]; cm = [meta[f]["mean"] for f in contact]
    print("scored means", round(min(sm), 2), round(max(sm), 2), "SD", round(st.pstdev(sm), 3), "| contact", round(min(cm), 2),
          round(max(cm), 2), "SD", round(st.pstdev(cm), 3))
    print("raters per key", min(meta[f]["raters"] for f in keys), max(meta[f]["raters"] for f in keys),
          "median", st.median(meta[f]["raters"] for f in keys))
