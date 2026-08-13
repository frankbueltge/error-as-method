#!/usr/bin/env python3
"""harvest.py — record what was fetched, from where, and with what SHA-256.

Run with --verify (the default) to hash what is in sources/ and rewrite
sources/MANIFEST.json. Run with --fetch to re-download the retrievable files first.

One of the sources has no version. `runways.csv` is rebuilt from a live community
database and its content changes without any identifier changing; the upstream file
carried `last-modified: Thu, 13 Aug 2026 01:54:04 GMT` when this night took it. The
hash below is therefore the only fixed identifier of what was actually measured, which
is the same predicament session 51 recorded for a Living Standard, and the same
predicament this night's subject is about: an address whose referent moves under it.

Two of the files are derived rather than fetched whole and say so:
  runways.csv.gz         gzip -9 of the fetched runways.csv, byte-identical inside
  airports-subset.csv.gz four columns of airports.csv (ident, type, scheduled_service,
                         iso_country); the whole file is 12.7 MB and only these are
                         used. The SHA-256 of the ORIGINAL airports.csv is recorded
                         alongside so the projection can be checked against it.
"""

import gzip
import hashlib
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")

SOURCES = [
    {"file": "runways.csv.gz",
     "url": "https://davidmegginson.github.io/ourairports-data/runways.csv",
     "what": "Every runway OurAirports holds: identifiers, threshold coordinates, "
             "length, surface, closed flag. Public domain (OurAirports).",
     "note": "stored gzipped; upstream last-modified 2026-08-13T01:54:04Z; the "
             "upstream file has no version identifier",
     "derived": "gzip -9"},
    {"file": "airports-subset.csv.gz",
     "url": "https://davidmegginson.github.io/ourairports-data/airports.csv",
     "what": "Airport ident, type, scheduled_service, iso_country. Public domain.",
     "derived": "four columns of the fetched airports.csv, gzipped",
     "sha256_of_original_airports_csv":
         "9e5055bd1a812a60a1ef60a2be99d849f43d0b81237275ae81b8a45e20d66b20",
     "original_bytes": 12698180},
    {"file": "igrf14coeffs.txt",
     "url": "https://www.ngdc.noaa.gov/IAGA/vmod/coeffs/igrf14coeffs.txt",
     "what": "IGRF-14 Schmidt semi-normalised spherical harmonic coefficients, "
             "1900.0-2025.0 plus the 2025-30 secular variation column. IAGA."},
    {"file": "WMM2025.COF",
     "url": "https://www.ncei.noaa.gov/sites/default/files/2024-12/WMM2025COF.zip",
     "what": "World Magnetic Model 2025 coefficients, from the NCEI zip.",
     "derived": "extracted from WMM2025COF.zip"},
    {"file": "WMM2025_TestValues.txt",
     "url": "https://www.ncei.noaa.gov/sites/default/files/2024-12/WMM2025COF.zip",
     "what": "The model authors' own published test values. This is the outside "
             "authority geomag.py is checked against.",
     "derived": "extracted from WMM2025COF.zip"},
    {"file": "README-WMM-COEFS.txt",
     "url": "https://www.ncei.noaa.gov/sites/default/files/2024-12/WMM2025COF.zip",
     "what": "The zip's own README, kept so the coefficient files are not orphaned.",
     "derived": "extracted from WMM2025COF.zip"},
]

# Documents read but not committed here: they are large PDFs, they are stable at their
# publishers, and this repository is not their archive. Their retrieval is dated in the
# work and the journal.
READ_NOT_COMMITTED = [
    {"url": "https://www.faa.gov/documentlibrary/media/advisory_circular/150_5340_1l.pdf",
     "what": "FAA AC 150/5340-1L, Standards for Airport Markings, 9/27/2013. "
             "Paragraph 2.3.e(3)-(4): the designator rule and its licensed deviation.",
     "retrieved": "2026-08-13"},
    {"url": "https://www.navcanada.ca/en/magnetic-north-vs-true-north.pdf",
     "what": "NAV CANADA, 'Magnetic to True North - Change by 2030', Anthony MacKay, "
             "Director Operational Safety, 28 February 2022. The world-wide runway "
             "impact counts and the cost figures.",
     "retrieved": "2026-08-13"},
    {"url": "https://www.navcanada.ca/en/005aic2026en.pdf",
     "what": "NAV CANADA Aeronautical Information Circular 005/2026, published "
             "2 April 2026: operations in Canadian Northern Domestic Airspace.",
     "retrieved": "2026-08-13"},
    {"url": "https://www.icao.int/sites/default/files/safety/CAPSCA/PublishingImages/"
            "Pages/ICAO-SARPs-(Annexes-and-PANS)/an15_1.pdf",
     "what": "ICAO Annex 15, Chapter 6: the AIRAC system, 28-day common effective "
             "dates, and 6.2.7(d) naming magnetic variation change by name.",
     "retrieved": "2026-08-13"},
    {"url": "https://corporate.berlin-airport.de/en/company-media/media-portal/"
            "pressemitteilungen/2024-10-01-slb-umbenennung.html",
     "what": "Berlin Brandenburg Airport press release, 1 October 2024: both runways "
             "renumbered on 3 October 2024.",
     "retrieved": "2026-08-13"},
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def inner_sha256_gz(path):
    h = hashlib.sha256()
    with gzip.open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if "--fetch" in sys.argv:
        for s in SOURCES:
            if s.get("derived"):
                print(f"skip (derived): {s['file']}")
                continue
            print(f"fetch {s['url']}")
            urllib.request.urlretrieve(s["url"], os.path.join(SRC, s["file"]))

    manifest = {
        "harvested": "2026-08-13",
        "by": "Ulysses (the nightly line), Session 52",
        "work": "works/2026-08-13-the-drifting-address/",
        "files": [],
        "read_not_committed": READ_NOT_COMMITTED,
    }
    for s in SOURCES:
        p = os.path.join(SRC, s["file"])
        rec = dict(s)
        rec["bytes"] = os.path.getsize(p)
        rec["sha256"] = sha256(p)
        if s["file"].endswith(".gz"):
            rec["sha256_uncompressed"] = inner_sha256_gz(p)
        manifest["files"].append(rec)
        print(f"{rec['sha256'][:16]}…  {rec['bytes']:>9,}  {s['file']}")

    with open(os.path.join(SRC, "MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    print(f"\nsources/MANIFEST.json written: {len(manifest['files'])} committed, "
          f"{len(READ_NOT_COMMITTED)} read and cited but not committed")


if __name__ == "__main__":
    main()
