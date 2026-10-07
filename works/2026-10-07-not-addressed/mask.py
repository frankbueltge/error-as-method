"""mask.py -- copies shots/<maker>.png to coder/p01..p12.png in an order shuffled with seed 1150.
The key (maker -> picture) goes to coder/key.json, which the coder never sees."""
import json, os, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
makers = ["m%02d" % i for i in range(1, 13)]
order = makers[:]
random.Random(1150).shuffle(order)
os.makedirs(os.path.join(HERE, "coder", "pictures"), exist_ok=True)
key = {}
for i, m in enumerate(order, 1):
    pid = "p%02d" % i
    shutil.copy(os.path.join(HERE, "shots", m + ".png"), os.path.join(HERE, "coder", "pictures", pid + ".png"))
    key[pid] = m
json.dump(key, open(os.path.join(HERE, "coder", "key.json"), "w"), indent=1)
print(key)
