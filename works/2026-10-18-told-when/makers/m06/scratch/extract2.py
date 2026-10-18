import json
d=open('rec.raw','rb').read();W,H=300,90
dk=[[255-d[y*W+x] for x in range(W)] for y in range(H)]
best=None
for s in [i/100 for i in range(400,700)]:
  for sp in [i/1000 for i in range(4500,4700,5)]:
    sc=0
    for k in range(18):
      c=s+sp*k
      for y in (int(c),int(c)+1):
        if y<H: sc+=sum(dk[y])
    if not best or sc>best[0]: best=(sc,s,sp)
print(best)
_,s,sp=best
cent=[s+sp*k for k in range(18)]
occ=[[max(dk[y][x] for y in (int(c)-0,int(c)+1)) for x in range(W)] for c in cent]
for li in range(18):
  print('%2d '%li+''.join('#' if v>120 else ('+' if v>60 else ' ') for v in occ[li]))
json.dump({'cent':cent,'occ':occ},open('occ.json','w'))
