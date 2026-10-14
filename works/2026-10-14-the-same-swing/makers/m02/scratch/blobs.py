from PIL import Image
im=Image.open('/tmp/claude-0/s124/mk/m02/work/record.jpg').convert('L')
w,h=im.size;px=im.load()
# darkness map
d=[[max(0,255-px[x,y]) for y in range(h)] for x in range(w)]
# per column: local maxima of darkness (vertical), as weighted 
cols=[]
for x in range(w):
    pk=[]
    for y in range(1,h-1):
        v=d[x][y]
        if v>60 and v>=d[x][y-1] and v>d[x][y+1]:
            pk.append(y)
    cols.append(pk)
import json
json.dump(cols,open('cols.json','w'))
print(sum(len(c) for c in cols))
for x in range(0,300,1): 
    if x<40 or 85<x<135: print(x,cols[x])
