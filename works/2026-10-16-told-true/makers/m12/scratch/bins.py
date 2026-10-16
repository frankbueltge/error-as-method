from PIL import Image
import json
im=Image.open('/tmp/claude-0/s130/mk/m12/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
x0=2; ppd=296/61; ph=0.85
S=[(x,89-y,255-px[x,y]) for x in range(W) for y in range(H) if 255-px[x,y]>45]
bins={}
for x,v,d in S:
    t=(x+0.5-x0-ph)/ppd   # cycle coordinate
    k=int(t//1)+1          # bin 0 = partial first
    bins.setdefault(k,[]).append((round(t-(k-1),3),v,d))
ks=sorted(bins); print(ks[0],ks[-1],len(ks))
floors=[];tops=[]
for k in ks:
    b=sorted(bins[k],key=lambda s:s[1]); tot=sum(s[2] for s in b if s[2]>90); acc=0; f=None
    for s in b:
        if s[2]<=90: continue
        acc+=s[2]
        if acc>=0.08*tot: f=s[1]; break
    floors.append(f); tops.append(max(s[1] for s in b if s[2]>90))
print('floor',floors); print('top',tops)
print('excess',[t-f for t,f in zip(tops,floors)])
json.dump({'ppd':ppd,'ph':ph,'x0':x0,'S':[[x,v,d] for x,v,d in S]},open('samples.json','w'))
