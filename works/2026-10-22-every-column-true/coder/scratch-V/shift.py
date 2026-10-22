import sys,pickle
a,b=sys.argv[1],sys.argv[2];x0,x1=int(sys.argv[3]),int(sys.argv[4])
A=pickle.load(open('cache_%s.pkl'%a,'rb'));B=pickle.load(open('cache_%s.pkl'%b,'rb'))
bpp=A[2]
def ink(I,x,y):
  p=I[3][y][x*bpp:x*bpp+3]; return 1 if sum(p)<600 else 0
for band in range(40,770,60):
  best=None
  for dy in range(-8,9):
   for dx in range(-8,9):
    s=0
    for y in range(band,band+60):
      if not(0<=y+dy<800): continue
      for x in range(x0,x1):
        s+=ink(A,x,y)*ink(B,x+dx,y+dy)
    if best is None or s>best[0]: best=(s,dx,dy)
  print(band,best)
