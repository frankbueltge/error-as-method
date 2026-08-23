#!/usr/bin/env python3
"""CPython probe. Reads a job on stdin, answers on stdout, in its own words.

Rendering:
  default -- str(datetime.fromtimestamp(e)). This is what Python prints for a local datetime:
             datetime.__str__ is documented as equivalent to isoformat(sep=' ').
  iso     -- datetime.fromtimestamp(e, timezone.utc).astimezone().isoformat(): aware, with offset.
Parsing:
  datetime.fromisoformat(s), documented as the inverse of isoformat. A NAIVE result is converted
  with .timestamp(), which Python documents as assuming local time. That assumption is Python's,
  not this harness's, and it is the whole subject of the night.
Numbers:
  float(s) -- Python has no implicit string-to-number coercion; float() is its only conversion.
"""
import sys
import json
import datetime as dt


def render(e):
    try:
        d = dt.datetime.fromtimestamp(e)
        default = str(d)
    except (OSError, OverflowError, ValueError) as exc:
        default = None
        default_err = f"{type(exc).__name__}: {exc}"
    else:
        default_err = None
    try:
        a = dt.datetime.fromtimestamp(e, dt.timezone.utc).astimezone()
        iso = a.isoformat()
    except (OSError, OverflowError, ValueError) as exc:
        iso = None
        iso_err = f"{type(exc).__name__}: {exc}"
    else:
        iso_err = None
    return {"default": default, "default_error": default_err,
            "iso": iso, "iso_error": iso_err}


def parse(s):
    try:
        d = dt.datetime.fromisoformat(s)
    except (ValueError, TypeError) as exc:
        return {"status": "refused", "error": f"{type(exc).__name__}: {exc}"}
    naive = d.tzinfo is None
    try:
        epoch = d.timestamp()
    except (OSError, OverflowError, ValueError) as exc:
        return {"status": "refused", "error": f"{type(exc).__name__}: {exc}"}
    return {"status": "ok", "epoch": epoch, "naive": naive}


def numparse(s):
    out = {}
    try:
        out["strict"] = float(s)
    except (ValueError, TypeError) as exc:
        out["strict"] = None
        out["strict_error"] = type(exc).__name__
    out["lenient"] = None          # Python has no lenient coercion; recorded as absent, not as 0
    out["lenient_absent"] = True
    return out


def main():
    job = json.load(sys.stdin)
    out = {"runtime": "python", "version": sys.version.split()[0]}
    if "instants" in job:
        out["render"] = [render(e) for e in job["instants"]]
    if "strings" in job:
        out["parse"] = [parse(s) for s in job["strings"]]
    if "numbers" in job:
        out["numparse"] = [numparse(s) for s in job["numbers"]]
    json.dump(out, sys.stdout)


if __name__ == "__main__":
    main()
