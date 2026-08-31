#!/usr/bin/env python3
"""The published vocabulary against the vocabulary that runs.

Not predicted. Found while looking up the wording of two flags, and kept because it is the
second half of the same question: if the box selects which norms can reach a record, it is
worth knowing which norms the institution has *described*.

Two lists:

  * what the API will accept and apply — `/v1/enumeration/basic/OccurrenceIssue`, 105 values,
    every one of them a legal value of the `issue` search parameter;
  * what the institution's own flag reference describes — the page *Occurrence issues and
    flags* in GBIF's technical documentation.

Two independent rules are applied and both are reported, because the first version of this file
ran a third rule that was simply broken.

  * **by text** — a flag counts as described if its enum name, or its name spelled out in words,
    occurs anywhere in the page's text;
  * **by example link** — a flag counts as described if the page links a search for it, in the
    form `?issue=NAME`.

They agree exactly: 80 described, 25 not. The broken third rule was the example-link rule written
with the character class `[A-Z_]+`, which cannot match a flag name containing a digit and so
silently truncated `GEODETIC_DATUM_ASSUMED_WGS84` — a flag this same night measures on 5,428,125
records — to `GEODETIC_DATUM_ASSUMED_WGS`, reporting it as absent from a page that carries its
row, its description and its example link. That is F-093, and the two surviving rules are kept
side by side because one rule agreeing with itself is not a check.

Writes `documentation.json` and appends to `sources/MANIFEST-docs.json`.
"""
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = "https://techdocs.gbif.org/en/data-use/occurrence-issues-and-flags"
UA = "error-as-method nightly research line (+https://frankbueltge.de/error-as-method)"


def main():
    req = urllib.request.Request(PAGE, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        status, raw = r.status, r.read()
    page = raw.decode("utf-8", "replace")
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", page)))

    with open(os.path.join(HERE, "harvest.json"), encoding="utf-8") as fh:
        h = json.load(fh)
    enum = h["issue_enum"]
    inc = h["flag_incidence"]

    fires = {i: sum(inc[b].get(i, 0) for b in inc) for i in enum}
    described = {}
    for i in enum:
        spelled = i.replace("_", " ")
        described[i] = bool(i in text or re.search(re.escape(spelled), text, re.I))

    # the stricter rule, kept so the correction above can be checked
    linked = set(re.findall(r"issue=([A-Z0-9_]+)", page))

    quad = {
        "described_and_fires": [i for i in enum if described[i] and fires[i]],
        "described_never_fires": [i for i in enum if described[i] and not fires[i]],
        "undescribed_and_fires": [i for i in enum if not described[i] and fires[i]],
        "undescribed_never_fires": [i for i in enum if not described[i] and not fires[i]],
    }
    out = {
        "page": PAGE, "http_status": status, "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "enum_size": len(enum),
        "described_count": sum(described.values()),
        "undescribed_count": len(enum) - sum(described.values()),
        "second_rule_example_links": len(linked),
        "second_rule_undescribed": [i for i in enum if i not in linked],
        "the_two_rules_agree": sorted(i for i in enum if described[i]) == sorted(i for i in enum if i in linked),
        "broken_first_rule_pattern": "issue=([A-Z_]+) — cannot match a name containing a digit; see F-093",
        "quadrants": quad,
        "quadrant_sizes": {k: len(v) for k, v in quad.items()},
        "window_flag_totals": fires,
        "note": (
            "'fires' counts a flag as firing if any branch of the window carries at least one "
            "record with it. Records may carry several flags, so these totals do not sum to the "
            "number of flagged records and are not used as if they did."
        ),
    }
    with open(os.path.join(HERE, "documentation.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(json.dumps({k: out[k] for k in ("http_status", "bytes", "described_count",
                                          "undescribed_count", "quadrant_sizes")}, indent=1))
    for k, v in quad.items():
        if k != "described_and_fires":
            print(f"\n{k} ({len(v)}):\n  " + "\n  ".join(v))


if __name__ == "__main__":
    main()
