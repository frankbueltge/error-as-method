from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s130/mk/m04/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
cols=[]
for x in range(W):
    ws=[(y,max(0,230-p[x,y])/230) for y in range(H)]
    ws=[(y,w) for y,w in ws if w>0.15]
    cols.append(ws)
mean=[]; top=[]; bot=[]; ink=[]
for ws in cols:
    s=sum(w for _,w in ws); ink.append(s)
    mean.append(sum(y*w for y,w in ws)/s if s else float('nan'))
    top.append(min(y for y,_ in ws) if ws else None); bot.append(max(y for y,_ in ws) if ws else None)
print('ink min/max',min(ink),max(ink))
# periodogram of mean
m=[v for v in mean]; mu=sum(m)/len(m); m=[v-mu for v in m]
res=[]
for k in range(1,150):
    re=sum(m[i]*math.cos(2*math.pi*k*i/W) for i in range(W)); im_=sum(m[i]*math.sin(2*math.pi*k*i/W) for i in range(W))
    res.append((re*re+im_*im_,k,W/k))
res.sort(reverse=True)
for r in res[:15]: print('%.0f k=%d period=%.2fpx = %.2f days'%(r[0],r[1],r[2],r[2]/(300/61)))
# smoothed series of mean, top, bot every 5 px
for i in range(0,W,5):
    seg=range(i,min(W,i+5))
    print(i, round(sum(mean[j] for j in seg)/len(seg),1), min(top[j] for j in seg), max(bot[j] for j in seg))
json.dump({'mean':mean,'top':top,'bot':bot},open('cols.json','w'))
