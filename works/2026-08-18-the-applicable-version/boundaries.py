#!/usr/bin/env python3
"""Read three Unicode pages as three populations, and ask where the written rules are dated.

Populations fixed in PREDICTIONS.md before this file was written:

  P-A  every named clause on the Unicode stability policy page, with its Applicable Version
  P-B  every corrigendum on the Unicode corrigenda page, with the versions it says were
       defective and the version that fixed it
  P-C  every published version of the Unicode Standard, with its year — the denominator

The question is Session 60's falsifier 1: are an institution's *written* rules datably minted
at breakdowns, or in anticipation? A policy's Applicable Version is the first version from
which its guarantee holds — the page says so itself — so if a rule is a reaction to a
breakdown, its boundary should sit at the version where that breakdown stopped, and the
versions before it should be the ones the institution admits were broken.

The instrument counts. It does not adjudicate: which defect a clause answers is a reading,
and every reading is signed by hand in adjudication.json with the source that carries it.

    python3 boundaries.py            # writes results.json

Offline: reads only sources/, never the network. stdlib only.
"""
import html
import json
import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")


def text_of(fragment):
    """Strip tags from an HTML fragment and normalise whitespace."""
    out = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(out)).strip()


def read(name):
    with open(os.path.join(SRC, name), encoding="utf-8", errors="replace") as fh:
        return fh.read()


# ---------------------------------------------------------------- P-A: the clauses

def clauses():
    """Every named clause on the stability page, with the applicable versions under it.

    The page's own markup carries the structure: `clauseName` opens a clause, and every
    `clauseApplicability` until the next `clauseName` belongs to it. Normalization Stability
    has two (a strong form and a weaker earlier one) and Alias Stability has two; that is a
    property of the page, not of this parser, and both are kept rather than flattened.
    """
    page = read("stability_policy.html")
    marks = list(re.finditer(
        r"class=[\"']?(clauseName|clauseApplicability|clauseStatement)[\"']?[^>]*>(.*?)</",
        page, flags=re.S))
    found, current = [], None
    for kind, raw in ((m.group(1), text_of(m.group(2))) for m in marks):
        if kind == "clauseName":
            current = {"clause": raw, "applicable": [], "statement": None}
            found.append(current)
        elif current is None:
            continue
        elif kind == "clauseApplicability":
            for ver in re.findall(r"Unicode (\d+\.\d+)\+", raw):
                current["applicable"].append(ver)
        elif kind == "clauseStatement" and current["statement"] is None:
            current["statement"] = raw
    return found


# ---------------------------------------------------------------- P-B: the corrigenda

def corrigenda():
    """Every row of the Table of Corrigenda."""
    page = read("corrigenda.html")
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", page, flags=re.S | re.I):
        cells = [text_of(td) for td in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, flags=re.S | re.I)]
        if len(cells) < 5 or not cells[0].lower().startswith("corrigendum"):
            continue
        number = int(re.search(r"#(\d+)", cells[0]).group(1))
        # "3.0.0 and 3.0.1" / "3.0.0 to 4.0.1" / "5.0.0"
        broken = re.findall(r"\d+\.\d+\.\d+", cells[2])
        fixed = re.search(r"\d+\.\d+\.\d+", cells[3])
        rows.append({
            "corrigendum": number,
            "title": cells[0],
            "effective": cells[1],
            "versions_declared_defective": cells[2],
            "defective_endpoints": broken,
            "fixed_in": fixed.group(0) if fixed else None,
            "fixed_date": cells[3],
            "documented_in": cells[4] if len(cells) > 4 else None,
        })
    return sorted(rows, key=lambda r: r["corrigendum"])


# ---------------------------------------------------------------- P-C: the versions

def versions():
    """Every published version of the standard, with its year of record."""
    page = read("enumeratedversions.html")
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", page, flags=re.S | re.I):
        flat = text_of(tr)
        ver = re.match(r"Unicode (\d+\.\d+\.\d+)", flat)
        if not ver:
            continue
        year = re.search(r"\b(19|20)\d{2}\b", flat)
        out.append({"version": ver.group(1), "year": int(year.group(0)) if year else None})
    return out


def short(version):
    """2.0.0 -> 2.0 — the form the policy page uses for its boundaries."""
    return ".".join(version.split(".")[:2])


# ---------------------------------------------------------------- the aliases

def aliases():
    first = read("namealiases-5.0.0.txt").splitlines()
    now = read("namealiases.txt").splitlines()
    first_entries = [ln for ln in first if ln.strip() and not ln.startswith("#")]
    now_entries = [ln for ln in now if ln.strip() and not ln.startswith("#")]
    by_type = Counter(ln.rsplit(";", 1)[1].strip() for ln in now_entries if ln.count(";") >= 2)
    date = next((ln for ln in first if ln.startswith("# Date:")), "")

    # The encoded names of the characters the first alias file repairs, read from
    # UnicodeData.txt rather than typed from memory. The pairing is the finding: the name in
    # the standard is the wrong one, permanently, and the alias is the repair beside it.
    wanted = {ln.split(";")[0]: ln.split(";")[1] for ln in first_entries}
    encoded = {}
    with open(os.path.join(SRC, "unicodedata.txt"), encoding="utf-8") as fh:
        for line in fh:
            cp = line.split(";", 1)[0]
            if cp in wanted:
                encoded[cp] = line.split(";")[1]
    repairs = [{"code_point": cp, "name_in_the_standard": encoded.get(cp),
                "corrected_by_alias": alias} for cp, alias in sorted(wanted.items())]

    return {
        "first_file": "NameAliases-5.0.0.txt",
        "first_file_date": date.replace("# Date:", "").strip(),
        "first_file_entries": len(first_entries),
        "first_file_all_untyped_corrections": all(ln.count(";") == 1 for ln in first_entries),
        "first_file_code_points": [ln.split(";")[0] for ln in first_entries],
        "first_file_repairs": repairs,
        "current_file_entries": len(now_entries),
        "current_by_type": dict(sorted(by_type.items())),
    }


# ---------------------------------------------------------------- the measurement

def main():
    P_A, P_B, P_C = clauses(), corrigenda(), versions()

    boundaries = sorted({v for c in P_A for v in c["applicable"]},
                        key=lambda s: [int(x) for x in s.split(".")])
    fixed_versions = {short(c["fixed_in"]) for c in P_B if c["fixed_in"]}
    # Every version a corrigendum names as defective, expanded from its endpoints by position
    # in the published order rather than by arithmetic on version numbers.
    order = [v["version"] for v in P_C][::-1]
    defective = set()
    for c in P_B:
        pts = [p for p in c["defective_endpoints"] if p in order]
        if not pts:
            continue
        lo, hi = min(order.index(p) for p in pts), max(order.index(p) for p in pts)
        defective.update(short(v) for v in order[lo:hi + 1])

    hits = [b for b in boundaries if b in fixed_versions]
    base_rate = len({short(v["version"]) for v in P_C} & fixed_versions) / len(
        {short(v["version"]) for v in P_C})
    hit_rate = len(hits) / len(boundaries)

    results = {
        "night": "2026-08-18",
        "session": 61,
        "populations": {
            "P_A_clauses": len(P_A),
            "P_A_applicability_lines": sum(len(c["applicable"]) for c in P_A),
            "P_B_corrigenda": len(P_B),
            "P_C_versions": len(P_C),
        },
        "clauses": P_A,
        "corrigenda": P_B,
        "versions": P_C,
        "boundaries": {
            "distinct_boundary_versions": boundaries,
            "versions_that_fixed_a_corrigendum": sorted(fixed_versions),
            "versions_declared_defective": sorted(defective),
            "boundaries_on_a_fixing_version": hits,
            "hit_rate": round(hit_rate, 4),
            "base_rate_of_fixing_versions": round(base_rate, 4),
            "excess_over_base_rate_points": round((hit_rate - base_rate) * 100, 1),
            "boundaries_immediately_after_a_defective_version": sorted(
                b for b in boundaries if b in defective or any(
                    short(v) in defective for v in [b])),
        },
        "aliases": aliases(),
    }

    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"clauses {len(P_A)} · applicability lines {results['populations']['P_A_applicability_lines']}"
          f" · corrigenda {len(P_B)} · versions {len(P_C)}")
    print(f"distinct boundaries: {', '.join(boundaries)}")
    print(f"fixing versions   : {', '.join(sorted(fixed_versions))}")
    print(f"hit rate {hit_rate:.2%} vs base rate {base_rate:.2%} "
          f"({results['boundaries']['excess_over_base_rate_points']:+} points)")
    print(f"first alias file  : {results['aliases']['first_file_entries']} entries, "
          f"{results['aliases']['first_file_date']}")


if __name__ == "__main__":
    main()
