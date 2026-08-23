#!/usr/bin/env python3
"""Build sources/MANIFEST.json.

Per the protocol amendment of 2026-08-18: commit a source's bytes only where its licence
permits redistribution. Every source here is a third-party documentation page or specification
whose redistribution terms this practice has not established, so NONE of the bytes are
committed. The manifest is the warrant instead: URL, HTTP status, byte count, SHA-256, what
the source is and what claim in the work it carries. A stranger re-fetches and compares.
"""
import hashlib
import json
import os
import subprocess
import sys

SOURCES = [
    ("https://www.php.net/manual/en/function.date-default-timezone-get.php",
     "PHP manual, date_default_timezone_get",
     "Gives PHP's complete precedence order for the default timezone -- "
     "date_default_timezone_set(), then the date.timezone ini option, then UTC. The TZ "
     "environment variable is not in the list. This is the page that acquits PHP of the "
     "largest block of divergences in the night."),
    ("https://www.php.net/manual/en/datetime.configuration.php",
     "PHP manual, date/time runtime configuration",
     "States the default value of date.timezone as \"UTC\". Read together with this "
     "machine's php.ini, where date.timezone is commented out, it establishes that the UTC "
     "reading is PHP's own default and not a setting of this environment."),
    ("https://tc39.es/ecma262/multipage/numbers-and-dates.html#sec-date-time-string-format",
     "ECMA-262, Date Time String Format and Date.parse",
     "\"When the UTC offset representation is absent, date-only forms are interpreted as a "
     "UTC time and date-time forms are interpreted as a local time.\" And: a non-conforming "
     "string \"may fall back to any implementation-specific heuristics\". The norm in the "
     "room specifies the divergence rather than forbidding it."),
    ("https://docs.python.org/3/library/datetime.html",
     "Python documentation, datetime",
     "\"Naive datetime instances are assumed to represent local time and this method relies "
     "on platform C functions to perform the conversion.\" (datetime.timestamp) And: "
     "\"The timestamp() method uses the fold attribute to disambiguate the times during a "
     "repeated interval.\""),
    ("https://peps.python.org/pep-0495/",
     "PEP 495, Local Time Disambiguation",
     "\"the information displayed on a local clock (or stored in a Python datetime "
     "instance) is insufficient to identify a particular moment in time.\" The language's "
     "own standards document stating that the string cannot carry the instant."),
    ("https://docs.ruby-lang.org/en/3.3/Time.html",
     "Ruby 3.3 documentation, class Time",
     "Time.parse \"attempts to parse it using a heuristic. This method does not function as "
     "a validator. If the input string does not match valid formats strictly, you may get a "
     "cryptic result.\" The page that acquits Ruby of discarding the offset in GMT+0200."),
    ("https://perldoc.perl.org/functions/localtime",
     "perldoc, localtime",
     "\"In scalar context, localtime returns the ctime(3) value\", e.g. "
     "\"Thu Oct 13 04:54:34 1994\" -- a form carrying no offset and no zone name. "
     "Establishes that Perl's default rendering is the documented one."),
    ("https://www.iana.org/time-zones",
     "IANA Time Zone Database",
     "The upstream of the tzdata this machine ships. The night's three-hour differences at "
     "1945-07-26 are Europe/Berlin's CEMT (UTC+3, 1945-05-24 to 1945-09-24), which zdump "
     "reports locally and which this database is the source of."),
]


def main():
    out = []
    for url, what, why in SOURCES:
        name = url.split("://", 1)[1].replace("/", "_").replace("#", "_")[:80]
        path = os.path.join(os.path.dirname(__file__) or ".", name)
        r = subprocess.run(["curl", "-sS", "-L", "-o", path, "-w", "%{http_code}",
                            "--max-time", "60", url], capture_output=True, text=True)
        status = r.stdout.strip()
        if not os.path.exists(path):
            out.append({"url": url, "http_status": status, "fetched": False,
                        "what": what, "why": why})
            continue
        data = open(path, "rb").read()
        out.append({
            "url": url,
            "http_status": status,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "what": what,
            "why_this_night_needed_it": why,
            "bytes_committed": False,
            "bytes_not_committed_because":
                "third-party documentation; redistribution terms not established by this "
                "practice. Protocol amendment of 2026-08-18.",
        })
        os.remove(path)          # read, hashed, not kept

    manifest = {
        "work": "2026-08-23-the-hour-that-is-not-there",
        "session": 68,
        "fetched": "2026-08-23",
        "rule": "Bytes are committed only where the licence permits redistribution. None here "
                "do, so none are. The hash is the warrant: re-fetch and compare.",
        "sources": out,
        "local_evidence_not_fetched": [
            {"what": "this machine's /etc/php/8.4/cli/php.ini",
             "finding": "date.timezone is present only as the commented line ';date.timezone ='"
                        " at line 966, so PHP's UTC is its own default, not this machine's "
                        "setting. Reproduce with: grep -n 'date.timezone' "
                        "/etc/php/8.4/cli/php.ini"},
            {"what": "zdump -v Europe/Berlin",
             "finding": "Thu May 24 00:00:00 1945 UT = Thu May 24 03:00:00 1945 CEMT "
                        "isdst=1 gmtoff=10800 ... Mon Sep 24 00:00:00 1945 UT = "
                        "Mon Sep 24 02:00:00 1945 CEST isdst=1 gmtoff=7200. The source of the "
                        "night's two three-hour differences."},
        ],
    }
    with open(os.path.join(os.path.dirname(__file__) or ".", "MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
    for s in out:
        print(f"{s.get('http_status'):>4}  {s.get('bytes', 0):>8}  "
              f"{s.get('sha256', '-')[:16]}  {s['url']}")


if __name__ == "__main__":
    sys.exit(main())
