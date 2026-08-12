#!/usr/bin/env python3
"""
The Permanent Correction -- measuring an incorrigible norm.

Object: the Unicode Name property, and the channel the standard opened beside it
when it discovered it could not repair one.

Two published guarantees make the object:

  Name Stability, Unicode 2.0+ :
      "The Unicode Name property value for any non-reserved code point will not be
       changed. In particular, once a character is encoded, its name will not be
       changed."
      ... "In cases of outright errors in character names such as misspellings, a
       character may be given a formal name alias."

  Formal Name Alias Stability, Unicode 5.0+ :
      "Formal aliases, once assigned to a character, will not be changed or removed."

  -- https://www.unicode.org/policies/stability_policy.html (retrieved 2026-08-12)

So the wrong name is permanent and its correction is permanent. This script
measures the pair: when each error was instituted, when its correction was filed
beside it, how long the gap was, what kind of error it was, and whether the two
channels are allowed to collide.

Everything is computed from the files in data/ (see data/MANIFEST.txt for URLs and
SHA-256). No network at run time. Stdlib only. No randomness, so no seed.

Eleven predictions are written into PREDICTIONS below and were fixed BEFORE the
first execution of this script. One further quantity (P7) was observed during the
harvest, before any prediction was written, and is marked as an observation, not a
test -- see the note on P7.
"""

import hashlib
import json
import os
import re
import unicodedata  # only for its version string, printed for the record

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# --------------------------------------------------------------------------
# The ledger. Fixed before the first run; verdicts appended by the run itself.
# --------------------------------------------------------------------------

PREDICTIONS = [
    ("P1", "No code point that has ever carried a correction alias is missing from a "
           "later version's correction set (Formal Name Alias Stability, tested rather "
           "than trusted)."),
    ("P2", "For at least two thirds of the corrections, the correction was filed in a "
           "LATER Unicode version than the one that first encoded the character."),
    ("P3", "At least one correction entered in the same version that encoded the "
           "character -- the name was known to be wrong at birth."),
    ("P4", "The longest interval between a character being encoded and its correction "
           "being filed exceeds 15 years."),
    ("P5", "Misspellings are the policy's stated example but not its main business: at "
           "most 10 of the corrections are single-token misspellings by the "
           "classification rule below; the majority replace a name component outright."),
    ("P6", "The live namespace -- character names, all formal aliases, named character "
           "sequences -- has zero collisions under loose matching rule UAX44-LM2."),
    ("P7", "NOT A PREDICTION. Observed during the harvest, before the ledger existed: "
           "the ISO_Comment field of UnicodeData.txt is empty on every line. The run "
           "recomputes it for the record; it is not scored."),
    ("P8", "The retired channel is allowed to collide with the live one: at least one "
           "Unicode_1_Name matches, under UAX44-LM2, the current Name of a DIFFERENT "
           "character -- and there are at most 20 such cases."),
    ("P9", "Characters first encoded in Unicode 10.0 or later carry fewer corrections "
           "per thousand encoded characters than those first encoded in 5.0-9.0. "
           "(Right-censored: recent cohorts have had less time to be caught. Stated "
           "before the run, and the censoring is not a defence of the prediction.)"),
    ("P10", "No character carries more than one correction alias."),
    ("P11", "At least one corrected character was first encoded in Unicode 1.1 or earlier."),
]

VERDICTS = {}


def verdict(key, ok, detail):
    VERDICTS[key] = {"result": "CONFIRMED" if ok else "REFUTED", "detail": detail}
    return ok


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def load_versions():
    """{version_string: year_of_record}, plus major.minor keys for DerivedAge.

    DerivedAge.txt writes ages as major.minor ("1.1", "3.0"), while the version list
    has update releases under the same major.minor ("1.1.0" 1993, "1.1.5" 1995). An
    age of 1.1 means the character was there in Unicode 1.1, so the short key takes
    the EARLIEST year among its update releases.

    (Written after the first run of this script, which used setdefault over the table
    in its published order and so resolved 1.1 to 1995 — the year of Unicode 1.1.5 —
    making every gap for a 1993 character two years too short. The first run reported
    a longest gap of 22 years; it is 24. Recorded here rather than quietly fixed.)
    """
    years = {}
    with open(os.path.join(DATA, "versions.tsv"), encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or line.startswith("version"):
                continue
            v, y = line.strip().split("\t")
            years[v] = int(y)
    for v in list(years):
        short = ".".join(v.split(".")[:2])              # 5.0.0 -> 5.0
        if short not in years or years[v] < years[short]:
            years[short] = years[v]
    return years


HARVESTED_VERSIONS = ["5.0.0", "5.1.0", "5.2.0", "6.0.0", "6.1.0", "6.2.0", "6.3.0",
                      "7.0.0", "8.0.0", "9.0.0", "10.0.0", "11.0.0", "12.0.0", "12.1.0",
                      "13.0.0", "14.0.0", "15.0.0", "15.1.0", "16.0.0", "17.0.0"]


def load_aliases(version):
    """Return {code: [(alias, type)]} for one harvested NameAliases file.

    Versions 5.0.0-6.0.0 have two fields and no type column. In those versions the
    file contained nothing but the corrections -- the type labels were introduced in
    6.1.0, when the control/abbreviation/figment/alternate material was added. Those
    early two-field entries are therefore read as type 'correction'; the run checks
    that reading by verifying every one of them still carries type 'correction' in
    17.0.0 (the early_mistyped check at the top of main, which must come out empty).
    """
    out = {}
    path = os.path.join(DATA, "NameAliases-%s.txt" % version)
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.split("#")[0].strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(";")]
            if len(parts) == 2:
                code, alias, typ = parts[0], parts[1], "correction"
            else:
                code, alias, typ = parts[0], parts[1], parts[2].lower()
            out.setdefault(code.upper(), []).append((alias, typ))
    return out


def load_age():
    """DerivedAge.txt -> {code_int: version_string}."""
    age = {}
    path = os.path.join(DATA, "DerivedAge.txt")
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.split("#")[0].strip()
            if not line:
                continue
            rng, ver = [p.strip() for p in line.split(";")]
            if ".." in rng:
                a, b = rng.split("..")
                a, b = int(a, 16), int(b, 16)
            else:
                a = b = int(rng, 16)
            for cp in range(a, b + 1):
                age[cp] = ver
    return age


def load_unicodedata_slim():
    """data/UnicodeData-slim.txt: code;Name;Unicode_1_Name;ISO_Comment.

    Fields 0, 1, 10 and 11 of UnicodeData.txt, extracted verbatim, one line per
    original line. Range rows keep their <First>/<Last> markers.
    """
    rows = []
    with open(os.path.join(DATA, "UnicodeData-slim.txt"), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            code, name, u1, iso = line.split(";")
            rows.append({"code": code.upper(), "cp": int(code, 16), "name": name,
                         "u1name": u1, "iso": iso})
    return rows


def load_named_sequences():
    seqs = []
    with open(os.path.join(DATA, "NamedSequences.txt"), encoding="utf-8") as f:
        for line in f:
            line = line.split("#")[0].strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(";")]
            if len(parts) >= 2:
                seqs.append((parts[0], parts[1]))
    return seqs


# --------------------------------------------------------------------------
# UAX44-LM2, implemented from the rule text
# --------------------------------------------------------------------------
# "Ignore case, whitespace, underscore ('_'), and all medial hyphens except the
#  hyphen in U+1180 HANGUL JUNGSEONG O-E."
# "In this rule 'medial hyphen' is to be construed as a hyphen occurring immediately
#  between two alphanumeric characters [A..Z, 0..9] in the normative Unicode
#  character name" -- https://www.unicode.org/reports/tr44/ (retrieved 2026-08-12)

ALNUM = re.compile(r"[A-Za-z0-9]")


def lm2(name, is_u1180=False):
    if is_u1180:
        kept = name
    else:
        chars = list(name)
        out = []
        for i, ch in enumerate(chars):
            if ch == "-" and i > 0 and i + 1 < len(chars) \
                    and ALNUM.match(chars[i - 1]) and ALNUM.match(chars[i + 1]):
                continue                        # medial hyphen: drop
            out.append(ch)
        kept = "".join(out)
    kept = kept.replace(" ", "").replace("\t", "").replace("_", "")
    return kept.lower()


# --------------------------------------------------------------------------
# Edit distance and the classification rule for P5
# --------------------------------------------------------------------------

def levenshtein(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def classify(name, correction):
    """Auditable, stated rule -- raw numbers are reported so a reader can re-derive
    with a different threshold.

    'misspelling' iff exactly one whitespace-delimited token differs between the two
    names, the token counts are equal, and the differing pair is either an anagram of
    each other (a transposition, e.g. BRAKCET/BRACKET) or within Levenshtein
    distance 2.  Everything else is 'replacement': the name says a different thing.
    """
    ta, tb = name.split(), correction.split()
    dist = levenshtein(name, correction)
    if len(ta) != len(tb):
        return "replacement", dist, None
    diff = [(x, y) for x, y in zip(ta, tb) if x != y]
    if len(diff) != 1:
        return "replacement", dist, len(diff)
    x, y = diff[0]
    td = levenshtein(x, y)
    if sorted(x) == sorted(y) or td <= 2:
        return "misspelling", dist, 1
    return "replacement", dist, 1


# --------------------------------------------------------------------------
# Run
# --------------------------------------------------------------------------

def excluded_intervals(rows):
    """Private Use and Surrogate ranges, paired off the <..., First>/<..., Last> rows.

    They have an Age and would otherwise dominate the cohort denominators in P9 --
    137,468 code points nobody ever named. Reported separately, not silently dropped.
    """
    out = []
    open_start = None
    for r in rows:
        n = r["name"]
        if n.endswith(", First>") and ("Private Use" in n or "Surrogate" in n):
            open_start = r["cp"]
        elif n.endswith(", Last>") and open_start is not None:
            out.append((open_start, r["cp"]))
            open_start = None
    return out


def main():
    years = load_versions()
    age = load_age()
    rows = load_unicodedata_slim()
    seqs = load_named_sequences()

    by_code = {}
    for r in rows:
        if not r["name"].startswith("<"):
            by_code[r["code"]] = r

    # Validity check on reading the untyped 5.0.0-6.0.0 entries as corrections:
    # every code point in those files must still carry type 'correction' in 17.0.0.
    early = set()
    for v in ("5.0.0", "5.1.0", "5.2.0", "6.0.0"):
        early |= set(load_aliases(v))
    latest_types = {}
    for code, lst in load_aliases("17.0.0").items():
        latest_types[code] = set(t for _, t in lst)
    early_mistyped = sorted(c for c in early if "correction" not in latest_types.get(c, set()))

    # --- the correction series, version by version -------------------------
    series = []
    first_seen = {}
    ever = set()
    removals = []
    for v in HARVESTED_VERSIONS:
        al = load_aliases(v)
        corr = {c: [a for a, t in lst if t == "correction"]
                for c, lst in al.items()}
        corr = {c: a for c, a in corr.items() if a}
        present = set(corr)
        gone = sorted(ever - present)
        if gone:
            removals.append({"version": v, "missing": gone})
        ever |= present
        for c in sorted(present):
            first_seen.setdefault(c, v)
        series.append({"version": v, "year": years[v], "corrections": len(present),
                       "aliases_total": sum(len(l) for l in al.values()),
                       "new_this_version": sorted(c for c in present
                                                  if first_seen[c] == v)})

    latest = load_aliases("17.0.0")
    corrections = []
    for code, lst in latest.items():
        for alias, typ in lst:
            if typ == "correction":
                corrections.append((code, alias))
    corrections.sort(key=lambda t: int(t[0], 16))

    # P1 -- stability of the alias channel
    verdict("P1", not removals,
            "no correction ever absent from a later version" if not removals
            else "removals: %r" % removals)

    # P10 -- one correction per character?
    multi = {}
    for code, alias in corrections:
        multi.setdefault(code, []).append(alias)
    multi = {c: a for c, a in multi.items() if len(a) > 1}
    verdict("P10", not multi, "characters with >1 correction: %r" % multi)

    # --- per-correction table ---------------------------------------------
    table = []
    for code, alias in corrections:
        cp = int(code, 16)
        row = by_code.get(code)
        name = row["name"] if row else None
        enc_v = age.get(cp)
        fil_v = first_seen.get(code)
        enc_y = years.get(enc_v)
        fil_y = years.get(fil_v)
        kind, dist, ntok = classify(name, alias) if name else ("unknown", None, None)
        table.append({
            "code": code, "name": name, "correction": alias,
            "encoded_version": enc_v, "encoded_year": enc_y,
            "filed_version": fil_v, "filed_year": fil_y,
            "unmarked_years": None if (enc_y is None or fil_y is None) else fil_y - enc_y,
            "years_since_filed": None if fil_y is None else 2025 - fil_y,
            "kind": kind, "edit_distance": dist, "tokens_differing": ntok,
        })

    later = [t for t in table if t["unmarked_years"] is not None and t["unmarked_years"] > 0]
    same = [t for t in table if t["unmarked_years"] == 0]
    verdict("P2", len(later) >= (2 * len(table)) / 3,
            "%d of %d filed later than encoded (%.1f%%)"
            % (len(later), len(table), 100.0 * len(later) / len(table)))
    verdict("P3", len(same) >= 1,
            "%d filed in the encoding version: %s"
            % (len(same), ", ".join("U+" + t["code"] for t in same)))
    mx = max(table, key=lambda t: (t["unmarked_years"] or -1))
    verdict("P4", (mx["unmarked_years"] or 0) > 15,
            "longest gap %s years: U+%s %s -> %s (encoded %s, filed %s)"
            % (mx["unmarked_years"], mx["code"], mx["name"], mx["correction"],
               mx["encoded_version"], mx["filed_version"]))

    misspellings = [t for t in table if t["kind"] == "misspelling"]
    verdict("P5", len(misspellings) <= 10,
            "%d misspellings, %d replacements: %s"
            % (len(misspellings), len(table) - len(misspellings),
               ", ".join("U+" + t["code"] for t in misspellings)))

    oldest = min(table, key=lambda t: (t["encoded_year"] or 9999))
    verdict("P11", oldest["encoded_version"] in ("1.0.0", "1.0.1", "1.1", "1.1.0", "1.1.5"),
            "oldest corrected character: U+%s, encoded %s (%s)"
            % (oldest["code"], oldest["encoded_version"], oldest["encoded_year"]))

    # --- P6: the live namespace under LM2 ---------------------------------
    ns = {}
    collisions = []

    def put(key, kind, ident, raw):
        k = lm2(raw, is_u1180=(ident == "U+1180"))
        if k in ns and ns[k]["ident"] != ident:
            collisions.append({"key": k, "a": ns[k], "b": {"kind": kind,
                                                           "ident": ident, "raw": raw}})
        else:
            ns[k] = {"kind": kind, "ident": ident, "raw": raw}

    named_rows = 0
    for r in rows:
        if r["name"].startswith("<"):
            continue                      # range markers and code point labels
        named_rows += 1
        put(r["name"], "name", "U+" + r["code"], r["name"])
    n_alias = 0
    for code, lst in latest.items():
        for alias, typ in lst:
            n_alias += 1
            put(alias, "alias:" + typ, "U+" + code.upper(), alias)
    for name, seq in seqs:
        put(name, "named_sequence", "seq:" + seq, name)

    verdict("P6", not collisions,
            "namespace of %d character names + %d formal aliases + %d named sequences: "
            "%d collisions" % (named_rows, n_alias, len(seqs), len(collisions)))

    # --- P7 (observation, not scored): ISO_Comment ------------------------
    iso_nonempty = [r["code"] for r in rows if r["iso"].strip()]
    VERDICTS["P7"] = {"result": "OBSERVED (not a prediction)",
                      "detail": "ISO_Comment non-empty on %d of %d lines of "
                                "UnicodeData.txt" % (len(iso_nonempty), len(rows))}

    # --- P8: the retired channel -----------------------------------------
    u1 = [r for r in rows if r["u1name"].strip()]
    live = {}
    for r in rows:
        if not r["name"].startswith("<"):
            live[lm2(r["name"], is_u1180=(r["code"] == "1180"))] = r["code"]
    retired_collisions = []
    for r in u1:
        k = lm2(r["u1name"])
        if k in live and live[k] != r["code"]:
            retired_collisions.append({"code": r["code"], "current_name": r["name"],
                                       "unicode_1_name": r["u1name"],
                                       "now_the_name_of": live[k],
                                       "that_characters_name":
                                           by_code[live[k]]["name"]})
    # Descriptive breakdown of the P8 set. Grouping chosen AFTER seeing the result --
    # it is a description of the refutation, not a test.
    u1_by_code = {r["code"]: r["u1name"] for r in rows if r["u1name"].strip()}
    for r in retired_collisions:
        holder = r["now_the_name_of"]
        r["exact_string_equal"] = (r["unicode_1_name"] == r["that_characters_name"])
        r["holder_age"] = age.get(int(holder, 16))
        r["holder_also_renamed"] = u1_by_code.get(holder)
        r["group"] = r["that_characters_name"].split()[0]
    verdict("P8", 1 <= len(retired_collisions) <= 20,
            "%d Unicode_1_Name values now name a different character (of %d "
            "non-empty Unicode_1_Name fields)" % (len(retired_collisions), len(u1)))

    # --- P9: cohort correction rate --------------------------------------
    excl = excluded_intervals(rows)

    def is_excluded(cp):
        return any(a <= cp <= b for a, b in excl)

    cohort_size = {}
    cohort_size_raw = {}
    n_excluded = 0
    for cp, v in age.items():
        cohort_size_raw[v] = cohort_size_raw.get(v, 0) + 1
        if is_excluded(cp):
            n_excluded += 1
            continue
        cohort_size[v] = cohort_size.get(v, 0) + 1
    cohort_err = {}
    for t in table:
        cohort_err[t["encoded_version"]] = cohort_err.get(t["encoded_version"], 0) + 1

    def rate(vers):
        n = sum(cohort_size.get(v, 0) for v in vers)
        e = sum(cohort_err.get(v, 0) for v in vers)
        return e, n, (1000.0 * e / n if n else 0.0)

    def vers_between(lo, hi):
        out = []
        for v in cohort_size:
            try:
                maj, mnr = (int(x) for x in v.split(".")[:2])
            except ValueError:
                continue
            key = maj + mnr / 10.0
            if lo <= key <= hi:
                out.append(v)
        return out

    r_early = rate(vers_between(5.0, 9.9))
    late = rate(vers_between(10.0, 99.0))
    pre5 = rate(vers_between(0.0, 4.9))
    verdict("P9", late[2] < r_early[2],
            "cohort 5.0-9.x: %d/%d = %.4f per 1000; cohort 10.0+: %d/%d = %.4f per "
            "1000; cohort <=4.1: %d/%d = %.4f per 1000"
            % (r_early[0], r_early[1], r_early[2], late[0], late[1], late[2],
               pre5[0], pre5[1], pre5[2]))

    # --- reconciliation: a second apparatus on the same quantity -----------
    # Published counts for Unicode 17.0.0, transcribed from
    # https://www.unicode.org/versions/stats/charcountv17_0.html (retrieved 2026-08-12):
    #   graphic 159,629 + format 172 = graphic+format 159,801; controls 65;
    #   private use 137,468; total assigned 297,334.
    # Surrogates (2,048) and noncharacters (66) are not in that total but do carry an
    # Age. The identity below is not an arithmetic identity: it fails if my parse of
    # DerivedAge.txt, or my pairing of the private-use and surrogate ranges, is wrong.
    PUB = {"graphic": 159629, "format": 172, "controls": 65, "private_use": 137468,
           "total_assigned": 297334, "surrogates": 2048, "noncharacters": 66}
    kept = len(age) - n_excluded
    recon = {
        "published": PUB,
        "code_points_with_an_age": len(age),
        "expected_from_published": PUB["total_assigned"] + PUB["surrogates"] + PUB["noncharacters"],
        "excluded_by_me_private_use_and_surrogate": n_excluded,
        "expected_excluded": PUB["private_use"] + PUB["surrogates"],
        "kept_denominator": kept,
        "expected_kept": PUB["graphic"] + PUB["format"] + PUB["controls"] + PUB["noncharacters"],
    }
    recon["agrees"] = (
        recon["code_points_with_an_age"] == recon["expected_from_published"]
        and recon["excluded_by_me_private_use_and_surrogate"] == recon["expected_excluded"]
        and recon["kept_denominator"] == recon["expected_kept"])

    # --- aggregates -------------------------------------------------------
    unmarked_total = sum(t["unmarked_years"] or 0 for t in table)
    coexist_total = sum(t["years_since_filed"] or 0 for t in table)

    result = {
        "object": "the Unicode Name property and its correction channel",
        "unicode_version_measured": "17.0.0",
        "runtime_unicodedata_version_for_the_record": unicodedata.unidata_version,
        "corrections_now": len(corrections),
        "characters_corrected": len(set(c for c, _ in corrections)),
        "series": series,
        "table": table,
        "aggregate": {
            "character_years_unmarked": unmarked_total,
            "character_years_of_coexistence_to_2025": coexist_total,
            "mean_unmarked_years": round(unmarked_total / len(table), 2),
            "median_unmarked_years": sorted(t["unmarked_years"] for t in table)[len(table) // 2],
        },
        "namespace": {
            "character_names": named_rows,
            "formal_aliases": n_alias,
            "named_sequences": len(seqs),
            "collisions_lm2": collisions,
        },
        "iso_comment_nonempty": len(iso_nonempty),
        "unicode_1_name_nonempty": len(u1),
        "retired_channel_collisions": retired_collisions,
        "cohort_rates_per_1000": {"le_4.1": pre5, "5.0_to_9.x": r_early,
                                  "10.0_plus": late},
        "reconciliation_against_published_counts": recon,
        "cohort_denominators": {
            "code_points_with_an_age": len(age),
            "excluded_private_use_and_surrogate": n_excluded,
            "excluded_intervals": [["%04X" % a, "%04X" % b] for a, b in excl],
        },
        "early_untyped_entries_not_corrections_in_17.0.0": early_mistyped,
        "predictions": [{"id": k, "claim": c, **VERDICTS[k]} for k, c in PREDICTIONS],
    }

    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
        f.write("\n")

    # --- report -----------------------------------------------------------
    print("corrections in Unicode 17.0.0 : %d on %d characters"
          % (len(corrections), result["characters_corrected"]))
    print("untyped 5.0.0-6.0.0 entries not typed 'correction' in 17.0.0 : %s"
          % (", ".join("U+" + c for c in early_mistyped) or "none"))
    print("code points with an Age: %d, of which private-use/surrogate: %d"
          % (len(age), n_excluded))
    print("series (version, year, corrections, all aliases):")
    for s in series:
        print("   %-8s %s  %3d  %5d   new: %s"
              % (s["version"], s["year"], s["corrections"], s["aliases_total"],
                 " ".join("U+" + c for c in s["new_this_version"]) or "-"))
    print()
    print("%-8s %-6s %-6s %-5s %-12s %s" % ("code", "enc", "filed", "gap", "kind", "name -> correction"))
    for t in sorted(table, key=lambda t: (-(t["unmarked_years"] or 0), t["code"])):
        print("%-8s %-6s %-6s %-5s %-12s %s -> %s"
              % ("U+" + t["code"], t["encoded_version"], t["filed_version"],
                 t["unmarked_years"], t["kind"], t["name"], t["correction"]))
    print()
    for k, c in PREDICTIONS:
        print("%-4s %-9s %s" % (k, VERDICTS[k]["result"], VERDICTS[k]["detail"]))
    print()
    print("reconciliation against unicode.org's published counts for 17.0.0: %s"
          % ("AGREES to the unit" if recon["agrees"] else "DISAGREES"))
    for k in ("code_points_with_an_age", "expected_from_published",
              "excluded_by_me_private_use_and_surrogate", "expected_excluded",
              "kept_denominator", "expected_kept"):
        print("   %-42s %d" % (k, recon[k]))
    print()
    print("character-years the norm circulated with an unmarked error : %d" % unmarked_total)
    print("character-years the two names have coexisted (to 2025)     : %d" % coexist_total)
    if retired_collisions:
        print()
        print("retired names now naming someone else: %d" % len(retired_collisions))
        groups = {}
        for r in retired_collisions:
            groups[r["group"]] = groups.get(r["group"], 0) + 1
        print("   by first token of the new holder's name: %s"
              % ", ".join("%s %d" % (k, v) for k, v in
                          sorted(groups.items(), key=lambda kv: -kv[1])))
        loose_only = [r for r in retired_collisions if not r["exact_string_equal"]]
        print("   equal only under LM2, not as strings: %d %s"
              % (len(loose_only), ["U+" + r["code"] for r in loose_only]))
        swaps = [r for r in retired_collisions if r["holder_also_renamed"]]
        print("   where the new holder was itself renamed (a transfer, not a "
              "re-issue): %d" % len(swaps))
        for r in swaps:
            print("      U+%s %r -> now %r ; the name %r went to U+%s, whose own "
                  "1.0 name was %r"
                  % (r["code"], r["unicode_1_name"], r["current_name"],
                     r["that_characters_name"], r["now_the_name_of"],
                     r["holder_also_renamed"]))
        holder_ages = {}
        for r in retired_collisions:
            holder_ages[r["holder_age"]] = holder_ages.get(r["holder_age"], 0) + 1
        print("   version in which the new holder was encoded: %s"
              % ", ".join("%s: %d" % (k, v) for k, v in sorted(holder_ages.items())))
    print()
    print("results.json written; sha256 = %s"
          % hashlib.sha256(open(os.path.join(HERE, "results.json"), "rb").read()).hexdigest()[:16])


if __name__ == "__main__":
    main()
