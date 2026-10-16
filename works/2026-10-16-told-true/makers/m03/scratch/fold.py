from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s130/mk/m03/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
X0,X1=3.0,296.3
def t_of(x): return (x-X0)*1463/(X1-X0)
# refine period with corrected axis
S=[]
for x in range(2,298):
  ws=[(y,max(0,230-p[x,y])) for y in range(H)]; m=sum(w for _,w in ws)
  if m==0: continue
  c=sum(y*w for y,w in ws)/m
  dk=[y for y,w in ws if w>90]
  S.append((t_of(x),c,min(dk) if dk else c,max(dk) if dk else c,m))
mu=sum(s[1] for s in S)/len(S)
best=max(((sum((s[1]-mu)*math.cos(2*math.pi*s[0]/T) for s in S)**2+sum((s[1]-mu)*math.sin(2*math.pi*s[0]/T) for s in S)**2),T) for T in [x/100 for x in range(2300,2500)])
print('period h',best[1])
# fold: 24 bins, each column covers t..t+5h; assign its midpoint hour
for k,name in ((1,'centroid'),(2,'top'),(3,'bottom'),(4,'mass')):
  bins=[[] for _ in range(24)]
  for s in S: bins[int((s[0]+2.5)%24)].append(s[k])
  print(name,[round(sum(b)/len(b),1) for b in bins])
# daily: per day mean centroid, top (5th pct), bottom
