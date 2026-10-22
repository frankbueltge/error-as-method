import sys,pickle,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import png
cache={}
def get(n):
  if n not in cache:
    f='cache_%s.pkl'%n
    if os.path.exists(f): cache[n]=pickle.load(open(f,'rb'))
    else:
      cache[n]=png.read(n+'.png'); pickle.dump(cache[n],open(f,'wb'))
  return cache[n]
groups=[a.split(',') for a in sys.argv[1:]]
for g in groups:
  for i in range(len(g)):
    for j in range(i+1,len(g)):
      W,H,bpp,A=get(g[i]);_,_,_,B=get(g[j])
      cnt=0;minx=miny=10**9;maxx=maxy=-1
      for y in range(H):
        if A[y]!=B[y]:
          for x in range(W):
            if A[y][x*bpp:x*bpp+3]!=B[y][x*bpp:x*bpp+3]:
              cnt+=1;minx=min(minx,x);maxx=max(maxx,x);miny=min(miny,y);maxy=max(maxy,y)
      print(g[i],g[j],cnt,(minx,miny,maxx,maxy))
