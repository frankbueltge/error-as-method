from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s130/mk/m02/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
cols=[]
for x in range(W):
    ink=[(y,(255-p[x,y])/255) for y in range(H)]
    ink=[(y,w) for y,w in ink if w>0.25]
    if ink:
        tot=sum(w for _,w in ink); mean=sum(y*w for y,w in ink)/tot
        cols.append((x,min(y for y,_ in ink),max(y for y,_ in ink),mean,tot))
    else: cols.append((x,None,None,None,0))
json.dump(cols,open('cols.json','w'))
# overall bounds
ys=[c for c in cols if c[1] is not None]
print('cols with ink',len(ys),'first x',ys[0][0],'last x',ys[-1][0])
print('ytop',min(c[1] for c in ys),'ybot',max(c[2] for c in ys))
for c in cols[:20]+cols[-10:]: print(c)
# periodicity of mean y via autocorrelation
m=[c[3] for c in cols if c[3] is not None]
mu=sum(m)/len(m); d=[v-mu for v in m]
for lag in range(1,30):
    r=sum(d[i]*d[i+lag] for i in range(len(d)-lag))/sum(v*v for v in d)
    print(lag, round(r,3))
