"""order.py -> the order in which the twelve fresh readers are run (seed 112)."""
import random
cells = [f'{k}-{t}{r}' for k in ('K0', 'K1', 'K2') for t in ('T1', 'T3') for r in 'ab']
random.Random(112).shuffle(cells)
print(' '.join(cells))
