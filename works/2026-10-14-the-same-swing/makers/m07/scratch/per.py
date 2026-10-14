import math
exec(open('cols.py').read().split("print(' '.join('%d'%")[0])
sm=[sum(mean[max(0,i-7):i+8])/len(mean[max(0,i-7):i+8]) for i in range(W)]
r=[mean[i]-sm[i] for i in range(W)]
best=[]
for k in range(400,560):
  P=k/100
  c=sum(r[i]*math.cos(2*math.pi*i/P) for i in range(W)); s=sum(r[i]*math.sin(2*math.pi*i/P) for i in range(W))
  best.append((c*c+s*s,P))
best.sort(reverse=True); print(best[:5])
for P,lab in [(4.92,'24h'),(5.09,'24.84h'),(2.54,'12.42h')]:
  c=sum(r[i]*math.cos(2*math.pi*i/P) for i in range(W)); s=sum(r[i]*math.sin(2*math.pi*i/P) for i in range(W)); print(lab, round(c*c+s*s))
for P in [2.3,2.43,2.46,2.5,2.6,34.4]:
  c=sum(r[i]*math.cos(2*math.pi*i/P) for i in range(W)); s=sum(r[i]*math.sin(2*math.pi*i/P) for i in range(W)); print(P, round(c*c+s*s))
