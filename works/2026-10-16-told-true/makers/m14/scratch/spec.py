import json, math
c=json.load(open('cent.json'))  # x=2..297
hpp=1463/295.0
t=[(i+2-2.5)*hpp for i in range(len(c))]
def pw(P):
  a=sum(v*math.cos(2*math.pi*tt/P) for v,tt in zip(c,t)); b=sum(v*math.sin(2*math.pi*tt/P) for v,tt in zip(c,t))
  return (a*a+b*b)/len(c), math.atan2(b,a)
for name,P in [('M2',12.42),('S2',12.0),('N2',12.66),('K1',23.93),('S1',24.0),('O1',25.82),('Q1',26.87),('P1',24.07),('M4',6.21)]:
  print(name,P,'%.1f'%pw(P)[0])
print('scan 20-30h:')
P=20.0
while P<30.5:
  print('%.2f %.0f'%(P,pw(P)[0])); P+=0.25
print('scan 10-14h:')
P=10.0
while P<14.6:
  print('%.2f %.0f'%(P,pw(P)[0])); P+=0.2
# noise floor
import random
vals=[pw(P)[0] for P in [x*0.37+30 for x in range(200)]]
print('median power 30-100h', sorted(vals)[100])
