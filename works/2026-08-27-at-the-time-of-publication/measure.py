#!/usr/bin/env python3
"""measure.py — Session 72, 2026-08-27.

Offline. Reads only what harvest.py wrote into the raw cache and emits
results.json, which every number in work.md comes out of. No network.

The object: 8,021 errata reported against published RFCs, and the RFC index they
point into. The question the night asks of them is Session 71's open thread 1 —
whether two norms crossing over one difference is a property of norms or a
property of software review.

Declared precision limits, in the file that produces the numbers:

  * rfc-index.xml dates RFCs to a MONTH, not a day. Every publication date here
    is read as the first day of that month. Where a comparison is within one
    month of a boundary the result is reported as such, never rounded silently.
  * `section` is free text as the submitter typed it; it is used only as part of
    a grouping key, never parsed.
  * An erratum's `doc-id` is the RFC it was reported against; RFCs are never
    edited after publication, so that join is stable.

Usage:
    python3 measure.py --raw ../../.raw --out results.json
"""

import argparse
import collections
import datetime
import json
import re
import statistics
import unicodedata
import sys
import xml.etree.ElementTree as ET

TONIGHT = datetime.date(2026, 8, 27)
NS = {"r": "https://www.rfc-editor.org/rfc-index"}

# One record in the source carries an impossible date and is quarantined from every
# statistic that uses dates — named here rather than filtered silently, and reported
# in results.json under "quarantine". Erratum 6534 against RFC 2367 is dated
# `submit_date: 9999-04-13` and `update_date: 2021-04-13`: the verdict precedes the
# report by 7,978 years. It is displayed that way on the RFC Editor's own page
# (https://www.rfc-editor.org/errata/eid6534). Left in, it moved three of this night's
# means by more than half their value. It stays in every count; it leaves every mean.
QUARANTINE = {"6534"}

# The two dated versions of the written norm for the IETF stream.
NORM_2008 = datetime.date(2008, 7, 30)
NORM_2021 = datetime.date(2021, 5, 7)

MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}


def norm_text(s):
    """The normalisation named in PREDICTIONS.md: strip, collapse whitespace, casefold."""
    return re.sub(r"\s+", " ", (s or "").strip()).casefold()


def parse_day(s):
    if not s:
        return None
    try:
        return datetime.datetime.strptime(s.strip()[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def load_index(path):
    """doc-id -> {date, stream, status, obsoleted_by[], updated_by[]}"""
    root = ET.parse(path).getroot()
    out = {}
    for e in root.findall("r:rfc-entry", NS):
        did = e.findtext("r:doc-id", default="", namespaces=NS)
        d = e.find("r:date", NS)
        date = None
        if d is not None:
            y = d.findtext("r:year", namespaces=NS)
            m = d.findtext("r:month", namespaces=NS)
            if y and m in MONTHS:
                date = datetime.date(int(y), MONTHS[m], 1)
        out[did] = {
            "date": date,
            "stream": e.findtext("r:stream", default="", namespaces=NS),
            "status": e.findtext("r:current-status", default="", namespaces=NS),
            "obsoleted_by": [x.text for x in e.findall("r:obsoleted-by/r:doc-id", NS)],
            "updated_by": [x.text for x in e.findall("r:updated-by/r:doc-id", NS)],
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="../../.raw")
    ap.add_argument("--out", default="results.json")
    args = ap.parse_args()

    errata = json.load(open(f"{args.raw}/errata.json"))
    index = load_index(f"{args.raw}/rfc-index.xml")
    R = {"tonight": TONIGHT.isoformat(), "n_errata": len(errata), "n_rfcs": len(index)}

    # The quarantine, declared in the results before anything is computed from dates.
    q = [e for e in errata if e["errata_id"] in QUARANTINE]
    R["quarantine"] = {
        "reason": "impossible date in the source; excluded from every statistic over dates, "
                  "kept in every count",
        "records": [{"id": e["errata_id"], "doc": e["doc-id"], "status": e["errata_status_code"],
                     "type": e["errata_type_code"], "submit_date": e["submit_date"],
                     "update_date": e["update_date"], "section": e.get("section"),
                     "page": f"https://www.rfc-editor.org/errata/eid{e['errata_id']}"} for e in q],
    }
    dated = [e for e in errata if e["errata_id"] not in QUARANTINE]

    # ---------------------------------------------------------------- tallies
    R["status"] = dict(collections.Counter(e["errata_status_code"] for e in errata))
    R["type"] = dict(collections.Counter(e["errata_type_code"] for e in errata))
    R["status_by_type"] = {
        t: dict(collections.Counter(e["errata_status_code"] for e in errata
                                    if e["errata_type_code"] == t))
        for t in sorted({e["errata_type_code"] for e in errata})}

    R["errata_docs"] = len({e["doc-id"] for e in errata})
    R["docs_not_in_index"] = sorted({e["doc-id"] for e in errata} - set(index))

    # ------------------------------------------------- P1: the same difference
    groups = collections.defaultdict(list)
    for e in errata:
        key = (e["doc-id"], norm_text(e.get("section")), norm_text(e.get("orig_text")))
        if key[2]:                      # empty orig_text excluded, as declared
            groups[key].append(e)
    multi = {k: v for k, v in groups.items() if len(v) > 1}
    divergent = {k: v for k, v in multi.items()
                 if len({x["errata_status_code"] for x in v}) > 1}
    hard = {k: v for k, v in divergent.items()
            if "Rejected" in {x["errata_status_code"] for x in v}
            and {"Verified", "Held for Document Update"} & {x["errata_status_code"] for x in v}}
    R["P1"] = {
        "groups_with_key": len(groups),
        "groups_multi": len(multi),
        "errata_in_multi": sum(len(v) for v in multi.values()),
        "groups_divergent": len(divergent),
        "groups_rejected_vs_accepted": len(hard),
        "divergent_pairs_by_statuses": dict(collections.Counter(
            " / ".join(sorted({x["errata_status_code"] for x in v}))
            for v in divergent.values())),
        "examples": sorted(
            [{"doc": k[0], "section": v[0].get("section"),
              "orig_len": len(v[0].get("orig_text") or ""),
              "orig_head": (v[0].get("orig_text") or "")[:180],
              "members": [{"id": x["errata_id"], "status": x["errata_status_code"],
                           "type": x["errata_type_code"], "submitted": x["submit_date"],
                           "verifier": x.get("verifier_name"),
                           "correct_head": (x.get("correct_text") or "")[:180]}
                          for x in sorted(v, key=lambda y: int(y["errata_id"]))]}
             for k, v in hard.items()],
            key=lambda g: g["orig_len"])[:12],
    }

    # P1, second pass: a divergent group is not automatically two observers. Split the
    # 44 hard groups three ways — different reviewer; the SAME reviewer at two different
    # moments; the same reviewer on one day (a workflow artefact, not a disagreement).
    def who(x):
        """A reviewer's identity, as the record gives it — and as it has to be repaired.

        The record identifies a reviewer by display string. Two of the divergent groups
        found below carry the SAME person under two strings ('Éric Vyncke' / 'Eric Vyncke',
        'Eliot Lear (ISE)' / 'Eliot Lear'), and a first pass counted them as two observers.
        So: strip a parenthetical role suffix, fold accents, casefold. This is a repair with
        a cost, declared: it would also merge two different people who share a spelling.
        Both the raw and the folded classification are reported.
        """
        s = (x.get("verifier_name") or "").strip()
        s = re.sub(r"\s*\([^)]*\)\s*$", "", s)
        s = unicodedata.normalize("NFKD", s)
        return "".join(c for c in s if not unicodedata.combining(c)).casefold()

    def cls(v, fold=True):
        key = who if fold else (lambda x: (x.get("verifier_name") or "").strip())
        names = {key(x) for x in v if (x.get("verifier_name") or "").strip()}
        days = {parse_day(x.get("update_date")) for x in v if parse_day(x.get("update_date"))}
        if len(names) > 1:
            return "different reviewer"
        if len(names) == 1 and len(days) > 1:
            return "same reviewer, different day"
        if len(names) == 1:
            return "same reviewer, same day"
        return "no reviewer recorded"

    def gap(v):
        subs = [parse_day(x["submit_date"]) for x in v if parse_day(x["submit_date"])]
        return (max(subs) - min(subs)).days if len(subs) > 1 else None

    R["P1"]["hard_group_classes"] = dict(collections.Counter(cls(v) for v in hard.values()))
    R["P1"]["hard_group_classes_unfolded_names"] = dict(collections.Counter(
        cls(v, fold=False) for v in hard.values()))
    R["P1"]["name_folding_moved"] = sum(
        1 for v in hard.values() if cls(v) != cls(v, fold=False))
    R["P1"]["hard_group_submission_gap_days"] = sorted(
        [g for g in (gap(v) for v in hard.values()) if g is not None])
    R["P1"]["hard_groups"] = sorted(
        [{"doc": k[0], "section": v[0].get("section"),
          "orig_len": len(v[0].get("orig_text") or ""),
          "class": cls(v), "submission_gap_days": gap(v),
          "members": [{"id": x["errata_id"], "status": x["errata_status_code"],
                       "type": x["errata_type_code"], "submitted": x["submit_date"],
                       "adjudicated": (x.get("update_date") or "")[:10],
                       "verifier": x.get("verifier_name")}
                      for x in sorted(v, key=lambda y: int(y["errata_id"]))]}
         for k, v in hard.items()],
        key=lambda g: (g["class"], -(g["submission_gap_days"] or 0)))

    # P1, third pass — the decisive one, and it was not predicted.
    #
    # Verifying two of the divergent groups against the RFC Editor's own pages showed that
    # the members share the reported difference (`orig_text`) and differ in the CORRECTION
    # they propose (`correct_text`). So the grouping above establishes "one difference, two
    # verdicts" and NOT "one claim, two verdicts". Tighten the key to include the proposed
    # correction: if divergence survives, the verdict is not a function of the pair either.
    pair_groups = collections.defaultdict(list)
    for e in errata:
        key = (e["doc-id"], norm_text(e.get("section")),
               norm_text(e.get("orig_text")), norm_text(e.get("correct_text")))
        if key[2] and key[3]:
            pair_groups[key].append(e)
    pair_multi = {k: v for k, v in pair_groups.items() if len(v) > 1}
    pair_div = {k: v for k, v in pair_multi.items()
                if len({x["errata_status_code"] for x in v}) > 1}
    pair_hard = {k: v for k, v in pair_div.items()
                 if "Rejected" in {x["errata_status_code"] for x in v}
                 and {"Verified", "Held for Document Update"} & {x["errata_status_code"] for x in v}}
    R["P1_pairs"] = {
        "note": "key = doc + section + orig_text + correct_text: the same difference AND the "
                "same proposed repair.",
        "groups_multi": len(pair_multi),
        "groups_divergent": len(pair_div),
        "groups_rejected_vs_accepted": len(pair_hard),
        "classes": dict(collections.Counter(cls(v) for v in pair_hard.values())),
        "groups": sorted(
            [{"doc": k[0], "section": v[0].get("section"),
              "orig_len": len(v[0].get("orig_text") or ""),
              "class": cls(v), "submission_gap_days": gap(v),
              "members": [{"id": x["errata_id"], "status": x["errata_status_code"],
                           "type": x["errata_type_code"], "submitted": x["submit_date"],
                           "adjudicated": (x.get("update_date") or "")[:10],
                           "verifier": x.get("verifier_name"),
                           "page": f"https://www.rfc-editor.org/errata/eid{x['errata_id']}"}
                          for x in sorted(v, key=lambda y: int(y["errata_id"]))]}
             for k, v in pair_div.items()],
            key=lambda g: -(g["submission_gap_days"] or 0)),
    }

    # ----------------------------- P2: the verdict that names a future event
    hfdu = [e for e in dated if e["errata_status_code"] == "Held for Document Update"]
    no_occasion, occasion, unjoinable, within_month = [], [], [], 0
    for e in hfdu:
        sub = parse_day(e["submit_date"])
        meta = index.get(e["doc-id"])
        if not sub or not meta:
            unjoinable.append(e["errata_id"])
            continue
        successors = [index.get(d) for d in meta["obsoleted_by"] + meta["updated_by"]]
        later = [s for s in successors if s and s["date"] and s["date"] > sub]
        near = [s for s in successors if s and s["date"]
                and abs((s["date"] - sub).days) <= 31 and s["date"] <= sub]
        if later:
            occasion.append(e["errata_id"])
        else:
            no_occasion.append(e["errata_id"])
            if near:
                within_month += 1
    ages = sorted(((TONIGHT - parse_day(e["submit_date"])).days / 365.2425)
                  for e in hfdu if e["errata_id"] in set(no_occasion) and parse_day(e["submit_date"]))
    R["P2"] = {
        "hfdu": len(hfdu),
        "no_revision_since": len(no_occasion),
        "revised_since": len(occasion),
        "unjoinable": len(unjoinable),
        "share_no_revision": round(len(no_occasion) / len(hfdu), 4),
        "within_one_month_of_boundary": within_month,
        "age_years_of_unfulfilled": {
            "median": round(statistics.median(ages), 2) if ages else None,
            "mean": round(statistics.fmean(ages), 2) if ages else None,
            "max": round(max(ages), 2) if ages else None,
            "over_10y": sum(1 for a in ages if a > 10),
            "over_15y": sum(1 for a in ages if a > 15),
        },
    }

    # ----------------------------------- P3: the queue with no norm on it yet
    def age_stats(subset):
        a = sorted((TONIGHT - parse_day(e["submit_date"])).days / 365.2425
                   for e in subset if parse_day(e["submit_date"]))
        if not a:
            return None
        return {"n": len(a), "median": round(statistics.median(a), 2),
                "mean": round(statistics.fmean(a), 2),
                "max": round(a[-1], 2), "min": round(a[0], 2),
                "over_2y": sum(1 for x in a if x > 2),
                "over_5y": sum(1 for x in a if x > 5),
                "over_12y": sum(1 for x in a if x > 12)}

    reported = [e for e in dated if e["errata_status_code"] == "Reported"]
    R["P3"] = {
        "reported": age_stats(reported),
        "by_type": {t: age_stats([e for e in reported if e["errata_type_code"] == t])
                    for t in sorted({e["errata_type_code"] for e in reported})},
        "for_comparison_all": age_stats(dated),
        "oldest_ten": [{"id": e["errata_id"], "doc": e["doc-id"], "submitted": e["submit_date"],
                        "type": e["errata_type_code"], "section": e.get("section"),
                        "orig_len": len(e.get("orig_text") or "")}
                       for e in sorted(reported, key=lambda x: x["submit_date"])[:10]],
        "submitted_per_year": dict(sorted(collections.Counter(
            e["submit_date"][:4] for e in reported).items())),
    }

    # ------------------------------ P4: is the moment of judgement datable?
    days = collections.Counter((e.get("update_date") or "")[:10] for e in errata)
    top_day, top_n = days.most_common(1)[0]
    R["P4"] = {
        "distinct_update_days": len(days),
        "top_day": top_day,
        "top_day_n": top_n,
        "top_day_share": round(top_n / len(errata), 4),
        "top_five": days.most_common(5),
        "missing_update_date": sum(1 for e in errata if not (e.get("update_date") or "").strip()),
        "update_before_submit": sum(
            1 for e in errata
            if parse_day(e.get("update_date")) and parse_day(e["submit_date"])
            and parse_day(e["update_date"]) < parse_day(e["submit_date"])),
    }
    # If update_date survives as a verdict date for the post-migration era, use it there.
    post = [e for e in dated
            if parse_day(e.get("update_date")) and parse_day(e["submit_date"])
            and parse_day(e["update_date"]) > parse_day(top_day)
            and e["errata_status_code"] != "Reported"]
    waits = sorted((parse_day(e["update_date"]) - parse_day(e["submit_date"])).days
                   for e in post)
    R["P4"]["post_migration_wait_days"] = {
        "n": len(waits),
        "median": statistics.median(waits) if waits else None,
        "mean": round(statistics.fmean(waits), 1) if waits else None,
        "max": max(waits) if waits else None,
        "over_1y": sum(1 for w in waits if w > 365),
    } if waits else None
    R["P4"]["post_migration_by_status"] = {
        s: (lambda w: {"n": len(w), "median": statistics.median(w)} if w else None)(
            sorted((parse_day(e["update_date"]) - parse_day(e["submit_date"])).days
                   for e in post if e["errata_status_code"] == s))
        for s in sorted({e["errata_status_code"] for e in post})}

    # --------------------------- one verdict, more than one relation to a norm
    #
    # The RFC Editor defines Rejected as "The erratum was redundant or incorrect and has
    # been discarded"; the IESG's 2021 statement defines it as "The erratum is invalid or
    # proposes a significant change to the RFC that should be done by publishing a new RFC".
    # Those are not one relation. Under the standing position they are three:
    #   (a) there is no difference — the report is invalid;
    #   (b) there is a difference and it is not an error under this norm — a change proposal;
    #   (c) there is a difference, it IS an error, and it is already recorded — redundant.
    # The record gives all three the same code. This block puts a floor under (b) and (c)
    # using the reviewers' own notes, which the dump appends after a "--VERIFIER NOTES--"
    # marker. Keyword rules are conservative, stated here in full, and deliberately
    # NON-exhaustive: they establish a lower bound, never a partition.
    rejected = [e for e in dated if e["errata_status_code"] == "Rejected"]
    MARK = re.compile(r"--\s*VERIFIER NOTES\s*--", re.I)
    RE_REDUNDANT = re.compile(
        r"\b(duplicate|redundant|already (been )?(reported|submitted|filed|verified|"
        r"covered|addressed)|same as (errata|erratum|eid)|see (errata|erratum|eid))\b", re.I)
    RE_CHANGE = re.compile(
        r"(not an error|no error|is not errata|errata (are|is) not|not errata material|"
        r"new rfc|revision of the (rfc|document)|-bis\b|working group|wg (list|mailing)|"
        r"future update|update to the (rfc|document)|change to the protocol|"
        r"changes the protocol|new document)", re.I)

    def note_of(e):
        t = e.get("notes") or ""
        m = MARK.search(t)
        return t[m.end():] if m else ""

    with_note = [e for e in rejected if note_of(e).strip()]
    red = [e for e in with_note if RE_REDUNDANT.search(note_of(e))]
    chg = [e for e in with_note if RE_CHANGE.search(note_of(e))]
    R["rejected_reasons"] = {
        "rejected": len(rejected),
        "with_verifier_note": len(with_note),
        "share_with_note": round(len(with_note) / len(rejected), 4),
        "matches_redundant": len(red),
        "matches_change_not_error": len(chg),
        "matches_both": len([e for e in red if e in chg]),
        "matches_either": len({e["errata_id"] for e in red} | {e["errata_id"] for e in chg}),
        "share_either_of_rejected": round(
            len({e["errata_id"] for e in red} | {e["errata_id"] for e in chg}) / len(rejected), 4),
        "regex_redundant": RE_REDUNDANT.pattern,
        "regex_change": RE_CHANGE.pattern,
        "caveat": "Keyword rules over reviewers' free text. A lower bound on (b) and (c), "
                  "not a classification: a rejection that says neither may still be either, "
                  "and a match is not proof. Counted, never quoted in bulk.",
    }
    # A second, text-independent floor under (c): a Rejected erratum whose identical
    # normalised orig_text was already accepted on the same document and section, earlier.
    floor_c = 0
    for k, v in multi.items():
        acc = [x for x in v if x["errata_status_code"] in ("Verified", "Held for Document Update")
               and parse_day(x["submit_date"])]
        for x in v:
            if x["errata_status_code"] == "Rejected" and parse_day(x["submit_date"]):
                if any(parse_day(a["submit_date"]) < parse_day(x["submit_date"]) for a in acc):
                    floor_c += 1
    R["rejected_reasons"]["floor_c_identical_text_already_accepted"] = floor_c

    # ------------------------------------- who is looking: the four streams
    by_stream = collections.defaultdict(collections.Counter)
    for e in errata:
        meta = index.get(e["doc-id"])
        by_stream[meta["stream"] if meta else "(not in index)"][e["errata_status_code"]] += 1
    R["streams"] = {s: dict(c) for s, c in sorted(by_stream.items())}
    R["stream_rates"] = {
        s: {"n": sum(c.values()),
            "rejected": round(c["Rejected"] / sum(c.values()), 4),
            "verified": round(c["Verified"] / sum(c.values()), 4),
            "hfdu": round(c["Held for Document Update"] / sum(c.values()), 4),
            "pending": round(c["Reported"] / sum(c.values()), 4)}
        for s, c in sorted(by_stream.items()) if sum(c.values()) >= 25}

    # ------------------------------------------- the norm has a date, too
    def era(d):
        if d is None:
            return "undated"
        if d < NORM_2008:
            return "before 2008-07-30"
        if d < NORM_2021:
            return "2008 statement"
        return "2021 statement"
    eras = collections.defaultdict(collections.Counter)
    for e in dated:
        eras[era(parse_day(e["submit_date"]))][e["errata_status_code"]] += 1
    R["eras_by_submission"] = {
        k: {"n": sum(c.values()), **{s: c[s] for s in
            ["Verified", "Held for Document Update", "Rejected", "Reported"]},
            "hfdu_share": round(c["Held for Document Update"] / sum(c.values()), 4),
            "rejected_share": round(c["Rejected"] / sum(c.values()), 4)}
        for k, c in eras.items()}

    # ---------------- how far the difference is from the document it is about
    lags = []
    for e in dated:
        sub, meta = parse_day(e["submit_date"]), index.get(e["doc-id"])
        if sub and meta and meta["date"]:
            lags.append((sub - meta["date"]).days / 365.2425)
    lags.sort()
    R["lag_publication_to_report_years"] = {
        "n": len(lags), "median": round(statistics.median(lags), 2),
        "mean": round(statistics.fmean(lags), 2), "max": round(lags[-1], 2),
        "min": round(lags[0], 2),
        "over_10y": sum(1 for x in lags if x > 10),
        "over_20y": sum(1 for x in lags if x > 20),
        "negative": sum(1 for x in lags if x < 0),
    }

    # errata against RFCs that have already been superseded
    obsolete_docs = {d for d, m in index.items() if m["obsoleted_by"]}
    R["errata_on_obsoleted_rfcs"] = {
        "n": sum(1 for e in errata if e["doc-id"] in obsolete_docs),
        "by_status": dict(collections.Counter(
            e["errata_status_code"] for e in errata if e["doc-id"] in obsolete_docs)),
    }

    json.dump(R, open(args.out, "w"), indent=1, default=str)
    print(json.dumps({k: v for k, v in R.items()
                      if k in ("status", "P1", "P2", "P3", "P4")}, indent=1, default=str)[:6000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
