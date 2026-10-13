from PIL import Image
import json,sys
im=Image.open('/tmp/claude-0/s123/mk/m02/work/record.jpg').convert('L')
w,h=im.size; px=im.load()
th=int(sys.argv[1]) if len(sys.argv)>1 else 160
seen=set(); blobs=[]
for x in range(w):
  for y in range(h):
    if px[x,y]<th and (x,y) not in seen:
      st=[(x,y)]; seen.add((x,y)); pts=[]
      while st:
        a,b=st.pop(); pts.append((a,b,255-px[a,b]))
        for da in(-1,0,1):
          for db in(-1,0,1):
            n=(a+da,b+db)
            if 0<=n[0]<w and 0<=n[1]<h and n not in seen and px[n]<th:
              seen.add(n); st.append(n)
      s=sum(p[2] for p in pts)
      blobs.append((sum(p[0]*p[2] for p in pts)/s, sum(p[1]*p[2] for p in pts)/s, len(pts), s))
print(len(blobs))
import collections
print(collections.Counter(b[2] for b in blobs).most_common(12))
print(min(b[1] for b in blobs), max(b[1] for b in blobs))
json.dump(blobs,open('blobs.json','w'))
