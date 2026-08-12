#!/usr/bin/env python3
"""Harvest the tz database's own release history into two committed evidence files.

This is the ONLY step that needs the network. It reads a local clone of the tz
repository (https://github.com/eggert/tz), walks its release tags, and writes:

    data/releases.json.gz  one record per release: tag, commit, date, and for every
                           timezone identifier its kind (Zone/Link), its link target,
                           and a digest of its normalised data rows
    data/edits.json        every change event between consecutive releases, with the
                           before/after rows for every retroactive edit
    data/NEWS-<tag>.txt    the release NEWS file, as quoted in work.md
    data/theory-<tag>.html the design rationale, as quoted in work.md
    data/MANIFEST.md       SHA-256 of every file above, the clone's HEAD, the tag list

`measure.py` then computes every number in `work.md` from `data/` alone, offline.

Usage:
    git clone https://github.com/eggert/tz.git /path/to/tz
    python3 harvest.py /path/to/tz

Why a git clone and not the release tarballs: the tags are the releases (the tz
distribution's own "Downloading the tz database" documents tag-per-release), and one
clone gives all 87 without 87 downloads. The commit SHA of each tag is recorded so any
reader can check the extract against the same tree.

Normalisation, stated because everything downstream depends on it:
  * a Zone block is the `Zone NAME ...` line plus every following line that begins with
    whitespace and is not a comment;
  * inline comments (`#` to end of line) are stripped, whitespace runs collapse to one
    space. Commentary churn is therefore NOT counted as a data edit. This is deliberate:
    the tz database changes its comments constantly and that is not the question.
"""

import gzip
import hashlib
import json
import os
import subprocess
import sys
from difflib import SequenceMatcher

# The files installed by default. `backzone` is excluded because the database's own
# `backward` header calls it data "out of scope for tzdb proper"; `systemv` is excluded
# because it is not built by default. `pacificnew` is included: it was distributed.
DATA_FILES = [
    "africa", "antarctica", "asia", "australasia", "europe",
    "northamerica", "southamerica", "etcetera", "factory",
    "backward", "pacificnew",
]

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data")


def git(repo, *args):
    """Run git and decode as latin-1.

    Not a guess: early releases in this window are not valid UTF-8 (the first run of
    this script died on byte 0xf3 in a pre-2015 file). latin-1 is a lossless byte->char
    map, and every byte that matters here is ASCII: non-ASCII appears only inside
    comments, which `norm()` strips before anything is hashed or compared. Mojibake in a
    contributor's name in a comment cannot reach the measurement.
    """
    out = subprocess.run(["git", "-C", repo, *args],
                         capture_output=True, check=True).stdout
    return out.decode("latin-1")


def strip_comment(line):
    i = line.find("#")
    return line if i < 0 else line[:i]


def norm(line):
    return " ".join(strip_comment(line).split())


def parse_release(repo, tag):
    """Return {identifier: {kind, target, rows}} for one release tag."""
    ids = {}
    files_present = []
    for fname in DATA_FILES:
        try:
            text = git(repo, "show", f"{tag}:{fname}")
        except subprocess.CalledProcessError:
            continue
        files_present.append(fname)
        lines = text.split("\n")
        current = None
        for raw in lines:
            if not raw.strip():
                current = None
                continue
            if raw.lstrip().startswith("#"):
                # a comment line does not close a Zone block in zic's grammar, but it
                # also never carries data; leave `current` alone.
                continue
            if raw[0].isspace():
                if current is not None:
                    row = norm(raw)
                    if row:
                        ids[current]["rows"].append(row)
                continue
            current = None
            fields = norm(raw).split(" ")
            if not fields:
                continue
            if fields[0] == "Zone" and len(fields) >= 2:
                name = fields[1]
                ids[name] = {"kind": "Zone", "target": None,
                             "rows": [" ".join(fields[2:])], "file": fname}
                current = name
            elif fields[0] == "Link" and len(fields) >= 3:
                # Link TARGET LINK-NAME
                ids[fields[2]] = {"kind": "Link", "target": fields[1],
                                  "rows": [], "file": fname}
    return ids, files_present


def digest(rows):
    return hashlib.sha256("\n".join(rows).encode()).hexdigest()[:16]


def classify(old_rows, new_rows):
    """Classify a change to one Zone's row list.

    Returns (kind, ops) where kind is one of:
      'append'      new is a strict extension of old  -> only the future was written
      'tail_close'  the last old row gained trailing fields (an UNTIL) and rows were
                    appended; every earlier row is untouched -> also only the future
      'retro'       anything else: a published row was rewritten or deleted
    """
    if old_rows == new_rows:
        return None, []
    if len(new_rows) > len(old_rows) and new_rows[:len(old_rows)] == old_rows:
        return "append", []
    if old_rows and len(new_rows) >= len(old_rows):
        head_same = new_rows[:len(old_rows) - 1] == old_rows[:len(old_rows) - 1]
        last_old, last_new = old_rows[-1], new_rows[len(old_rows) - 1]
        if head_same and last_new.startswith(last_old + " "):
            return "tail_close", []
    sm = SequenceMatcher(None, old_rows, new_rows, autojunk=False)
    ops = [{"op": tag, "i1": i1, "old": old_rows[i1:i2], "new": new_rows[j1:j2]}
           for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]
    return "retro", ops


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    repo = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)

    tags = [t for t in git(repo, "tag").split() if t]
    # release tags are YYYY<letter>; sort by (year, letter)
    tags = sorted((t for t in tags if len(t) >= 5 and t[:4].isdigit()),
                  key=lambda t: (int(t[:4]), t[4:]))
    print(f"{len(tags)} release tags: {tags[0]} .. {tags[-1]}")

    releases = []
    prev_ids = None
    prev_tag = None
    edits = []

    for tag in tags:
        commit = git(repo, "rev-list", "-n", "1", tag).strip()
        date = git(repo, "log", "-1", "--format=%ad", "--date=short", tag).strip()
        ids, files_present = parse_release(repo, tag)
        releases.append({
            "tag": tag, "commit": commit, "date": date,
            "files": files_present,
            "n_ids": len(ids),
            "ids": {k: {"kind": v["kind"], "target": v["target"],
                        "file": v["file"], "nrows": len(v["rows"]),
                        "digest": digest(v["rows"])}
                    for k, v in sorted(ids.items())},
        })

        if prev_ids is not None:
            added = sorted(set(ids) - set(prev_ids))
            removed = sorted(set(prev_ids) - set(ids))
            for name in added:
                edits.append({"from": prev_tag, "to": tag, "id": name,
                              "event": "added", "kind": ids[name]["kind"]})
            for name in removed:
                edits.append({"from": prev_tag, "to": tag, "id": name,
                              "event": "removed", "kind": prev_ids[name]["kind"]})
            for name in sorted(set(ids) & set(prev_ids)):
                o, n = prev_ids[name], ids[name]
                if o["kind"] != n["kind"]:
                    edits.append({"from": prev_tag, "to": tag, "id": name,
                                  "event": "kind_change",
                                  "old": o["kind"], "new": n["kind"],
                                  "old_target": o["target"], "new_target": n["target"]})
                elif o["kind"] == "Link" and o["target"] != n["target"]:
                    edits.append({"from": prev_tag, "to": tag, "id": name,
                                  "event": "retarget",
                                  "old": o["target"], "new": n["target"]})
                if o["kind"] == "Zone" and n["kind"] == "Zone":
                    kind, ops = classify(o["rows"], n["rows"])
                    if kind:
                        rec = {"from": prev_tag, "to": tag, "id": name,
                               "event": kind,
                               "n_old": len(o["rows"]), "n_new": len(n["rows"])}
                        if kind == "retro":
                            rec["ops"] = ops
                        edits.append(rec)
        prev_ids, prev_tag = ids, tag

    # releases.json is ~5.5 MB uncompressed, almost all of it the same 600 identifier
    # names repeated 87 times. It is gzipped so the evidence can live in the repository
    # without dominating it; `measure.py` reads it with the stdlib.
    rel_path = os.path.join(OUT, "releases.json.gz")
    edit_path = os.path.join(OUT, "edits.json")
    with gzip.open(rel_path, "wt", compresslevel=9, encoding="utf-8") as f:
        json.dump({"source": "https://github.com/eggert/tz",
                   "files_in_scope": DATA_FILES,
                   "releases": releases}, f, separators=(",", ":"), sort_keys=True)
    with open(edit_path, "w") as f:
        json.dump({"source": "https://github.com/eggert/tz",
                   "edits": edits}, f, separators=(",", ":"), sort_keys=True)

    # Two documents are quoted in work.md; harvest them from the same tree so the
    # quotations can be checked against a hash rather than against my memory.
    quoted = []
    for fname, out_name in (("NEWS", "NEWS-%s.txt" % tags[-1]),
                            ("theory.html", "theory-%s.html" % tags[-1])):
        blob = git(repo, "show", "%s:%s" % (tags[-1], fname)).encode("latin-1")
        path = os.path.join(OUT, out_name)
        with open(path, "wb") as fh:
            fh.write(blob)
        quoted.append(path)

    def sha(p):
        return hashlib.sha256(open(p, "rb").read()).hexdigest()

    head = git(repo, "rev-parse", "HEAD").strip()
    with open(os.path.join(OUT, "MANIFEST.md"), "w") as f:
        f.write("# Manifest — harvested 2026-08-12 (Session 50)\n\n")
        f.write("Source: `https://github.com/eggert/tz` (the tz database's own repository; "
                "releases are git tags).\n\n")
        f.write(f"Clone HEAD at harvest time: `{head}`\n\n")
        f.write(f"Releases: **{len(releases)}**, `{releases[0]['tag']}` "
                f"({releases[0]['date']}) .. `{releases[-1]['tag']}` "
                f"({releases[-1]['date']}).\n\n")
        f.write("Files in scope: " + ", ".join(f"`{x}`" for x in DATA_FILES) + ".\n")
        f.write("Excluded: `backzone` (the `backward` header calls it out of scope for "
                "tzdb proper), `systemv` (not built by default).\n\n")
        f.write("| file | sha256 | bytes |\n|---|---|---|\n")
        for p in [rel_path, edit_path] + quoted:
            f.write(f"| `data/{os.path.basename(p)}` | `{sha(p)}` | "
                    f"{os.path.getsize(p)} |\n")
        f.write("\n## Release tags and their commits\n\n| tag | date | commit | identifiers |\n")
        f.write("|---|---|---|---|\n")
        for r in releases:
            f.write(f"| {r['tag']} | {r['date']} | `{r['commit'][:12]}` | {r['n_ids']} |\n")

    print(f"wrote {rel_path} ({os.path.getsize(rel_path)} B)")
    print(f"wrote {edit_path} ({os.path.getsize(edit_path)} B)")
    print(f"{len(edits)} change events")


if __name__ == "__main__":
    main()
