import sys, json
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; p=im.load()
out=[]
for x in range(W):
    for y in range(H):
        v=p[x,y]
        if v<200: out.append([x,y,round((255-v)/255*9)])
print(len(out), file=sys.stderr)
json.dump(out, open(sys.argv[2],'w'), separators=(',',':'))
