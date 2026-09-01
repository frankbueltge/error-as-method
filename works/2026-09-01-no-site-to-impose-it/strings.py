"""strings.py -- RULE C, written after the measurement and because the measurement was
wrong.

`instrument.py` counts a norm's sites by its **macro name**. Reading the five members of
bucket 2 by hand (F-096) showed that the macro is not the only way this system names a
SQLSTATE: `src/interfaces/ecpg/ecpglib/ecpglib_extern.h` defines its own constants as
five-character **string literals** -- `#define ECPG_SQLSTATE_NO_DATA "02000"` -- and the
embedded-SQL client library imposes codes through those, never touching the macro. Three
codes that rule B called siteless are named on that route.

So rule C: find every quoted five-character SQLSTATE-shaped literal in the tree, under the
same file classification, and report

  - which of the 268 published codes are named that way and where;
  - which of those names are themselves never used, i.e. a constant defined for a norm and
    then not imposed either;
  - and which SQLSTATE-shaped literals the implementation carries that the published
    vocabulary does **not** contain.

This file exists because the fixture in `interface_test.py` could not have caught the miss:
it was written by the same person who wrote rule A, out of the same model of the object, and
it contained only the form that model already had. **F-099.**

Usage:  python3 strings.py <tree-root> <results.json> <out.json>
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instrument  # noqa: E402

# A SQLSTATE is five characters from [0-9A-Z]; the vocabulary's own format comment says so.
LITERAL_RE = re.compile(r'"([0-9A-Z]{5})"')
# a C #define whose body is such a literal
DEFINE_RE = re.compile(r'^\s*#\s*define\s+([A-Za-z_][A-Za-z0-9_]*)\s+"([0-9A-Z]{5})"',
                       re.MULTILINE)


def main(root, results_path, out):
    res = json.load(open(results_path, encoding="utf-8"))
    published = {r["sqlstate"]: r for r in res["rows"]}
    siteless = {r["sqlstate"] for r in res["siteless"]}

    literal_hits = {}          # sqlstate -> [ "rel:line" ]
    defines = {}               # constant name -> {"sqlstate":..., "file":..., "line":...}
    unknown_literals = {}      # sqlstate not in the vocabulary -> [ "rel:line" ]

    for rel, klass, text in instrument.walk(root):
        pass  # walk() only yields files carrying ERRCODE_; not the right net here.

    # Walk the whole tree with the instrument's own file classification and extension set,
    # but without requiring the string 'ERRCODE_' to be present -- the ecpg header does not
    # contain it.
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            if os.path.splitext(name)[1].lower() not in instrument.READ_EXT:
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            try:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except (OSError, UnicodeError):
                continue
            head = "\n".join(text.split("\n", 3)[:3])
            klass = instrument.classify(rel, head)
            if klass != "implementation":
                continue
            lines = text.split("\n")
            for i, line in enumerate(lines, 1):
                for m in LITERAL_RE.finditer(line):
                    code = m.group(1)
                    where = "%s:%d" % (rel, i)
                    if code in published:
                        literal_hits.setdefault(code, []).append(where)
                    else:
                        unknown_literals.setdefault(code, []).append(where)
            for m in DEFINE_RE.finditer(text):
                const, code = m.group(1), m.group(2)
                line = text[:m.start()].count("\n") + 1
                defines[const] = {"sqlstate": code, "file": rel, "line": line,
                                  "published": code in published}

    # For every constant defined as a SQLSTATE literal: is the constant itself ever used?
    const_uses = {c: 0 for c in defines}
    const_res = {c: re.compile(r"\b%s\b" % re.escape(c)) for c in defines}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            if os.path.splitext(name)[1].lower() not in instrument.READ_EXT:
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            try:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except (OSError, UnicodeError):
                continue
            head = "\n".join(text.split("\n", 3)[:3])
            if instrument.classify(rel, head) != "implementation":
                continue
            for c, rx in const_res.items():
                n = len(rx.findall(text))
                if n:
                    # the defining line is not a use
                    if rel == defines[c]["file"]:
                        n -= 1
                    const_uses[c] += n

    # The correction to P1: siteless codes that rule C finds a live route to.
    rescued = []
    still_siteless = []
    for code in sorted(siteless):
        hits = literal_hits.get(code, [])
        # a hit is live if it is a #define whose constant is used, or a direct literal use
        live = []
        for h in hits:
            f, ln = h.rsplit(":", 1)
            const = None
            for c, d in defines.items():
                if d["sqlstate"] == code and d["file"] == f and d["line"] == int(ln):
                    const = c
                    break
            if const is None:
                live.append({"where": h, "via": "direct literal"})
            elif const_uses[const] > 0:
                live.append({"where": h, "via": const, "uses": const_uses[const]})
        row = {"sqlstate": code, "macro": published[code]["macro"],
               "condition": published[code]["condition"],
               "literal_hits": hits, "live_routes": live}
        (rescued if live else still_siteless).append(row)

    payload = {
        "why": "rule C, written after reading bucket 2 by hand; the macro is not the only "
               "way this tree names a SQLSTATE",
        "n_published": len(published),
        "published_codes_named_as_literals": {
            k: v for k, v in sorted(literal_hits.items())},
        "sqlstate_defines": {k: dict(v, uses=const_uses[k])
                             for k, v in sorted(defines.items())},
        "defines_never_used": sorted(c for c in defines if const_uses[c] == 0),
        # The loose scan below matches ANY five-character upper-case quoted string, which
        # in a SQL implementation means every keyword of that length -- ORDER, GROUP,
        # WHERE, TABLE -- plus test numbers. It is kept whole and labelled rather than
        # filtered silently, because the count is a fact about this instrument and about
        # how weak "SQLSTATE-shaped" is as a pattern in this tree. F-100.
        "loose_five_character_literals_not_in_the_vocabulary": {
            "warning": "this set is dominated by SQL keywords and numeric test data; it "
                       "is NOT a set of SQLSTATEs and no claim is made from it",
            "n": len(unknown_literals),
            "codes": {k: v[:3] for k, v in sorted(unknown_literals.items())},
        },
        # The defensible version: a five-character literal is treated as a SQLSTATE only
        # where the tree itself says so, by defining it under a name containing SQLSTATE.
        "sqlstates_the_implementation_defines_and_the_vocabulary_lacks": sorted(
            {d["sqlstate"] for c, d in defines.items()
             if "SQLSTATE" in c.upper() and not d["published"]}),
        "P1_correction": {
            "siteless_under_rules_A_and_B": len(siteless),
            "of_those_with_a_live_string_route": len(rescued),
            "siteless_under_A_B_and_C": len(still_siteless),
            "rescued": rescued,
        },
        "still_siteless": still_siteless,
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)

    print("rule C over %s" % os.path.basename(os.path.abspath(root)))
    print("  published codes named as string literals : %d" % len(literal_hits))
    print("  SQLSTATE-shaped #defines found           : %d (%d never used)"
          % (len(defines), len(payload["defines_never_used"])))
    loose = payload["loose_five_character_literals_not_in_the_vocabulary"]["n"]
    named = payload["sqlstates_the_implementation_defines_and_the_vocabulary_lacks"]
    print("  loose 5-char literals not in the vocabulary: %d (mostly SQL keywords -- "
          "not a finding)" % loose)
    print("  SQLSTATEs the tree DEFINES as such and the vocabulary lacks: %d  %s"
          % (len(named), ", ".join(named)))
    print("  P1: %d siteless under A+B -> %d rescued -> %d siteless under A+B+C"
          % (len(siteless), len(rescued), len(still_siteless)))
    for r in rescued:
        print("     rescued %s %s via %s"
              % (r["sqlstate"], r["macro"],
                 ", ".join(x.get("via", "?") for x in r["live_routes"])))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
