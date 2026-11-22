"""Read the licence section of each people's flag's Commons file page (action=raw) into people/MANIFEST.json."""
import json, re, time, urllib.request, urllib.parse
m = json.load(open("people/MANIFEST.json"))
for e in m:
    if e.get("licence_templates"): continue
    t = e["commons"].replace(" ", "_")
    u = "https://commons.wikimedia.org/w/index.php?" + urllib.parse.urlencode({"title": t, "action": "raw"})
    for a in range(5):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "nightly-research-practice/1.0"})).read().decode(); break
        except Exception as ex:
            time.sleep(20 * (a + 1)); raw = None
    if raw is None: continue
    sec = raw.split("license-header}}==")[-1] if "license-header" in raw else raw
    sec = sec.split("[[Category")[0]
    e["licence_templates"] = sorted(set(re.findall(r"\{\{\s*([A-Za-z][^|}\n]*)", sec)))
    time.sleep(3)
json.dump(m, open("people/MANIFEST.json", "w"), indent=1)
for e in m: print(e["state"], e.get("licence_templates"))
