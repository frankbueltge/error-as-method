import json, random, collections
codes = {int(k): v for k, v in json.load(open('codes.json')).items()}
K = "PXSDWTBOG"
share = {k: sum(1 for v in codes.values() if v == k) / 160 for k in K}
def tvd(d):
    c = collections.Counter(codes[n] for n in d)
    return 0.5 * sum(abs(c[k] / len(d) - share[k]) for k in K)
rng = random.Random(1890)
sims = []
for _ in range(20000):
    d = rng.sample(range(1, 161), 12); sims.append((tvd(d), d))
sims.sort(key=lambda x: x[0])
qs = [0.05, 0.25, 0.45, 0.65, 0.85, 0.99]
draws = []
for i, q in enumerate(qs):
    t, d = sims[int(q * len(sims))]
    draws.append({"draw": i + 1, "quantile": q, "tvd": round(t, 4), "items": d,
                  "kinds": "".join(codes[n] for n in d)})
tv = [s[0] for s in sims]
json.dump({"share": share, "draws": draws, "tvd_null_median": tv[len(tv)//2],
           "tvd_null_p05": tv[int(.05*len(tv))], "tvd_null_p95": tv[int(.95*len(tv))]}, open('draws.json', 'w'), indent=1)
for d in draws: print(d)
print(tv[len(tv)//2])
