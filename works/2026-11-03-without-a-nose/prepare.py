"""Session 168 (experiment 47, Without a Nose): keys, contact sets and briefs.

Reads the imagined-odour vocabularies of Hörberg et al. (https://osf.io/jstu7, CC BY-NC 4.0) from a download directory
holding SurveyData_trimmed.csv and Valence_Arousal_Dominance.csv, checks their SHA-256 against sources/MANIFEST.json, and
writes:
  people.json   per key used tonight: the odour name, how many English speakers described it, how many of their words carry a
                valence score, and the mean valence (1-9) of those words (derived values, attributed, non-commercial)
  plan.json     the 72 keys, which 24 are contact keys, the shuffled pairing, each maker's arrangement
  briefs/*.txt  the 24 briefs
The people's value for an odour: every word an English-speaking participant wrote for it (column Translation, which for
English is the word itself, lower-cased), looked up in the valence list the study ships (Warriner et al. 2013, 1 = very
unpleasant ... 9 = very pleasant); words without an entry are skipped; the value is the mean over the scored words.
Run: python3 prepare.py <download dir>
"""
import csv, hashlib, json, random, statistics as st, sys
from collections import defaultdict
from pathlib import Path

SEED = 168
HERE = Path(__file__).parent
DL = Path(sys.argv[1])
MAN = json.loads((HERE / "sources" / "MANIFEST.json").read_text())
for f in MAN["files"]:
    assert hashlib.sha256((DL / f["name"]).read_bytes()).hexdigest() == f["sha256"], f["name"]

val = {r["Word"].lower(): float(r["Valence"])
       for r in csv.DictReader(open(DL / "Valence_Arousal_Dominance.csv", encoding="latin-1"), delimiter=";")}
words, people, allw = defaultdict(list), defaultdict(set), defaultdict(int)
for r in csv.DictReader(open(DL / "SurveyData_trimmed.csv", encoding="latin-1"), delimiter=";"):
    if r["Language"] != "English":
        continue
    o = r["StimWords"].strip(); w = r["Translation"].strip().lower()
    people[o].add(r["ResponseID"]); allw[o] += 1
    if w in val:
        words[o].append(val[w])
meta = {o: dict(name=o, people=len(people[o]), words=allw[o], scored_words=len(words[o]),
                mean=round(st.mean(words[o]), 4), sd=round(st.pstdev(words[o]), 4)) for o in words}
assert len(meta) == 76, len(meta)

rng = random.Random(SEED)
keys = rng.sample(sorted(meta), 72)
contact, scored = keys[:24], keys[24:]
kid = {f: f"k{i+1:02d}" for i, f in enumerate(keys)}


def spearman(a, b):
    def rank(x):
        o = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0] * len(x); i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and x[o[j + 1]] == x[o[i]]: j += 1
            for t in range(i, j + 1): r[o[t]] = (i + j) / 2
            i = j + 1
        return r
    ra, rb = rank(a), rank(b); ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    return num / (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5


# Arm S: the first derangement from seed 168 upward whose Spearman rho with the true means lies within +-0.1 (rule of exp. 45/46).
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

ROOMS = "/home/user/error-as-method/works/2026-11-03-without-a-nose/rooms"
OBJ = "Below are the names of smells."
PEOPLE = ("In a study whose data were released in October 2026, 46 adults in the United Kingdom whose mother tongue is English "
          "read the name of a smell, imagined that smell, and wrote a few words describing it. Each smell was described by "
          "about 9 of them. Afterwards every word they wrote was scored with a published list of how pleasant English words "
          "are, from 1 = very unpleasant to 9 = very pleasant. For each smell, the people's value is the mean of those scores "
          "over all the words they wrote for it.")
ANSWER_A = ("For each of the 48 numbered smells, imagine the smell and rate it yourself: how pleasant is it, from 1 (very "
            "unpleasant) to 9 (very pleasant), with a whole number.")
ANSWER_D = ("For each of the 48 numbered smells, do not rate it yourself. State those people's value for it: the mean "
            "pleasantness, on the 1 to 9 scale, of the words they wrote for it (decimals allowed).")
RULE = ("Use no tool, program, search or lookup of any kind, except one: when you are done, write your answer, and nothing "
        "else, to the file {p} with your file-writing tool, then hand back the same text. Answer from what is written here.")
FORM_A = "Your answer is exactly 48 lines in the form\n1: <rating>\n2: <rating>\n... and then one more line:\nHOW: <one sentence on how you rated>"
FORM_D = ("Your answer is exactly 48 lines in the form\n1: mean <number>\n2: mean <number>\n... and then two more lines:\n"
          "HOW: <one sentence on how you arrived at the numbers>\nKNOWN: <yes, no or partly> - did you know this study or its data before today?")


def contact_block(arm, a):
    order = arr_c[a]; tm = told[arm]
    lines = [f"T{i+1}. {f}: mean {meta[tm[f]]['mean']:.2f}" for i, f in enumerate(order)]
    return ("First, here are 24 other smells from the same study, labelled T1 to T24, each with those people's value on the "
            "1 to 9 scale:\n" + "\n".join(lines) + "\n\n")


plan = {"seed": SEED, "keys": [{"id": kid[f], "name": f, "role": "contact" if f in contact else "scored"} for f in keys],
        "shuffle": {"seed": shuffle_seed, "rho_with_true_means": round(shuffle_rho, 4),
                    "told_S": {kid[f]: kid[g] for f, g in told["S"].items()}},
        "arrangements_scored": [[kid[f] for f in o] for o in arr_s],
        "arrangements_contact": [[kid[f] for f in o] for o in arr_c], "makers": {}}
(HERE / "briefs").mkdir(exist_ok=True); (HERE / "rooms").mkdir(exist_ok=True)
for arm in "ADBS":
    for i in range(1, 7):
        a, c = (i - 1) % 3, (i - 1) % 2
        mid = f"{arm}{i}"
        objs = "The 48 smells:\n" + "\n".join(f"{j+1}. {f}" for j, f in enumerate(arr_s[a]))
        rule = RULE.format(p=f"{ROOMS}/{mid}.txt")
        if arm == "A":
            text = OBJ + "\n\n" + objs + "\n\n" + ANSWER_A + "\n\n" + rule + "\n\n" + FORM_A
        else:
            text = (OBJ + "\n\n" + PEOPLE + "\n\n" + (contact_block(arm, c) if arm in "BS" else "") + objs + "\n\n" +
                    ANSWER_D + "\n\n" + rule + "\n\n" + FORM_D)
        (HERE / "briefs" / f"{mid}.txt").write_text(text + "\n")
        plan["makers"][mid] = {"scored_arrangement": a + 1, "contact_arrangement": (c + 1) if arm in "BS" else None}
(HERE / "plan.json").write_text(json.dumps(plan, indent=1))
(HERE / "people.json").write_text(json.dumps({"_source": MAN["source"], "_derivation": __doc__.split("The people's value")[1].split("Run:")[0].strip(),
                                              **{kid[f]: {**meta[f], "role": "contact" if f in contact else "scored"} for f in keys}},
                                             indent=1, ensure_ascii=False))
print("shuffle seed", shuffle_seed, "rho", round(shuffle_rho, 3))
sm = [meta[f]["mean"] for f in scored]; cm = [meta[f]["mean"] for f in contact]
print("scored means range", round(min(sm), 2), round(max(sm), 2), "SD", round(st.pstdev(sm), 2), "| contact SD", round(st.pstdev(cm), 2))
print("people per key", min(meta[f]["people"] for f in keys), max(meta[f]["people"] for f in keys),
      "| scored words per key", min(meta[f]["scored_words"] for f in keys), max(meta[f]["scored_words"] for f in keys))
print("left out:", sorted(set(meta) - set(keys)))
