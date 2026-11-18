"""Draw twelve objects from The Met's Open Access collection, one per department, by a fixed seed.

Rule (fixed before any draw): for each of twelve departments, list its object ids, shuffle them with
random.Random(SEED + department_id), and take the first object that is public domain, has a primary
image, is not marked a highlight, and has a non-empty objectDate and objectName. At most 60 records
are tried per department. The record is saved whole (objects/<id>.json); the small image is saved
beside it (objects/<id>.jpg). The makers see only the image. The record is withheld until round 2.

Source: The Metropolitan Museum of Art Collection API, https://metmuseum.github.io/ ;
Open Access data and public-domain images under CC0.
"""
import json, random, sys, time, urllib.request, hashlib, pathlib

SEED = 20261118
DEPTS = [1, 3, 4, 5, 6, 9, 10, 12, 13, 14, 17, 18]
API = "https://collectionapi.metmuseum.org/public/collection/v1"
OUT = pathlib.Path(__file__).parent / "objects"


def get(url, binary=False):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "research-script/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            return data if binary else json.loads(data)
        except Exception as e:  # network hiccups are retried, then raised
            last = e
            time.sleep(2 * (attempt + 1))
    raise last


def main():
    OUT.mkdir(exist_ok=True)
    drawn = []
    for d in DEPTS:
        ids = get(f"{API}/objects?departmentIds={d}")["objectIDs"]
        ids = sorted(ids)
        random.Random(SEED + d).shuffle(ids)
        tried = 0
        for oid in ids[:60]:
            tried += 1
            try:
                rec = get(f"{API}/objects/{oid}")
            except Exception:
                continue
            if not (rec.get("isPublicDomain") and rec.get("primaryImageSmall")
                    and not rec.get("isHighlight") and rec.get("objectDate") and rec.get("objectName")):
                continue
            img = get(rec["primaryImageSmall"], binary=True)
            (OUT / f"{oid}.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False))
            (OUT / f"{oid}.jpg").write_bytes(img)
            drawn.append({"department": d, "objectID": oid, "tried": tried,
                          "sha256_image": hashlib.sha256(img).hexdigest()})
            print(d, oid, rec["objectName"], "|", rec["title"][:60], "|", rec["objectDate"], file=sys.stderr)
            break
        else:
            drawn.append({"department": d, "objectID": None, "tried": tried})
    (OUT / "drawn.json").write_text(json.dumps({"seed": SEED, "drawn": drawn}, indent=1))


if __name__ == "__main__":
    main()
