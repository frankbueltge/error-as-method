"""The draw. Reads the commit that added PREDICTIONS.md, turns its first eight hex digits into an
index into the GovData catalogue (sorted by name), and walks forward until a dataset is admitted.
Writes draw-log.json. Admission rules are those in PREDICTIONS.md; rule (b) and (c) need a human
reading, so the script stops at each candidate that passes (a) and asks for a verdict on stdin."""
import json, subprocess, sys, urllib.request, urllib.parse, time
API = "https://www.govdata.de/ckan/api/3/action/package_search"
FORMATS = {"CSV", "JSON", "GEOJSON", "XLSX", "XLS", "TXT", "XML"}
def get(params):
    # run 2: retries added after run 1 died on a connection reset at index 153,986 (F-171)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(API + "?" + urllib.parse.urlencode(params), timeout=60) as r:
                return json.load(r)["result"]
        except Exception:
            time.sleep(2 ** attempt)
    raise RuntimeError("catalogue unreachable after 6 attempts")
def probe(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research; draw.py)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            n, chunk = 0, r.read(1 << 20)
            while chunk:
                n += len(chunk)
                if n > 50 << 20: return r.status, n, "over 50 MB"
                chunk = r.read(1 << 20)
            return r.status, n, None
    except Exception as e:
        return None, 0, repr(e)[:200]
commit = subprocess.run(["git", "log", "--format=%H", "--diff-filter=A", "--", "PREDICTIONS.md"],
                        capture_output=True, text=True, check=True).stdout.split()[-1]
count = get({"rows": 0})["count"]
index = int(commit[:8], 16) % count
log = {"commit": commit, "count_at_draw": count, "first_index": index, "sort": "name asc",
       "drawn_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "candidates": []}
i = index
while True:
    pkg = get({"rows": 1, "start": i, "sort": "name asc"})["results"][0]
    # run 3: the catalogue writes formats as EU vocabulary URIs (.../file-type/CSV); runs 1 and 2
    # compared the whole URI with "CSV" and refused datasets the rule admits (F-172)
    fmt = lambda r: (r.get("format") or "").strip().rstrip("/").rsplit("/", 1)[-1].upper().lstrip(".")
    res = [r for r in pkg.get("resources", []) if fmt(r) in FORMATS]
    cand = {"index": i, "name": pkg["name"], "title": pkg.get("title"),
            "organization": (pkg.get("organization") or {}).get("name"),
            "license": pkg.get("license_id"), "formats": [r.get("format") for r in pkg.get("resources", [])]}
    if not res:
        cand["verdict"] = "refused (a): no resource in an admitted format"
    else:
        st, n, err = probe(res[0]["url"])
        cand.update(resource_url=res[0]["url"], status=st, bytes=n)
        if st != 200 or err:
            cand["verdict"] = f"refused (a): resource not fetched ({err or st})"
        else:
            print(json.dumps(cand, ensure_ascii=False, indent=1))
            v = input("rules (b) and (c) -- admit? [y / reason for refusal]: ").strip()
            cand["verdict"] = "admitted" if v == "y" else f"refused: {v}"
    log["candidates"].append(cand); print(cand["index"], cand["verdict"], file=sys.stderr)
    json.dump(log, open("draw-log.json", "w"), ensure_ascii=False, indent=1)  # run 2: saved per candidate (F-171)
    time.sleep(0.2)
    if cand["verdict"] == "admitted": break
    i = (i + 1) % count
json.dump(log, open("draw-log.json", "w"), ensure_ascii=False, indent=1)
