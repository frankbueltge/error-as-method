import json, sys
from tangram import place
for p in json.load(open(sys.argv[1])):
    g = place(p)
    print(p["piece"], [(round(x, 3), round(y, 3)) for x, y in list(g.exterior.coords)[:-1]])
