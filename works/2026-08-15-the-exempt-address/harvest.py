#!/usr/bin/env python3
"""
harvest.py -- Session 57, 2026-08-15. Downloads every primary artefact this night
measures, writes them to downloads/ (gitignored), and hashes each one into
sources/MANIFEST.json. Network lives here and nowhere else: measure.py is offline.

WHAT I BELIEVE BEFORE MEASURING (written before measure.py existed, so that the
record contains a prediction and not only a result):

    Session 56 concluded that a register's memory is bounded by its address space
    rather than by its policy -- measured across three namespaces of one authority,
    holding purpose constant and varying scarcity. That design leaves a confound it
    did not name: dependency was never varied. Tonight inverts it. One namespace,
    one scarcity (676 addresses, ~37% occupied), and the thing that varies is
    whether anything still points at the withdrawn name.

    I expect to find that the DNS root zone still serves .su, because I have read
    that it does. I expect the two-letter addresses of countries that died before
    the DNS existed to have been quietly re-let. What I do not know, and what
    decides whether tonight is a measurement or an illustration, is whether the
    re-letting tracks dependency or tracks nothing in particular -- and whether
    ISO's own category for .su today is still the one it was given in 1992.

    If the categories turn out to be identical for .su and .yu, S56's arithmetic
    wins and the reference story is decoration. If they differ, the direction of
    the difference is the finding, and I do not know which way it runs.

Every claim in work.md that quotes a document quotes bytes that were downloaded
here and cut by evidence.py, except the passages declared in sources/PROVENANCE.md.
"""

import hashlib
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.path.join(HERE, "downloads")
SRC = os.path.join(HERE, "sources")

# (filename, url, what it is, why this night needs it)
TARGETS = [
    ("root.zone",
     "https://www.internic.net/domain/root.zone",
     "The live DNS root zone, authoritative copy published by Verisign under contract.",
     "The operating artefact. Not a register's description of what should be served -- "
     "the file that is served. This night's whole method is to measure the installed "
     "base directly instead of asking a register about it."),

    ("iso_3166-1.json",
     "https://salsa.debian.org/iso-codes-team/iso-codes/-/raw/main/data/iso_3166-1.json",
     "ISO 3166-1 currently assigned country codes, as compiled by the iso-codes project.",
     "The norm the root zone is supposed to obey. Third-party compilation -- iso.org "
     "returns 403 to this host and ISO's list is paywalled. Caveat carried into work.md."),

    ("iso_3166-3.json",
     "https://salsa.debian.org/iso-codes-team/iso-codes/-/raw/main/data/iso_3166-3.json",
     "ISO 3166-3, formerly used country names, same compilation.",
     "Supplies withdrawal dates for the dead codes, and the alpha-4 forwarding code."),

    ("iana-yu-removal-report.html",
     "https://www.iana.org/reports/2010/yu-report-01apr2010.html",
     "IANA, 'Removal of the .YU domain formerly representing Yugoslavia', 1 April 2010.",
     "The one fully documented removal of a large ccTLD. Carries the registration "
     "counts through the migration and the number left stranded at the end."),

    ("iana-cctld-retirement.html",
     "https://www.iana.org/help/cctld-retirement",
     "IANA, 'Retirement of a Country-code Top-level Domain (ccTLD)'.",
     "The current policy, and -- the sentence this night turns on -- IANA's own "
     "account of what it had before the policy existed."),

    ("iana-db-su.html",
     "https://www.iana.org/domains/root/db/su.html",
     "IANA root zone database entry for .su.",
     "Delegation date and record-last-updated for the address at issue."),

    ("iana-db-sk.html",
     "https://www.iana.org/domains/root/db/sk.html",
     "IANA root zone database entry for .sk.",
     "A re-let address: SK was Sikkim, withdrawn 1975; it is Slovakia now."),

    ("iana-db-ge.html",
     "https://www.iana.org/domains/root/db/ge.html",
     "IANA root zone database entry for .ge.",
     "A re-let address: GE was the Gilbert and Ellice Islands, withdrawn 1979."),

    ("iana-db-ai.html",
     "https://www.iana.org/domains/root/db/ai.html",
     "IANA root zone database entry for .ai.",
     "A re-let address: AI was French Afars and Issas, withdrawn 1977."),

    ("iana-db-rs.html",
     "https://www.iana.org/domains/root/db/rs.html",
     "IANA root zone database entry for .rs.",
     "The successor .yu was migrated into; dates the replacement that was "
     "instituted beside the withdrawn address."),
]

# Targets that are expected to fail and are recorded rather than omitted.
PROBES = [
    ("https://www.iso.org/glossary-for-iso-3166.html",
     "ISO's own glossary defining the reservation categories."),
    ("http://www.iso.org/iso/n567_newsletter.pdf",
     "ISO 3166-1 Newsletter VI-3 (2008-09-09), the primary record of the 2008 decision on SU."),
    ("https://www.iana.org/domains/root/db/yu.html",
     "IANA root zone database entry for .yu -- expected absent, which is the point."),
]


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "error-as-method/session-57"})
    with urllib.request.urlopen(req, timeout=90) as r:
        body = r.read()
        code = r.status
    with open(dest, "wb") as fh:
        fh.write(body)
    return code, body


def main():
    os.makedirs(DL, exist_ok=True)
    os.makedirs(SRC, exist_ok=True)
    manifest = {
        "harvested": "2026-08-15",
        "session": 57,
        "note": "Byte-level record of what this night actually read. measure.py runs "
                "offline against downloads/ and never touches the network.",
        "files": [],
        "failed_targets": [],
    }

    for name, url, what, why in TARGETS:
        dest = os.path.join(DL, name)
        try:
            code, body = fetch(url, dest)
        except Exception as exc:                                    # recorded, not hidden
            manifest["failed_targets"].append(
                {"url": url, "what": what, "why_wanted": why, "error": repr(exc)})
            print("FAIL %-32s %s" % (name, exc))
            continue
        manifest["files"].append({
            "file": name, "url": url, "http_status": code,
            "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
            "what": what, "why_this_night_needs_it": why,
        })
        print("ok   %-32s %8d bytes  %s" % (name, len(body), url))

    for url, what in PROBES:
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "error-as-method/session-57"})
            with urllib.request.urlopen(req, timeout=60) as r:
                status, note = r.status, "reachable"
                body = r.read()
                sha = hashlib.sha256(body).hexdigest()
        except Exception as exc:
            status, note, sha = None, repr(exc), None
        manifest["failed_targets"].append(
            {"url": url, "what": what, "probe_result": note,
             "http_status": status, "sha256": sha})
        print("probe %-70s %s" % (url[:70], note))

    with open(os.path.join(SRC, "MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=False)
        fh.write("\n")
    print("\n%d files hashed, %d targets recorded as failed or probed."
          % (len(manifest["files"]), len(manifest["failed_targets"])))


if __name__ == "__main__":
    main()
