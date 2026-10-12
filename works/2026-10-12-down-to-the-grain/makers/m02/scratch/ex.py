from PIL import Image
im=Image.open('/tmp/claude-0/s122/mk/m02/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
import collections
hist=collections.Counter(px[x,y]//16 for x in range(W) for y in range(H)); print(sorted(hist.items()))
# crop zoom
im.crop((0,170,200,330)).resize((800,640),Image.NEAREST).save('/tmp/claude-0/s122/mk/m02/scratch/zoom.png')
# column dark counts
dark=[[y for y in range(H) if px[x,y]<128] for x in range(W)]
print([len(d) for d in dark[:80]])
