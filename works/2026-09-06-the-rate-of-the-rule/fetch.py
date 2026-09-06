#!/usr/bin/env python3
"""Acquisition only.  Fetches the population and writes sources/MANIFEST.json.

This file deliberately measures NOTHING.  It reports, per source, only what a courier
reports: the URL, the HTTP status, the byte count and the SHA-256.  It does not count
recitals, articles, words, `shall`s or anything else, because it ran before
PREDICTIONS.md was closed and the predictions must not be informed by the answer.
measure.py, written after the predictions were committed, does all the counting.

Two strata, both fixed here before any measurement:

  STRATUM B -- the named comparators.  Acts of the European Parliament and of the
  Council (regulations and directives) that EUR-Lex serves with ELI subdivision
  anchors, chosen by three stated criteria: at least 40 recitals, adoption years
  spread across the whole anchored window, and distinct policy domains, so that the
  GDPR is not compared only with its own family.  This is a purposive sample and is
  named as one; it cannot support a claim about EU law as a whole.

  STRATUM A -- the mechanical sweep.  For each year 2011..2024, the CELEX numbers
  3<YEAR>R0100, R0500, R0900, R1300, R1700.  Seventy probes on an arithmetic rule
  fixed in advance; every one that returns HTTP 200 with at least one rct_ anchor
  enters the population, whatever it turns out to be.  Nobody chose these acts.
  Most will be Commission implementing or delegated regulations with small preambles.
  Stratum A exists to check Stratum B against the accusation that the comparators
  were picked, and its heterogeneity is reported rather than smoothed.

The bytes are NOT committed.  EUR-Lex's reuse policy would permit it (Commission
Decision 2011/833/EU), and the licence rule of 2026-08-18 in PROTOCOL.md turns on
permission -- but the raw HTML of this population is ~25 MB, and a manifest carrying
URL, status, byte count and SHA-256 is the better warrant at that size: a stranger
re-fetches and compares the hash.  What IS committed is corpus.json -- the extracted
recital and article text of every act in the population -- and every matched sentence,
so that each number in the work can be checked against the text it came from without
a network.  The one act whose raw bytes are already in this repository is the
reference act, the GDPR, committed by works/2026-09-05-the-fourth-safeguard/.

Writes: sources/MANIFEST.json, sources/raw/<celex>.html (gitignored, not committed).
"""

import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "sources" / "raw"
MANIFEST = HERE / "sources" / "MANIFEST.json"

URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%%3A%s"

# --------------------------------------------------------------------------- stratum B
# celex, adoption year, the domain label used in the figure.  The label is mine and is
# a convenience for reading the figure, not a classification anyone else recognises.
STRATUM_B = [
    ("32009R1223", 2009, "cosmetic products"),
    ("32010L0075", 2010, "industrial emissions"),
    ("32011L0083", 2011, "consumer rights"),
    ("32012R0648", 2012, "OTC derivatives"),
    ("32012L0027", 2012, "energy efficiency"),
    ("32013R0575", 2013, "bank capital"),
    ("32013R1308", 2013, "agricultural markets"),
    ("32014R0596", 2014, "market abuse"),
    ("32014L0024", 2014, "public procurement"),
    ("32015L2366", 2015, "payment services"),
    ("32016R0679", 2016, "data protection"),
    ("32016L0680", 2016, "data protection (police)"),
    ("32017R0745", 2017, "medical devices"),
    ("32017R0625", 2017, "official food controls"),
    ("32018R1725", 2018, "data protection (EU bodies)"),
    ("32018R1139", 2018, "aviation safety"),
    ("32019R0881", 2019, "cybersecurity"),
    ("32019R0631", 2019, "CO2 from vehicles"),
    ("32020R0852", 2020, "sustainable finance"),
    ("32021R0241", 2021, "recovery facility"),
    ("32021R1119", 2021, "climate"),
    ("32021R2115", 2021, "agricultural policy"),
    ("32022R2065", 2022, "digital services"),
    ("32022R1925", 2022, "digital markets"),
    ("32022R0868", 2022, "data governance"),
    ("32023R2854", 2023, "data"),
    ("32023R1115", 2023, "deforestation"),
    ("32024R1689", 2024, "artificial intelligence"),
]

# --------------------------------------------------------------------------- stratum A
SWEEP_YEARS = range(2011, 2025)
SWEEP_NUMBERS = (100, 500, 900, 1300, 1700)


def sweep_celex():
    for year in SWEEP_YEARS:
        for number in SWEEP_NUMBERS:
            yield "3%dR%04d" % (year, number)


def fetch(celex):
    """One fetch.  Returns the manifest record; the bytes go to sources/raw/."""
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / ("%s.html" % celex)
    proc = subprocess.run(
        ["curl", "-sS", "-o", str(path), "-w", "%{http_code}", URL % celex],
        capture_output=True, text=True, timeout=180,
    )
    status = int(proc.stdout.strip() or 0)
    raw = path.read_bytes() if path.exists() else b""
    record = {
        "celex": celex,
        "url": URL % celex,
        "http_status": status,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
    # The one structural fact acquisition is allowed to record, because it decides
    # whether the document is in the population at all: does EUR-Lex serve it with the
    # ELI subdivision anchors this instrument cuts on?  A count of anchors is a count
    # of divisions, not a measurement of anything the predictions speak about.
    text = raw.decode("utf-8", "replace")
    record["has_eli_anchors"] = bool(re.search(r'id="rct_1"', text))
    record["title"] = extract_title(text)
    return record


def extract_title(text):
    """The document title EUR-Lex puts in <title>, trimmed of its own boilerplate."""
    match = re.search(r"(?s)<title>(.*?)</title>", text)
    if not match:
        return None
    title = re.sub(r"\s+", " ", match.group(1)).strip()
    return re.sub(r"\s*-\s*EN\s*$", "", title)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    sources = []

    if only in (None, "b"):
        for celex, year, domain in STRATUM_B:
            record = fetch(celex)
            record.update(stratum="B", adoption_year=year, domain=domain)
            sources.append(record)
            print("B %s %s %d bytes anchors=%s"
                  % (celex, record["http_status"], record["bytes"], record["has_eli_anchors"]))
            time.sleep(0.4)

    if only in (None, "a"):
        for celex in sweep_celex():
            record = fetch(celex)
            record.update(stratum="A", adoption_year=int(celex[1:5]), domain=None)
            sources.append(record)
            print("A %s %s %d bytes anchors=%s"
                  % (celex, record["http_status"], record["bytes"], record["has_eli_anchors"]))
            time.sleep(0.4)

    existing = {}
    if MANIFEST.exists():
        existing = {s["celex"]: s for s in json.loads(MANIFEST.read_text())["sources"]}
    for record in sources:
        existing[record["celex"]] = record

    MANIFEST.write_text(json.dumps({
        "note": (
            "Acquisition record for the population of 'The Rate of the Rule'.  The bytes are not "
            "committed: EUR-Lex's reuse policy (Commission Decision 2011/833/EU) would permit it, "
            "but the population is ~25 MB of HTML and a hash manifest is the better warrant at that "
            "size -- re-fetch and compare.  corpus.json, which IS committed, carries the extracted "
            "text every number in this work is derived from.  Fetched by fetch.py, which measures "
            "nothing: it ran before PREDICTIONS.md was closed."
        ),
        "fetched": "2026-09-06",
        "licence": (
            "EUR-Lex legal notice, reuse policy based on Commission Decision 2011/833/EU: 'Unless "
            "otherwise specified, you can re-use the legal documents published in EUR-Lex for "
            "commercial or non-commercial purposes.' "
            "(https://eur-lex.europa.eu/content/legal-notice/legal-notice.html)"
        ),
        "strata": {
            "B": "named comparators -- purposive sample, criteria in fetch.py's docstring",
            "A": "mechanical sweep -- 3<YEAR>R0100/0500/0900/1300/1700 for 2011..2024, no choice exercised",
        },
        "sources": sorted(existing.values(), key=lambda s: (s["stratum"], s["celex"])),
    }, indent=1) + "\n")
    print("\nmanifest: %d sources" % len(existing))


if __name__ == "__main__":
    main()
