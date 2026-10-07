"""mask.py: copies screenshots under masked names for the blind coder (transitions per order.py; single images M01-M20, seed 1140)."""
import shutil, os, random, json
from order import ids, masks
os.makedirs('coder/pairs', exist_ok=True); os.makedirs('coder/single', exist_ok=True)
for i in ids:
    L, k = i.split('-'); k = int(k)
    shutil.copy(f'shots/{L}-v{k-1}.png', f'coder/pairs/{masks[i]}-before.png')
    shutil.copy(f'shots/{L}-v{k}.png', f'coder/pairs/{masks[i]}-after.png')
singles = [f'{L}-v{k}' for L in ('P1', 'P2', 'B1', 'B2') for k in range(5)]
random.Random(1140).shuffle(singles)
smask = {s: f'M{n:02d}' for n, s in enumerate(singles, 1)}
for s, m in smask.items(): shutil.copy(f'shots/{s}.png', f'coder/single/{m}.png')
json.dump({'transitions': masks, 'singles': smask}, open('coder/KEY.json', 'w'), indent=1)
