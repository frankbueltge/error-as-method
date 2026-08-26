#!/usr/bin/env python3
"""forecasts.py — Session 71, 2026-08-26.

POST-HOC. Not predicted, not scored. Written after the four predictions were
settled, because the only-H cell turned out to be full of one particular kind of
disagreement and the obvious next question had a cheap answer.

The question: `Changed` is documented as *"minor version when default changed"* —
past tense. At the moment a given state of table.go existed, had the release each
`Changed` value names actually happened? Where it had not, the field was holding
a **forecast**, whatever its comment says.

Session 69 asked exactly this of CPython's `__future__.OptionalRelease` and found
one forecast that lived an hour in review. Tonight it is asked of a whole
population, at two grids at once: every patch-set state, and every RELEASE. The
release grid is the one that matters, because a forecast in a shipped release is
not a state a reviewer caught in passing.

Adds its fetches to sources/MANIFEST.json rather than replacing it.

Usage:
    python3 forecasts.py
"""

import datetime as dt
import hashlib
import json
import os
import re
import urllib.parse
import urllib.request

from measure import parse_table

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
GRIDS = os.path.join(REPO, "works", "2026-08-25-under-the-commit", "grids.json")
GERRIT = "https://go-review.googlesource.com"
UA = "error-as-method/session-71 (nightly research line)"

NEW = []


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read()


def gerrit(url, what):
    st, raw = get(url)
    NEW.append({"url": url, "http_status": st, "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "fetched": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "what": what, "committed": False})
    txt = raw.decode("utf-8", "replace")
    i = txt.find("\n")
    if txt.startswith(")]}'") and i != -1:
        txt = txt[i + 1:]
    return json.loads(txt)


def ts(s):
    """Parse the three date shapes in play, always to naive UTC.

    Gerrit writes '2024-05-15 20:47:08.000000000' in UTC; the state grid writes
    git's own '2023-08-08T15:00:52+00:00' with an offset. Mixing them without
    normalising would shift a value by up to a day, which at this resolution
    would decide whether a release had happened.
    """
    if not s:
        return None
    s = s.strip()
    m = re.match(r"^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})"
                 r"(?:\.\d+)?(Z|[+-]\d{2}:?\d{2})?$", s)
    if not m:
        return None
    base = dt.datetime.strptime(m.group(1) + " " + m.group(2),
                                "%Y-%m-%d %H:%M:%S")
    off = m.group(3)
    if off and off != "Z":
        off = off.replace(":", "")
        sign = 1 if off[0] == "+" else -1
        base -= sign * dt.timedelta(hours=int(off[1:3]), minutes=int(off[3:5]))
    return base


# Which field carries the state's own moment, per grid.
#
# CORRECTION, filed rather than repaired quietly (see adjudication.json). The
# first version put git's AUTHOR date first for the commit grid. Author date is
# when a patch was written, not when it entered the history: CL 659315 was
# authored 2025-03-19 and committed seventeen months later, so every commit
# state inherited a date from before its own review and ten commit states were
# reported as forecasts looking one to five releases ahead. The tell was that
# they clustered on five dates, each shared by several unrelated settings —
# author dates of batches, not moments in a history. Committer date first now.
WHEN = {"release": ("cdate",), "commit": ("cdate", "date"),
        "patchset": ("created",)}


def when_of(p):
    for f in WHEN.get(p["grid"], ()):
        v = ts(p.get(f))
        if v:
            return v
    return None


def main():
    grids = json.load(open(GRIDS))
    blobs = grids["blobs"]
    parsed = {b: parse_table(t) for b, t in blobs.items()}

    print("forecasts -- when did the release a value names actually happen?"
          "  (post-hoc)\n")

    # --- release dates ---------------------------------------------------
    # The .0 tag is the release. Patch releases of a series are not new minor
    # versions and cannot make a Changed value true.
    # CORRECTION, filed rather than repaired quietly (see adjudication.json).
    # The first version of this function probed `go1.<N>.0` only, and reported
    # 1.18, 1.19 and 1.20 as never released — which made `netedns0: Changed 19`
    # a standing forecast in 61 of 78 SHIPPED releases, a number absurd enough
    # to look at. Go tagged its initial releases `go1.19` and only adopted the
    # `.0` suffix at Go 1.21. Both forms are probed now, in that order.
    # This is the same fault class Session 69 filed as F-060 against its own
    # instrument — a tag-name assumption mistaken for a fact about a project —
    # arrived at independently one night later.
    dates, tagname = {}, {}
    for n in range(18, 34):
        dates[n] = None
        for tag in (f"go1.{n}.0", f"go1.{n}"):
            url = (GERRIT + "/projects/go/tags/"
                   + urllib.parse.quote("refs/tags/" + tag, safe=""))
            try:
                d = gerrit(url, f"tag date for {tag}")
            except Exception:                # noqa: BLE001 - 404 = no such tag
                continue
            dates[n], tagname[n] = d["created"], tag
            break
    have = {k: v for k, v in dates.items() if v}
    print("  release dates:")
    for k in sorted(have):
        print(f"    1.{k}: {have[k][:10]}  ({tagname[k]})")
    unreleased = sorted(k for k, v in dates.items() if not v)
    print(f"  not released as of tonight: {unreleased}")

    def released_by(minor, when):
        """Had go1.<minor>.0 been tagged at datetime `when`?"""
        d = dates.get(minor)
        if not d:
            return False
        return ts(d) <= when

    # --- every state, both grids ----------------------------------------
    out = {"note": "POST-HOC. Not predicted, not scored.",
           "release_dates": dates, "release_tag_used": tagname, "grids": {}}

    for grid in ("release", "patchset", "commit"):
        pts = [p for p in grids["points"] if p["grid"] == grid]
        rows, states_with = [], 0
        for p in pts:
            when = when_of(p)
            if when is None:
                continue
            tab = parsed.get(p["blob"])
            if not tab:
                continue
            fc = []
            for info in tab["All"]:
                ch = info.get("Changed", 0)
                if isinstance(ch, int) and ch != 0 and not released_by(ch, when):
                    fc.append({"name": info.get("Name"), "changed": ch})
            if fc:
                states_with += 1
                rows.append({"point": p.get("point"), "grid": grid,
                             "change": p.get("change"), "ps": p.get("patchset"),
                             "tag": p.get("point"),
                             "when": when_of(p).strftime("%Y-%m-%dT%H:%M:%SZ"),
                             "forecasts": fc})
        out["grids"][grid] = {
            "points_with_a_date": sum(1 for p in pts if when_of(p)),
            "points": len(pts),
            "states_carrying_a_forecast": states_with,
            "rows": rows,
        }
        print(f"\n  {grid:9s}: {states_with} of {len(pts)} states carried at "
              f"least one forecast")
        seen = {}
        for r in rows:
            for f in r["forecasts"]:
                seen.setdefault((f["name"], f["changed"]), 0)
                seen[(f["name"], f["changed"])] += 1
        for (nm, ch), c in sorted(seen.items(), key=lambda kv: -kv[1])[:12]:
            print(f"      {nm}: Changed {ch}  in {c} states")

    # --- how far ahead does a forecast look? -----------------------------
    # A forecast is ordinary if it names the release the branch is heading to:
    # during the 1.24 cycle, master carries Changed: 24, false until the tag and
    # true forever after. Horizon 0. The interesting case is a value that will
    # STILL be false when the branch it sits on ships.
    def target_at(when):
        rel = [n for n, d in dates.items() if d and ts(d) <= when]
        return (max(rel) + 1) if rel else None

    horizon = {}
    hrows = []
    for grid in ("patchset", "commit"):
        for r in out["grids"][grid]["rows"]:
            when = ts(r["when"])
            t = target_at(when)
            if t is None:
                continue
            for f in r["forecasts"]:
                h = f["changed"] - t
                horizon[h] = horizon.get(h, 0) + 1
                if h > 0:
                    hrows.append({"grid": grid, "point": r["point"],
                                  "change": r.get("change"), "ps": r.get("ps"),
                                  "when": r["when"], "name": f["name"],
                                  "changed": f["changed"], "target": t,
                                  "horizon": h})
    out["horizon_histogram"] = {str(k): v for k, v in sorted(horizon.items())}
    out["horizon_above_zero"] = hrows
    print("\n  forecast horizon (Changed minus the release the branch is "
          "heading to), patchset + commit states:")
    for h in sorted(horizon):
        print(f"    horizon {h:+d}: {horizon[h]} entry-states")
    print(f"  entry-states looking PAST the release they sit on: {len(hrows)}"
          f" · names: {sorted({r['name'] for r in hrows})}")

    # --- the value standing in master tonight ----------------------------
    url = (GERRIT + "/projects/go/branches/master/files/"
           + urllib.parse.quote("src/internal/godebugs/table.go", safe="")
           + "/content")
    st, raw = get(url)
    NEW.append({"url": url, "http_status": st, "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "fetched": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "what": "master's table.go tonight", "committed": False})
    import base64
    master = base64.b64decode(raw).decode()
    mt = parse_table(master)
    today = dt.datetime.utcnow()
    live = [{"name": i.get("Name"), "changed": i.get("Changed")}
            for i in mt["All"]
            if isinstance(i.get("Changed", 0), int) and i.get("Changed", 0)
            and not released_by(i["Changed"], today)]
    out["master_tonight"] = {"entries": len(mt["All"]), "forecasts": live,
                             "all": [{"name": i.get("Name"),
                                      "changed": i.get("Changed", 0)}
                                     for i in mt["All"]],
                             "sha256": hashlib.sha256(master.encode()).hexdigest()}
    print(f"\n  master tonight: {len(mt['All'])} entries, "
          f"{len(live)} carrying a value whose release does not exist: {live}")

    with open(os.path.join(HERE, "forecasts.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)

    mp = os.path.join(HERE, "sources", "MANIFEST.json")
    man = json.load(open(mp))
    man["entries"].extend(NEW)
    with open(mp, "w") as f:
        json.dump(man, f, indent=1)
    print(f"\n  wrote forecasts.json; {len(NEW)} entries appended to MANIFEST")


if __name__ == "__main__":
    main()
