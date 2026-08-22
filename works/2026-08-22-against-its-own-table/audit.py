#!/usr/bin/env python3
"""
audit.py — Session 66, 2026-08-22

Session 65 measured CPython's nameprep against a second implementation and adjudged a
fault. Its own open thread 4 asked for a falsifier: "a genuinely independent UTS #46
implementation against the same table would test whether the 85 are CPython's or the
profile's."

This is the other test, and the one that can answer the question. A second observer can
only produce a difference. A fault needs a norm — and the norm here is not a rival
standard but the document `stringprep` is generated from and asserts at its own top:

    from unicodedata import ucd_3_2_0 as unicodedata
    assert unicodedata.unidata_version == '3.2.0'

RFC 3454 does not describe its tables in prose; it ENUMERATES them, seventeen of them,
between `----- Start Table X -----` and `----- End Table X -----` markers. So the whole
generated module can be held to its source, code point by code point, with no
interpretation anywhere in the loop.

WHAT IS COMPARED
----------------
Two things, in this order:

  1. TABLE CONFORMANCE. Every table `stringprep` exposes, against the enumerated table
     of the same name in RFC 3454, over the complete code point space 0..0x10FFFF
     (surrogates included: Table C.5 is about them). Set tables are compared by
     membership; mapping tables by target string.

  2. THE CONSEQUENCE AT THE MAPPING STAGE. For each code point, what RFC 3491 section 3
     prescribes ("Map: B.1 delete, B.2 map") using the RFC's own tables, against what
     this interpreter's `stringprep` actually does. Each deviation is then cross-
     referenced against the class Session 65's census put that code point in, which is
     what settles whether S65's instrument could have seen it at all.

SCOPE, STATED SO IT IS NOT CLAIMED AWAY
---------------------------------------
Mapping stage, single code points, table membership. NFKC is NOT audited: RFC 3454 does
not enumerate normalisation, it points at Unicode 3.2, and the only Unicode 3.2 NFKC in
this room is CPython's own `ucd_3_2_0.normalize`. Auditing CPython's normalisation
against CPython's normalisation would be a mirror, not a measurement. So this audit
isolates TABLE conformance and says nothing about normalisation conformance.

Standard library only, except for one optional cross-check (see crosscheck.py).
Deterministic. Offline at measuring time: the one input, sources/rfc3454.txt, is fetched
once beforehand and recorded in sources/MANIFEST.json with its SHA-256.
"""

import json
import os
import re
import stringprep
import sys
import unicodedata
from collections import Counter, defaultdict

from unicodedata import ucd_3_2_0 as ucd32

HERE = os.path.dirname(os.path.abspath(__file__))
RFC = os.path.join(HERE, "sources", "rfc3454.txt")
# Session 65's committed copy. Read, not re-fetched, and not copied into this directory:
# one night's source serves the next.
UTS46 = os.path.join(
    os.path.dirname(HERE), "2026-08-22-a-failure-with-no-fault", "sources",
    "IdnaMappingTable.txt")

MAXCP = 0x10FFFF
SURROGATES = range(0xD800, 0xE000)

# Line inside a table block: a code point or a hyphenated range, then optional
# semicolon-separated fields. Anything that does not match (page footers, the RFC
# header line, blank lines, form feeds) is not data and is skipped.
ROW = re.compile(r"^\s*([0-9A-F]{4,6})(?:-([0-9A-F]{4,6}))?\s*(?:;(.*))?$")

SET_TABLES = ["A.1", "C.1.1", "C.1.2", "C.2.1", "C.2.2", "C.3", "C.4", "C.5",
              "C.6", "C.7", "C.8", "C.9", "D.1", "D.2"]
MAP_TABLES = ["B.1", "B.2", "B.3"]

# The predicate or mapping function CPython exposes for each table.
PREDICATE = {
    "A.1": stringprep.in_table_a1,
    "C.1.1": stringprep.in_table_c11,
    "C.1.2": stringprep.in_table_c12,
    "C.2.1": stringprep.in_table_c21,
    "C.2.2": stringprep.in_table_c22,
    "C.3": stringprep.in_table_c3,
    "C.4": stringprep.in_table_c4,
    "C.5": stringprep.in_table_c5,
    "C.6": stringprep.in_table_c6,
    "C.7": stringprep.in_table_c7,
    "C.8": stringprep.in_table_c8,
    "C.9": stringprep.in_table_c9,
    "D.1": stringprep.in_table_d1,
    "D.2": stringprep.in_table_d2,
}


# ---------------------------------------------------------------- the norm

def parse_rfc3454(path):
    """Return {table_name: {"set": {cp,...}} or {"map": {cp: target}}}.

    Read straight out of the RFC's own enumerated blocks. A mapping row is
    `SOURCE; TARGET...; comment` where TARGET is zero or more space-separated hex
    code points -- empty target means "map to nothing", which is Table B.1 entire.
    """
    sets = defaultdict(set)
    maps = defaultdict(dict)
    current = None
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n").replace("\f", "").rstrip()
            start = re.match(r"\s*----- Start Table (\S+) -----\s*$", line)
            if start:
                current = start.group(1)
                continue
            if re.match(r"\s*----- End Table (\S+) -----\s*$", line):
                current = None
                continue
            if current is None or not line.strip():
                continue
            m = ROW.match(line)
            if not m:
                continue  # page furniture
            lo = int(m.group(1), 16)
            hi = int(m.group(2), 16) if m.group(2) else lo
            rest = m.group(3)
            if current in MAP_TABLES:
                if rest is None:
                    raise ValueError("mapping table %s row without target: %r"
                                     % (current, line))
                target_field = rest.split(";", 1)[0].strip()
                target = "".join(chr(int(h, 16)) for h in target_field.split())
                if lo != hi:
                    raise ValueError("range in mapping table %s: %r" % (current, line))
                maps[current][lo] = target
            else:
                sets[current].update(range(lo, hi + 1))
    out = {}
    for name in SET_TABLES:
        out[name] = {"set": sets[name]}
    for name in MAP_TABLES:
        out[name] = {"map": maps[name]}
    return out


# ---------------------------------------------------------------- the audit

def audit_sets(spec, report):
    """Membership of every set table, over the whole space."""
    for name in SET_TABLES:
        want = spec[name]["set"]
        pred = PREDICATE[name]
        extra, missing = [], []
        for cp in range(MAXCP + 1):
            has = pred(chr(cp))
            should = cp in want
            if has and not should:
                extra.append(cp)
            elif should and not has:
                missing.append(cp)
        report[name] = {
            "kind": "set",
            "rfc_entries": len(want),
            "cpython_extra": len(extra),
            "cpython_missing": len(missing),
            "extra_sample": ["U+%04X" % c for c in extra[:12]],
            "missing_sample": ["U+%04X" % c for c in missing[:12]],
            "_extra": extra,
            "_missing": missing,
        }


def audit_maps(spec, report):
    """Targets of the two mapping tables CPython exposes as functions.

    B.1 is exposed as a predicate (`in_table_b1`), because every one of its targets is
    the empty string; B.2 and B.3 as mapping functions. All three are compared against
    the enumerated rows.
    """
    # B.1 -- a predicate in CPython, a table of nine empty targets in the RFC.
    want_b1 = set(spec["B.1"]["map"])
    extra, missing = [], []
    for cp in range(MAXCP + 1):
        has = stringprep.in_table_b1(chr(cp))
        should = cp in want_b1
        if has and not should:
            extra.append(cp)
        elif should and not has:
            missing.append(cp)
    report["B.1"] = {
        "kind": "map-as-predicate",
        "rfc_entries": len(want_b1),
        "cpython_extra": len(extra),
        "cpython_missing": len(missing),
        "extra_sample": ["U+%04X" % c for c in extra[:12]],
        "missing_sample": ["U+%04X" % c for c in missing[:12]],
        "_extra": extra,
        "_missing": missing,
    }

    for name, fn in (("B.2", stringprep.map_table_b2), ("B.3", stringprep.map_table_b3)):
        want = spec[name]["map"]
        rows = []
        for cp in range(MAXCP + 1):
            src = chr(cp)
            got = fn(src)
            should = want.get(cp, src)  # not in the table -> unchanged
            if got != should:
                rows.append((cp, got, should))
        report[name] = {
            "kind": "map",
            "rfc_entries": len(want),
            "deviating_code_points": len(rows),
            "_rows": rows,
        }

    # A correction to this instrument's own first reading, kept rather than tidied away.
    # The raw B.3 number was recorded here as a conformance defect and it is not one.
    # `map_table_b3` is not built to reproduce Table B.3; it is the inner half of
    # `map_table_b2`, and CPython carries B.2's "Additional folding" rows inside it.
    # Those rows are counted below and excluded from every conformance claim in this
    # work. What remains is the same set the mapping stage finds.
    b2_map = spec["B.2"]["map"]
    b3_rows = report["B.3"]["_rows"]
    by_design = [r for r in b3_rows if r[0] in b2_map and r[1] == b2_map[r[0]]]
    report["B.3"]["of_which_are_table_B_2_additional_foldings_not_a_defect"] = len(by_design)
    report["B.3"]["of_which_are_the_live_lowercase_leak"] = len(b3_rows) - len(by_design)
    report["B.3"]["note"] = (
        "The raw count is NOT a conformance claim. Python's own documentation says this "
        "function returns Table B.3, and it does not; it returns the inner half of "
        "Table B.2, additional foldings included. That is an API/documentation mismatch "
        "with no consequence for nameprep, which calls map_table_b2. Recorded because "
        "this instrument published the raw number first and had to correct itself.")


# ------------------------------------------------- the consequence, and S65's view

def spec_mapping_stage(cp, spec):
    """RFC 3491 section 3: map with Table B.1 (delete) and Table B.2."""
    if cp in spec["B.1"]["map"]:
        return ""
    return spec["B.2"]["map"].get(cp, chr(cp))


def cpython_mapping_stage(cp):
    """The same stage as encodings.idna.nameprep runs it, before NFKC."""
    src = chr(cp)
    if stringprep.in_table_b1(src):
        return ""
    return stringprep.map_table_b2(src)


def parse_uts46(path):
    """Session 65's side B, re-read from its committed table so its classes can be
    reproduced here rather than quoted."""
    table = {}
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
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
    return table


REFUSED = object()


def uts46_nontransitional(cp, table):
    entry = table.get(cp)
    if entry is None:
        return REFUSED
    status, mapping = entry
    if status in ("valid", "deviation", "disallowed_STD3_valid"):
        return chr(cp)
    if status in ("mapped", "disallowed_STD3_mapped"):
        return mapping if mapping is not None else ""
    if status == "ignored":
        return ""
    if status == "disallowed":
        return REFUSED
    raise ValueError("unknown status %r at U+%04X" % (status, cp))


def python_full_nameprep(cp):
    """Session 65's side A: the whole nameprep, which may refuse."""
    import encodings.idna
    try:
        return encodings.idna.nameprep(chr(cp))
    except UnicodeError:
        return REFUSED


def s65_class(cp, uts46_table):
    a = python_full_nameprep(cp)
    b = uts46_nontransitional(cp, uts46_table)
    if a is REFUSED and b is REFUSED:
        return "agree"
    if a is REFUSED:
        return "refused_by_python"
    if b is REFUSED:
        return "refused_by_uts46"
    return "agree" if a == b else "silent_divergence"


def exists_in_3_2(ch):
    try:
        ucd32.name(ch)
        return True
    except ValueError:
        return ucd32.category(ch) != "Cn"


def make_repair(spec):
    """CPython's own map_table_b2, with one line changed.

    `stringprep.map_table_b3` ends `return code.lower()`. Everything else in
    `map_table_b2` -- the two normalisation passes, the second folding, the b != c test
    -- is left exactly as CPython wrote it, and the normalisation is CPython's own
    frozen 3.2 database, the one the module imports and asserts. The single substitution
    is the fallback: instead of asking the live database for a lowercase, look the
    character up in RFC 3454's enumerated Table B.3 and leave it alone if it is not
    there.

    This turns the attribution from a judgement into a test. If a deviation disappears
    under this substitution, that one line caused it. If it survives, something else
    did, and it is counted separately rather than folded in.
    """
    b3 = spec["B.3"]["map"]

    def b3_from_table(code):
        return b3.get(ord(code), code)

    def b2_repaired(a):
        al = b3_from_table(a)
        b = ucd32.normalize("NFKC", al)
        bl = "".join(b3_from_table(ch) for ch in b)
        c = ucd32.normalize("NFKC", bl)
        return c if b != c else al

    return b2_repaired


def attribute(cp, got, should, repaired):
    """Why does CPython's mapping stage differ from the enumerated table here?

    Mechanical, in order, no interpretation:

      repaired_by_the_table   substituting RFC 3454's enumerated Table B.3 for
                              `map_table_b3`'s `return code.lower()` makes the deviation
                              disappear. That one line caused it -- demonstrated by
                              repair, not adjudged.
      escaped_repertoire      as above, AND CPython's output contains a code point that
                              does not exist in Unicode 3.2 at all. A strict subset,
                              separated because it is the form of the evidence that
                              cannot be argued with: a profile whose repertoire is
                              Unicode 3.2 emitted something Unicode 3.2 does not have.
      survives_the_repair     the deviation is still there after the substitution. Not
                              this line's doing; left as its own class rather than
                              folded into the headline number.
    """
    src = chr(cp)
    if repaired(src) == should:
        if any(not exists_in_3_2(ch) for ch in got):
            return "escaped_repertoire"
        return "repaired_by_the_table"
    return "survives_the_repair"


# ---------------------------------------------------------------- main

def main():
    spec = parse_rfc3454(RFC)
    report = {}
    audit_sets(spec, report)
    audit_maps(spec, report)

    uts46_table = parse_uts46(UTS46)
    repaired = make_repair(spec)

    deviations = []
    causes = Counter()
    by_s65_class = Counter()
    directions = Counter()
    in_3_2 = Counter()

    for cp in range(MAXCP + 1):
        if cp in SURROGATES:
            continue  # S65's population, so the cross-reference lines up
        got = cpython_mapping_stage(cp)
        should = spec_mapping_stage(cp, spec)
        if got == should:
            continue
        cause = attribute(cp, got, should, repaired)
        cls = s65_class(cp, uts46_table)
        src = chr(cp)
        direction = ("cpython_maps_where_rfc_does_not" if should == src
                     else "cpython_ignores_an_rfc_row" if got == src
                     else "both_map_differently")
        causes[cause] += 1
        by_s65_class[cls] += 1
        directions[direction] += 1
        in_3_2["assigned" if exists_in_3_2(src) else "unassigned"] += 1
        deviations.append({
            "cp": "U+%04X" % cp,
            "name": unicodedata.name(src, "<unnamed>"),
            "cpython": got,
            "rfc3454": should,
            "cause": cause,
            "direction": direction,
            "assigned_in_unicode_3_2": exists_in_3_2(src),
            "session_65_class": cls,
        })

    # The one number the whole night turns on: of the deviations, how many did S65's
    # two-observer instrument have any chance of seeing?
    visible_to_s65 = by_s65_class["silent_divergence"]
    invisible = sum(v for k, v in by_s65_class.items() if k != "silent_divergence")

    # Does the one-line substitution clear the whole space, or only the rows it was
    # derived from? Run it over every code point, not just the deviating ones.
    remaining = []
    for cp in range(MAXCP + 1):
        if cp in SURROGATES:
            continue
        src = chr(cp)
        got = "" if cp in spec["B.1"]["map"] else repaired(src)
        if got != spec_mapping_stage(cp, spec):
            remaining.append("U+%04X" % cp)

    # The 3.2-assigned deviations are the ones S65's argument about queries cannot
    # reach, so name what they actually are rather than counting them.
    assigned_rows = [d for d in deviations if d["assigned_in_unicode_3_2"]]
    cherokee = [d for d in assigned_rows if 0x13A0 <= int(d["cp"][2:], 16) <= 0x13F5]
    not_cherokee = [d for d in assigned_rows if d not in cherokee]

    results = {
        "generated_by": "audit.py",
        "date": "2026-08-22",
        "session": 66,
        "takes_up": "Session 65, open thread 4 -- the falsifier it stated against itself",
        "scope": ("table conformance and the mapping stage, single code points; "
                  "normalisation is not audited and no claim is made about it"),
        "environment": {
            "python": sys.version.split()[0],
            "unicodedata_version": unicodedata.unidata_version,
            "frozen_database_stringprep_asserts": ucd32.unidata_version,
        },
        "norm": {
            "file": "sources/rfc3454.txt",
            "what": "RFC 3454, the enumerated tables, read verbatim",
            "tables_parsed": {n: (len(spec[n].get("set", spec[n].get("map"))))
                              for n in SET_TABLES + MAP_TABLES},
        },
        "table_conformance": {
            n: {k: v for k, v in report[n].items() if not k.startswith("_")}
            for n in SET_TABLES + MAP_TABLES
        },
        "mapping_stage": {
            "population": 1112064,
            "deviating_code_points": len(deviations),
            "by_cause": dict(causes),
            "by_direction": dict(directions),
            "assigned_in_unicode_3_2": dict(in_3_2),
            "by_session_65_class": dict(by_s65_class),
            "visible_to_session_65": visible_to_s65,
            "invisible_to_session_65": invisible,
        },
        "the_one_line_repair": {
            "what": ("stringprep.map_table_b3's `return code.lower()` replaced by a "
                     "lookup in RFC 3454's enumerated Table B.3; everything else in "
                     "map_table_b2 unchanged"),
            "deviating_code_points_after_repair": len(remaining),
            "remaining": remaining[:40],
        },
        "the_3_2_assigned_deviations": {
            "total": len(assigned_rows),
            "cherokee_U_13A0_13F5": len(cherokee),
            "everything_else": [
                {"cp": d["cp"], "name": d["name"], "cpython": d["cpython"],
                 "rfc3454": d["rfc3454"], "session_65_class": d["session_65_class"]}
                for d in not_cherokee],
        },
    }

    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    with open(os.path.join(HERE, "deviations.json"), "w", encoding="utf-8") as fh:
        json.dump({"count": len(deviations), "rows": deviations}, fh,
                  indent=2, ensure_ascii=False)
        fh.write("\n")

    print(json.dumps(results["table_conformance"], indent=2))
    print(json.dumps(results["mapping_stage"], indent=2))


if __name__ == "__main__":
    main()
