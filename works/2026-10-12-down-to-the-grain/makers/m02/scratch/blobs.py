from PIL import Image
import json,sys
im=Image.open('/tmp/claude-0/s122/mk/m02/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
for T in (230,215,200,180,160):
    seen=set(); blobs=[]
    for x in range(W):
        for y in range(H):
            if px[x,y]<T and (x,y) not in seen:
                st=[(x,y)]; seen.add((x,y)); pts=[]
                while st:
                    a,b=st.pop(); pts.append((a,b))
                    for da in (-1,0,1):
                        for db in (-1,0,1):
                            c,d=a+da,b+db
                            if 0<=c<W and 0<=d<H and (c,d) not in seen and px[c,d]<T:
                                seen.add((c,d)); st.append((c,d))
                w=[(255-px[a,b]) for a,b in pts]; s=sum(w)
                blobs.append((sum(a*q for (a,b),q in zip(pts,w))/s, sum(b*q for (a,b),q in zip(pts,w))/s, len(pts), min(px[a,b] for a,b in pts)))
    sizes=[b[2] for b in blobs]
    import collections
    print(T,len(blobs),sorted(collections.Counter(sizes).items())[:15])
    if T==200: json.dump(blobs,open('/tmp/claude-0/s122/mk/m02/scratch/blobs200.json','w'))
