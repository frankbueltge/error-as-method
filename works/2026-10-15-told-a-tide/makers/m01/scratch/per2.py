import math
rows=[l.split() for l in open('cols.txt')]
xs=[];sd=[];mn=[]
for r in rows:
    x=int(r[0])
    if 3<=x<=295: xs.append(x); sd.append(float(r[3])); mn.append(float(r[2]))
hpp=1464/295
def pw(v,Ph):
    P=Ph/hpp; m=sum(v)/len(v)
    c=sum((a-m)*math.cos(2*math.pi*x/P) for a,x in zip(v,xs)); s=sum((a-m)*math.sin(2*math.pi*x/P) for a,x in zip(v,xs))
    return round(c*c+s*s)
for Ph in [12.0,12.42,12.66,23.93,24.0,24.84,25.82,26.87,8,12*24,13.66*24,14.77*24,29.5*24, 6.21,18,30]:
    print(Ph, pw(sd,Ph), pw(mn,Ph))
