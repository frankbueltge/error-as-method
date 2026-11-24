"""Draw the people's pages from the Geocities Gallery (geocities.restorativland.org).

Seeded draw: 24 suburbs from the gallery's index (Tokyo excluded: the makers write in English),
every listed page in those suburbs whose 'Last modified' falls in 1996-2000, then 100 pages to
score and 20 further pages for the sheet one arm of makers reads. The pages' HTML is saved
outside the repository (argument 1); only paths, dates and SHA-256 hashes are committed.

usage: python3 -I sample.py OUTDIR MANIFEST.json
"""
import hashlib, json, random, re, sys, time, urllib.request

BASE = "https://geocities.restorativland.org/"
SEED = 186
out, manifest_path = sys.argv[1], sys.argv[2]


def get(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception as e:  # network hiccup: retry with backoff
            err = e
            time.sleep(2 * (attempt + 1))
    raise err


root = get(BASE).decode("utf-8", "replace")
suburbs = sorted(set(re.findall(r'href="([A-Za-z0-9]+/[A-Za-z0-9]+)"', root)))
suburbs = [s for s in suburbs if not s.startswith("Tokyo/")]
rng = random.Random(SEED)
drawn = sorted(rng.sample(suburbs, 24))

pool = []
for s in drawn:
    html = get(BASE + s + "/").decode("utf-8", "replace")
    for path, date in re.findall(
        r'www\.geocities\.com/([^ <]+) <br>Last modified: (\d{4}-\d{2}-\d{2})', html
    ):
        if "1996-01-01" <= date <= "2000-12-31":
            pool.append((path, date))
pool = sorted(set(pool))
pick = rng.sample(pool, 120)
scored, sheet = pick[:100], pick[100:]

rows = []
for role, items in (("scored", scored), ("sheet", sheet)):
    for path, date in items:
        url = BASE + path + "/"
        try:
            body = get(url)
        except Exception as e:
            rows.append({"role": role, "path": path, "last_modified": date, "error": str(e)})
            continue
        h = hashlib.sha256(body).hexdigest()
        with open(f"{out}/{h[:16]}.html", "wb") as f:
            f.write(body)
        rows.append({"role": role, "path": path, "last_modified": date, "url": url,
                     "sha256": h, "bytes": len(body)})
        time.sleep(0.3)

json.dump({"source": BASE, "seed": SEED, "suburbs_total": len(suburbs), "suburbs_drawn": drawn,
           "pool_1996_2000": len(pool), "pages": rows}, open(manifest_path, "w"), indent=1)
print(len(suburbs), "suburbs;", len(pool), "pages in pool;",
      sum(1 for r in rows if "sha256" in r), "fetched;", sum(1 for r in rows if "error" in r), "failed")
