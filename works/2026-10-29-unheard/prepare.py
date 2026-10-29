"""Session 163, experiment 43 (Unheard): build the keys, the people's values and the eighteen briefs.

Source: Kawai, Jaeggi, Georgiou, Meister, Pieren, Schaeffer (2026), dataset to "Short-term noise annoyance towards
drones and other transportation noise sources: a laboratory study", Zenodo record 22045972 (CC BY 4.0).
36 listeners each rated all 130 stimuli (65 sounds x 2 ambient backgrounds; each listener heard each sound once)
on the 0-10 scale of ISO/TS 15666. A key is one sound: the two background variants of the same sound are pooled,
because nothing in a written description can tell them apart. 65 keys, 36 ratings each.

Two keys are anchors (the lowest and the highest people's median, ties broken by key id): arm C is told the
people's p25, p50 and p75 on them. They are scored in no arm.
Run: python3 prepare.py   (writes plan.json, people.json, briefs/*.txt)
"""
import csv, json, random, statistics as st
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
SEED = 163
rows = list(csv.DictReader(open(HERE / "sources" / "JASA_dataset_kawai_et_al.csv"), delimiter=";"))
assert len(rows) == 2340 and len({r["subject_id"] for r in rows}) == 36

def kind(r):
    """The written description of a sound, from the dataset's columns and the parts of its stimulus name that the
    columns do not carry (drone flight height hoch/mittel/tief; a 2 m barrier and the speed for cars)."""
    c, t, m, d, sp, n = r["category"], r["type"], r["maneuver"], r["distance"], r["speed"], r["stimulus"]
    if c in ("Dronesmall", "Dronebig"):
        size = "small quadcopter drone (0.9 kg)" if c == "Dronesmall" else "large quadcopter drone (6.3 kg)"
        what = {"flyby": "flying past", "takeoff": "taking off", "landing": "landing"}[m]
        s = f"{size}, {what}, {d} m lateral distance, {sp} speed"
        if m == "flyby":
            h = {"hoch": "high", "mittel": "medium", "tief": "low"}[[x for x in ("hoch", "mittel", "tief") if f"_{x}_" in n][0]]
            s += f", {h} flight altitude"
        return s
    if c == "PKWsingle":
        v = "80 km/h" if n.startswith("T80") else "50 km/h"
        s = f"single passenger car passing at {d} m, {v}" + (", accelerating" if m == "acceleration" else "")
        return s + (", behind a 2 m noise barrier" if "2mBarr" in n else "")
    if c == "Jet":
        return f"jet airliner landing (recording labelled '{t}')"
    if c == "Prop":
        return f"propeller aircraft (type {t}) {'taking off' if m == 'takeoff' else 'landing'}, {d} m lateral distance"
    if c == "Heli":
        return f"helicopter (type {t}) {'taking off' if m == 'takeoff' else 'landing'}, {d} m lateral distance"
    raise ValueError(c)

keys = defaultdict(list)
for r in rows:
    k = (kind(r), round(float(r["LASmax"]), 1), round(float(r["LAE_auralisation"]), 1))
    keys[k].append(int(r["rating"]))
assert len(keys) == 65 and all(len(v) == 36 for v in keys.values())

def q(v, p):
    return float(st.quantiles(v, n=100, method="inclusive")[p - 1])

K = []
for i, k in enumerate(sorted(keys)):
    v = keys[k]
    K.append({"id": f"k{i+1:02d}", "text": f"{k[0]}; maximum level {k[1]} dB(A), sound exposure level {k[2]} dB(A)",
              "LASmax": k[1], "LAE": k[2], "n": len(v), "median": st.median(v), "mean": round(st.mean(v), 3),
              "p25": q(v, 25), "p75": q(v, 75), "ratings": sorted(v)})
order = sorted(K, key=lambda x: (x["median"], x["id"]))
anchors = [order[0]["id"], order[-1]["id"]]

HEAD_PEOPLE = ("Below are {n} sounds, each given as a written description. In a laboratory listening study in Switzerland "
    "in September and October 2023, 36 adults (aged 21 to 64, 17 women and 19 men) each heard every one of these sounds "
    "once, played back as a recording, mixed into a quiet ambient background, in random order. After each sound they "
    "answered, in German, the question: 'If this were the noise situation outside your home, which number between 0 and "
    "10 best describes how disturbed or annoyed you would be by it?' on a scale from 0 (not at all) to 10 (extremely), "
    "with a whole number. Before the session, a third of them had been told nothing about drones, a third that drones "
    "would be used for commercial deliveries, a third that they would be used for medical transport.\n\n"
    "For each sound, do not rate it yourself. State how those 36 people's ratings were spread, on their own 0 to 10 "
    "scale: give the 10th, 25th, 50th, 75th and 90th percentile of their ratings, and their mean rating (decimals allowed).")
ANCHOR = ("\n\nTwo of the sounds are given here with the people's actual results, so that you know where this group "
    "stood on them. They are not in the list below.\n{a}")
HEAD_SELF = ("Below are {n} sounds, each given as a written description. Imagine that you hear each one, as a "
    "recording, outside your home. For each, answer the question: 'If this were the noise situation outside your home, "
    "which number between 0 and 10 best describes how disturbed or annoyed you would be by it?' on a scale from 0 "
    "(not at all) to 10 (extremely). Answer each with a single whole number, as yourself.")
NOTOOLS = "\n\nDo not use any tool, program, file, search or lookup of any kind. Answer from what you have here.\n\n"
FOOT_PEOPLE = ("\n\nFormat your whole answer exactly like this, and nothing else:\nSPREADS\n1: p10=<n> p25=<n> p50=<n> "
    "p75=<n> p90=<n> mean=<n>\n...\n{n}: p10=<n> p25=<n> p50=<n> p75=<n> p90=<n> mean=<n>\n"
    "KNOWN: do you know this study or its data? Say yes or no, and if yes, from where, in at most 30 words.\n"
    "HOW: in at most 40 words, how you arrived at the spreads.\n"
    "TOOLS: every tool, program, file or search you used, or \"none\".")
FOOT_SELF = ("\n\nFormat your whole answer exactly like this, and nothing else:\nRATINGS\n1: <n>\n...\n{n}: <n>\n"
    "HOW: in at most 40 words, how you arrived at the ratings.\n"
    "TOOLS: every tool, program, file or search you used, or \"none\".")

rng = random.Random(SEED)
plan = {"seed": SEED, "anchors": anchors, "makers": {}}
byid = {k["id"]: k for k in K}
for arm in ("A", "D", "C"):
    for j in range(1, 7):
        mid = f"{arm}{j}"
        ks = [k["id"] for k in K if not (arm == "C" and k["id"] in anchors)]
        rng.shuffle(ks)
        lines = "\n".join(f"{i+1}: {byid[k]['text']}" for i, k in enumerate(ks))
        n = len(ks)
        if arm == "A":
            text = HEAD_SELF.format(n=n) + NOTOOLS + lines + FOOT_SELF.format(n=n)
        else:
            head = HEAD_PEOPLE.format(n=n)
            if arm == "C":
                a = "\n".join(f"- {byid[k]['text']}: 25th percentile {byid[k]['p25']:g}, median {byid[k]['median']:g}, "
                              f"75th percentile {byid[k]['p75']:g}" for k in anchors)
                head += ANCHOR.format(a=a)
            text = head + NOTOOLS + lines + FOOT_PEOPLE.format(n=n)
        (HERE / "briefs" / f"{mid}.txt").write_text(text + "\n")
        plan["makers"][mid] = ks
json.dump(plan, open(HERE / "plan.json", "w"), indent=1)
json.dump(K, open(HERE / "people.json", "w"), indent=1)
print("anchors", anchors, [byid[a]["median"] for a in anchors])
print("people's medians", sorted(k["median"] for k in K))
