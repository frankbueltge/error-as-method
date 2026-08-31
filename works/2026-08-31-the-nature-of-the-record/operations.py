#!/usr/bin/env python3
"""How much of this record of imposed norms is the imposer describing its own work.

Not predicted; found in the flag descriptions while looking up the wording of two of them.

GBIF's data blog distinguishes three kinds of remark — *Excluded* ("the original data couldn't
be interpreted, so is excluded in the interpreted fields"), *Altered* ("the original data is
modified in the interpretation process"), *Inferred* ("Using other record information the data
indexed is inferred, if the original is empty"). Only the first is a verdict on what the
publisher supplied. **That three-way classification is not published per flag anywhere this
night could find**, so it cannot simply be joined to the counts, and inventing the join would
be a fabrication.

What can be done instead, mechanically and auditably: apply a stated keyword rule to the
institution's **own description text** for each flag, and report the rule with the result so a
reader can disagree with the rule rather than with a hidden judgement.

    A flag is counted as SELF-REPORTING if its published description says the interpretation
    derived, inferred, assumed, rounded, reprojected, collapsed or otherwise altered a value —
    i.e. describes something the pipeline did — rather than a defect in what was supplied.

This is **this night's reading of the institution's wording, not the institution's own
classification of its flags.** It is marked as such wherever it is used.

The counts are then exact: the union of the self-reporting flags, and the union of all the
others, per branch and over the window — real queries, not sums of overlapping counts.

Writes `operations.json`.
"""
import html
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gbif import Client  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = "https://techdocs.gbif.org/en/data-use/occurrence-issues-and-flags"
UA = "error-as-method nightly research line (+https://frankbueltge.de/error-as-method)"
YEAR = "2025"

# TWO rules, both applied, both reported.
#
# RULE A is the one stated before it was applied. RULE B was written afterwards, for a reason
# worth stating: rule A misses GEODETIC_DATUM_ASSUMED_WGS84 -- whose published description reads
# "If the datum is null, data interpretation assumes the record coordinates are in WGS84", and
# which fires on 5,428,125 records in this window -- because A spells the word "assumed" and the
# institution wrote "assumes". That is a word-form failure, not a judgement about the flag, so
# rule B matches verb stems instead. Both results are reported, so a reader can see exactly what
# the amendment does rather than take the amended number on trust.
RULE_A = re.compile(
    r"\b(derives?|derived|infer(?:s|red)?|assumed|rounded|reprojected|collapsed|"
    r"is modified|are modified|interpretation (?:derives|assigns|sets))\b", re.I)
RULE_B = re.compile(
    r"\b(deriv|infer|assum|round|reproject|collaps)\w*\b|\b(is|are) modified\b", re.I)
SELF_REPORTING = RULE_B


def descriptions():
    """label -> description, from the institution's own flag reference."""
    req = urllib.request.Request(PAGE, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        page = r.read().decode("utf-8", "replace")

    def txt(c):
        return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip()

    out = {}
    for row in re.findall(r"<tr>(.*?)</tr>", page, re.S):
        cells = re.findall(r'<td class="tableblock[^"]*"[^>]*>(.*?)</td>', row, re.S)
        if len(cells) < 2:
            continue
        label, desc = txt(cells[0]), txt(cells[1])
        if not (label and desc):
            continue
        entry = {"label": label, "description": desc}
        # key on the flag name the row's own example link carries, when it has one --
        # [A-Z0-9_]+ and not [A-Z_]+, which is the bug filed as F-093
        named = re.search(r"issue=([A-Z0-9_]+)", row)
        if named:
            out[named.group(1)] = entry
        out[re.sub(r"[^a-z0-9]", "", label.lower())] = entry
    return out


def main():
    with open(os.path.join(HERE, "harvest.json"), encoding="utf-8") as fh:
        h = json.load(fh)
    enum, branches = h["issue_enum"], h["branches"]
    docs = descriptions()

    matched, unmatched, selected = {}, [], []
    for e in enum:
        d = docs.get(e) or docs.get(re.sub(r"[^a-z0-9]", "", e.replace("_", " ").lower()))
        if not d:
            unmatched.append(e)
            continue
        matched[e] = d
        if SELF_REPORTING.search(d["description"]):
            selected.append(e)

    other = [e for e in enum if e not in selected]

    c = Client(log=os.path.join(HERE, "operations.log"))
    counts = {"window": {}, "by_branch": {}}
    base = [("limit", "0"), ("year", YEAR)]
    counts["window"]["self_reporting_union"] = c.get(
        "occurrence/search", base + [("issue", i) for i in selected])["count"]
    counts["window"]["other_union"] = c.get(
        "occurrence/search", base + [("issue", i) for i in other])["count"]
    counts["window"]["total"] = h["window_total"]
    for b in branches:
        bb = base + [("basisOfRecord", b)]
        counts["by_branch"][b] = {
            "total": branches[b],
            "self_reporting_union": c.get("occurrence/search", bb + [("issue", i) for i in selected])["count"],
            "other_union": c.get("occurrence/search", bb + [("issue", i) for i in other])["count"],
            "any_union": h["union_of_all_flags"][b],
        }
        r = counts["by_branch"][b]
        c._log(f"{b}: self-reporting {r['self_reporting_union']:,}  other {r['other_union']:,}  "
               f"any {r['any_union']:,}  of {r['total']:,}")

    rule_a = sorted(e for e, d in matched.items() if RULE_A.search(d["description"]))
    out = {
        "rule_applied": RULE_B.pattern,
        "rule_as_first_stated": RULE_A.pattern,
        "rule_as_first_stated_selects": rule_a,
        "rule_as_first_stated_count": len(rule_a),
        "why_amended": ("rule A spells 'assumed'; GBIF wrote 'assumes' in the description of "
                        "GEODETIC_DATUM_ASSUMED_WGS84, which fires on 5,428,125 records here. "
                        "Both rules and both selections are reported."),
        "rule_is": ("this night's reading of the institution's own description text, NOT the "
                    "institution's classification of its own flags — GBIF publishes the three-way "
                    "Excluded/Altered/Inferred distinction per record, not per flag"),
        "source_page": PAGE,
        "flags_with_a_published_description": len(matched),
        "flags_with_no_published_description": len(unmatched),
        "undescribed": unmatched,
        "self_reporting": sorted(selected),
        "self_reporting_count": len(selected),
        "descriptions_of_the_selected": {e: matched[e]["description"] for e in sorted(selected)},
        "counts": counts,
    }
    out["window_shares"] = {
        "self_reporting_pct": 100.0 * counts["window"]["self_reporting_union"] / h["window_total"],
        "other_pct": 100.0 * counts["window"]["other_union"] / h["window_total"],
    }
    with open(os.path.join(HERE, "operations.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, "sources", "MANIFEST-operations.json"), "w", encoding="utf-8") as fh:
        json.dump(c.manifest_json(what="Queries behind the self-reporting split.",
                                  why="Exact unions rather than sums of overlapping flag counts."),
                  fh, indent=1, ensure_ascii=False)
    print(json.dumps({k: out[k] for k in ("flags_with_a_published_description",
                                          "flags_with_no_published_description",
                                          "self_reporting_count", "window_shares")}, indent=1))
    print("selected:", out["self_reporting"])


if __name__ == "__main__":
    main()
