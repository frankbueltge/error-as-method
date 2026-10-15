from PIL import Image
import math
im=Image.open('/tmp/claude-0/s128/mk/m07/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
hpc=1464/296
for P in (23.80,23.93,24.0,24.07):
  bins=[[] for _ in range(12)]
  for x in range(3,297):
    ys=[y for y in range(H) if px[x,y]<140]
    if not ys: continue
    t=(x-2)*hpc
    ph=(t%P)/P
    bins[int(ph*12)].append((H-min(ys), H-max(ys), len(ys)))
  print(P)
  for i,b in enumerate(bins):
    print(f" {i*2:2d}h top {sum(a for a,_,_ in b)/len(b):5.1f} bottom {sum(c for _,c,_ in b)/len(b):5.1f} n {len(b)}")
