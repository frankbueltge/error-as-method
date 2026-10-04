"""Builds index.html from page.tpl.html, data.js and results.json (everything inline)."""
import json
data = open("data.js").read().split("=", 1)[1].strip().rstrip(";")
res = json.load(open("results.json"))
html = open("page.tpl.html").read().replace("/*DATA*/", data).replace("/*RESULTS*/", json.dumps(res, ensure_ascii=False))
open("index.html", "w").write(html); print("index.html", len(html), "bytes")
