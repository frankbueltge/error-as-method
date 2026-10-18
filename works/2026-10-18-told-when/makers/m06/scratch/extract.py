import json
d=open('rec.raw','rb').read();W,H=300,90
dk=[[255-d[y*W+x] for x in range(W)] for y in range(H)]
prof=[sum(r) for r in dk]
# find level bands: groups of rows with significant darkness
rows=[y for y in range(H) if prof[y]>300]
bands=[];cur=[]
for y in rows:
  if cur and y-cur[-1]>1: bands.append(cur);cur=[]
  cur.append(y)
bands.append(cur)
cent=[sum(y*prof[y] for y in b)/sum(prof[y] for y in b) for b in bands]
print('bands',[(b,round(c,1)) for b,c in zip(bands,cent)])
print('gaps',[round(cent[i+1]-cent[i],2) for i in range(len(cent)-1)])
# occupancy per level per column: max darkness over band rows +-1
occ=[]
for c in cent:
  yc=round(c)
  occ.append([max(dk[y][x] for y in range(max(0,yc-1),min(H,yc+2))) for x in range(W)])
# runs
runs=[]
for li,row in enumerate(occ):
  x=0
  while x<W:
    if row[x]>110:
      s=x
      while x<W and row[x]>110: x+=1
      runs.append((li,s,x-1))
    else: x+=1
print(len(runs),'runs')
json.dump({'cent':cent,'occ':occ,'runs':runs},open('occ.json','w'))
lv=len(cent)
for li in range(lv):
  print('%2d '%li+''.join('#' if v>110 else ' ' for v in occ[li]))
