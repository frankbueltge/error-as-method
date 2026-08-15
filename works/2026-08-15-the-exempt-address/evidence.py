#!/usr/bin/env python3
"""
evidence.py -- Session 57. Cuts every passage quoted in work.md out of the bytes
harvest.py downloaded, and writes them to sources/*.txt with the file, the URL and
the SHA-256 they came from. Offline.

The rule this repository works under: a quotation in work.md is a cut from a hashed
file, not something retyped from a reading. Passages that could not be cut here are
declared in sources/PROVENANCE.md with the route by which they were read instead.
"""

import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.path.join(HERE, "downloads")
SRC = os.path.join(HERE, "sources")
MAN = json.load(open(os.path.join(SRC, "MANIFEST.json")))
BY_FILE = {f["file"]: f for f in MAN["files"]}


def plain(name):
    raw = open(os.path.join(DL, name), "rb").read()
    t = raw.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.replace("&#8220;", '"').replace("&#8221;", '"')
    t = t.replace("&#8216;", "'").replace("&#8217;", "'")
    t = t.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#8211;", "-")
    return re.sub(r"\s+", " ", t).strip()


def write(out_name, source_file, title, cuts):
    """cuts: list of (label, regex). Each must match or the file records the miss."""
    text = plain(source_file)
    meta = BY_FILE[source_file]
    lines = [
        "# %s" % title,
        "",
        "source file : %s" % source_file,
        "url         : %s" % meta["url"],
        "sha256      : %s" % meta["sha256"],
        "bytes       : %d" % meta["bytes"],
        "cut by      : evidence.py, Session 57, 2026-08-15",
        "",
        "Every block below is a literal substring of the file above after tag "
        "stripping and whitespace collapse. Nothing is retyped.",
        "",
    ]
    misses = 0
    for label, pat in cuts:
        m = re.search(pat, text)
        lines.append("-" * 74)
        lines.append("[%s]" % label)
        if m:
            lines.append("")
            lines.append(m.group(0).strip())
        else:
            lines.append("")
            lines.append("*** NOT FOUND in this file. Pattern: %s" % pat)
            misses += 1
        lines.append("")
    with open(os.path.join(SRC, out_name), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("%-40s %d cuts, %d missed" % (out_name, len(cuts), misses))
    return misses


total = 0

total += write(
    "iana-retirement-policy.txt", "iana-cctld-retirement.html",
    "IANA -- Retirement of a Country-code Top-level Domain (ccTLD)",
    [("the eligibility rule that .su fails",
      r"ccTLD eligibility is determined by the associated country or territory "
      r"being assigned in the ISO 3166-1 standard\..{0,240}?"
      r"orderly transition period\."),
     ("the default period",
      r"By default the ccTLD will be removed after five years\s*\..{0,200}?"
      r"target removal date\."),
     ("the maximum",
      r"Extensions are limited to a maximum of five additional years,.{0,120}?"
      r"10 years\."),
     ("what there was before the policy -- the sentence this night turns on",
      r"Prior to this policy, retirements were bilaterally discussed.{0,240}?"
      r"reasonable timeframe\."),
     ("when the policy was adopted",
      r"The .{0,4}Policy for the Retirement of a ccTLD.{0,4} was adopted by the "
      r"ICANN Board of Directors on 22 September 2022\.")])

total += write(
    "iana-yu-removal.txt", "iana-yu-removal-report.html",
    "IANA -- Removal of the .YU domain formerly representing Yugoslavia (2010-04-01)",
    [("the status YU and SU shared, and what it required",
      r"With the removal of .{0,4}YU.{0,4} from the ISO 3166-1 standard, the code "
      r"was deemed .{0,4}transitionally reserved.{0,4}.{0,140}?ASAP.{0,4}\."),
     ("the reassignment of the address in 2003",
      r"On 23 July 2003, a new two-letter code of .{0,4}CS.{0,4} was designated for "
      r"Serbia and Montenegro\..{0,400}?IANA Staff\."),
     ("what pointed at the address -- the search index",
      r"Pages on \.YU sites are still referenced by Internet search engines.{0,180}?"
      r"September 2007\)"),
     ("what pointed at the address -- other top-level domains",
      r"Used as contact email addresses for other top-level domains, including gTLDs\."),
     ("the migration, counted",
      r"As of June 2009, there were [\d,]+ \.YU domains still delegated, down from "
      r"[\d,]+\..{0,120}?registered in \.RS\."),
     ("what was left stranded when the address was finally repaired",
      r"It is worth noting that of these remaining [\d,]+ domains, only "
      r"approximately \d+ did not also have the matching \.RS domain\.")])

# The operating artefact itself. No tag stripping -- these are zone-file lines.
zone = open(os.path.join(DL, "root.zone"), "rb").read().decode("utf-8", "replace")
meta = BY_FILE["root.zone"]
keep = [l for l in zone.splitlines()
        if re.match(r"^(su|ac|eu|uk)\.\s", l) and ("\tNS\t" in l or "\tDS\t" in l)]
soa = [l for l in zone.splitlines() if "\tSOA\t" in l][:1]
with open(os.path.join(SRC, "root-zone-cut.txt"), "w") as fh:
    fh.write("# The four two-letter delegations ISO 3166-1 does not currently assign\n\n")
    fh.write("source file : root.zone\nurl         : %s\nsha256      : %s\nbytes       : %d\n"
             % (meta["url"], meta["sha256"], meta["bytes"]))
    fh.write("\nSOA (the serial dates the measurement):\n\n")
    fh.write("\n".join(soa) + "\n")
    fh.write("\nNS and DS records, cut verbatim from the zone file. .su carries six\n"
             "name servers and a DS record -- a chain of trust, not a stub.\n\n")
    fh.write("\n".join(keep) + "\n")
print("%-40s %d zone lines" % ("root-zone-cut.txt", len(keep) + len(soa)))

print("\n%d missed cuts overall." % total)
