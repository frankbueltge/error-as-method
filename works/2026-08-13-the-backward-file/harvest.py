#!/usr/bin/env python3
"""harvest.py -- fetch every published tzdata release and record what it contained.

The IANA time zone database publishes its complete release history as one directory:
https://data.iana.org/time-zones/releases/ . Every tzdata tarball since 1996 is there.
That directory is the thing this night needed and could not get anywhere else: a norm's
own revision history, complete, machine-readable, from an institution that still exists.

This script downloads the tarballs, hashes them, parses the namespace out of each one,
and writes two derived tables. The tarballs themselves are NOT committed (54 MB); the
manifest of SHA-256 digests is, so the derived tables can be re-checked against them.

  python3 harvest.py            # download into ./sources/tarballs, then parse
  python3 harvest.py --parse-only

Outputs:
  sources/MANIFEST.json      release -> {file, sha256, bytes, release_date}
  releases.csv               one row per release: counts and deltas
  identifiers.csv            one row per identifier ever to exist: its whole life

stdlib only, no network at measuring time.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import tarfile
import urllib.request

BASE = "https://data.iana.org/time-zones/releases/"
HERE = os.path.dirname(os.path.abspath(__file__))
TARDIR = os.path.join(HERE, "sources", "tarballs")

# The files the reference Makefile compiles into the default installed namespace:
# the seven geographic files, plus etcetera, plus backward -- the compatibility file.
# Everything else in a tarball is excluded, and each exclusion is a decision this
# measurement has to defend:
#   backzone   not installed unless PACKRATDATA is set; it is the 2021b episode's
#              destination and is counted SEPARATELY below, never mixed in.
#   systemv, factory, pacificnew, solar87/88/89
#              legacy non-geographic sets, not part of the AREA/LOCATION namespace
#              whose corrigibility is under test here.
INSTALLED = {
    "africa", "antarctica", "asia", "australasia", "europe",
    "northamerica", "southamerica", "etcetera", "backward",
}
SEPARATE = {"backzone"}

ZONE_RE = re.compile(r"^Zone\s+(\S+)")
LINK_RE = re.compile(r"^Link\s+(\S+)\s+(\S+)")


def release_key(name):
    """Sort key for a release name like 'tzdata96i' or 'tzdata2021b'.

    Two-digit years in the archive are 1993-1999; four-digit years are literal.
    The trailing letter is the within-year sequence; a release with no letter
    sorts before 'a'.
    """
    m = re.match(r"^tzdata(\d{2}|\d{4})([a-z]*)$", name)
    if not m:
        return None
    year = int(m.group(1))
    if year < 100:
        year += 1900
    letter = m.group(2)
    seq = 0
    for ch in letter:
        seq = seq * 27 + (ord(ch) - ord("a") + 1)
    return (year, seq)


def list_releases():
    with urllib.request.urlopen(BASE, timeout=120) as fh:
        html = fh.read().decode("utf-8", "replace")
    out = []
    for fn in sorted(set(re.findall(r'href="(tzdata[^"]+\.tar\.gz)"', html))):
        rel = fn[: -len(".tar.gz")]
        if release_key(rel) is None:      # 'tzdatabeta' and friends
            continue
        out.append((rel, fn))
    out.sort(key=lambda p: release_key(p[0]))
    return out


def download(releases):
    os.makedirs(TARDIR, exist_ok=True)
    for rel, fn in releases:
        dest = os.path.join(TARDIR, fn)
        if os.path.exists(dest):
            continue
        sys.stderr.write("fetch %s\n" % fn)
        urllib.request.urlretrieve(BASE + fn, dest)


def parse_tarball(path):
    """Return (zones, links, backzone_zones, release_date).

    zones  : set of canonical Zone names in the default installed namespace
    links  : dict linkname -> target, likewise
    bzones : set of Zone names in backzone (present from 2013 on, not installed)
    date   : latest mtime in the archive, ISO date -- the release date
    """
    zones, links, bzones = set(), {}, set()
    latest = 0
    with tarfile.open(path) as tf:
        for member in tf.getmembers():
            if not member.isfile():
                continue
            latest = max(latest, member.mtime)
            base = os.path.basename(member.name)
            if base not in INSTALLED and base not in SEPARATE:
                continue
            fh = tf.extractfile(member)
            if fh is None:
                continue
            text = fh.read().decode("utf-8", "replace")
            for raw in text.splitlines():
                line = raw.split("#", 1)[0].rstrip()
                if not line or line[0].isspace():
                    continue          # Zone continuation lines are indented
                mz = ZONE_RE.match(line)
                if mz:
                    (bzones if base in SEPARATE else zones).add(mz.group(1))
                    continue
                ml = LINK_RE.match(line)
                if ml and base not in SEPARATE:
                    links[ml.group(2)] = ml.group(1)
    import datetime
    date = datetime.datetime.utcfromtimestamp(latest).strftime("%Y-%m-%d")
    return zones, links, bzones, date


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parse-only", action="store_true")
    args = ap.parse_args()

    if args.parse_only:
        files = sorted(os.listdir(TARDIR))
        releases = [(f[: -len(".tar.gz")], f) for f in files if f.endswith(".tar.gz")]
        releases = [r for r in releases if release_key(r[0]) is not None]
        releases.sort(key=lambda p: release_key(p[0]))
    else:
        releases = list_releases()
        download(releases)

    manifest, history = {}, []
    for rel, fn in releases:
        path = os.path.join(TARDIR, fn)
        zones, links, bzones, date = parse_tarball(path)
        manifest[rel] = {
            "file": fn,
            "sha256": sha256(path),
            "bytes": os.path.getsize(path),
            "release_date": date,
            "url": BASE + fn,
        }
        history.append({"release": rel, "date": date, "zones": zones,
                        "links": links, "backzone": bzones})
        sys.stderr.write("%-14s %s  zones=%-4d links=%-4d backzone=%d\n"
                         % (rel, date, len(zones), len(links), len(bzones)))

    with open(os.path.join(HERE, "sources", "MANIFEST.json"), "w") as fh:
        json.dump({"source": BASE, "releases": manifest}, fh, indent=1, sort_keys=True)

    # ---- releases.csv : one row per release -------------------------------
    rows = []
    prev = None
    for h in history:
        names = set(h["zones"]) | set(h["links"])
        if prev is None:
            added = removed = promoted = demoted = 0
        else:
            pnames = set(prev["zones"]) | set(prev["links"])
            added = len(names - pnames)
            removed = len(pnames - names)
            demoted = len([n for n in h["links"] if n in prev["zones"]])
            promoted = len([n for n in h["zones"] if n in prev["links"]])
        rows.append((h["release"], h["date"], len(h["zones"]), len(h["links"]),
                     len(h["backzone"]), added, removed, demoted, promoted))
        prev = h
    with open(os.path.join(HERE, "releases.csv"), "w") as fh:
        fh.write("release,date,zones,links,backzone,added,removed,demoted,promoted\n")
        for r in rows:
            fh.write(",".join(str(x) for x in r) + "\n")

    # ---- identifiers.csv : one row per identifier ever to exist -----------
    lives = {}
    for i, h in enumerate(history):
        for n in h["zones"]:
            lives.setdefault(n, {"first": h["release"], "states": []})["states"].append((i, "Z", ""))
        for n, tgt in h["links"].items():
            lives.setdefault(n, {"first": h["release"], "states": []})["states"].append((i, "L", tgt))
    nrel = len(history)
    with open(os.path.join(HERE, "identifiers.csv"), "w") as fh:
        fh.write("name,first_release,first_date,last_release,last_date,"
                 "present_now,ever_zone,ever_link,final_state,final_target,"
                 "demotions,releases_present\n")
        for name in sorted(lives):
            st = lives[name]["states"]
            first_i, last_i = st[0][0], st[-1][0]
            ever_z = any(s[1] == "Z" for s in st)
            ever_l = any(s[1] == "L" for s in st)
            demotions = sum(1 for a, b in zip(st, st[1:])
                            if a[1] == "Z" and b[1] == "L" and b[0] == a[0] + 1)
            fh.write("%s,%s,%s,%s,%s,%d,%d,%d,%s,%s,%d,%d\n" % (
                name,
                history[first_i]["release"], history[first_i]["date"],
                history[last_i]["release"], history[last_i]["date"],
                1 if last_i == nrel - 1 else 0,
                1 if ever_z else 0, 1 if ever_l else 0,
                st[-1][1], st[-1][2], demotions, len(st)))

    sys.stderr.write("\n%d releases, %d identifiers ever seen\n" % (nrel, len(lives)))


if __name__ == "__main__":
    main()
