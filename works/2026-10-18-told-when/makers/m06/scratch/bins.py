import json
o=json.load(open('occ.json'))['occ'];W=300
core=[[0]*W for _ in range(18)]
for l in range(18):
  row=[v>90 for v in o[l]];x=0
  while x<W:
    if row[x]:
      s=x
      while x<W and row[x]: x+=1
      e=x-1;L=e-s+1
      if L>=3:
        for c in range(s+1,e): core[l][c]=1
      else: core[l][s]=1
    else: x+=1
hpp=1464/W
grid=[[[0]*5 for _ in range(18)] for _ in range(61)]
for l in range(18):
  for x in range(W):
    if core[l][x]:
      h=hpp*(x+0.5);d=min(60,int(h//24));b=int((h%24)//4.8)
      grid[d][l][b]=1
json.dump(grid,open('grid.json','w'))
from collections import Counter
peak=Counter();trough=Counter()
for d in range(61):
  ls=[l for l in range(18) if any(grid[d][l])]
  if not ls: print(d,'empty');continue
  hi=min(ls);lo=max(ls)
  peak.update(b for b in range(5) if grid[d][hi][b]); trough.update(b for b in range(5) if grid[d][lo][b])
  print(d,'levels',hi,'-',lo,' '.join(''.join('#' if grid[d][l][b] else '.' for b in range(5)) for l in range(18)))
print('high-value bins',peak,'low-value bins',trough)
