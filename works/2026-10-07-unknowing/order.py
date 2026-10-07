"""order.py -> the reading orders of the two sequential readers (seed 111)."""
import random
r = random.Random(111)
for s in ('S1', 'S2'):
    o = ['T1', 'T2', 'T3', 'T4']; r.shuffle(o); print(s, ' '.join(o))
