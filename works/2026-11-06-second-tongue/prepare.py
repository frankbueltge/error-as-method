"""Session 171 (experiment 49, A Second Tongue): words, contact sets and briefs.

Reads Rodriguez-Cuadrado's L2 familiarity norms (https://osf.io/rnbs5, no licence stated) and the Glasgow Norms
(Scott et al. 2019, CC BY 4.0) from a download directory, checks SHA-256 against sources/MANIFEST.json, and writes:
  people.json   per word used tonight: the L2 people's value (mean familiarity, 1-7, over the raters who knew the word,
                re-computed from the raw file and asserted equal to the authors' mean_familiarity), its rater counts,
                and the native public's value (Glasgow FAM mean, 1-7)
  plan.json     the 72 words, contact/scored, the S and R pairings, each maker's arrangement
  briefs/*.txt  the briefs for arms A, D, B, S, R
The raw re-computation is recorded per word (it differs for some words: the raw file holds fewer rows than the\nauthors' n for them). The choice of words (fixed before any maker ran): over the 1,600 words in both sets, d = L2 mean - native mean;
the 150 lowest d and the 150 highest d form two tails; seed 171 draws 36 from each; 12 of each tail are contact, 24 scored.
Run: python3 prepare.py <download dir>
"""
import csv, hashlib, json, random, statistics as st, sys, collections
from pathlib import Path
import openpyxl

SEED = 171
HERE = Path(__file__).parent
DL = Path(sys.argv[1])
MAN = json.loads((HERE / "sources" / "MANIFEST.json").read_text())
for f in MAN["files"]:
    assert hashlib.sha256((DL / f["name"]).read_bytes()).hexdigest() == f["sha256"], f["name"]

wb = openpyxl.load_workbook(DL / "db.xlsx", read_only=True)
L2 = {r[1]: dict(spanish=r[2], mean=r[3], n=r[5], knew=r[6], unknown=r[7])
      for r in list(wb["Familiarity"].iter_rows(values_only=True))[1:] if r[0]}
NAT = {}
for r in list(csv.reader(open(DL / "g2.csv", encoding="latin-1")))[2:]:
    NAT[r[0]] = dict(mean=float(r[17]), n=int(r[19]))
common = sorted(w for w in L2 if w in NAT)
assert len(common) == 1600

d = sorted(common, key=lambda w: (L2[w]["mean"] - NAT[w]["mean"], w))
low, high = d[:150], d[-150:]
rng = random.Random(SEED)
lo, hi = rng.sample(low, 36), rng.sample(high, 36)
contact = lo[:12] + hi[:12]
scored = lo[12:] + hi[12:]
keys = contact + scored
order = random.Random(SEED + 1).sample(keys, 72)          # ids k01..k72 carry no tail information
kid = {w: f"k{i+1:02d}" for i, w in enumerate(order)}

# re-compute the 72 L2 means from the raw file
raw = openpyxl.load_workbook(DL / "raw.xlsx", read_only=True).worksheets[0]
R = collections.defaultdict(list)
for r in raw.iter_rows(min_row=2, values_only=True):
    if r[39] == 4 and r[41] in kid: R[r[41]].append(r[43])
RAWCHK = {}
for w in keys:   # the authors' mean is the people's value; the raw re-computation is recorded beside it, not asserted
    v = R[w]; k = [x for x in v if x and x > 0]
    RAWCHK[w] = dict(rows=len(v), knew=len(k), mean=round(st.mean(k), 4) if k else None,
                     agrees=len(v) == L2[w]["n"] and len(k) == L2[w]["knew"] and bool(k) and abs(st.mean(k) - L2[w]["mean"]) < 1e-9)


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


val = {w: round(L2[w]["mean"], 2) for w in keys}
# Arm S: first derangement from seed 171 upward with |rho| <= 0.1 against the true means (rule of exp. 45-48).
s = SEED
while True:
    r2 = random.Random(s); perm = contact[:]; r2.shuffle(perm)
    if all(a != b for a, b in zip(contact, perm)):
        rho = spearman([val[f] for f in contact], [val[f] for f in perm])
        if abs(rho) <= 0.1: break
    s += 1
shuffle_seed, shuffle_rho = s, rho
# Arm R: the true values dealt in reversed order: the word with the k-th highest true value is told the k-th lowest.
by_val = sorted(contact, key=lambda w: (val[w], w))
told_R = {w: v for w, v in zip(by_val, reversed(by_val))}
told = {"B": {f: f for f in contact}, "S": dict(zip(contact, perm)), "R": told_R}

arr_s = [random.Random(SEED * 10 + a).sample(scored, 48) for a in range(3)]
arr_c = [random.Random(SEED * 100 + a).sample(contact, 24) for a in range(2)]
arr_all = [random.Random(SEED * 1000 + a).sample(keys, 72) for a in range(3)]

ROOMS = "/home/user/error-as-method/works/2026-11-06-second-tongue/rooms"
OBJ = "Below are English words."
PEOPLE = ("In a study whose data were released in July 2026, 300 adults whose native language is Spanish, and who learned "
          "English as a second language, rated English words for how familiar each word was to them, from 1 = not familiar "
          "at all to 7 = very familiar. Anyone who did not know a word could say so instead, and those answers are left out. "
          "Each word was rated by about 25 of them. For each word, the people's value is the mean familiarity rating of those who "
          "knew it.")
ANSWER_A = ("For each of the 72 numbered words, rate it yourself: how familiar is this word to you, from 1 (not familiar at "
            "all) to 7 (very familiar), with a whole number.")
ANSWER_D = ("For each of the 48 numbered words, do not rate it yourself. State those people's value for it: their mean "
            "familiarity rating on the 1 to 7 scale (decimals allowed).")
RULE = ("Use no tool, program, search or lookup of any kind, except one: when you are done, write your answer, and nothing "
        "else, to the file {p} with your file-writing tool, then hand back the same text. Answer from what is written here.")
FORM_A = "Your answer is exactly 72 lines in the form\n1: <rating>\n2: <rating>\n... and then one more line:\nHOW: <one sentence on how you rated>"
FORM_D = ("Your answer is exactly 48 lines in the form\n1: mean <number>\n2: mean <number>\n... and then two more lines:\n"
          "HOW: <one sentence on how you arrived at the numbers>\nKNOWN: <yes, no or partly> - did you know this study or its data before today?")


def contact_block(tm, c):
    lines = [f"T{i+1}. {w} -> mean {val[tm[w]]:.2f}" for i, w in enumerate(arr_c[c])]
    return ("First, here are 24 other words from the same study, labelled T1 to T24, each with those people's value on the "
            "1 to 7 scale:\n" + "\n".join(lines) + "\n\n")


def brief(mid, arm, a, c, tm=None):
    rule = RULE.format(p=f"{ROOMS}/{mid}.txt")
    if arm == "A":
        objs = "The 72 words:\n" + "\n".join(f"{j+1}. {w}" for j, w in enumerate(arr_all[a]))
        return OBJ + "\n\n" + objs + "\n\n" + ANSWER_A + "\n\n" + rule + "\n\n" + FORM_A + "\n"
    objs = "The 48 words:\n" + "\n".join(f"{j+1}. {w}" for j, w in enumerate(arr_s[a]))
    return (OBJ + "\n\n" + PEOPLE + "\n\n" + (contact_block(tm, c) if tm else "") + objs + "\n\n" + ANSWER_D + "\n\n" + rule +
            "\n\n" + FORM_D + "\n")


if __name__ == "__main__":
    plan = {"seed": SEED, "keys": [{"id": kid[w], "word": w, "role": "contact" if w in contact else "scored",
                                    "tail": "L2 below native" if w in lo else "L2 above native"} for w in keys],
            "shuffle": {"seed": shuffle_seed, "rho_with_true_means": round(shuffle_rho, 4),
                        "told_S": {kid[f]: kid[g] for f, g in told["S"].items()}},
            "reversed": {"rho_with_true_means": round(spearman([val[f] for f in contact], [val[told_R[f]] for f in contact]), 4),
                         "rho_with_native_means": round(spearman([NAT[f]["mean"] for f in contact], [val[told_R[f]] for f in contact]), 4),
                         "told_R": {kid[f]: kid[g] for f, g in told_R.items()}},
            "arrangements_all": [[kid[w] for w in o] for o in arr_all],
            "arrangements_scored": [[kid[w] for w in o] for o in arr_s],
            "arrangements_contact": [[kid[w] for w in o] for o in arr_c], "makers": {}}
    for arm in "ADBSR":
        for i in range(1, 7):
            a, c = (i - 1) % 3, (i - 1) % 2
            mid = f"{arm}{i}"
            (HERE / "briefs" / f"{mid}.txt").write_text(brief(mid, arm, a, c, told.get(arm)))
            plan["makers"][mid] = {"arrangement": a + 1, "contact_arrangement": (c + 1) if arm in "BSR" else None}
    (HERE / "plan.json").write_text(json.dumps(plan, indent=1))
    (HERE / "people.json").write_text(json.dumps(
        {"_source": MAN["source"], "_rights": MAN["rights"],
         "_derivation": "l2: mean familiarity (1-7) over the L2 raters who knew the word (the authors' mean_familiarity, re-computed); native: Glasgow Norms FAM mean (1-7)",
         **{kid[w]: {"word": w, "spanish": L2[w]["spanish"], "l2": round(L2[w]["mean"], 4), "l2_raters": L2[w]["n"],
                     "l2_knew": L2[w]["knew"], "raw_recomputed": RAWCHK[w], "native": NAT[w]["mean"], "native_raters": NAT[w]["n"],
                     "role": "contact" if w in contact else "scored",
                     "tail": "L2 below native" if w in lo else "L2 above native"} for w in keys}}, indent=1, ensure_ascii=False))
    sl = [L2[w]["mean"] for w in scored]; sn = [NAT[w]["mean"] for w in scored]
    print("shuffle seed", shuffle_seed, "rho", round(shuffle_rho, 3), "| R rho true", plan["reversed"]["rho_with_true_means"],
          "R rho native", plan["reversed"]["rho_with_native_means"])
    print("scored L2", round(min(sl), 2), round(max(sl), 2), "SD", round(st.pstdev(sl), 3), "| native", round(min(sn), 2),
          round(max(sn), 2), "SD", round(st.pstdev(sn), 3), "| rho(L2, native) scored", round(spearman(sl, sn), 3))
    print("tails d: low", round(L2[low[-1]]["mean"] - NAT[low[-1]]["mean"], 2), "high", round(L2[high[0]]["mean"] - NAT[high[0]]["mean"], 2))
    bad = [w for w in keys if not RAWCHK[w]["agrees"]]
    print("raw re-computation agrees on", 72 - len(bad), "of 72; differs:", [(w, L2[w]["n"], L2[w]["knew"], round(L2[w]["mean"], 3), RAWCHK[w]) for w in bad])
    print("lo:", lo); print("hi:", hi)
