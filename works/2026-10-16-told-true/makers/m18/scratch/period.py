from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m18/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
x0,x1=2,297
m=[]
for x in range(x0,x1+1):
    ys=[(y,255-px[x,y]) for y in range(H) if px[x,y]<170]
    w=sum(v for _,v in ys) or 1
    m.append(sum(y*v for y,v in ys)/w if ys else None)
# fill
for i in range(len(m)):
    if m[i] is None: m[i]=m[i-1]
# detrend with running mean of 15
n=len(m)
d=[m[i]-sum(m[max(0,i-7):i+8])/len(m[max(0,i-7):i+8]) for i in range(n)]
for lag in range(2,30):
    s=sum(d[i]*d[i+lag] for i in range(n-lag))/(n-lag)
    s0=sum(v*v for v in d)/n
    print(lag, round(s/s0,3))
