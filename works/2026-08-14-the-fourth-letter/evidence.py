#!/usr/bin/env python3
"""evidence.py -- cut every passage the work quotes out of the downloaded file, by script.

House rule since Session 52: a quotation in the work is not retyped from a browser, it is
sliced out of the exact bytes that harvest.py hashed. Anything that could not be cut here
is declared in sources/PROVENANCE.md instead of being quoted as if it had been.

    python3 evidence.py           -> sources/*.txt
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
SOURCES = os.path.join(HERE, "sources")


def load(name):
    with open(os.path.join(CACHE, name), encoding="utf-8", errors="replace") as f:
        return f.read()


def cut(text, start, end, pad=0):
    i = text.find(start)
    if i < 0:
        return None
    j = text.find(end, i + len(start))
    if j < 0:
        return None
    return text[max(0, i - pad):j + len(end)]


def write(name, header, body):
    path = os.path.join(SOURCES, name)
    with open(path, "w") as f:
        f.write(header.rstrip() + "\n\n" + body.strip() + "\n")
    print("wrote %-46s %5d bytes" % (name, os.path.getsize(path)))


def main():
    os.makedirs(SOURCES, exist_ok=True)

    r4645 = load("rfc4645.txt")
    r4646 = load("rfc4646.txt")
    r5646 = load("rfc5646.txt")
    r1766 = load("rfc1766.txt")
    r3066 = load("rfc3066.txt")
    reg = load("language-subtag-registry.txt")
    cldr = load("cldr-supplementalMetadata.xml")

    # 1. The floor rule and the rule that permits a change of meaning, with its parenthesis.
    body = cut(r4645, "1.  For each source standard", "Serbia and\n          Montenegro).")
    write("rfc4645-rules-1-and-2.txt",
          "RFC 4645, 'Initial Language Subtag Registry', September 2006, section 2. Cut from\n"
          "https://www.rfc-editor.org/rfc/rfc4645.txt -- page furniture between the two rules\n"
          "left in place, because removing it would be a silent edit.", body)

    # 2. The edition that fixes the floor date.
    body = cut(r1766, "[ISO 3166]", "1988-08-15.")
    write("rfc1766-the-referenced-edition.txt",
          "RFC 1766, March 1995, reference list. The date RFC 4645 rule 1 turns into a floor.",
          body)

    # 3. What RFC 3066 did with the same question in 2001.
    body = cut(r3066, "- All 2-letter subtags", "relates.")
    write("rfc3066-subsequently-assigned.txt",
          "RFC 3066, January 2001, section 2.1. The intermediate rule: the standard, or what "
          "the\nmaintenance agency does to it afterwards.", body)

    # 4. The recycled-code rule, in both versions, for the diff.
    body = cut(r4646, "C.  UN numeric codes for countries or areas with", "are defined.")
    write("rfc4646-rule-C-ambiguous.txt",
          "RFC 4646, September 2006, section 2.2.4, rule 3.C. The first version.", body)
    body = cut(r5646, "C.  When ISO 3166-1 reassigns a code", "ISO 3166-1 code).")
    write("rfc5646-rule-C-recycled.txt",
          "RFC 5646, September 2009, section 2.2.4, rule 3.C. The version in force, and the\n"
          "condition that decides everything: 'and that code already is present in the "
          "registry'.", body)

    # 5. The registry's own records for every two-letter address this work touches.
    wanted = ["CS", "BQ", "SK", "AI", "GE", "BY", "AN", "SU", "YU", "DD"]
    out = []
    for block in reg.split("\n%%\n"):
        m = re.search(r"^Type: region\nSubtag: (\w+)$", block, re.M)
        if m and m.group(1) in wanted:
            out.append(block.strip())
    write("registry-region-records.txt",
          "The IANA Language Subtag Registry, File-Date %s. Ten region records, cut whole.\n"
          "https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry"
          % re.search(r"File-Date:\s*(\S+)", reg).group(1),
          "\n\n%%\n\n".join(out))

    # 6. CLDR's decision about the same addresses.
    codes = ["CS", "YU", "SU", "PC", "NQ", "PZ", "VD", "HV", "CT", "DY", "AN"]
    lines = [ln.strip() for ln in cldr.split("\n")
             if any('type="%s"' % c in ln for c in codes) and "territoryAlias" in ln]
    write("cldr-territory-aliases.txt",
          "CLDR common/supplemental/supplementalMetadata.xml, territoryAlias entries for the\n"
          "addresses this work touches. https://github.com/unicode-org/cldr",
          "\n".join(lines))

    # 7. The one negative fact that carries an argument: the string is not in the file.
    write("registry-negative-check.txt",
          "A negative result, produced by search over the whole registry file rather than by "
          "eye.",
          "\n".join([
              "needle                      occurrences in the 9,296-record registry file",
              "--------------------------  ---------------------------------------------",
              "'Czechoslovak'              %d" % reg.count("Czechoslovak"),
              "'Serbia and Montenegro'     %d" % reg.count("Serbia and Montenegro"),
              "'Sikkim' (the country)      %d" % (reg.count("Sikkim") - reg.count("Sikkimese")),
              "'Sikkimese' (the language)  %d" % reg.count("Sikkimese"),
              "'French Afars'              %d" % reg.count("French Afars"),
              "'Gilbert and Ellice'        %d" % reg.count("Gilbert and Ellice"),
              "'British Antarctic'         %d" % reg.count("British Antarctic"),
          ]))

    # 8. The join itself, as a table anyone can re-derive.
    res = json.load(open(os.path.join(HERE, "results.json")))
    hdr = ("alpha_4  a2  a3   withdrawn    floor  IANA                  "
           "CLDR alias        alpha-2 in use now")
    lines = [hdr, "-" * len(hdr)]
    for r in res["rows"]:
        lines.append("%-8s %-3s %-4s %-12s %-6s %-21s %-17s %s" % (
            r["alpha_4"], r["alpha_2"], r["alpha_3"], r["withdrawal_date"],
            "pre" if r["before_floor"] else "post", r["iana"],
            r["cldr_alias"] or "-", r["alpha_2_live_now"] or "-"))
    write("join-31-dead-codes.txt",
          "The whole measurement, 31 rows. Sources: ISO 3166-3 (iso-codes compilation), the "
          "IANA\nregistry, CLDR territoryAlias, ISO 3166-1 (iso-codes compilation). "
          "Regenerate with\n  python3 harvest.py && python3 measure.py && python3 evidence.py",
          "\n".join(lines))

    return 0


if __name__ == "__main__":
    sys.exit(main())
