import json, math
d=json.load(open('peaks.json')); c=d['colmean']; W=len(c)
mu=sum(c)/W; 
# detrend with 15px moving avg
k=7; r=[c[i]-sum(c[max(0,i-k):i+k+1])/len(c[max(0,i-k):i+k+1]) for i in range(W)]
res=[]
for P10 in range(25,200):
  P=P10/10; f=2*math.pi/P
  a=sum(r[i]*math.cos(f*i) for i in range(W)); b=sum(r[i]*math.sin(f*i) for i in range(W))
  res.append((math.hypot(a,b),P))
for a,P in sorted(res)[-12:]: print(round(a,1),P, 'hours', round(P*1464/300,1))
print([round(x) for x in c])
