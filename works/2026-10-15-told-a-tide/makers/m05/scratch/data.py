from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m05/work/record.jpg').convert('L');px=im.load()
out=[]
for x in range(300):
    s=''.join(chr(48+y)+chr(48+min(9,(255-px[x,y])//25)) for y in range(90) if px[x,y]<170)
    out.append(s)
import json;open('data.json','w').write(json.dumps(out));print(sum(len(s)//2 for s in out), len(json.dumps(out)))
