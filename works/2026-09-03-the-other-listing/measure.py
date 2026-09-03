#!/usr/bin/env python3
"""Session 78 (2026-09-03) -- the other listing.

Measures the several published faces of one institution's SQLSTATE vocabulary
against each other and against the machine that imposes them.

Usage:  python3 measure.py <path-to-postgresql-18.6-tree> <out.json>

Nothing is fetched here and nothing is built.  The tree is the unpacked source
tarball, identified by the SHA-256 in sources/MANIFEST.json.

Sets, exactly as fixed in PREDICTIONS.md before this file existed:

  V  the published vocabulary   -- field 1 of every code line of errcodes.txt
  A  the Appendix A face        -- members of V whose line carries a condition name
  E  the ecpg face              -- 5-char codes named after the word SQLSTATE in ecpg.sgml
  M  the manual face            -- the same rule over every file of doc/src/sgml/
  C  the constant face          -- bodies of #defines whose name contains SQLSTATE

Every count is a count of distinct codes.  Every match is kept with its file,
line and surrounding text, so that a reader can disagree with the rule rather
than only with the number (F-100: look at the hits before counting them).
"""

import json
import os
import re
import sys

CODE = r"[0-9A-Z]{5}"

# The extraction rule for E and M, fixed in PREDICTIONS.md: the word SQLSTATE,
# then only whitespace and SGML markup, then a five-character code.
ADJ_RE = re.compile(r"\bSQLSTATE\b(?:\s|<[^>]*>)*(" + CODE + r")(?![0-9A-Za-z_])")

# Everything the same corpus offers that the rule does NOT take, so the rule can
# be argued with (F-087: a limit observed once is a conjecture -- test it).
BARE_RE = re.compile(r"(?<![0-9A-Za-z_])(" + CODE + r")(?![0-9A-Za-z_])")

DEFINE_RE = re.compile(
    r"#\s*define\s+(\w*SQLSTATE\w*)\s+\"(" + CODE + r")\""
)

# "the tree itself says so", second form: a five-character literal handed to
# something whose name contains sqlstate.
ASSIGN_RE = re.compile(
    r"(\w*[sS][qQ][lL][sS][tT][aA][tT][eE]\w*)[^;\n]{0,80}?\"(" + CODE + r")\""
)

SKIP_DIRS = {".git"}
TEXT_EXT = {
    ".c", ".h", ".y", ".l", ".pl", ".pm", ".py", ".sgml", ".xml", ".txt",
    ".sql", ".pgc", ".out", ".source", ".md", ".in", ".am", ".mk", ".conf",
    ".tcl", ".pool", ".dtd", ".xsl", ".css", ".sh", ".data", ".spec", ".po",
}


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except (OSError, UnicodeError):
        return None


def walk(root, subdir=""):
    base = os.path.join(root, subdir) if subdir else root
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield os.path.join(dirpath, name)


def rel(root, path):
    return os.path.relpath(path, root)


# ---------------------------------------------------------------- V and A

def parse_vocabulary(root):
    """Parse errcodes.txt as ROWS, not as a mapping keyed by code.

    The first version of this function keyed a dict by the SQLSTATE, which is
    not a key: six codes carry two rows each.  That defect is the reason the
    duplication was found at all, and it also produced a false count, so the
    parser is row-based and both units are reported (register 034, F-102).
    """
    path = os.path.join(root, "src/backend/utils/errcodes.txt")
    text = read(path)
    lines = text.split("\n")
    rows, dropped, section = [], [], None
    for n, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("Section:"):
            section = stripped[len("Section:"):].strip()
            dropped.append([n, stripped[:70]])
            continue
        if not stripped or stripped.startswith("#"):
            dropped.append([n, stripped[:70]])
            continue
        fields = stripped.split()
        if not re.fullmatch(CODE, fields[0]):
            dropped.append([n, stripped[:70]])
            continue
        rows.append({
            "sqlstate": fields[0],
            "line": n,
            "section": section,
            "severity": fields[1] if len(fields) > 1 else None,
            "macro": fields[2] if len(fields) > 2 else None,
            "condition": fields[3] if len(fields) > 3 else None,
            "nfields": len(fields),
        })
    return rows, dropped, len(lines)


# ---------------------------------------------------- E, M and their misses

def adjacency_hits(root, paths):
    """Every code the adjacency rule takes, with evidence."""
    hits = {}
    for path in paths:
        text = read(path)
        if text is None:
            continue
        for m in ADJ_RE.finditer(text):
            code = m.group(1)
            line = text.count("\n", 0, m.start()) + 1
            ctx = " ".join(text[max(0, m.start() - 90):m.end() + 60].split())
            hits.setdefault(code, []).append(
                {"file": rel(root, path), "line": line, "context": ctx}
            )
    return hits


def adjacency_misses(root, paths, taken):
    """Every bare five-character token the rule did NOT take, for hand-reading."""
    misses = {}
    for path in paths:
        text = read(path)
        if text is None:
            continue
        taken_spans = [m.span(1) for m in ADJ_RE.finditer(text)]
        for m in BARE_RE.finditer(text):
            if m.span(1) in taken_spans:
                continue
            code = m.group(1)
            line = text.count("\n", 0, m.start()) + 1
            ctx = " ".join(text[max(0, m.start() - 70):m.end() + 40].split())
            misses.setdefault(code, []).append(
                {"file": rel(root, path), "line": line, "context": ctx}
            )
    return misses


# ------------------------------------------------- the ecpg varlist entries

ENTRY_RE = re.compile(r"<varlistentry\b.*?</varlistentry>", re.S)
TERM_RE = re.compile(r"<term>(.*?)</term>", re.S)


def ecpg_entries(root):
    path = os.path.join(root, "doc/src/sgml/ecpg.sgml")
    text = read(path)
    entries = []
    for m in ENTRY_RE.finditer(text):
        block = m.group(0)
        codes = ADJ_RE.findall(block)
        if not codes:
            continue
        term = TERM_RE.search(block)
        term_text = " ".join(re.sub(r"<[^>]*>", "", term.group(1)).split()) if term else None
        body = re.sub(r"<term>.*?</term>", "", block, flags=re.S)
        body = " ".join(re.sub(r"<[^>]*>", " ", body).split())
        entries.append({
            "line": text.count("\n", 0, m.start()) + 1,
            "term": term_text,
            "codes": sorted(set(codes)),
            "text": body,
        })
    return entries


# ------------------------------------------------------------------ C, S2

def constant_face(root):
    defines, assigns = {}, {}
    for path in walk(root):
        ext = os.path.splitext(path)[1]
        if ext not in TEXT_EXT:
            continue
        text = read(path)
        if text is None:
            continue
        for m in DEFINE_RE.finditer(text):
            name, code = m.group(1), m.group(2)
            line = text.count("\n", 0, m.start()) + 1
            defines.setdefault(code, []).append(
                {"file": rel(root, path), "line": line, "name": name}
            )
        for m in ASSIGN_RE.finditer(text):
            name, code = m.group(1), m.group(2)
            if DEFINE_RE.search(m.group(0)):
                continue
            line = text.count("\n", 0, m.start()) + 1
            ctx = " ".join(m.group(0).split())
            assigns.setdefault(code, []).append(
                {"file": rel(root, path), "line": line, "via": name, "context": ctx}
            )
    return defines, assigns


# ------------------------------------------------------- literal occurrence

def literal_sites(root, codes, subdir):
    """Every plain occurrence of each code literal under subdir."""
    found = {c: [] for c in codes}
    pattern = re.compile(
        r"(?<![0-9A-Za-z_])(" + "|".join(sorted(codes)) + r")(?![0-9A-Za-z_])"
    ) if codes else None
    if pattern is None:
        return found
    for path in walk(root, subdir):
        ext = os.path.splitext(path)[1]
        if ext not in TEXT_EXT:
            continue
        text = read(path)
        if text is None:
            continue
        for m in pattern.finditer(text):
            code = m.group(1)
            line = text.count("\n", 0, m.start()) + 1
            ctx = " ".join(text[max(0, m.start() - 70):m.end() + 40].split())
            found[code].append({"file": rel(root, path), "line": line, "context": ctx})
    return found


# ----------------------------------------------------------------- the run

def main():
    root, out = sys.argv[1], sys.argv[2]

    rows, dropped, nlines = parse_vocabulary(root)
    by_code = {}
    for r in rows:
        by_code.setdefault(r["sqlstate"], []).append(r)
    V = set(by_code)
    A = {r["sqlstate"] for r in rows if r["condition"]}
    A_rows = [r for r in rows if r["condition"]]
    duplicates = {c: rs for c, rs in by_code.items() if len(rs) > 1}
    classes = sorted({c[:2] for c in V})
    severity_by_code = {}
    for c, rs in by_code.items():
        severity_by_code[c] = sorted({r["severity"] for r in rs})

    doc_paths = sorted(p for p in walk(root, "doc/src/sgml"))
    ecpg_path = os.path.join(root, "doc/src/sgml/ecpg.sgml")

    E_hits = adjacency_hits(root, [ecpg_path])
    M_hits = adjacency_hits(root, doc_paths)
    E, M = set(E_hits), set(M_hits)

    other_doc = [p for p in doc_paths if os.path.abspath(p) != os.path.abspath(ecpg_path)]
    M_other_hits = adjacency_hits(root, other_doc)
    M_other = set(M_other_hits)

    misses = adjacency_misses(root, [ecpg_path], E)

    entries = ecpg_entries(root)
    defines, assigns = constant_face(root)
    C = set(defines)

    seven = ["07001", "07002", "07006", "07009", "33000", "YE000", "YE001"]
    seven_in_doc = literal_sites(root, set(seven), "doc/src/sgml")

    ecpg_src = literal_sites(root, E, "src/interfaces/ecpg")

    result = {
        "object": "postgresql-18.6 source tarball",
        "vocabulary": {
            "file": "src/backend/utils/errcodes.txt",
            "file_lines": nlines,
            "n_rows": len(rows),
            "V": sorted(V),
            "n_V": len(V),
            "A": sorted(A),
            "n_A": len(A),
            "n_A_rows": len(A_rows),
            "duplicate_codes": {c: rs for c, rs in sorted(duplicates.items())},
            "n_duplicate_codes": len(duplicates),
            "classes": classes,
            "n_classes": len(classes),
            "non_code_lines": len(dropped),
            "severity_by_code": severity_by_code,
            "rows": rows,
        },
        "ecpg_face": {
            "n_E": len(E),
            "E": sorted(E),
            "hits": E_hits,
            "E_minus_V": sorted(E - V),
            "n_E_minus_V": len(E - V),
            "E_and_V": sorted(E & V),
            "entries": entries,
            "rule_misses_in_ecpg_sgml": {k: v for k, v in sorted(misses.items())},
        },
        "manual_face": {
            "n_M": len(M),
            "M": sorted(M),
            "M_minus_V": sorted(M - V),
            "n_M_minus_V": len(M - V),
            "files_with_hits": sorted({h["file"] for hs in M_hits.values() for h in hs}),
            "outside_ecpg": {
                "n": len(M_other),
                "codes": sorted(M_other),
                "minus_V": sorted(M_other - V),
                "n_minus_V": len(M_other - V),
                "hits": M_other_hits,
            },
        },
        "constant_face": {
            "n_C": len(C),
            "C": sorted(C),
            "C_minus_V": sorted(C - V),
            "n_C_minus_V": len(C - V),
            "defines": defines,
            "sqlstate_named_assignments": assigns,
        },
        "session_77_seven": {
            "codes": seven,
            "in_doc_sources": {c: seven_in_doc[c] for c in seven},
            "n_in_doc": sum(1 for c in seven if seven_in_doc[c]),
        },
        "ecpg_implementation": {
            "codes_with_no_literal_under_src_interfaces_ecpg":
                sorted(c for c in E if not ecpg_src[c]),
            "n_absent": sum(1 for c in E if not ecpg_src[c]),
            "sites": {c: ecpg_src[c] for c in sorted(E)},
        },
    }

    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, sort_keys=False)

    print(f"rows = {len(rows)}   |V| = {len(V)}   codes with two rows = {len(duplicates)}")
    print(f"|A| = {len(A)}   rows with a condition name = {len(A_rows)}"
          f"   classes = {len(classes)}")
    print(f"|E| = {len(E)}   |E\\V| = {len(E - V)}   -> {sorted(E - V)}")
    print(f"|M| = {len(M)}   |M\\V| = {len(M - V)}")
    print(f"outside ecpg.sgml: |M'| = {len(M_other)}   |M'\\V| = {len(M_other - V)}"
          f"   -> {sorted(M_other - V)}")
    print(f"|C| = {len(C)}   |C\\V| = {len(C - V)}   -> {sorted(C - V)}")
    print(f"seven of S77 present in doc/src/sgml: {result['session_77_seven']['n_in_doc']} of 7")
    print(f"E-codes with no literal in ecpg's own source: "
          f"{result['ecpg_implementation']['n_absent']}"
          f" -> {result['ecpg_implementation']['codes_with_no_literal_under_src_interfaces_ecpg']}")
    print(f"ecpg varlist entries naming a SQLSTATE: {len(entries)}")


if __name__ == "__main__":
    main()
