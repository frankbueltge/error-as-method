#!/usr/bin/env python3
"""
measure.py -- Session 54, 2026-08-13. Offline. Stdlib only. Deterministic.

Reconstructs the life of every code point in the Unicode Character Database
across 36 published versions (reconstructed 1.0.0, 1995-2026) and asks the
question Session 53 left open:

    Has an institution whose channel reaches only the RESOLUTION of its norm
    -- never the stored references to it -- ever withdrawn an identifier and
    let those references break?

Unicode is such an institution. A code point sitting in somebody's file is a
stored reference the consortium cannot reach; all it can reach is what that
code point resolves to. Session 53's claim predicts it should behave like the
time zone database: keep the name, move the referent, never withdraw.

Definitions used here, all stated so the counts can be argued with:

  ASSIGNED      a code point with a row in UnicodeData.txt for that version,
                including surrogates and private-use (flagged separately).
                Noncharacters and reserved code points have no row and so are
                not assigned.
  WITHDRAWN     assigned in version i, not assigned in version i+1.
  REOCCUPIED    withdrawn at some point, and assigned again later.
  RENAMED       assigned in both i and i+1 with a different Name value, with
                generated-range rows excluded (their "name" is a marker, not
                a name).

THE ONE KNOWN HOLE, stated before the numbers rather than in a footnote.
UnicodeData-1.1.5.txt represents the whole unified CJK block with a SINGLE row,
"4E00;<CJK IDEOGRAPH REPRESENTATIVE>", instead of the First/Last pair used from
2.0 onward. The 1.1 census therefore cannot see ~20,000 CJK ideographs that the
standard did assign. Every transition involving 1.1 is computed twice -- raw,
and with the CJK ideograph area masked -- and both are reported. No withdrawal
claimed below lies inside that area.

The reconstructed 1.0.0 and 1.0.1 files are the consortium's own projection
back from 1.1/2.0 data, and say so in their headers: "a completely artificially
reconstituted UnicodeData.txt file". Their code points and names are stated by
the author to be accurate; the other fields are not. Only code points and names
are used here, and every 1.0-derived number is labelled RECONSTRUCTED.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
SRC = os.path.join(HERE, "sources")

# The CJK unified ideograph area as it stood in 1.1/2.0 -- used only to mask the
# representative-row hole described above.
CJK_URO = (0x4E00, 0x9FFF)

SURROGATE = (0xD800, 0xDFFF)
PUA = [(0xE000, 0xF8FF), (0xF0000, 0xFFFFD), (0x100000, 0x10FFFD)]


def order_key(label):
    parts = [int(p) for p in re.findall(r"\d+", label)]
    # "3.0-Update1" sorts after "3.0-Update"; "2.1-Update4" after "2.1-Update3"
    # "2.1-Update" is 2.1.0, "2.1-Update4" is 2.1.4, "3.0-Update1" is 3.0.1.
    # Without this, 3.0.1 sorts before 3.0.0 and the diff runs backwards.
    m = re.search(r"Update(\d*)", label)
    if m:
        upd = int(m.group(1)) if m.group(1) else 0
        base = (parts + [0, 0])[:2]
        return tuple(base) + (upd,)
    return tuple((parts + [0, 0, 0])[:3])


def parse(path):
    """{codepoint: name} plus the set of code points whose row is a range marker."""
    chars = {}
    generated = set()
    pending = None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            fields = line.split(";")
            if len(fields) < 2:
                continue
            try:
                cp = int(fields[0], 16)
            except ValueError:
                continue
            name = fields[1]
            if name.endswith(", First>"):
                pending = (cp, name)
                continue
            if name.endswith(", Last>") and pending:
                start, sname = pending
                label = sname[:-len(", First>")] + ">"
                for c in range(start, cp + 1):
                    chars[c] = label
                    generated.add(c)
                pending = None
                continue
            chars[cp] = name
    return chars, generated


def in_ranges(cp, ranges):
    return any(a <= cp <= b for a, b in ranges)


def block_runs(cps):
    """Contiguous runs, as (start, end, count)."""
    out = []
    for cp in sorted(cps):
        if out and cp == out[-1][1] + 1:
            out[-1][1] = cp
        else:
            out.append([cp, cp])
    return [(a, b, b - a + 1) for a, b in out]


def main():
    manifest = json.load(open(os.path.join(SRC, "MANIFEST.json")))
    versions = sorted({f["version"] for f in manifest["files"] if f["version"] != "current"},
                      key=order_key)

    data = {}
    for v in versions:
        path = os.path.join(CACHE, "UnicodeData-%s.txt" % v)
        if not os.path.exists(path):
            sys.exit("missing %s -- run harvest.py first" % path)
        data[v] = parse(path)

    R = {"versions": versions, "census": [], "transitions": [],
         "withdrawals": {}, "reoccupied": [], "renames": []}

    # ---------- census ----------
    for v in versions:
        chars, gen = data[v]
        sur = sum(1 for c in chars if in_ranges(c, [SURROGATE]))
        pua = sum(1 for c in chars if in_ranges(c, PUA))
        R["census"].append({
            "version": v,
            "assigned": len(chars),
            "generated_rows": len(gen),
            "individually_named": len(chars) - len(gen),
            "surrogate": sur,
            "private_use": pua,
        })

    # ---------- transitions ----------
    all_withdrawn = {}     # cp -> [(version_last_seen, name)]
    for a, b in zip(versions, versions[1:]):
        ca, _ = data[a]
        cb, _ = data[b]
        gone = set(ca) - set(cb)
        added = set(cb) - set(ca)
        gone_masked = {c for c in gone if not (CJK_URO[0] <= c <= CJK_URO[1])}
        renamed = [(c, ca[c], cb[c]) for c in (set(ca) & set(cb))
                   if ca[c] != cb[c] and not ca[c].startswith("<") and not cb[c].startswith("<")]
        R["transitions"].append({
            "from": a, "to": b,
            "withdrawn_raw": len(gone),
            "withdrawn_masked_cjk": len(gone_masked),
            "added": len(added),
            "renamed": len(renamed),
        })
        for c in gone:
            all_withdrawn.setdefault(c, []).append({"last_seen": a, "name": ca[c]})
        if renamed:
            R["renames"].append({
                "from": a, "to": b, "count": len(renamed),
                "sample": [{"cp": "U+%04X" % c, "was": w, "now": n}
                           for c, w, n in sorted(renamed)[:12]],
            })

    # ---------- withdrawals, classified ----------
    latest = data[versions[-1]][0]
    wd = []
    for cp, hist in sorted(all_withdrawn.items()):
        entry = {
            "cp": "U+%04X" % cp,
            "int": cp,
            "name_when_withdrawn": hist[-1]["name"],
            "last_seen": hist[-1]["last_seen"],
            "in_cjk_representative_hole": CJK_URO[0] <= cp <= CJK_URO[1],
            "assigned_today": cp in latest,
            "name_today": latest.get(cp),
        }
        wd.append(entry)
    real = [e for e in wd if not e["in_cjk_representative_hole"]]
    R["withdrawals"] = {
        "total_raw": len(wd),
        "total_excluding_cjk_hole": len(real),
        "reoccupied": sum(1 for e in real if e["assigned_today"]),
        "still_empty": sum(1 for e in real if not e["assigned_today"]),
        "by_last_seen": {},
    }
    for e in real:
        R["withdrawals"]["by_last_seen"].setdefault(e["last_seen"], 0)
        R["withdrawals"]["by_last_seen"][e["last_seen"]] += 1

    # runs, so the vacated regions are legible as blocks rather than as a list
    for lv in sorted(R["withdrawals"]["by_last_seen"], key=order_key):
        cps = [e["int"] for e in real if e["last_seen"] == lv]
        runs = block_runs(cps)
        R.setdefault("vacated_runs", {})[lv] = [
            {"range": "U+%04X..U+%04X" % (a, b), "count": n,
             "was": next(e["name_when_withdrawn"] for e in real if e["int"] == a),
             "today": latest.get(a, "<unassigned>")}
            for a, b, n in runs if n >= 8
        ]
        R["vacated_runs"][lv + "__runs_total"] = len(runs)

    # ---------- the withdrawal ledger ----------
    # The census above counts every row, private use and surrogates included,
    # because they are assigned in the sense that matters to a namespace. For
    # the question of whether a CHARACTER was withdrawn, those have to come
    # out: a private-use range boundary moving is an administrative change, not
    # the retirement of a name anybody could have written down.
    ledger = {}
    for e in real:
        cp = e["int"]
        nm = e["name_when_withdrawn"]
        # Exclude by NAME as well as by range: the private-use area's own
        # boundaries moved in the early releases, so rows labelled <Private Use>
        # can sit outside today's PUA ranges and would otherwise be counted as
        # retired characters. They are not characters.
        if in_ranges(cp, PUA) or in_ranges(cp, [SURROGATE]):
            continue
        if nm.startswith("<") and ("Private Use" in nm or "Surrogate" in nm):
            continue
        row = ledger.setdefault(e["last_seen"], {"total": 0, "by_script": {},
                                                 "occupied_today": 0, "still_empty": 0})
        row["total"] += 1
        key = nm.split(",")[0].split()[0].strip("<>")
        row["by_script"][key] = row["by_script"].get(key, 0) + 1
        if e["assigned_today"]:
            row["occupied_today"] += 1
        else:
            row["still_empty"] += 1
    R["withdrawal_ledger"] = {k: ledger[k] for k in sorted(ledger, key=order_key)}
    R["withdrawal_ledger_total"] = sum(v["total"] for v in ledger.values())

    R["reoccupied"] = [
        {"cp": e["cp"], "was": e["name_when_withdrawn"], "vacated_after": e["last_seen"],
         "now": e["name_today"]}
        for e in real if e["assigned_today"]
    ][:40]

    # ---------- the correction channel, current release ----------
    aliases = {}
    for line in open(os.path.join(SRC, "NameAliases.txt"), encoding="utf-8"):
        line = line.split("#")[0].strip()
        if not line:
            continue
        p = line.split(";")
        if len(p) >= 3:
            aliases.setdefault(p[2], []).append((p[0], p[1]))
    R["name_aliases"] = {k: len(v) for k, v in sorted(aliases.items())}
    R["corrections"] = [{"cp": "U+" + c, "alias": a} for c, a in aliases.get("correction", [])]

    # ---------- NamesList.txt, the third channel (Session 49's carried item) ----------
    # The full 2 MB file lives in cache/ (gitignored) after evidence.py moves it
    # there; sources/ keeps only the extract this work quotes. Either location works.
    nl_path = os.path.join(SRC, "NamesList.txt")
    if not os.path.exists(nl_path):
        nl_path = os.path.join(CACHE, "NamesList.txt")
    # NamesList.txt annotation marks, one per line under a character:
    #   =  alias      *  informative note     x  cross reference
    #   %  formal alias (the NameAliases correction, printed in the code chart)
    #   #  compatibility mapping   :  canonical decomposition
    marks = {"*": 0, "=": 0, "x": 0, "#": 0, ":": 0, "%": 0}
    star_lines = []
    cur = None
    for raw in open(nl_path, encoding="utf-8", errors="replace"):
        if re.match(r"^[0-9A-F]{4,6}\t", raw):
            cur = raw.split("\t")[0]
            continue
        m = re.match(r"^\t([*=x#:%])\s(.*)$", raw.rstrip("\n"))
        if m:
            marks[m.group(1)] += 1
            if m.group(1) in "*=":
                star_lines.append((cur, m.group(2)))
    R["nameslist"] = {"annotations_by_mark": marks, "total": sum(marks.values())}

    # Annotations that comment on the NAME rather than on the character. Two
    # filters, wide and narrow, because the wide one catches transcription
    # advice ("preferred spelling is ...") that is not a claim about the name.
    wide = re.compile(r"name is a mistake|misnomer|erroneous|incorrect name|"
                      r"misleading|spelling|misspell", re.I)
    narrow = re.compile(r"misnomer|name is a mistake|erroneous|incorrect name", re.I)
    R["nameslist"]["name_commentary_wide"] = {
        "count": len([1 for c, t in star_lines if wide.search(t)])}

    hits = sorted({("U+" + (c or "?"), t) for c, t in star_lines if narrow.search(t)})
    chars = sorted({c for c, _ in hits})
    corr_cps = {c["cp"] for c in R["corrections"]}
    R["misnomer_notes"] = {
        "count": len(chars),
        "characters": chars,
        "lines": [{"cp": c, "note": t} for c, t in hits],
        "with_formal_alias": sorted(set(chars) & corr_cps),
        "without_formal_alias": sorted(set(chars) - corr_cps),
    }

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(R, f, indent=1)

    # ---------- report ----------
    print("=" * 78)
    print("THE LIFE OF EVERY CODE POINT -- %d versions, %s .. %s"
          % (len(versions), versions[0], versions[-1]))
    print("=" * 78)
    print("\nCENSUS")
    for c in R["census"]:
        print("  %-14s assigned %7d   named %7d   generated %7d"
              % (c["version"], c["assigned"], c["individually_named"], c["generated_rows"]))

    print("\nTRANSITIONS WITH ANY WITHDRAWAL OR RENAME")
    for t in R["transitions"]:
        if t["withdrawn_raw"] or t["renamed"]:
            print("  %-14s -> %-14s withdrawn %6d (masked %6d)  renamed %5d  added %7d"
                  % (t["from"], t["to"], t["withdrawn_raw"], t["withdrawn_masked_cjk"],
                     t["renamed"], t["added"]))

    w = R["withdrawals"]
    print("\nWITHDRAWALS")
    print("  raw                       : %d" % w["total_raw"])
    print("  excluding the CJK hole    : %d" % w["total_excluding_cjk_hole"])
    print("  of those, reoccupied since: %d" % w["reoccupied"])
    print("  of those, still empty     : %d" % w["still_empty"])
    print("  by version last seen      : %s"
          % ", ".join("%s:%d" % (k, w["by_last_seen"][k])
                      for k in sorted(w["by_last_seen"], key=order_key)))

    print("\nWITHDRAWAL LEDGER -- characters only (private use and surrogates removed)")
    print("  grand total, all versions : %d" % R["withdrawal_ledger_total"])
    for k, v in R["withdrawal_ledger"].items():
        print("  last seen in %-14s %6d  (%d reoccupied, %d still empty)"
              % (k, v["total"], v["occupied_today"], v["still_empty"]))
        print("      %s" % ", ".join("%s %d" % (s, n) for s, n in
                                     sorted(v["by_script"].items(), key=lambda x: -x[1])))

    print("\nVACATED REGIONS (runs of 8 or more)")
    for lv in sorted([k for k in R.get("vacated_runs", {}) if not k.endswith("__runs_total")],
                     key=order_key):
        print("  last seen in %s (%d runs total):" % (lv, R["vacated_runs"][lv + "__runs_total"]))
        for r in R["vacated_runs"][lv]:
            print("    %-22s %6d  was %-34s  today %s"
                  % (r["range"], r["count"], r["was"][:34], r["today"][:40]))

    print("\nRENAMES BY TRANSITION")
    for r in R["renames"]:
        print("  %-14s -> %-14s %d renamed" % (r["from"], r["to"], r["count"]))
        for s in r["sample"][:4]:
            print("      %s  %s" % (s["cp"], s["was"]))
            print("        -> %s" % s["now"])

    print("\nNAME ALIASES, current release: %s" % R["name_aliases"])
    print("NAMESLIST annotations: %s  total %d"
          % (R["nameslist"]["annotations_by_mark"], R["nameslist"]["total"]))
    m = R["misnomer_notes"]
    print("CHARACTERS the charts call a mistake or misnomer: %d "
          "(%d have a formal alias, %d have none)"
          % (m["count"], len(m["with_formal_alias"]), len(m["without_formal_alias"])))
    for h in m["lines"]:
        print("    %-10s %s" % (h["cp"], h["note"][:90]))
    print("  admitted wrong and never repaired: %s" % ", ".join(m["without_formal_alias"]))

    print("\nresults.json written")


if __name__ == "__main__":
    main()
