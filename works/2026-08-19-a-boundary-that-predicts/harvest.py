#!/usr/bin/env python3
"""Fetch the population: Lib/__future__.py at every published CPython release, plus the
documents that govern it.

The bytes are hashed into sources/MANIFEST.json and deliberately NOT committed
(PROTOCOL.md, amendment of 2026-08-18). Note for this night in particular: CPython is
PSF-2.0 licensed and the PEPs are public domain, so these bytes *could* lawfully be
redistributed. They are still not committed — forty-odd copies of one file would be a
worse warrant than one hash apiece, and a stranger re-fetches and compares.

stdlib only, network only here. Re-run from an empty sources/ and the measurement is
identical.

    python3 harvest.py
"""

import hashlib
import json
import os
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")

RAW = "https://raw.githubusercontent.com/python/cpython/{tag}/Lib/__future__.py"

# Every minor series of CPython that has ever shipped a Lib/__future__.py, 2.1 (where the
# module was introduced) to 3.14. The tag naming is not uniform across the project's
# history — some series are tagged vX.Y, some vX.Y.0 — so both forms are probed and the
# first that answers 200 is the one recorded. This is the complete population of released
# minor versions, not a sample.
SERIES = [
    (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
    (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
    (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14),
]

# The documents that say why the fields hold the values they hold.
DOCS = [
    ("pep-0236", "https://peps.python.org/pep-0236/",
     "PEP 236, 'Back to the __future__', Tim Peters, 2001",
     "The rule that sets the boundary: what OptionalRelease and MandatoryRelease mean and "
     "how far apart the policy puts them"),
    ("pep-0563", "https://peps.python.org/pep-0563/",
     "PEP 563, 'Postponed Evaluation of Annotations'",
     "The feature whose MandatoryRelease moved three times and then became None"),
    ("pep-0649", "https://peps.python.org/pep-0649/",
     "PEP 649, 'Deferred Evaluation Of Annotations Using Descriptors'",
     "What replaced PEP 563 and is the reason the boundary was withdrawn rather than met"),
    ("pep-0401", "https://peps.python.org/pep-0401/",
     "PEP 401, 'BDFL Retirement'",
     "The governing document of barry_as_FLUFL, whose MandatoryRelease is (4, 0, 0)"),
    ("pep-0004", "https://peps.python.org/pep-0004/",
     "PEP 4, 'Deprecation of Standard Modules'",
     "Control: the project's other written rule about phasing things out, for comparison"),
    ("pep-0387", "https://peps.python.org/pep-0387/",
     "PEP 387, 'Backwards Compatibility Policy'",
     "The project's standing compatibility rule, and whether it carries a boundary at all"),
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "error-as-method/night-2026-08-19"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:  # noqa: BLE001 - recorded, not swallowed
        return None, str(e).encode()


def main():
    os.makedirs(SRC, exist_ok=True)
    manifest = {
        "night": "2026-08-19",
        "session": 62,
        "note": (
            "Bytes fetched and hashed, deliberately not committed; see PROTOCOL.md, amendment "
            "of 2026-08-18. These particular bytes are redistributable (CPython is PSF-2.0, the "
            "PEPs are public domain) and are still not committed: one hash apiece is the better "
            "warrant. Re-fetch and compare sha256 to reproduce."
        ),
        "sources": [],
    }

    for major, minor in SERIES:
        got = None
        # Tag naming is not uniform across the project's history: most series are v{M}.{m}
        # or v{M}.{m}.0, but a few early ones only ever carried the bare {M}.{m} tag (2.3).
        for tag in (f"v{major}.{minor}", f"v{major}.{minor}.0", f"{major}.{minor}"):
            status, body = fetch(RAW.format(tag=tag))
            if status == 200:
                got = (tag, status, body)
                break
        if got is None:
            # Recorded as a hole in the population, never guessed at.
            manifest["sources"].append({
                "key": f"future-{major}.{minor}",
                "url": RAW.format(tag=f"v{major}.{minor}[.0]"),
                "what": f"Lib/__future__.py at the first final release of CPython {major}.{minor}",
                "why": "Population P-A: the boundary field as published in that release",
                "status": 404,
                "note": "no tag of either probed form answered 200; this series is a hole",
            })
            print(f"  {major}.{minor:<3} MISSING")
            continue
        tag, status, body = got
        name = f"future-{major}.{minor}.py"
        with open(os.path.join(SRC, name), "wb") as fh:
            fh.write(body)
        manifest["sources"].append({
            "key": f"future-{major}.{minor}",
            "url": RAW.format(tag=tag),
            "tag": tag,
            "series": f"{major}.{minor}",
            "what": f"Lib/__future__.py as published in CPython {tag}",
            "why": "Population P-A: the boundary field as published in that release",
            "status": status,
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "retrieved": "2026-08-19",
            "local": f"{name} (fetched, not committed)",
        })
        print(f"  {major}.{minor:<3} {tag:<9} {len(body):>6} bytes")

    for key, url, what, why in DOCS:
        status, body = fetch(url)
        name = f"{key}.html"
        if status == 200:
            with open(os.path.join(SRC, name), "wb") as fh:
                fh.write(body)
        manifest["sources"].append({
            "key": key,
            "url": url,
            "what": what,
            "why": why,
            "status": status,
            "bytes": len(body) if status == 200 else None,
            "sha256": hashlib.sha256(body).hexdigest() if status == 200 else None,
            "retrieved": "2026-08-19",
            "local": f"{name} (fetched, not committed)" if status == 200 else None,
        })
        print(f"  {key:<10} {status} {len(body) if status == 200 else ''}")

    with open(os.path.join(SRC, "MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")

    gitignore = os.path.join(SRC, ".gitignore")
    with open(gitignore, "w") as fh:
        fh.write(
            "# The harvested bytes are fetched and hashed, never committed: PROTOCOL.md,\n"
            "# amendment of 2026-08-18. MANIFEST.json beside them is the warrant — re-fetch\n"
            "# and compare the sha256. This file lives here rather than in the repository\n"
            "# root because the auto-land gate's allowlist covers works/ and does not cover\n"
            "# /.gitignore, and it refused the night of 2026-08-18 for exactly that (F-046).\n"
            "*\n"
            "!.gitignore\n"
            "!MANIFEST.json\n"
        )

    ok = sum(1 for s in manifest["sources"] if s["status"] == 200)
    print(f"\n{ok}/{len(manifest['sources'])} sources at 200; manifest written")


if __name__ == "__main__":
    main()
