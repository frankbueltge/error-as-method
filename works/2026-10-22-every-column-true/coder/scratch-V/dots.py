import sys,pickle,collections
for n in sys.argv[1:]:
  W,H,bpp,R=pickle.load(open('cache_%s.pkl'%n,'rb'))
  pts=[]
  for y in range(100,750):
    r=R[y]
    for x in range(100,1060):
      p=r[x*bpp:x*bpp+3]
      if p[0]>110 and p[0]<180 and p[1]<40 and p[2]<40: pts.append((x,y))
  # cluster
  cl=[]
  for x,y in pts:
    for c in cl:
      if abs(c[0]-x)<5 and abs(c[1]-y)<5: c[2].append((x,y));break
    else: cl.append([x,y,[(x,y)]])
  out=[(round(sum(p[0] for p in c[2])/len(c[2])),round(sum(p[1] for p in c[2])/len(c[2])),len(c[2])) for c in cl]
  print(n,sorted(out))
