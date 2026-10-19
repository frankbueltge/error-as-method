from PIL import Image
import json
im=Image.open('/tmp/claude-0/s137/mk/m14/work/record.jpg').convert('L')
W,H=im.size;px=im.load()
TH=200
pts=[]  # (x, y, mass) blobs per column
cols=[]
for x in range(W):
    ink=[max(0,TH-px[x,y]) for y in range(H)]
    blobs=[];cur=None
    for y in range(H):
        if ink[y]>15:
            if cur is None: cur=[0,0]
            cur[0]+=ink[y];cur[1]+=ink[y]*y
        elif cur is not None:
            blobs.append((cur[1]/cur[0],cur[0]));cur=None
    if cur: blobs.append((cur[1]/cur[0],cur[0]))
    cols.append(blobs)
# estimate mass per dot from tail region (one dot per blob roughly)
masses=[b[1] for c in cols[215:245] for b in c]
masses.sort();unit=masses[len(masses)//2]
print('unit',unit)
seq=[]
prev=None
for x,c in enumerate(cols):
    if not c: continue
    items=[]
    for y,m in c:
        n=max(1,round(m/unit*1.0))
        items.append((y,n))
    asc=sorted(items); desc=asc[::-1]
    if prev is None: order=asc
    else: order=asc if abs(asc[0][0]-prev)<=abs(desc[0][0]-prev) else desc
    for y,n in order:
        for k in range(n): seq.append((x,y))
    prev=order[-1][0]
print(len(seq), seq[0], seq[-1])
json.dump(seq,open('seq.json','w'))
