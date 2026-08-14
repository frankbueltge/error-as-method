#!/usr/bin/env python3
"""harvest.py -- download and hash every source this night measures.

Session 56. The question is Session 55's second open thread, written down by that night
as the case that would kill its own finding:

    "Falsifier 1 for tonight's claim: a permanent registry founded by importing the dead
     as well as the living. If that founding pattern is common, 'the first act of a
     permanent record is a deletion' is a habit of one working group and not a property
     of permanence."

S55's claim, the thing this night is trying to break:

    "A permanence policy is not a promise about names; it is a promise about a period.
     The first act of a permanent record is a deletion that leaves no trace."

The object is ISO 3166's dead -- the country codes withdrawn from the standard since its
first edition in 1974 -- and the three registers that stand downstream of or beside it:
ISO 3166-3 (the authority's own register of formerly used names, first published 1999),
the IANA Language Subtag Registry (S55's object, measured here on its *other* upstream),
and the CLDR territory aliases.

What I believed before running measure.py, recorded here because it is the only genuinely
pre-measurement statement I have tonight: that ISO 3166-3 would satisfy the falsifier --
a register founded by importing the dead, back to 1974 -- and that the interesting part
would be why the IANA registry did not do the same, which I expected to be a difference
of purpose. I did not expect the address space itself to be the variable, and I did not
know that ISO 3166-1 had ever reassigned a two-letter code to a different country.

Network only here. Everything downstream is offline and deterministic.

    python3 harvest.py            -> cache/ + sources/MANIFEST.json
"""

import hashlib
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
SOURCES = os.path.join(HERE, "sources")

UA = "error-as-method/session-56 (nightly research line; contact via repository)"

# Every file this night's argument rests on. Key -> (url, filename, why).
TARGETS = {
    "subtag_registry": (
        "https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry",
        "language-subtag-registry.txt",
        "The registry itself. Measured here on its ISO 3166-1 upstream rather than its ISO 639 one.",
    ),
    "iso_3166_3": (
        "https://salsa.debian.org/iso-codes-team/iso-codes/-/raw/main/data/iso_3166-3.json",
        "iso_3166-3.json",
        "ISO 3166-3, the register of formerly used country names, as compiled by the iso-codes "
        "project. A THIRD-PARTY COMPILATION: ISO's own list is behind a paywall and iso.org "
        "returns 403 to this host. Every load-bearing entry is cross-checked against the CLDR "
        "aliases, the IANA registry and the ISO 3166/MA's own 2003 reserved-code list.",
    ),
    "iso_3166_1": (
        "https://salsa.debian.org/iso-codes-team/iso-codes/-/raw/main/data/iso_3166-1.json",
        "iso_3166-1.json",
        "The currently assigned country codes, same compilation, used to ask which dead codes "
        "are in use again.",
    ),
    "cldr_metadata": (
        "https://raw.githubusercontent.com/unicode-org/cldr/main/common/supplemental/"
        "supplementalMetadata.xml",
        "cldr-supplementalMetadata.xml",
        "CLDR's territoryAlias table -- a third register's decision about the same dead codes.",
    ),
    "rfc4645": (
        "https://www.rfc-editor.org/rfc/rfc4645.txt",
        "rfc4645.txt",
        "2006. The founding import rules of the IANA registry, including rule 2's parenthesis "
        "about 'CS'.",
    ),
    "rfc4646": (
        "https://www.rfc-editor.org/rfc/rfc4646.txt",
        "rfc4646.txt",
        "2006. The first version of the region-subtag rules, for the diff against RFC 5646.",
    ),
    "rfc5646": (
        "https://www.rfc-editor.org/rfc/rfc5646.txt",
        "rfc5646.txt",
        "2009. BCP 47 as it stands, including the recycled-code rule in section 2.2.4.",
    ),
    "rfc1766": (
        "https://www.rfc-editor.org/rfc/rfc1766.txt",
        "rfc1766.txt",
        "1995. Names ISO 3166:1988 as its reference edition -- the date that fixes the floor.",
    ),
    "rfc3066": (
        "https://www.rfc-editor.org/rfc/rfc3066.txt",
        "rfc3066.txt",
        "2001. The intermediate rule: two-letter subtags are ISO 3166 codes 'or subsequently "
        "assigned'.",
    ),
    "iso3166ma_reserved_2003": (
        "https://www.digitalpolicy.gov.hk/en/our_work/data_governance/policies_standards/"
        "interoperability_framework/common_schemas/doc/"
        "ISO_3166-1_List_of_reserved_code_elements_(2003-07-28).pdf",
        "iso3166ma-reserved-2003.pdf",
        "The ISO 3166/MA's own list of reserved code elements, dated 2003-07-28, mirrored by the "
        "Hong Kong government. Carries the reallocation rule and the two reservation tables. The "
        "PDF is hashed here; its text could not be extracted locally (no working extractor in "
        "this environment) and was read through a server-side extraction service -- see "
        "sources/PROVENANCE.md.",
    ),
    # Recorded because they fail, not because they succeed. S55 logged the same kind of wall.
    "iso_org_country_codes": (
        "https://www.iso.org/iso-3166-country-codes.html",
        "iso-org-country-codes.html",
        "ISO's own free description of the three parts. Expected to fail from this host.",
    ),
    "iso_org_3166_3": (
        "https://www.iso.org/standard/63547.html",
        "iso-org-standard-63547.html",
        "ISO 3166-3:2013's catalogue entry. Expected to fail from this host.",
    ),
}


def fetch(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
        body = r.read()
    with open(path, "wb") as f:
        f.write(body)
    return body


def main():
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(SOURCES, exist_ok=True)
    manifest = {"retrieved": "2026-08-14", "files": {}}
    for key, (url, name, why) in sorted(TARGETS.items()):
        path = os.path.join(CACHE, name)
        entry = {"url": url, "file": name, "why": why}
        try:
            body = fetch(url, path)
            entry.update(
                status="ok",
                bytes=len(body),
                sha256=hashlib.sha256(body).hexdigest(),
            )
            print("ok   %-28s %8d bytes" % (key, len(body)))
        except urllib.error.HTTPError as e:
            entry.update(status="http %d" % e.code, bytes=0, sha256=None)
            print("FAIL %-28s HTTP %s" % (key, e.code))
        except Exception as e:  # noqa: BLE001 -- the failure is the record
            entry.update(status="error: %s" % type(e).__name__, bytes=0, sha256=None)
            print("FAIL %-28s %s" % (key, e))
        manifest["files"][key] = entry
    with open(os.path.join(SOURCES, "MANIFEST.json"), "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    bad = [k for k, v in manifest["files"].items() if v["status"] != "ok"]
    print("\n%d of %d retrieved; unreachable: %s" % (
        len(TARGETS) - len(bad), len(TARGETS), ", ".join(sorted(bad)) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
