import json,math,random
d=json.load(open('gray.json'));g=d['g']
blobs=json.load(open('blobs.json'))
# ink mass using full neighbourhood (include faint AA pixels)
def mass(b):
  return sum(255-p[2] for p in b)
singles=[mass(b) for b in blobs if 6<=len(b)<=8]
singles.sort(); unit=singles[len(singles)//2]
print('unit',unit, singles[len(singles)//10], singles[9*len(singles)//10])
random.seed(1)
dots=[]
for b in blobs:
  m=mass(b); n=max(1,round(m/unit))
  pts=[(p[0]+.5,p[1]+.5,255-p[2]) for p in b]
  if n==1:
    W=sum(p[2] for p in pts); dots.append((sum(p[0]*p[2] for p in pts)/W,sum(p[1]*p[2] for p in pts)/W,1));continue
  # weighted kmeans
  srt=sorted(pts,key=lambda p:-p[2])
  C=[(p[0],p[1]) for p in random.sample(pts,n)]
  for it in range(30):
    acc=[[0,0,0] for _ in C]
    for p in pts:
      k=min(range(n),key=lambda i:(p[0]-C[i][0])**2+(p[1]-C[i][1])**2)
      acc[k][0]+=p[0]*p[2];acc[k][1]+=p[1]*p[2];acc[k][2]+=p[2]
    C=[(a[0]/a[2],a[1]/a[2]) if a[2] else C[i] for i,a in enumerate(acc)]
  for c in C: dots.append((c[0],c[1],n))
print('dots',len(dots))
# convert
def val(y): return 17000-(y-19.5)*2000/71.67
def day(x): return (x-79.5)/1000*5479
out=[(round(day(x),1),round(val(y))) for x,y,n in dots]
out.sort()
json.dump(out,open('dots.json','w'))
up=sum(1 for o in out if o[1]>10300); print('upper',up,'lower',len(out)-up, 'ratio',up/len(out))
gap=[o for o in out if 9700<o[1]<11300]; print('gap',len(gap))
for o in gap: print(o)
