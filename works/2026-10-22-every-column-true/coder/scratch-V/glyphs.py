import sys,pickle
n=sys.argv[1];X0,X1,Y0,Y1=map(int,sys.argv[2:6])
W,H,bpp,R=pickle.load(open('cache_%s.pkl'%n,'rb'))
bg=R[5][5*bpp:5*bpp+3]
ink=set()
for y in range(Y0,Y1):
  for x in range(X0,X1):
    p=R[y][x*bpp:x*bpp+3]
    if sum(abs(p[i]-bg[i]) for i in range(3))>60: ink.add((x,y))
# connected comps 8-neighb
seen=set();comps=[]
for p in ink:
  if p in seen: continue
  st=[p];seen.add(p);c=[]
  while st:
    q=st.pop();c.append(q)
    for dx in (-1,0,1):
      for dy in (-1,0,1):
        r=(q[0]+dx,q[1]+dy)
        if r in ink and r not in seen: seen.add(r);st.append(r)
  xs=[a for a,b in c];ys=[b for a,b in c]
  comps.append((min(xs),min(ys),max(xs),max(ys),len(c)))
comps.sort(key=lambda c:(c[1],c[0]))
pickle.dump(comps,open('comps_%s.pkl'%n,'wb'))
print(len(comps)); xs=[c[0] for c in comps]+[c[2] for c in comps]; ys=[c[1] for c in comps]+[c[3] for c in comps]
print(min(xs),max(xs),min(ys),max(ys))
