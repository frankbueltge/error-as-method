"""Fetch the 50 current US state flags from Wikimedia Commons, with licence metadata."""
import urllib.error, json, urllib.request, urllib.parse, hashlib, pathlib, time
STATES = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida",
"the State of Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
"Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire",
"New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
"Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington",
"West Virginia","Wisconsin","Wyoming"]
UA = {"User-Agent": "nightly-research-practice/1.0 (flag study)"}
out = pathlib.Path(__file__).parent / "people"; out.mkdir(exist_ok=True)
manifest = []
for s in STATES:
    title = f"File:Flag of {s}.svg"
    name = title[5:].replace(" ", "_")
    h = hashlib.md5(name.encode()).hexdigest()
    url = f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{urllib.parse.quote(name)}"
    f = out / f"{s.replace('the State of ','').lower().replace(' ', '-')}.svg"
    if f.exists():
        data = f.read_bytes()
    else:
        for attempt in range(6):
            try:
                data = urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read(); break
            except urllib.error.HTTPError as e:
                if e.code != 429: print("MISSING", title, e.code); data = None; break
                time.sleep(30 * (attempt + 1))
        time.sleep(6)
    if data is None: continue
    slug = s.split(" (")[0].replace("the State of ","").lower().replace(" ", "-")
    (out / f"{slug}.svg").write_bytes(data)
    manifest.append({"state": s.replace("the State of ",""), "file": f"people/{slug}.svg", "commons": title,
        "url": url, "fetched": time.strftime("%Y-%m-%d"),
        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
json.dump(manifest, open(out / "MANIFEST.json","w"), indent=1)
print(len(manifest)); 
