#!/usr/bin/env python3
"""The one client every query in this night goes through.

Written before the predictions were closed, because F-090 (register 031) says a public
endpoint's refusal is data about the night and not an exception to route around, and because
the first attempt at an interface test on this endpoint died on a reset connection rather than
on anything the endpoint said.

What it does, and why each part is here:

  * **cache-first.** Every distinct query is stored under a SHA-256 of its canonical URL in a
    cache directory *outside this repository* (the default is the session scratchpad). A
    resumed run re-asks for nothing that has been answered. This is F-090's rule.
  * **it counts what it is told.** HTTP 429 and 503 are waited out — the interval the endpoint
    names in `Retry-After` if it names one, otherwise an exponential backoff — and every wait
    is counted into the manifest. A reset connection is retried on the same schedule and
    counted separately, because a reset is a fact about the route and a 429 is a fact about
    the endpoint, and this night should not report one as the other.
  * **it records the bytes it read without committing them.** `sources/MANIFEST.json` gets URL,
    HTTP status, byte count and SHA-256 for every distinct query. Per the protocol's 2026-08-18
    amendment, the bytes themselves stay out of the repository; the hash is the warrant.

GBIF's API is open and requires no key. Its terms ask for reasonable use; this night's whole
budget is under two hundred count-only queries (`limit=0`), which return no records at all.
"""
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.gbif.org/v1/"
CACHE = os.environ.get(
    "NIGHT_CACHE",
    "/tmp/claude-0/-home-user/04ee80ac-8523-5458-8e2a-2f6101cfab61/scratchpad/gbif-cache",
)
UA = "error-as-method nightly research line (+https://frankbueltge.de/error-as-method)"
PAUSE = 0.35  # deliberate, not required by the endpoint: see the journal for the reason


class Client:
    def __init__(self, cache=CACHE, log=None):
        self.cache = cache
        os.makedirs(self.cache, exist_ok=True)
        self.manifest = {}
        self.waits = []          # every time the endpoint said stop
        self.resets = []         # every time the route dropped
        self.requests_made = 0
        self.cache_hits = 0
        self.log_path = log

    def _log(self, line):
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        text = f"{stamp}  {line}"
        print(text, flush=True)
        if self.log_path:
            with open(self.log_path, "a", encoding="utf-8") as fh:
                fh.write(text + "\n")

    def url(self, path, params):
        """Canonical URL: parameters in the order given, so the cache key is stable."""
        return BASE + path + "?" + urllib.parse.urlencode(params)

    def get(self, path, params):
        url = self.url(path, params)
        key = hashlib.sha256(url.encode("utf-8")).hexdigest()
        blob = os.path.join(self.cache, key + ".json")

        if os.path.exists(blob):
            with open(blob, "rb") as fh:
                raw = fh.read()
            self.cache_hits += 1
            self._note(url, 200, raw, cached=True)
            return json.loads(raw.decode("utf-8"))

        delay = 2.0
        for attempt in range(6):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=120) as resp:
                    raw = resp.read()
                    status = resp.status
                self.requests_made += 1
                with open(blob, "wb") as fh:
                    fh.write(raw)
                self._note(url, status, raw, cached=False)
                time.sleep(PAUSE)
                return json.loads(raw.decode("utf-8"))
            except urllib.error.HTTPError as err:
                if err.code in (429, 500, 502, 503, 504):
                    named = err.headers.get("Retry-After")
                    wait = float(named) if named and named.isdigit() else delay
                    self.waits.append({"url": url, "status": err.code, "retry_after_header": named, "waited_s": wait})
                    self._log(f"endpoint said {err.code}; waiting {wait:.0f}s  [{url[:110]}]")
                    time.sleep(wait)
                    delay = min(delay * 2, 60.0)
                    continue
                self._note(url, err.code, b"", cached=False)
                raise
            except (urllib.error.URLError, TimeoutError, ConnectionError) as err:
                self.resets.append({"url": url, "error": repr(err)[:200], "waited_s": delay})
                self._log(f"route dropped ({err}); waiting {delay:.0f}s  [{url[:110]}]")
                time.sleep(delay)
                delay = min(delay * 2, 60.0)
                continue
        raise RuntimeError(f"gave up after six attempts: {url}")

    def _note(self, url, status, raw, cached):
        self.manifest[url] = {
            "url": url,
            "http_status": status,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest() if raw else None,
            "served_from_cache_this_run": cached,
        }

    def manifest_json(self, what, why):
        return {
            "what": what,
            "why": why,
            "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "bytes_are_not_committed": (
                "Per PROTOCOL.md (architect, 2026-08-18): a source's bytes are committed only "
                "where the licence permits redistribution. GBIF's API responses are re-fetchable "
                "by anyone without a key; the SHA-256 below is the warrant, the cache is outside "
                "this repository."
            ),
            "requests_made": self.requests_made,
            "cache_hits": self.cache_hits,
            "throttled": len(self.waits),
            "throttle_events": self.waits,
            "connection_resets": len(self.resets),
            "reset_events": self.resets,
            "queries": sorted(self.manifest.values(), key=lambda q: q["url"]),
        }


def count(client, **params):
    """One count-only query. Returns the integer the endpoint reports and nothing else."""
    p = [("limit", "0")] + [(k, v) for k, v in params.items()]
    return client.get("occurrence/search", p)["count"]
