"""Experiment 50, *Half Turned* (Session 172). Prepares people.json, plan.json and the thirty briefs.

Run:  python3 prepare.py <path to NeFeLaE_final_dataset.xlsx> <path to occupations list as text>
The raw files are not committed (osf.io/j86z4 states no licence); their hashes are in sources/MANIFEST.json.
"""
import json, random, re, statistics as st, sys
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
XLSX, LISTTXT = sys.argv[1], sys.argv[2]

wb = openpyxl.load_workbook(XLSX, read_only=True)


def means(sheet):
    rows = list(wb[sheet].iter_rows(values_only=True))
    head = rows[0]
    occ = head[5:]
    out = {}
    for j, o in enumerate(occ):
        vals = [r[5 + j] for r in rows[1:] if r[5 + j] is not None]
        out[o] = (st.mean(vals), len(vals))
    return out, len(rows) - 1


br, n_br = means("Dataset_Brazil_N110")
fr, n_fr = means("Dataset_France_N116")
pub = {r[0]: (r[5], r[6]) for r in list(wb["Means_by_country_and_scale_dir"].iter_rows(values_only=True))[1:]}
for o in br:  # my recomputation must match the authors' own means sheet
    assert abs(br[o][0] - pub[o][0]) < 1e-9 and abs(fr[o][0] - pub[o][1]) < 1e-9, o

# Brazilian Portuguese masculine / feminine forms, from the study's own list (NeFeLaE_occupations_list.pdf)
pt = {}
for line in open(LISTTXT, encoding="utf-8"):
    for o in sorted(br, key=len, reverse=True):
        if line.strip().startswith(o + " ") or line.strip().startswith(o + "  "):
            cells = [c for c in re.split(r"\s{2,}", line.strip()) if c]
            if len(cells) >= 5 and o not in pt:
                pt[o] = (cells[-2], cells[-1])
            break
# one row of the PDF runs its last two cells together with a single space
pt.setdefault("specialist educator", ("educador especializado", "educadora especializada"))
assert len(pt) == 56, sorted(set(br) - set(pt))

occs = sorted(br)
rng = random.Random(172)
order = occs[:]
rng.shuffle(order)
contact, scored = order[:24], order[24:]


def rho(a, b):
    def ranks(x):
        s = sorted(range(len(x)), key=lambda i: x[i])
        r = [0.0] * len(x)
        i = 0
        while i < len(s):
            j = i
            while j + 1 < len(s) and x[s[j + 1]] == x[s[i]]:
                j += 1
            for k in range(i, j + 1):
                r[s[k]] = (i + j) / 2
            i = j + 1
        return r
    ra, rb = ranks(a), ranks(b)
    ma, mb = st.mean(ra), st.mean(rb)
    num = sum((p - ma) * (q - mb) for p, q in zip(ra, rb))
    return num / (sum((p - ma) ** 2 for p in ra) * sum((q - mb) ** 2 for q in rb)) ** 0.5


true_c = [round(br[o][0], 1) for o in contact]
# R: the same 24 values dealt in exactly reversed order of the truth
srt = sorted(range(24), key=lambda i: true_c[i])
rev = [0.0] * 24
for k, i in enumerate(srt):
    rev[i] = true_c[srt[23 - k]]
# H: the same 24 values dealt so that rho with the truth is -0.50 +- 0.02, first hit of seed 1720
hr = random.Random(1720)
tries = 0
while True:
    tries += 1
    perm = true_c[:]
    hr.shuffle(perm)
    r = rho(perm, true_c)
    if -0.52 <= r <= -0.48 and all(p != t for p, t in zip(perm, true_c)):
        half = perm
        break

deal = {"B": true_c, "H": half, "R": rev}
deal_rho = {k: round(rho(v, true_c), 3) for k, v in deal.items()}

people = {
    "source": "NeFeLaE, osf.io/j86z4, NeFeLaE_final_dataset.xlsx (posted 2026-07-17, no licence stated); means recomputed here and checked against the authors' sheet Means_by_country_and_scale_dir",
    "scale": "perceived femininity of the occupation, 0 = masculine, 50 = neutral, 100 = feminine (slider; both scale directions recoded by the authors)",
    "n_brazil": n_br, "n_france": n_fr,
    "occupations": {o: {"pt_m": pt[o][0], "pt_f": pt[o][1], "brazil": round(br[o][0], 2), "france": round(fr[o][0], 2),
                        "n_brazil": br[o][1], "n_france": fr[o][1]} for o in occs},
}
plan = {"seed_split": 172, "seed_half": 1720, "half_tries": tries, "contact": contact, "scored": scored,
        "deal": deal, "deal_rho_with_truth": deal_rho,
        "rho_brazil_france_scored": round(rho([br[o][0] for o in scored], [fr[o][0] for o in scored]), 3),
        "rho_brazil_france_all": round(rho([br[o][0] for o in occs], [fr[o][0] for o in occs]), 3)}
(HERE / "people.json").write_text(json.dumps(people, indent=1, ensure_ascii=False))
(HERE / "plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))

ROOM = "/home/user/error-as-method/works/2026-11-07-half-turned/rooms/"
WHO = ("In a study whose data were released in July 2026, 110 adults in Brazil, answering in Brazilian Portuguese, "
       "rated occupations for how each is perceived today, on a slider from 0 = masculine through 50 = neutral to "
       "100 = feminine. Each occupation was named in Portuguese; its masculine and feminine forms are given in brackets "
       "as the study lists them. For each occupation, the people's value is the mean rating of all 110.")


def term(o, with_pt):
    return f"{o} ({pt[o][0]} / {pt[o][1]})" if with_pt else o


def brief_describe(arm, i):
    lines = ["Below are occupations.", "", WHO, ""]
    if arm != "D":
        lines.append("First, here are 24 other occupations from the same study, labelled T1 to T24, each with those "
                     "people's value on the 0 to 100 scale:")
        for k, o in enumerate(contact):
            lines.append(f"T{k + 1}. {term(o, True)} -> mean {deal[arm][k]:.1f}")
        lines.append("")
    lines.append("The 32 occupations:")
    for k, o in enumerate(scored):
        lines.append(f"{k + 1}. {term(o, True)}")
    lines += ["", "For each of the 32 numbered occupations, do not rate it yourself. State those people's value for it: "
              "their mean rating on the 0 to 100 scale (decimals allowed).", "",
              f"Use no tool, program, search or lookup of any kind, except one: when you are done, write your answer, "
              f"and nothing else, to the file {ROOM}{arm}{i}.txt with your file-writing tool, then hand back the same "
              f"text. Answer from what is written here.", "",
              "Your answer is exactly 32 lines in the form", "1: mean <number>", "2: mean <number>",
              "... and then two more lines:", "HOW: <one sentence on how you arrived at the numbers>",
              "KNOWN: <yes, no or partly> - did you know this study or its data before today?"]
    return "\n".join(lines) + "\n"


a_order = occs[:]
random.Random(1721).shuffle(a_order)
plan["a_order"] = a_order
(HERE / "plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))


def brief_answer(i):
    lines = ["Below are occupations.", "", "The 56 occupations:"]
    lines += [f"{k + 1}. {o}" for k, o in enumerate(a_order)]
    lines += ["", "For each of the 56 numbered occupations, rate it yourself: in your opinion, how is this occupation "
              "perceived today, from 0 = masculine through 50 = neutral to 100 = feminine? Whole numbers.", "",
              f"Use no tool, program, search or lookup of any kind, except one: when you are done, write your answer, "
              f"and nothing else, to the file {ROOM}A{i}.txt with your file-writing tool, then hand back the same text. "
              f"Answer from what is written here.", "",
              "Your answer is exactly 56 lines in the form", "1: <rating>", "2: <rating>",
              "... and then one more line:", "HOW: <one sentence on how you rated>"]
    return "\n".join(lines) + "\n"


(HERE / "briefs").mkdir(exist_ok=True)
(HERE / "rooms").mkdir(exist_ok=True)
for i in range(1, 7):
    (HERE / "briefs" / f"A{i}.txt").write_text(brief_answer(i))
    for arm in "DBHR":
        (HERE / "briefs" / f"{arm}{i}.txt").write_text(brief_describe(arm, i))
print(json.dumps({k: plan[k] for k in ("deal_rho_with_truth", "half_tries", "rho_brazil_france_scored", "rho_brazil_france_all")}))
