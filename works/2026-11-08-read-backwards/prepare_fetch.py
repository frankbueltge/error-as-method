"""Fetch English Wikipedia user pageviews, October 2026, for elements 1-56 (Wikimedia REST API, CC0)."""
import json, subprocess, urllib.parse, time, hashlib
EL = ["Hydrogen","Helium","Lithium","Beryllium","Boron","Carbon","Nitrogen","Oxygen","Fluorine","Neon",
"Sodium","Magnesium","Aluminium","Silicon","Phosphorus","Sulfur","Chlorine","Argon","Potassium","Calcium",
"Scandium","Titanium","Vanadium","Chromium","Manganese","Iron","Cobalt","Nickel","Copper","Zinc",
"Gallium","Germanium","Arsenic","Selenium","Bromine","Krypton","Rubidium","Strontium","Yttrium","Zirconium",
"Niobium","Molybdenum","Technetium","Ruthenium","Rhodium","Palladium","Silver","Cadmium","Indium","Tin",
"Antimony","Tellurium","Iodine","Xenon","Caesium","Barium"]
BASE = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{}/monthly/2026100100/2026103100"
out, raw = [], {}
import os
os.makedirs("sources/cache", exist_ok=True)
for z, t in enumerate(EL, 1):
    url = BASE.format(urllib.parse.quote(t))
    cp = "sources/cache/" + t + ".json"
    if os.path.exists(cp):
        raw[t] = json.load(open(cp)); out.append({"z": z, "element": t, "views": raw[t]["items"][0]["views"], "url": url}); continue
    for attempt in range(20):  # the API rate-limits; obey a pause and retry
        r = subprocess.run(["curl", "-sS", "-f", "-A", "error-as-method-research/1.0 (https://github.com/frankbueltge/error-as-method)", url],
                           capture_output=True)
        if r.returncode == 0:
            break
        print("429/err", t, attempt, r.stderr.decode()[:80], flush=True); time.sleep(40)
    else:
        raise SystemExit("gave up on " + t)
    body = r.stdout
    raw[t] = json.loads(body)
    open(cp, "wb").write(body)
    print("ok", z, t, flush=True)
    items = raw[t]["items"]
    assert len(items) == 1 and items[0]["timestamp"] == "2026100100", t
    out.append({"z": z, "element": t, "views": items[0]["views"], "url": url})
    time.sleep(6)
json.dump(out, open("sources/pageviews-2026-10.json", "w"), indent=1)
json.dump(raw, open("sources/api-responses.json", "w"), indent=1)
print(hashlib.sha256(open("sources/api-responses.json","rb").read()).hexdigest())
for r in out: print(r["z"], r["element"], r["views"])
