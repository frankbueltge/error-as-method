from PIL import Image
import json
im=Image.open('/tmp/claude-0/s137/mk/m05/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
x0,x1=2,297; N=1464
cm={}
for x in range(x0,x1+1):
    sw=sy=0; ys=[]
    for y in range(H):
        w=max(0,200-p[x,y])
        sw+=w; sy+=w*y
        if p[x,y]<150: ys.append(y)
    cm[x]=(sy/sw if sw else None, min(ys) if ys else None, max(ys) if ys else None)
xs=[x for x in cm if cm[x][0] is not None]
def interp(xf, k):
    a=max([x for x in xs if x<=xf], default=xs[0]); b=min([x for x in xs if x>=xf], default=xs[-1])
    if a==b: return cm[a][k]
    t=(xf-a)/(b-a); return cm[a][k]*(1-t)+cm[b][k]*t
mean=[];top=[];bot=[]
for i in range(N):
    xf=x0-0.5+(i+0.5)*(x1+1-x0)/N
    mean.append(round((H-interp(xf,0))/H*100,1))
    top.append(round((H-interp(xf,1))/H*100,1)); bot.append(round((H-interp(xf,2))/H*100,1))
json.dump({'mean':mean,'top':top,'bot':bot},open('series2.json','w'))
s=[0]*24;c=[0]*24
for i,x in enumerate(mean): s[i%24]+=x;c[i%24]+=1
print([round(s[k]/c[k],1) for k in range(24)])
for d in [3,20,26,45]: print(d, mean[24*d:24*d+24])
