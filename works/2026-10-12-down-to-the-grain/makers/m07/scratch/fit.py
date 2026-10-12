import json,math
d=json.load(open('pts2.json')); pts=d['pts']
def solve3(A,b):
  import copy
  M=[A[i]+[b[i]] for i in range(3)]
  for i in range(3):
    piv=max(range(i,3),key=lambda r:abs(M[r][i])); M[i],M[piv]=M[piv],M[i]
    for r in range(3):
      if r!=i:
        f=M[r][i]/M[i][i]
        for c in range(4): M[r][c]-=f*M[i][c]
  return [M[i][3]/M[i][i] for i in range(3)]
def fitwin(ps,p):
  A=[[0]*3 for _ in range(3)]; b=[0]*3
  for x,y,v in ps:
    f=[1,math.cos(2*math.pi*x/p),math.sin(2*math.pi*x/p)]
    for i in range(3):
      b[i]+=f[i]*y
      for j in range(3): A[i][j]+=f[i]*f[j]
  c=solve3(A,b)
  res=sum((y-(c[0]+c[1]*math.cos(2*math.pi*x/p)+c[2]*math.sin(2*math.pi*x/p)))**2 for x,y,v in ps)
  return c,res
def score(p,w=20):
  tot=0
  for s in range(0,300,w):
    ps=[q for q in pts if s<=q[0]<s+w and not (212<q[0]<226)]
    if len(ps)>5: tot+=fitwin(ps,p)[1]
  return tot
best=min((score(2.40+i*0.001),2.40+i*0.001) for i in range(200))
print('best p px',best)
p=best[1]
for s in range(0,300,10):
  ps=[q for q in pts if s<=q[0]<s+10]
  if len(ps)>5:
    c,r=fitwin(ps,p); amp=math.hypot(c[1],c[2]); ph=math.degrees(math.atan2(c[2],c[1]))
    print(s,len(ps),'mean %.1f amp %.1f phase %.0f rms %.1f'%(c[0],amp,ph,math.sqrt(r/len(ps))))
print('---global')
r=[(score(2.44+i*0.0005,w=300),2.44+i*0.0005) for i in range(200)]
r.sort(); print(r[:5])
p=r[0][1]
for s in range(0,300,20):
  ps=[q for q in pts if s<=q[0]<s+20]
  c,rr=fitwin(ps,p); print(s,'amp %.1f phase %.0f'%(math.hypot(c[1],c[2]),math.degrees(math.atan2(c[2],c[1]))))
