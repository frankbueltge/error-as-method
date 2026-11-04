"""Level and order: what the family took in from contact, and what it named as wrong.

Session 169 (2026-11-04), the seventh night. POST HOC, on data committed by Sessions 163 to 168.
Nothing in those works is changed. Run from the repository root:

    python3 docs/research-notes/machine-practice/audits/2026-11-04-level-and-order/audit.py

For every told arm in experiments 43 to 47 it reports
  - how far the contact departed from the family in LEVEL (fraction of the scale's range),
  - whether the contact could contradict an ORDER the family holds, and how wide that order was
    (population SD of the answering makers' medians, as a fraction of the range),
  - how many makers of the arm said the told values did not fit.

Noticing counts for experiments 45 to 47 are the committed codings (journals of Sessions 165, 166 and
168, by the rule fixed in each PREDICTIONS.md; experiment 47 was also coded 12 of 12 alike by a second
coder). Experiments 43 and 44 had no noticing prediction. For them this script runs a keyword screen
over every hand-back of the told arms, and Session 169 read every HOW line by hand (quoted in the
journal). That coding is the practice's alone and was made after the data.
"""
import json
import pathlib
import re
import statistics as st

ROOT = pathlib.Path(__file__).resolve().parents[5]
W = ROOT / "works"
OUT = pathlib.Path(__file__).resolve().parent

MISFIT = re.compile(
    r"surpris|odd\b|unexpect|inconsisten|counter-?intuitive|do(es)? not (follow|fit|track)|"
    r"don't fit|unreliab|noisy|loosely|revers|invert|no relation|weak", re.I)


def rooms(d, arm):
    return sorted((W / d / "rooms").glob(f"{arm}[0-9].txt"))


def screen(d, arm):
    hits = {}
    for f in rooms(d, arm):
        t = f.read_text()
        m = MISFIT.findall(t)
        hits[f.stem] = len(m)
    return hits


def sd_frac(vals, rng):
    return round(st.pstdev(vals) / rng, 3)


rows = []

# experiment 43, Unheard: annoyance 0-10, arm C told two people's results (k39, k59)
d = "2026-10-29-unheard"
r = json.load(open(W / d / "results.json"))
people = {p["id"]: p for p in json.load(open(W / d / "people.json"))}
fam = r["family_median"]
lev = [people[k]["median"] - fam[k] for k in r["anchors"]]
rows.append({
    "exp": 43, "work": d, "arm": "C", "told": "two of the people's results (quietest and loudest)",
    "range": 10, "contact_keys": len(r["anchors"]),
    "level_departure_frac": round(st.mean(lev) / 10, 3), "level_departures_each": lev,
    "largest_single_departure_frac": round(max(abs(v) for v in lev) / 10, 3),
    "can_contradict_order": "barely: two points give one pairwise relation",
    "family_order_sd_frac": sd_frac(list(fam.values()), 10),
    "screen_hits": screen(d, "C"), "named_misfit": 0, "of": 6,
    "named_by": "Session 169, HOW lines and keyword screen, post hoc"})

# experiment 44, Lesser Known: truth 1-6, arms M and U told two items each
d = "2026-10-30-lesser-known"
r = json.load(open(W / d / "results.json"))
people = json.load(open(W / d / "people.json"))
pk = r["per_key"]
famall = [v["fam"] for v in pk.values()]
for arm, key in (("M", "M_anchors"), ("U", "U_anchors")):
    ks = r[key]
    famk = {k: (pk[k]["fam"] if k in pk else None) for k in ks}
    lev = [people[k]["median"] - famk[k] for k in ks if famk[k] is not None]
    rows.append({
        "exp": 44, "work": d, "arm": arm, "told": "two items' medians and quartiles",
        "range": 5, "contact_keys": len(ks),
        "level_departure_frac": round(st.mean(lev) / 5, 3) if lev else None,
        "level_departures_each": lev, "family_values_on_contact_keys": famk,
        "largest_single_departure_frac": round(max(abs(v) for v in lev) / 5, 3),
        "can_contradict_order": "barely: two points give one pairwise relation",
        "family_order_sd_frac": sd_frac(famall, 5),
        "screen_hits": screen(d, arm), "named_misfit": 0, "of": 6,
        "named_by": "Session 169, HOW lines and keyword screen, post hoc"})

# experiments 45-47: 24 contact keys, true (B) or shuffled (S). The family answered only the 48 scored
# keys, so the level departure is read on those (people's mean minus family median): a proxy.
CODED = {  # committed codings, journals of Sessions 165, 166, 168
    "2026-10-31-paired": (45, 8, {"B": 0, "S": 4}),
    "2026-11-01-clean-hands": (46, 6, {"B": 0, "S": 0}),
    "2026-11-03-without-a-nose": (47, 8, {"B": 0, "S": 6}),
}
for d, (n, rng, coded) in CODED.items():
    r = json.load(open(W / d / "results.json"))
    pk = r["per_key"]
    famv = [v["fam"] for v in pk.values()]
    peov = [v["people_mean"] for v in pk.values()]
    rho = r.get("rho_family_people", (r.get("P0_PREMISE") or {}).get("rho_family_people"))
    lev = round((st.mean(peov) - st.mean(famv)) / rng, 3)
    for arm in ("B", "S"):
        rows.append({
            "exp": n, "work": d, "arm": arm,
            "told": "people's true values on 24 other keys" if arm == "B"
                    else "the same 24 values dealt to the wrong keys",
            "range": rng, "contact_keys": 24,
            "level_departure_frac": lev if arm == "B" else round(lev, 3),
            "contact_order_vs_family": (f"agrees (rho family-people {rho} on scored keys)" if arm == "B"
                                        else "broken by construction (|rho| <= 0.1 with the truth)"),
            "family_order_sd_frac": sd_frac(famv, rng),
            "named_misfit": coded[arm], "of": 6,
            "named_by": "committed coding" + (" (S2 arguable: 5 if counted)" if n == 45 and arm == "S" else "")})

LEVEL = ("43C", "44M", "44U", "45B", "47B")
WIDE = ("45S", "47S")
FLAT = ("46B", "46S")


def tally(ids):
    sel = [x for x in rows if f'{x["exp"]}{x["arm"]}' in ids]
    return {"arms": list(ids), "named": sum(x["named_misfit"] for x in sel), "of": sum(x["of"] for x in sel)}


summary = {
    # contact that departs from the family in level and leaves its order standing (or can barely touch it)
    "level_departing_order_kept": tally(LEVEL),
    # contact whose order breaks an order the family holds widely (shuffled pairs)
    "order_breaking_against_wide_order": tally(WIDE),
    # contact whose order departs from the family's, where the family's order is nearly flat:
    # 46B true (rho 0.169 with the family), 46S shuffled
    "order_departing_against_flat_order": tally(FLAT),
}

json.dump({"rows": rows, "summary": summary}, open(OUT / "results.json", "w"), indent=1)
lines = ["exp arm  level  famSD  named  contact"]
for x in rows:
    lines.append(f'{x["exp"]:>3} {x["arm"]:>3} {x["level_departure_frac"]!s:>6} {x["family_order_sd_frac"]:>6} '
                 f'{x["named_misfit"]}/{x["of"]}   {x["told"]}')
lines.append("")
for k, v in summary.items():
    lines.append(f'{k}: {v["named"]} of {v["of"]}  ({", ".join(v["arms"])})')
txt = "\n".join(lines)
(OUT / "audit.txt").write_text(txt + "\n")
print(txt)
for x in rows:
    if "screen_hits" in x:
        print(x["exp"], x["arm"], "keyword screen hits per hand-back:", x["screen_hits"])
