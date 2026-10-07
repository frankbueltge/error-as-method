"""order.py: the blind coder's order of the 16 transitions (seed 114). Prints one id per line."""
import random
ids = [f'{L}-{k}' for L in ('P1', 'P2', 'B1', 'B2') for k in range(1, 5)]
r = random.Random(114); r.shuffle(ids)
masks = {i: f'T{n:02d}' for n, i in enumerate(ids, 1)}
if __name__ == '__main__':
    for i in ids: print(masks[i], i)
