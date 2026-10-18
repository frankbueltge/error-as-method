from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m18/work/record.jpg').convert('L')
w,h=im.size; p=im.load()
d=[[max(0,255-p[x,y]) for x in range(w)] for y in range(h)]
# column darkness of bottom rows 83-84
col=[d[83][x]+d[84][x] for x in range(w)]
print(' '.join(str(c//10) for c in col))
# peaks: local maxima
pk=[]
for y in range(1,h-1):
  for x in range(1,w-1):
    v=d[y][x]
    if v<60: continue
    if all(v>=d[y+j][x+i] for i in (-1,0,1) for j in (-1,0,1)):
      s=sum(d[y+j][x+i] for i in (-1,0,1) for j in (-1,0,1))
      cx=sum((x+i)*d[y+j][x+i] for i in (-1,0,1) for j in (-1,0,1))/s
      cy=sum((y+j)*d[y+j][x+i] for i in (-1,0,1) for j in (-1,0,1))/s
      pk.append((round(cx,2),round(cy,2),v,s))
print(len(pk), sum(1 for q in pk if q[1]<81))
import json; json.dump(pk,open('peaks.json','w'))
