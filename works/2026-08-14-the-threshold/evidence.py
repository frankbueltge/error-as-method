#!/usr/bin/env python3
"""evidence.py -- cut the decisive passages out of the downloaded files, never retype them.

Every sentence quoted in work.md is extracted from cache/ by this script and written to
sources/, so a reader can check the quotation against the file whose SHA-256 is in
sources/MANIFEST.json, and check that against the published URL. Nothing here is typed
out by hand; where a passage is located by a line range, the range is in the code.

    python3 evidence.py   -> sources/*.txt, sources/*.csv
"""

import collections
import csv
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
SOURCES = os.path.join(HERE, "sources")

# Passages cut by anchor: (source file, first-line anchor, number of lines, out file, why)
PASSAGES = [
    ("rfc4645.txt", "      1.  For each source standard, the date of the standard", 6,
     "rfc4645-rule-1-the-first-floor.txt",
     "RFC 4645 (2006), rule 1: what the initial registry did NOT take."),
    ("rfc4645.txt", "      2.  For each successive change to the standard", 4,
     "rfc4645-rule-2-deprecated-not-removed.txt",
     "RFC 4645 (2006), rule 2: withdrawn values are marked deprecated, but not removed."),
    ("rfc4645.txt", "   The remainder of this section specified the initial set", 5,
     "rfc4645-section-3-contents-deleted.txt",
     "RFC 4645 section 3: the memo's own contents, deleted on publication."),
    ("rfc5645.txt", "   Language code elements that were already retired", 3,
     "rfc5645-the-second-floor.txt",
     "RFC 5645 (2009): retirements before the import 'were not considered in this update'."),
    ("rfc4646.txt", "        withdrawn by their respective maintenance or registration", 3,
     "rfc4646-2006-the-promise.txt",
     "RFC 4646 (2006) section 3.4 rule 14: the promise, three years before the import."),
    ("rfc5646.txt", "   14.  Codes assigned by ISO 639, ISO 15924, or ISO 3166-1 that are", 7,
     "rfc5646-rule-14-remain-valid.txt",
     "RFC 5646 (2009) section 3.4 rule 14: withdrawn codes remain valid in language tags."),
    ("rfc5646.txt", "   In some historical cases, it might not have been possible", 7,
     "rfc5646-3-1-6-earlier-date-than-added.txt",
     "RFC 5646 section 3.1.6: the registry's own note on records deprecated before they were added."),
    ("rfc5646.txt", "   The field 'Deprecated' contains the date the record was deprecated", 11,
     "rfc5646-3-1-6-no-replacement-mapping.txt",
     "RFC 5646 section 3.1.6: a deprecated record with no Preferred-Value has no replacement."),
    ("rfc1766.txt", "    [ISO 639]", 9,
     "rfc1766-the-referenced-editions.txt",
     "RFC 1766 (1995): the 1988 editions whose date fixes the first floor."),
]


def cut(fname, anchor, n, out, why):
    src = os.path.join(CACHE, fname)
    with open(src, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    for i, line in enumerate(lines):
        if line.startswith(anchor):
            # skip RFC page breaks and headers inside the window
            picked, j = [], i
            while len(picked) < n and j < len(lines):
                l = lines[j]
                if not (l.startswith("\f") or re.match(r"^(Ewell|Phillips|Alvestrand)\s", l)
                        or re.match(r"^RFC \d+\s", l) or l.strip() == ""
                        and picked and picked[-1].strip() == ""):
                    picked.append(l)
                j += 1
            body = "\n".join(picked).rstrip()
            with open(os.path.join(SOURCES, out), "w") as fh:
                fh.write("# %s\n# cut from %s by evidence.py, line %d\n\n%s\n"
                         % (why, fname, i + 1, body))
            print("cut  %-46s <- %s:%d" % (out, fname, i + 1))
            return True
    print("MISS %-46s <- %s (anchor not found)" % (out, fname))
    return False


def cut_ggm_message():
    """The Language Subtag Reviewer's own account of the one absence after the cut."""
    path = os.path.join(CACHE, "ietf-languages-2014-02-10-batch1.html")
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = html.unescape(re.sub(r"<[^>]+>", "", fh.read()))
    author = re.search(r"^\s*(Doug Ewell)\s*$", text, re.M)
    date = re.search(r"^\s*(\w{3} \w{3} +\d+ [\d:]+ \w+ \d{4})\s*$", text, re.M)
    para = re.search(r"This first batch is from the section.*?in the first place\.",
                     text, re.S)
    with open(os.path.join(SOURCES, "ietf-languages-2014-the-tip.txt"), "w") as fh:
        fh.write("# ietf-languages list, 'ISO 639-3 changes: batch 1'\n")
        fh.write("# author: %s\n# date  : %s\n" % (
            author.group(1) if author else "(not parsed)",
            date.group(1) if date else "(not parsed)"))
        fh.write("# cut from ietf-languages-2014-02-10-batch1.html by evidence.py\n\n")
        fh.write(re.sub(r"\n+", "\n", para.group(0)).strip() + "\n" if para
                 else "(paragraph not located)\n")
    print("cut  %-46s <- ietf-languages-2014-02-10-batch1.html" % "ietf-languages-2014-the-tip.txt")


def cut_registry_records():
    """The records the argument names, verbatim, plus every ISO 639-3 retirement joined."""
    with open(os.path.join(CACHE, "language-subtag-registry.txt"), encoding="utf-8") as fh:
        text = fh.read()
    head, *chunks = text.split("%%")
    wanted = {"in", "iw", "ji", "BU", "YD", "DD", "SU", "NT", "ZR", "TP",
              "ggr", "gtu", "ikr", "elp", "pgy", "xtz", "AN", "CS", "YU"}
    out = [head.strip(), ""]
    for chunk in chunks:
        m = re.search(r"^(?:Subtag|Tag): (\S+)$", chunk, re.M)
        if m and m.group(1) in wanted:
            out.append("%%" + chunk.rstrip())
    with open(os.path.join(SOURCES, "registry-records-quoted.txt"), "w") as fh:
        fh.write("# Records named in work.md, cut verbatim out of the registry by evidence.py.\n"
                 "# 'ggm' is deliberately absent: that absence is the finding.\n\n")
        fh.write("\n".join(out) + "\n")
    print("cut  %-46s <- language-subtag-registry.txt" % "registry-records-quoted.txt")

    # the full join, as a checkable table
    recs = {}
    for chunk in chunks:
        t = re.search(r"^Type: (\S+)$", chunk, re.M)
        s = re.search(r"^Subtag: (\S+)$", chunk, re.M)
        if t and s and t.group(1) == "language":
            recs[s.group(1)] = chunk
    with open(os.path.join(CACHE, "iso-639-3_Retirements.tab"), encoding="utf-8") as fh:
        RET = list(csv.DictReader(fh, delimiter="\t"))
    with open(os.path.join(SOURCES, "floor-test.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["iso639_3_code", "name", "retired_effective", "reason",
                    "in_subtag_registry", "subtag_deprecated", "preferred_value"])
        for r in sorted(RET, key=lambda r: (r["Effective"], r["Id"])):
            chunk = recs.get(r["Id"])
            dep = pref = ""
            if chunk:
                d = re.search(r"^Deprecated: (\S+)$", chunk, re.M)
                p = re.search(r"^Preferred-Value: (\S+)$", chunk, re.M)
                dep, pref = (d.group(1) if d else ""), (p.group(1) if p else "")
            w.writerow([r["Id"], r["Ref_Name"], r["Effective"], r["Ret_Reason"],
                        "yes" if chunk else "no", dep, pref])
    print("cut  %-46s <- both files, joined" % "floor-test.csv")


def main():
    os.makedirs(SOURCES, exist_ok=True)
    for args in PASSAGES:
        cut(*args)
    cut_ggm_message()
    cut_registry_records()


if __name__ == "__main__":
    main()
