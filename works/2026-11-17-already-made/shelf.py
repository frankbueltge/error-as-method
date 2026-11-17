"""Shared instrument for *Already Made* (Session 179).

The shelf is the house's atlas of neighbouring works (https://frankbueltge.de/atlas/werke.json, CC0),
read from a local snapshot whose path is passed in; it is NOT copied into this repository.
Texts are embedded with BAAI/bge-small-en-v1.5 (MIT) through fastembed; cosine similarity on
unit vectors. Only the decisive-move sentence is embedded, for atlas works and proposals alike.
"""
import json, re, hashlib
import numpy as np

MODEL = "BAAI/bge-small-en-v1.5"
PRIZE = re.compile(r"prize|award|golden nica|honorary mention|winner|laureate", re.I)

def load_atlas(path):
    raw = open(path, "rb").read()
    entries = json.loads(raw)["entries"]
    return entries, hashlib.sha256(raw).hexdigest()

def embedder(cache):
    from fastembed import TextEmbedding
    m = TextEmbedding(MODEL, cache_dir=cache)
    def embed(texts):
        v = np.array(list(m.embed(list(texts))), dtype=np.float64)
        return v / np.linalg.norm(v, axis=1, keepdims=True)
    return embed

def mean_pairwise(V):
    S = V @ V.T
    n = len(V)
    return (S.sum() - n) / (n * (n - 1))

def parse_proposals(text):
    """Blocks start with 'TITLE:'; fields TITLE, MATERIAL, FORM, MOVE, (CHANGED, WHY)."""
    out = []
    for block in re.split(r"(?m)^(?=TITLE:)", text):
        if not block.startswith("TITLE:"):
            continue
        d = {}
        key = None
        for line in block.splitlines():
            m = re.match(r"^(TITLE|MATERIAL|FORM|MOVE|CHANGED|WHY):\s*(.*)$", line)
            if m:
                key = m.group(1).lower(); d[key] = m.group(2).strip()
            elif key and line.strip():
                d[key] += " " + line.strip()
        out.append(d)
    return out
