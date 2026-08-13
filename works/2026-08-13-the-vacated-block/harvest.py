#!/usr/bin/env python3
"""
harvest.py -- Session 54, 2026-08-13.

Downloads one UnicodeData.txt per published version of the Unicode Character
Database, from the consortium's own public archive, plus the two files that
carry the standard's correction channel.

    https://www.unicode.org/Public/

WHAT IS COLLECTED, and the choices behind it -- stated here so the numbers in
measure.py can be argued with rather than taken.

1. ONE FILE PER VERSION.  UnicodeData.txt is the file that answers "which code
   points exist and what are they called".  Field 0 is the code point, field 1
   the character name.  Everything measured tonight comes out of those two
   fields.  Other UCD files (Blocks, PropList, DerivedAge) are not fetched.

2. WHICH VERSIONS.  Every directory under /Public/ that holds a UnicodeData
   file, plus /Public/reconstructed/ (1.0.0 and 1.0.1 -- the consortium's own
   reconstruction of the pre-ISO-10646-merger namespace, published later and
   labelled as a reconstruction; treated here as evidence about 1991 with that
   label attached, never as a 1991 artefact).  Update releases that reissue the
   database (2.1-Update4, 3.0-Update1, 4.0-Update1 ...) are kept as their own
   points, because a reissue is exactly the event this measurement is about.

3. RANGE MARKERS ARE EXPANDED.  UnicodeData.txt compresses large blocks into
   two rows -- "<CJK Ideograph, First>" and "<..., Last>".  A run of 20,000
   ideographs is two lines.  Left unexpanded, the CJK and Hangul blocks -- the
   exact blocks this night is about -- would be invisible in the counts.  They
   are expanded to one entry per code point.  Their names are generated
   algorithmically by the standard rather than listed, so an expanded entry
   carries the marker's label, not a per-character name, and the NAME analysis
   below excludes them.

4. SURROGATES AND PRIVATE USE are kept in the code-point census (they are
   assigned in the sense that matters here: the standard says something is
   there) and are flagged so measure.py can exclude them; noncharacters are not
   listed in UnicodeData.txt at all and so do not appear.

Network is used HERE ONLY.  measure.py runs offline over ./sources/.
Every downloaded file is hashed into sources/MANIFEST.json.
Stdlib only.
"""

import hashlib
import json
import os
import re
import sys
import time
import urllib.request

BASE = "https://www.unicode.org/Public/"
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")
CACHE = os.path.join(HERE, "cache")

UA = {"User-Agent": "error-as-method/session-54 (research; one pass over the public UCD archive)"}


def get(url, tries=3):
    for n in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read()
        except Exception as e:
            if n == tries - 1:
                raise
            sys.stderr.write("  retry %d %s (%s)\n" % (n + 1, url, e))
            time.sleep(3 * (n + 1))


def listing(url):
    """Href names one level below url."""
    try:
        html = get(url).decode("utf-8", "replace")
    except Exception as e:
        sys.stderr.write("  listing failed %s (%s)\n" % (url, e))
        return []
    out = []
    for h in re.findall(r'href="([^"]+)"', html):
        if h.startswith("?") or h.startswith("/") or h.startswith("http"):
            continue
        out.append(h)
    return out


def discover():
    """(version_label, url_of_UnicodeData) for every published version."""
    found = []
    roots = [(BASE, d) for d in listing(BASE) if re.match(r"^\d+\.\d+", d)]
    roots += [(BASE + "reconstructed/", d) for d in listing(BASE + "reconstructed/")
              if re.match(r"^\d+\.\d+", d)]
    for parent, d in roots:
        vdir = parent + d
        label = d.rstrip("/")
        # UnicodeData sits either at the top of the version directory (old
        # layout, versioned filename) or under ucd/ (4.1.0 onward).
        for sub in ("", "ucd/"):
            names = listing(vdir + sub)
            cands = [n for n in names
                     if n.lower().startswith("unicodedata") and n.endswith(".txt")]
            if cands:
                # prefer the plain name, else the highest versioned one
                cands.sort(key=lambda n: (n.lower() != "unicodedata.txt", n))
                found.append((label, vdir + sub + cands[0]))
                break
        else:
            sys.stderr.write("  no UnicodeData under %s\n" % vdir)
    return found


def vkey(label):
    parts = re.findall(r"\d+", label)
    return tuple(int(p) for p in (parts + ["0", "0", "0"])[:3]) + (label,)


def main():
    os.makedirs(SRC, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)

    versions = sorted(discover(), key=lambda t: vkey(t[0]))
    print("discovered %d version directories with a UnicodeData file" % len(versions))

    manifest = {"retrieved": "2026-08-13", "base": BASE, "files": []}
    rows = []
    for label, url in versions:
        fn = os.path.join(CACHE, "UnicodeData-%s.txt" % label)
        if not os.path.exists(fn):
            print("  fetching %-14s %s" % (label, url))
            data = get(url)
            with open(fn, "wb") as f:
                f.write(data)
            time.sleep(0.5)
        else:
            data = open(fn, "rb").read()
        manifest["files"].append({
            "version": label,
            "url": url,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
        rows.append((label, url, len(data)))
        print("    %-14s %9d bytes" % (label, len(data)))

    # The correction channel, current release. NameAliases.txt carries the
    # formal aliases, including type=correction -- the standard's own record of
    # the names it considers wrong and cannot change. NamesList.txt carries the
    # annotation layer beside the immutable names.
    extra = {
        "NameAliases.txt": "https://www.unicode.org/Public/UCD/latest/ucd/NameAliases.txt",
        "NamesList.txt": "https://www.unicode.org/Public/UCD/latest/ucd/NamesList.txt",
        "stability_policy.html": "https://www.unicode.org/policies/stability_policy.html",
    }
    for name, url in extra.items():
        print("  fetching %s" % name)
        data = get(url)
        with open(os.path.join(SRC, name), "wb") as f:
            f.write(data)
        manifest["files"].append({
            "version": "current",
            "url": url,
            "name": name,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
        time.sleep(0.5)

    with open(os.path.join(SRC, "MANIFEST.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    print("\n%d files hashed into sources/MANIFEST.json" % len(manifest["files"]))
    print("cache/ holds the %d UnicodeData files; it is gitignored (68 MB)." % len(rows))


if __name__ == "__main__":
    main()
