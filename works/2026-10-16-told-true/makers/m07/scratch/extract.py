from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s130/mk/m07/work/record.jpg').convert('L')
w,h=im.size; px=im.load()
cols=[]
for x in range(w):
    ink=[(y,(255-px[x,y])/255) for y in range(h) if px[x,y]<200]
    cols.append(ink)
# column weighted mean y
mean=[]
for c in cols:
    s=sum(a for _,a in c)
    mean.append(sum(y*a for y,a in c)/s if s>0 else None)
print('empty cols',sum(1 for m in mean if m is None))
vals=[m for m in mean if m is not None]
mu=sum(vals)/len(vals)
# fill
m2=[m if m is not None else mu for m in mean]
# detrend with moving avg 25
def ma(a,k):
    out=[]
    for i in range(len(a)):
        s=a[max(0,i-k):i+k+1]; out.append(sum(s)/len(s))
    return out
d=[a-b for a,b in zip(m2,ma(m2,12))]
for lag in range(2,40):
    n=len(d)-lag
    r=sum(d[i]*d[i+lag] for i in range(n))/n/(sum(x*x for x in d)/len(d))
    print(lag, round(r,3), '#'*int(max(0,r)*50))
json.dump([[ (y,round(a,3)) for y,a in c] for c in cols], open('cols.json','w'))
