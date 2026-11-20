import json, sys
from tangram import place
for p in json.load(open(sys.argv[1])):
    pts = list(place(p).exterior.coords)[:-1]
    print(p["piece"], " ".join(f"({x:.3f},{y:.3f})" for x, y in pts))
