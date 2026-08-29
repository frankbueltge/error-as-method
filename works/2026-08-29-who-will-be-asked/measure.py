#!/usr/bin/env python3
"""measure.py — Session 74, 2026-08-29.

Offline and stdlib-only. It reads the raw cache `harvest.py` wrote and writes `results.json`.
Nothing here fetches anything; nothing here is fetched from.

It answers, in this order:

  P5  is the window clean — does it carry either of this record's two known migrations?
  P1  does the reporter's own type choice predict whether a norm is ever imposed?
  P2  on the branch the policy actually names, does the norm arrive?
  P3  is the type in the field the one the person filing put there?
  P4  is the address revised much more often than the branch?

and then the things nobody predicted, which is where the last three nights found their results.

The method rule, from PREDICTIONS.md: this file derives **no** threshold of lateness from the
distribution. Where it says `late`, it means past the one week Mozilla's own policy names.

Usage:
    python3 measure.py --raw ../../../.raw
"""

import argparse
import collections
import datetime
import json
import os
import statistics
import sys

TODAY = datetime.datetime(2026, 8, 29, tzinfo=datetime.timezone.utc)
WEEK = 7.0

OLD_SEVERITIES = {"blocker", "critical", "major", "normal", "minor", "trivial", "enhancement"}
NEW_SEVERITIES = {"--", "N/A", "S1", "S2", "S3", "S4"}
CLOSED = {"RESOLVED", "VERIFIED", "CLOSED"}
TYPES = ["defect", "enhancement", "task", "--"]


HIST_EDGES = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]


def histogram(days):
    """Counts in doubling day-bins. Doubling because the spread runs from same-day to years, and
    a linear axis would put every branch's mass in the first pixel."""
    out = [0] * (len(HIST_EDGES) + 1)
    for value in days:
        placed = False
        for i, edge in enumerate(HIST_EDGES):
            if value <= edge:
                out[i] += 1
                placed = True
                break
        if not placed:
            out[-1] += 1
    return out


def parse(ts):
    if not ts:
        return None
    return datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=datetime.timezone.utc)


def pct(part, whole):
    return round(100.0 * part / whole, 2) if whole else None


def share_table(bugs, key):
    """For each value of `key`: how many, how many still un-normed, how many N/A, how many
    satisfy the institution's own three-part definition of Triaged."""
    out = {}
    groups = collections.defaultdict(list)
    for b in bugs:
        groups[b.get(key) or "--"].append(b)
    for value, rows in groups.items():
        n = len(rows)
        unnormed = sum(1 for b in rows if b["severity"] == "--")
        na = sum(1 for b in rows if b["severity"] == "N/A")
        triaged = sum(1 for b in rows
                      if b["type"] == "defect"
                      and b["component"] != "Untriaged"
                      and b["severity"] not in ("--", "N/A"))
        opened = [b for b in rows if b["status"] not in CLOSED]
        out[value] = {
            "n": n,
            "unnormed": unnormed,
            "unnormed_pct": pct(unnormed, n),
            "na": na,
            "na_pct": pct(na, n),
            "triaged_by_policy": triaged,
            "triaged_by_policy_pct": pct(triaged, n),
            "open": len(opened),
            "open_unnormed": sum(1 for b in opened if b["severity"] == "--"),
            "open_unnormed_pct": pct(sum(1 for b in opened if b["severity"] == "--"), len(opened)),
        }
    return dict(sorted(out.items(), key=lambda kv: -kv[1]["n"]))


def measure(raw):
    with open(os.path.join(raw, "population.json"), encoding="utf-8") as fh:
        bugs = json.load(fh)
    res = {
        "night": "2026-08-29",
        "session": 74,
        "measured_utc": TODAY.isoformat(),
        "population": {
            "n": len(bugs),
            "window": ["2024-01-01", "2025-07-01"],
            "products": sorted({b["product"] for b in bugs}),
            "note": "publicly visible bugs only; security bugs are hidden from an "
                    "unauthenticated client and are not in this population",
        },
    }

    ages = [(TODAY - parse(b["creation_time"])).days for b in bugs]
    res["population"]["min_age_days"] = min(ages)
    res["population"]["max_age_days"] = max(ages)
    res["population"]["min_age_weeks_vs_policy"] = round(min(ages) / WEEK, 1)

    # ---------------------------------------------------------------- P5 (a)
    sev_counts = collections.Counter(b["severity"] for b in bugs)
    old_in_window = {s: n for s, n in sev_counts.items() if s in OLD_SEVERITIES}
    unknown = {s: n for s, n in sev_counts.items()
               if s not in OLD_SEVERITIES and s not in NEW_SEVERITIES}
    res["P5a_vocabulary"] = {
        "claim": "zero bugs in W carry a pre-2020 severity value",
        "severity_counts": dict(sev_counts.most_common()),
        "pre_2020_values_present": old_in_window,
        "pre_2020_total": sum(old_in_window.values()),
        "values_outside_both_vocabularies": unknown,
        "won": sum(old_in_window.values()) == 0 and not unknown,
    }
    res["type_counts"] = dict(collections.Counter(b["type"] for b in bugs).most_common())

    # ---------------------------------------------------------------- P1, P2
    by_type = share_table(bugs, "type")
    res["by_type"] = by_type
    d = by_type.get("defect", {})
    e = by_type.get("enhancement", {})
    t = by_type.get("task", {})
    gap = None
    if d.get("unnormed_pct") is not None and e.get("unnormed_pct") is not None:
        gap = round(e["unnormed_pct"] - d["unnormed_pct"], 2)
    gap_open = None
    if d.get("open_unnormed_pct") is not None and e.get("open_unnormed_pct") is not None:
        gap_open = round(e["open_unnormed_pct"] - d["open_unnormed_pct"], 2)
    res["P1_routing_gap"] = {
        "claim": "unnormed%(enhancement) - unnormed%(defect) >= 15 pp, enhancement higher",
        "defect_unnormed_pct": d.get("unnormed_pct"),
        "enhancement_unnormed_pct": e.get("unnormed_pct"),
        "task_unnormed_pct": t.get("unnormed_pct"),
        "gap_pp": gap,
        "gap_pp_open_only": gap_open,
        "won": gap is not None and gap >= 15.0,
    }
    res["P2_norm_arrives_on_defect"] = {
        "claim": "unnormed% for type=defect < 10%",
        "value": d.get("unnormed_pct"),
        "n": d.get("n"),
        "won": d.get("unnormed_pct") is not None and d["unnormed_pct"] < 10.0,
    }

    # the reporter's other box: the component, and the one that means "I don't know"
    res["by_product"] = share_table(bugs, "product")
    untriaged_component = [b for b in bugs if b["component"] == "Untriaged"]
    res["untriaged_component"] = {
        "n": len(untriaged_component),
        "pct_of_W": pct(len(untriaged_component), len(bugs)),
        "unnormed_pct": pct(sum(1 for b in untriaged_component if b["severity"] == "--"),
                            len(untriaged_component)),
        "by_type": dict(collections.Counter(b["type"] for b in untriaged_component).most_common()),
        "what": "the component a reporter picks when they decline to name a desk; "
                "the policy's definition of Triaged excludes it by name",
    }

    # disposal: is the gap about norms, or about enhancements being closed unread?
    disposal = {}
    for typ in TYPES:
        rows = [b for b in bugs if b["type"] == typ]
        if not rows:
            continue
        closed = [b for b in rows if b["status"] in CLOSED]
        closed_unnormed = [b for b in closed if b["severity"] == "--"]
        res_counts = collections.Counter(b["resolution"] for b in closed)
        disposal[typ] = {
            "n": len(rows),
            "closed": len(closed),
            "closed_pct": pct(len(closed), len(rows)),
            "closed_without_a_severity": len(closed_unnormed),
            "closed_without_a_severity_pct": pct(len(closed_unnormed), len(closed)),
            "resolutions": dict(res_counts.most_common(8)),
        }
    res["disposal_by_type"] = disposal

    # The three stages the figure draws, as counts: what the filer chose, what norm state the bug
    # is in today, and what happened to it. Fate is read off the institution's own status and
    # resolution vocabulary and not invented here.
    def norm_state(bug):
        if bug["severity"] == "--":
            return "none"
        if bug["severity"] == "N/A":
            return "N/A"
        return "severity"

    def fate(bug):
        if bug["status"] not in CLOSED:
            return "still open"
        return "fixed" if bug["resolution"] == "FIXED" else "closed otherwise"

    stage1 = collections.Counter(b["type"] for b in bugs)
    stage2 = collections.Counter((b["type"], norm_state(b)) for b in bugs)
    stage3 = collections.Counter((norm_state(b), fate(b)) for b in bugs)
    res["flow"] = {
        "total": len(bugs),
        "by_type": dict(stage1.most_common()),
        "type_to_norm_state": {f"{t}|{s}": n for (t, s), n in sorted(stage2.items())},
        "norm_state_to_fate": {f"{s}|{f}": n for (s, f), n in sorted(stage3.items())},
        "fate_of_the_unnormed": {
            f: n for (s, f), n in sorted(stage3.items()) if s == "none"},
        "fate_by_norm_state_and_type": {
            f"{t}|{s}|{f}": n for (t, s, f), n in sorted(collections.Counter(
                (b["type"], norm_state(b), fate(b)) for b in bugs).items())},
    }

    # P5(a) lost by twelve bugs. Does removing them move anything the argument uses?
    clean = [b for b in bugs if b["severity"] in NEW_SEVERITIES]
    clean_by_type = share_table(clean, "type")
    res["P5a_sensitivity"] = {
        "what": "every share above, recomputed with the pre-2020-vocabulary bugs dropped",
        "dropped": len(bugs) - len(clean),
        "defect_unnormed_pct": clean_by_type.get("defect", {}).get("unnormed_pct"),
        "enhancement_unnormed_pct": clean_by_type.get("enhancement", {}).get("unnormed_pct"),
        "gap_pp": round(clean_by_type["enhancement"]["unnormed_pct"]
                        - clean_by_type["defect"]["unnormed_pct"], 2)
        if "enhancement" in clean_by_type and "defect" in clean_by_type else None,
        "the_twelve": [{"id": b["id"], "severity": b["severity"], "type": b["type"],
                        "product": b["product"], "creation_time": b["creation_time"],
                        "status": b["status"]}
                       for b in bugs if b["severity"] in OLD_SEVERITIES],
    }

    # what the un-normed defects are: a norm not arriving, or a report that died before it could
    closed_unnormed_res = collections.Counter(
        b["resolution"] for b in bugs
        if b["type"] == "defect" and b["severity"] == "--" and b["status"] in CLOSED)
    res["unnormed_defects"] = {
        "n": sum(1 for b in bugs if b["type"] == "defect" and b["severity"] == "--"),
        "closed": sum(closed_unnormed_res.values()),
        "closed_resolutions": dict(closed_unnormed_res.most_common(8)),
        "still_open": sum(1 for b in bugs if b["type"] == "defect" and b["severity"] == "--"
                          and b["status"] not in CLOSED),
    }

    # the second pass: is the filer the person the work is assigned to?
    creators_path = os.path.join(raw, "creators.json")
    if os.path.exists(creators_path):
        with open(creators_path, encoding="utf-8") as fh:
            creators = {row["id"]: row for row in json.load(fh)}
        self_filed = {}
        for typ in TYPES:
            rows = [creators[b["id"]] for b in bugs
                    if b["type"] == typ and b["id"] in creators]
            if not rows:
                continue
            same = sum(1 for r in rows
                       if r.get("assigned_to") and r["assigned_to"] == r.get("creator"))
            unassigned = sum(1 for r in rows if r.get("assigned_to") == "nobody@mozilla.org")
            self_filed[typ] = {
                "n": len(rows),
                "filer_is_assignee": same,
                "filer_is_assignee_pct": pct(same, len(rows)),
                "assigned_to_nobody": unassigned,
                "assigned_to_nobody_pct": pct(unassigned, len(rows)),
                "distinct_filers": len({r.get("creator") for r in rows}),
            }
        # The control the confound demands: recompute P1's gap on the subset in which the filer
        # is demonstrably not the person the work sits with, i.e. the reports that really are a
        # difference handed to somebody else. Crude -- assignment is read at today's value, not at
        # filing -- and reported as crude.
        controls = {}
        for name, keep in (
            ("filer_is_not_the_assignee",
             lambda r: r.get("assigned_to") != r.get("creator")),
            ("assigned_to_nobody",
             lambda r: r.get("assigned_to") == "nobody@mozilla.org"),
        ):
            subset = [b for b in bugs
                      if b["id"] in creators and keep(creators[b["id"]])]
            table = share_table(subset, "type")
            controls[name] = {
                "n": len(subset),
                "defect_unnormed_pct": table.get("defect", {}).get("unnormed_pct"),
                "enhancement_unnormed_pct": table.get("enhancement", {}).get("unnormed_pct"),
                "task_unnormed_pct": table.get("task", {}).get("unnormed_pct"),
                "gap_pp": round(table["enhancement"]["unnormed_pct"]
                                - table["defect"]["unnormed_pct"], 2)
                if "enhancement" in table and "defect" in table else None,
                "n_by_type": {k: v["n"] for k, v in table.items()},
            }
        res["who_files_what"] = {
            "what": "the confound the predictions did not see: a task may be an engineer writing "
                    "themselves a work item rather than a difference reported to somebody else. "
                    "Second pass, after the predictions were scored.",
            "by_type": self_filed,
            "controls": controls,
        }

    # time to resolution, for the branches that reach one at all
    ttr = {}
    for typ in TYPES:
        days = [(parse(b["cf_last_resolved"]) - parse(b["creation_time"])).days
                for b in bugs
                if b["type"] == typ and b.get("cf_last_resolved") and b["status"] in CLOSED]
        days = [x for x in days if x >= 0]
        if len(days) >= 20:
            days.sort()
            ttr[typ] = {
                "n": len(days),
                "median_days": statistics.median(days),
                "p25": days[len(days) // 4],
                "p75": days[3 * len(days) // 4],
                "deciles": [days[min(len(days) - 1, (len(days) * k) // 10)] for k in range(11)],
                "within_7_days": sum(1 for x in days if x <= 7),
                "within_7_days_pct": pct(sum(1 for x in days if x <= 7), len(days)),
                "histogram_bins_days": HIST_EDGES,
                "histogram": histogram(days),
            }
    res["time_to_resolution_by_type"] = ttr

    # ------------------------------------------------------------ P3, P4, P5b
    hist_path = os.path.join(raw, "history.json")
    if os.path.exists(hist_path):
        with open(hist_path, encoding="utf-8") as fh:
            hist = json.load(fh)
        res.update(measure_history(hist, bugs))

    # ---------------------------------------------------- the named population
    # what a dated falsifier needs: bugs that are open, past the policy's week many times over,
    # and still carry no severity at all. Ids only, so a later session can re-fetch and compare.
    standing = [b for b in bugs
                if b["severity"] == "--" and b["status"] not in CLOSED]
    standing.sort(key=lambda b: b["creation_time"])
    res["falsifier_population"] = {
        "id": "S74.UNNORMED",
        "n": len(standing),
        "by_type": dict(collections.Counter(b["type"] for b in standing).most_common()),
        "oldest_creation_time": standing[0]["creation_time"] if standing else None,
        "committed_as": "unnormed-2026-08-29.json",
    }
    return res, bugs, standing


def measure_history(hist, bugs):
    """P3, P4 and P5(b): what the change history says about who set what, and when."""
    by_id = {b["id"]: b for b in bugs}
    sample = hist["sample"]
    history = hist["history"]
    out = {}

    type_changed, comp_changed, prod_changed, sev_events = 0, 0, 0, []
    comp_changers, type_changers = collections.Counter(), collections.Counter()
    first_sev_days, first_sev_by_type = [], collections.defaultdict(list)
    never_sev_by_type = collections.Counter()
    n_by_type = collections.Counter()
    per_bug = {}

    for bug_id in sample:
        key = str(bug_id)
        if key not in history:
            continue
        bug = by_id.get(bug_id)
        if bug is None:
            continue
        n_by_type[bug["type"]] += 1
        created = parse(bug["creation_time"])
        t_ch = c_ch = p_ch = 0
        first_sev = None
        for change_set in history[key]:
            when = parse(change_set["when"])
            who = change_set.get("who", "?")
            for change in change_set["changes"]:
                field = change["field_name"]
                if field == "type":
                    t_ch += 1
                    type_changers[who] += 1
                elif field == "component":
                    c_ch += 1
                    comp_changers[who] += 1
                elif field == "product":
                    p_ch += 1
                elif field == "severity" and change.get("removed") == "--" \
                        and change.get("added") != "--":
                    sev_events.append({"who": who, "day": when.date().isoformat()})
                    if first_sev is None:
                        first_sev = when
        type_changed += 1 if t_ch else 0
        comp_changed += 1 if c_ch else 0
        prod_changed += 1 if p_ch else 0
        if first_sev is not None:
            days = (first_sev - created).total_seconds() / 86400.0
            first_sev_days.append(days)
            first_sev_by_type[bug["type"]].append(days)
        else:
            never_sev_by_type[bug["type"]] += 1
        per_bug[key] = {"type": bug["type"], "type_changes": t_ch, "component_changes": c_ch,
                        "product_changes": p_ch,
                        "days_to_first_severity": round(days, 3) if first_sev else None}

    n = len(per_bug)
    type_kept = n - type_changed
    out["P3_type_is_the_filers"] = {
        "claim": "type has no change event for >= 90% of the sample",
        "n_sample": n,
        "unchanged": type_kept,
        "unchanged_pct": pct(type_kept, n),
        "changed": type_changed,
        "who_changed_it": dict(type_changers.most_common(10)),
        "won": pct(type_kept, n) is not None and pct(type_kept, n) >= 90.0,
    }
    ratio = round(comp_changed / type_changed, 2) if type_changed else None
    out["P4_address_revised_more_than_branch"] = {
        "claim": "component changes for >= 25% of the sample, and at >= 3x the type-change rate",
        "component_changed": comp_changed,
        "component_changed_pct": pct(comp_changed, n),
        "type_changed_pct": pct(type_changed, n),
        "ratio_component_to_type": ratio,
        "product_changed": prod_changed,
        "product_changed_pct": pct(prod_changed, n),
        "who_moved_components": dict(comp_changers.most_common(12)),
        "won": (pct(comp_changed, n) or 0) >= 25.0 and (ratio or 0) >= 3.0,
    }
    day_counter = collections.Counter((e["who"], e["day"]) for e in sample_events(sev_events))
    top = day_counter.most_common(5)
    out["P5b_no_bulk_edit"] = {
        "claim": "no single (account, day) pair is more than 10% of severity-setting events",
        "severity_setting_events": len(sev_events),
        "largest_account_day": [{"who": w, "day": d, "n": c,
                                 "pct": pct(c, len(sev_events))} for (w, d), c in top],
        "won": (not sev_events) or pct(top[0][1], len(sev_events)) <= 10.0,
    }
    tt = {}
    for typ, days in first_sev_by_type.items():
        days = sorted(days)
        tt[typ] = {
            "n_with_a_severity_set": len(days),
            "n_never_set": never_sev_by_type[typ],
            "n_in_sample": n_by_type[typ],
            "median_days": round(statistics.median(days), 2) if days else None,
            "within_one_week": sum(1 for x in days if x <= WEEK),
            "within_one_week_pct_of_those_set": pct(sum(1 for x in days if x <= WEEK), len(days)),
            "within_one_week_pct_of_all": pct(sum(1 for x in days if x <= WEEK), n_by_type[typ]),
        }
    out["time_to_first_severity_sample"] = {
        "what": "days from filing to the first severity value, on the seeded sample only; "
                "small cells, reported as such, and used descriptively",
        "overall_median_of_those_set": round(statistics.median(first_sev_days), 2)
        if first_sev_days else None,
        "by_type": tt,
    }
    # Nobody predicted this one. A bug whose severity has no change event at all, and which
    # nevertheless carries a severity, has carried it since the instant it was filed: the value
    # was in the record before anyone could have triaged it. The history endpoint records changes
    # after creation only, so it cannot say WHO put it there -- the filer on the form, a client
    # posting through the API, a default. What it does establish is that no later observer touched
    # it, and that is enough to say the imposition was not an act of triage.
    at_filing = collections.Counter()
    for bug_id in sample:
        key = str(bug_id)
        if key not in history:
            continue
        bug = by_id.get(bug_id)
        if bug is None:
            continue
        touched = any(c["field_name"] == "severity"
                      for cs in history[key] for c in cs["changes"])
        state = ("still --" if bug["severity"] == "--"
                 else ("carried since filing" if not touched else "set later"))
        at_filing[(bug["type"], state)] += 1
    normed = sum(n for (_, s), n in at_filing.items() if s != "still --")
    since_filing = sum(n for (_, s), n in at_filing.items() if s == "carried since filing")
    out["norm_present_at_filing"] = {
        "what": "of the sampled bugs that carry a severity, how many have carried it since the "
                "moment of filing (no severity change event in the whole history)",
        "cells": {f"{t}|{s}": n for (t, s), n in sorted(at_filing.items())},
        "sample_with_a_severity": normed,
        "carried_since_filing": since_filing,
        "carried_since_filing_pct_of_normed": pct(since_filing, normed),
        "caveat": "the history endpoint records changes after creation only; it cannot name who "
                  "set the creation-time value, only that no one changed it afterwards",
    }
    out["per_bug_history"] = per_bug
    return out


def sample_events(events):
    return events


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="../../../.raw")
    args = ap.parse_args()
    raw = os.path.abspath(args.raw)
    res, bugs, standing = measure(raw)

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    with open(os.path.join(here, "unnormed-2026-08-29.json"), "w", encoding="utf-8") as fh:
        json.dump({
            "falsifier": "S74.UNNORMED",
            "measured_utc": res["measured_utc"],
            "what": "Every bug in the population that is open and still carries no severity "
                    "value. Ids, type, product, component and creation time only -- no summary, "
                    "no reporter, no text: enough for a later session to re-fetch and compare, "
                    "and nothing that republishes anyone's words.",
            "n": len(standing),
            "bugs": [{"id": b["id"], "type": b["type"], "product": b["product"],
                      "component": b["component"], "creation_time": b["creation_time"],
                      "status": b["status"]} for b in standing],
        }, fh, indent=0)
        fh.write("\n")

    for key in ("P1_routing_gap", "P2_norm_arrives_on_defect", "P3_type_is_the_filers",
                "P4_address_revised_more_than_branch", "P5a_vocabulary", "P5b_no_bulk_edit"):
        if key in res:
            print(f"{key:38s} won={res[key].get('won')}")
    print(f"\npopulation {res['population']['n']:,}  "
          f"min age {res['population']['min_age_days']} days "
          f"({res['population']['min_age_weeks_vs_policy']} weeks of a one-week rule)")
    for typ, row in res["by_type"].items():
        print(f"  {typ:12s} n={row['n']:>6,}  unnormed {row['unnormed_pct']:>6}%  "
              f"N/A {row['na_pct']:>5}%  triaged-by-policy {row['triaged_by_policy_pct']:>6}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
