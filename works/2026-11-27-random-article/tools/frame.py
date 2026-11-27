"""Seeded chance draw of English Wikipedia articles via the public datasets-server rows API
(wikimedia/wikipedia, config 20231101.en, 6,407,814 rows). Seed 189."""
import json, random, re, sys, time, urllib.request
N_ROWS = 6407814
out = sys.argv[1]; n = int(sys.argv[2])
rng = random.Random(189)
offs = rng.sample(range(N_ROWS), n)
def lead(text):
    para = text.strip().split("\n")[0].strip()
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"“(])', para)
    s = " ".join(sents[:2])
    return s[:420]
with open(out, "w") as f:
    for i, o in enumerate(offs):
        url = f"https://datasets-server.huggingface.co/rows?dataset=wikimedia/wikipedia&config=20231101.en&split=train&offset={o}&length=1"
        for attempt in range(6):
            try:
                with urllib.request.urlopen(url, timeout=60) as r: d = json.load(r); break
            except Exception as e:
                print("retry", o, e, file=sys.stderr); time.sleep(5 * (attempt + 1))
        row = d["rows"][0]["row"]
        text = row["text"]
        rec = {"n": i + 1, "row": o, "id": row["id"], "title": row["title"], "url": row["url"],
               "lead": lead(text), "words": len(text.split())}
        f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
        time.sleep(0.3)
print("ok")
