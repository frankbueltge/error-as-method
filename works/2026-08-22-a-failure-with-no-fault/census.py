#!/usr/bin/env python3
"""
census.py — Session 65, 2026-08-22

An exhaustive census of disagreement between two live IDNA norms, over the complete
Unicode code point space. Standard library only. Deterministic. No network at
measuring time: the one input file, sources/IdnaMappingTable.txt, is fetched once
beforehand and recorded in sources/MANIFEST.json with its SHA-256.

WHAT IS COMPARED, AND WHAT IS NOT
---------------------------------
The two norms are compared at the MAPPING STAGE ONLY, on single code points.

  Side A -- "the interpreter in this room". CPython's encodings.idna.nameprep(),
            which the Python documentation describes as implementing RFC 3490
            (IDNA2003); nameprep itself is RFC 3491. This is the actual function
            object in this interpreter, called for real, not a reimplementation.

  Side B -- "the norm the web platform implements". UTS #46 status and mapping,
            read from the Unicode IDNA mapping table, with
            Transitional_Processing = false and UseSTD3ASCIIRules = false --
            the two parameter settings the WHATWG URL Standard fixes for a
            non-strict domain parse (URL Standard, section 3.3 IDNA).

NOT compared, and therefore not claimed: the validity criteria (CheckHyphens,
CheckBidi, CheckJoiners), label length, the Punycode stage, or any behaviour that
depends on more than one code point. nameprep applies NFKC, which is contextual;
on a one-character string it is well defined, and that is the whole scope here.
A disagreement found here is a disagreement about what one character maps to. It
is not by itself a claim that any particular domain name resolves anywhere.

THE CLASSIFICATION
------------------
For each code point both sides are run and the pair is placed in exactly one class:

  agree              -- same output, or both refuse
  refused_by_python  -- side A raises, side B produces a name
  refused_by_uts46   -- side B disallows, side A produces a name
  silent_divergence  -- BOTH produce a name, and the names differ

The last class is the one with teeth: neither side signals anything, and two
conformant programs hand their callers two different domain names for one input.

Every silent divergence is additionally tagged with whether the code point was
assigned in Unicode 3.2 -- the repertoire RFC 3491 section 2 fixes for this
profile -- using stringprep.in_table_a1(), which is the standard library's own
copy of that table. This separates two structurally different causes that would
otherwise be one number.
"""

import json
import os
import stringprep
import sys
import unicodedata
from collections import Counter

import encodings.idna
from unicodedata import ucd_3_2_0 as ucd32  # the frozen 3.2 database encodings.idna itself imports

HERE = os.path.dirname(os.path.abspath(__file__))
TABLE = os.path.join(HERE, "sources", "IdnaMappingTable.txt")
OUT = os.path.join(HERE, "results.json")

SURROGATES = range(0xD800, 0xE000)
MAXCP = 0x10FFFF

REFUSED = object()  # sentinel: this side declines to produce a name
UTS46_TABLE = {}  # filled by main(); attribute() reads it


# ---------------------------------------------------------------- side B

def parse_mapping_table(path):
    """Return (version, date, {cp: (status, mapping_or_None)}).

    Fields per UTS #46 'Data File Fields': code point or range ; status ;
    mapping ; IDNA2008 status. Only the first three are used here.
    """
    version = date = None
    table = {}
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            if raw.startswith("#"):
                if version is None and raw.startswith("# Version:"):
                    version = raw.split(":", 1)[1].strip()
                if date is None and raw.startswith("# Date:"):
                    date = raw.split(":", 1)[1].strip()
                continue
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(";")]
            rng, status = parts[0], parts[1]
            mapping = None
            if len(parts) > 2 and parts[2]:
                mapping = "".join(chr(int(h, 16)) for h in parts[2].split())
            if ".." in rng:
                lo, hi = (int(x, 16) for x in rng.split(".."))
            else:
                lo = hi = int(rng, 16)
            for cp in range(lo, hi + 1):
                table[cp] = (status, mapping)
    return version, date, table


def uts46_nontransitional(cp, table):
    """UTS #46 mapping-stage output for one code point.

    Transitional_Processing = false: a 'deviation' code point is left alone
    rather than mapped, which is what the URL Standard fixes for the web.
    UseSTD3ASCIIRules = false: the two disallowed_STD3_* statuses relax into
    valid and mapped respectively, which is what beStrict = false gives.
    """
    entry = table.get(cp)
    if entry is None:
        return REFUSED  # not listed at all -> not a permitted input
    status, mapping = entry
    if status == "valid":
        return chr(cp)
    if status == "mapped":
        return mapping if mapping is not None else ""
    if status == "deviation":
        return chr(cp)  # non-transitional keeps it
    if status == "ignored":
        return ""
    if status == "disallowed_STD3_valid":
        return chr(cp)
    if status == "disallowed_STD3_mapped":
        return mapping if mapping is not None else ""
    if status == "disallowed":
        return REFUSED
    raise ValueError("unknown status %r at U+%04X" % (status, cp))


# ---------------------------------------------------------------- side A

def python_idna2003(cp):
    """What this interpreter's RFC 3490 codec does to one code point."""
    try:
        return encodings.idna.nameprep(chr(cp))
    except UnicodeError:
        return REFUSED


# ---------------------------------------------------------------- census

def attribute(cp, a, b):
    """Which side left its own declared repertoire? Computed, not asserted.

    Two mechanical tests, run in order, using CPython's own frozen Unicode 3.2
    database (unicodedata.ucd_3_2_0) as the arbiter -- the same database
    encodings.idna imports, and the repertoire RFC 3491 section 2 fixes:

      escaped_repertoire  side A emitted at least one code point that does not
                          exist in Unicode 3.2. A profile whose repertoire is
                          Unicode 3.2 cannot legitimately produce one; the
                          mapping came from somewhere else.
      frozen_vs_current   side A's output is exactly the Unicode 3.2 NFKC of the
                          input and side B's is exactly the current NFKC, and
                          those two differ. Both sides are doing their own job
                          correctly; the two jobs were specified years apart.
      by_design           the code point is in the UTS #46 deviation set: the
                          disagreement is documented and intended.
      unattributed        none of the above fits; left as a residue rather than
                          argued into one of the classes above.
    """
    if any(not cp_exists_in_3_2(ch) for ch in a):
        return "escaped_repertoire"
    if UTS46_TABLE[cp][0] == "deviation":
        return "by_design"
    src = chr(cp)
    if a == ucd32.normalize("NFKC", src) and b == unicodedata.normalize("NFKC", src) and a != b:
        return "frozen_vs_current"
    return "unattributed"


def cp_exists_in_3_2(ch):
    try:
        ucd32.name(ch)
        return True
    except ValueError:
        # ucd_3_2_0.name() also raises for assigned-but-unnamed characters
        # (control codes, and the ideograph/Hangul ranges that carry rule-based
        # names). Fall back to the category, which is Cn only when unassigned.
        return ucd32.category(ch) != "Cn"


def classify(a, b):
    if a is REFUSED and b is REFUSED:
        return "agree"
    if a is REFUSED:
        return "refused_by_python"
    if b is REFUSED:
        return "refused_by_uts46"
    return "agree" if a == b else "silent_divergence"


def main():
    global UTS46_TABLE
    version, date, table = parse_mapping_table(TABLE)
    UTS46_TABLE = table

    counts = Counter()
    causes = Counter()
    divergences = []          # every silent divergence, in full
    post32_divergences = 0
    deviation_rows = []

    for cp in range(MAXCP + 1):
        if cp in SURROGATES:
            continue
        a = python_idna2003(cp)
        b = uts46_nontransitional(cp, table)
        cls = classify(a, b)
        counts[cls] += 1
        if cls == "silent_divergence":
            after_32 = stringprep.in_table_a1(chr(cp))
            if after_32:
                post32_divergences += 1
            cause = attribute(cp, a, b)
            causes[("post-3.2" if after_32 else "in-3.2", cause)] += 1
            divergences.append({
                "cause": cause,
                "cp": "U+%04X" % cp,
                "name": unicodedata.name(chr(cp), "<unnamed>"),
                "uts46_status": table[cp][0],
                "python_idna2003": a,
                "uts46_nontransitional": b,
                "unassigned_in_unicode_3_2": bool(after_32),
            })
        if table.get(cp, (None, None))[0] == "deviation":
            deviation_rows.append({
                "cp": "U+%04X" % cp,
                "name": unicodedata.name(chr(cp), "<unnamed>"),
                "python_idna2003": "REFUSED" if a is REFUSED else a,
                "uts46_nontransitional": "REFUSED" if b is REFUSED else b,
                "differs": not (a is REFUSED or b is REFUSED) and a != b,
            })

    total = sum(counts.values())
    in_32 = len(divergences) - post32_divergences

    # The deviation set, as an independent check that the census found what the
    # standard says is there rather than what the instrument hoped for.
    deviation_cps = sorted(cp for cp, (s, _) in table.items() if s == "deviation")

    results = {
        "generated_by": "census.py",
        "date": "2026-08-22",
        "session": 65,
        "scope": (
            "mapping stage only, single code points; validity criteria, label "
            "length and the Punycode stage are out of scope and not claimed"
        ),
        "environment": {
            "python": sys.version.split()[0],
            "unicodedata_version": unicodedata.unidata_version,
            "stringprep_repertoire": "Unicode 3.2 (RFC 3454 Appendix A / RFC 3491 s2)",
        },
        "mapping_table": {
            "file": "sources/IdnaMappingTable.txt",
            "version": version,
            "date": date,
            "entries": len(table),
        },
        "population": {
            "code_points_examined": total,
            "surrogates_excluded": len(SURROGATES),
            "note": "0..0x10FFFF inclusive, minus the surrogate range",
        },
        "classes": dict(counts),
        "silent_divergence": {
            "total": len(divergences),
            "assigned_in_unicode_3_2": in_32,
            "unassigned_in_unicode_3_2": post32_divergences,
        },
        "silent_divergence_causes": {
            "%s / %s" % k: v for k, v in sorted(causes.items())
        },
        "deviation_set": {
            "count": len(deviation_cps),
            "code_points": ["U+%04X" % c for c in deviation_cps],
            "rows": deviation_rows,
        },
        "worked_example": worked_example(),
    }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    # The full divergence list is large; it is written beside results.json so a
    # reader can check any row rather than take the counts on trust.
    with open(os.path.join(HERE, "divergences.json"), "w", encoding="utf-8") as fh:
        json.dump(divergences, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    for k in ("agree", "refused_by_python", "refused_by_uts46", "silent_divergence"):
        print("%-20s %8d" % (k, counts[k]))
    print("%-20s %8d  (of which %d unassigned in Unicode 3.2)"
          % ("  divergences", len(divergences), post32_divergences))
    for k, v in sorted(causes.items()):
        print("    %-9s %-20s %6d" % (k[0], k[1], v))
    print("deviation set:", ", ".join("U+%04X" % c for c in deviation_cps))


def worked_example():
    """One whole name carried through, for the boundary trace in the work.

    Every value here is computed, not asserted.
    """
    name = "fa\u00df.de"  # LATIN SMALL LETTER SHARP S, written as an escape so this file stays ASCII
    py = name.encode("idna")
    # The non-transitional form of the same name, built with this interpreter's
    # own Punycode codec (RFC 3492) rather than asserted from memory.
    label, tld = name.split(".")
    nt_label = b"xn--" + label.encode("punycode")
    return {
        "input": name,
        "python_idna2003_encode": py.decode("ascii"),
        "python_idna2003_roundtrip": py.decode("idna"),
        "roundtrip_recovers_input": py.decode("idna") == name,
        "uts46_nontransitional_ascii": nt_label.decode("ascii") + "." + tld,
        "uts46_roundtrip": nt_label[4:].decode("punycode") + "." + tld,
        "the_two_ascii_forms_differ": py.decode("ascii") != nt_label.decode("ascii") + "." + tld,
    }


if __name__ == "__main__":
    main()
