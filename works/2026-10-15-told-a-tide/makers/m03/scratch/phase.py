import json,math
d=json.load(open('cols.json'));cols=d['cols']
x0,x1=2,296
# dark-weighted "depth" per column: sum of weight*(y - 35)+ for y below band
ser=[]
for x in range(x0,x1+1):
    ser.append(sum(w*max(0,y-42) for y,w in cols[x])/1000)
n=len(ser);m=sum(ser)/n
span=x1-x0+1
for hrs in [23.0,23.5,24.0,24.4,24.84,25.2,12.0,12.42]:
    P=span/(1464/hrs)
    w=2*math.pi/P
    c=sum((ser[i]-m)*math.cos(w*i) for i in range(n));s=sum((ser[i]-m)*math.sin(w*i) for i in range(n))
    print(hrs,round(P,3),round(math.hypot(c,s),1))
# phase in thirds of record using 24h
P=span/61;w=2*math.pi/P
for k in range(6):
    a=k*n//6;b=(k+1)*n//6
    c=sum((ser[i]-m)*math.cos(w*i) for i in range(a,b));s=sum((ser[i]-m)*math.sin(w*i) for i in range(a,b))
    ph=math.atan2(s,c)/(2*math.pi)*24 % 24
    print('seg',k,'amp',round(math.hypot(c,s),1),'phase h',round(ph,1))
