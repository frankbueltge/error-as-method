"""Build index.html from page.tpl.html, census.json and the readers' answers. Run from anywhere."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
census = json.load(open(os.path.join(HERE, "census.json")))["rows"]
readers = {}
for k in ("A", "B"):
    p = os.path.join(HERE, "readers", f"reader-{k}.json")
    if os.path.exists(p):
        readers[k] = {r["id"]: r["wrong"] for r in json.load(open(p))}
data = json.dumps({"rows": census, "readers": readers}, ensure_ascii=False).replace("</", "<\\/")
tpl = open(os.path.join(HERE, "page.tpl.html")).read()
open(os.path.join(HERE, "index.html"), "w").write(tpl.replace("__DATA__", data))
print("index.html", len(census), "rows,", len(readers), "readers")
