"""Session 166 (experiment 46, Clean Hands): keys, contact sets and briefs.

Reads the Turkish Objects-on-Hands norms (Rengiiyiler & Tekozel, https://osf.io/9zfsu, no licence stated) from a download
directory holding Turkish_Objects_on_Hands_Normative_Data.xlsx, checks its SHA-256 against sources/MANIFEST.json, and writes:
  people.json   per key used tonight: English name, category, n, the people's perceived-disease-risk mean and SD (derived values)
  plan.json     the 72 keys, which 24 are contact keys, the shuffled pairing, each maker's arrangement
  briefs/*.txt  the 24 briefs
Run: python3 prepare.py <download dir>
"""
import hashlib, json, random, statistics as st, sys
from pathlib import Path
import openpyxl

SEED = 166
HERE = Path(__file__).parent
DL = Path(sys.argv[1])
MAN = json.loads((HERE / "sources" / "MANIFEST.json").read_text())
for f in MAN["files"]:
    assert hashlib.sha256((DL / f["name"]).read_bytes()).hexdigest() == f["sha256"], f["name"]

ws = openpyxl.load_workbook(DL / "Turkish_Objects_on_Hands_Normative_Data.xlsx", read_only=True)["Turkish_Norms"]
rows = list(ws.iter_rows(values_only=True)); head = rows[0]
ix = {k: head.index(k) for k in ("Picture_No", "English_Intended_Name", "Category", "Disease_Risk_N", "Disease_Risk_Mean", "Disease_Risk_SD")}
meta = {}
for r in rows[1:]:
    if r[ix["Picture_No"]] is None or r[ix["Disease_Risk_Mean"]] in (None, "", "NA"):
        continue
    name = str(r[ix["English_Intended_Name"]]).strip()
    meta[name] = dict(name=name, picture_no=int(r[ix["Picture_No"]]), category=r[ix["Category"]],
                      n=int(float(r[ix["Disease_Risk_N"]])), mean=float(r[ix["Disease_Risk_Mean"]]), sd=float(r[ix["Disease_Risk_SD"]]))
assert len(meta) == 126, len(meta)

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


# Arm S: a derangement of the contact keys' means, the first from seed 166 upward whose Spearman rho with the true means
# lies within +-0.1. Every number told to S is true of some object.
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

ROOMS = "/home/user/error-as-method/works/2026-11-01-clean-hands/rooms"
OBJ = ("Below are everyday objects. In a study each object was shown as a colour photograph, front view, held in a person's "
       "clean hands. The objects come from six groups: fruit, vegetables, kitchen utensils, office supplies, toys, and "
       "women's accessories.")
PEOPLE = ("In a study published in September 2026, 107 adults who speak Turkish saw such photographs one at a time. For each "
          "object they named it, said how familiar it was, and rated its perceived disease risk, from 1 = not at all risky to "
          "7 = very risky, with a whole number. Each object was rated by about 53 of them.")
ANSWER_A = ("For each of the 48 numbered objects, rate it yourself: how risky is this object, held like that, in terms of "
            "disease, from 1 (not at all risky) to 7 (very risky), with a whole number.")
ANSWER_D = ("For each of the 48 numbered objects, do not rate it yourself. State how those people rated it, on their 1 to 7 "
            "scale: give their mean rating (decimals allowed).")
RULE = ("Use no tool, program, search or lookup of any kind, except one: when you are done, write your answer, and nothing "
        "else, to the file {p} with your file-writing tool, then hand back the same text. Answer from what is written here.")
FORM_A = "Your answer is exactly 48 lines in the form\n1: <rating>\n2: <rating>\n... and then one more line:\nHOW: <one sentence on how you rated>"
FORM_D = ("Your answer is exactly 48 lines in the form\n1: mean <number>\n2: mean <number>\n... and then two more lines:\n"
          "HOW: <one sentence on how you arrived at the numbers>\nKNOWN: <yes, no or partly> - did you know this study or its data before today?")


def contact_block(arm, a):
    order = arr_c[a]; tm = told[arm]
    lines = [f"T{i+1}. {f}: mean {meta[tm[f]]['mean']:.2f}" for i, f in enumerate(order)]
    return ("First, here are 24 other objects from the same study, labelled T1 to T24, each with the mean of those "
            "people's ratings on the 1 to 7 scale:\n" + "\n".join(lines) + "\n\n")


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
        objs = "The 48 objects:\n" + "\n".join(f"{j+1}. {f}" for j, f in enumerate(arr_s[a]))
        rule = RULE.format(p=f"{ROOMS}/{mid}.txt")
        if arm == "A":
            text = OBJ + "\n\n" + objs + "\n\n" + ANSWER_A + "\n\n" + rule + "\n\n" + FORM_A
        else:
            text = (OBJ + "\n\n" + PEOPLE + "\n\n" + (contact_block(arm, c) if arm in "BS" else "") + objs + "\n\n" +
                    ANSWER_D + "\n\n" + rule + "\n\n" + FORM_D)
        (HERE / "briefs" / f"{mid}.txt").write_text(text + "\n")
        plan["makers"][mid] = {"scored_arrangement": a + 1, "contact_arrangement": (c + 1) if arm in "BS" else None}
(HERE / "plan.json").write_text(json.dumps(plan, indent=1))
(HERE / "people.json").write_text(json.dumps({kid[f]: {**meta[f], "role": "contact" if f in contact else "scored"} for f in keys},
                                             indent=1, ensure_ascii=False))
print("shuffle seed", shuffle_seed, "rho", round(shuffle_rho, 3))
sm = [meta[f]["mean"] for f in scored]; cm = [meta[f]["mean"] for f in contact]
print("scored means range", round(min(sm), 2), round(max(sm), 2), "SD", round(st.pstdev(sm), 2), "| contact SD", round(st.pstdev(cm), 2))
print("categories scored:", {c: sum(1 for f in scored if meta[f]["category"] == c) for c in sorted(set(m["category"] for m in meta.values()))})
