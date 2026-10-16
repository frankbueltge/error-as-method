from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m04/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
# per column: string of pairs (y as 2 chars base-36-ish, weight digit 1-9)
out=[]; n=0
for x in range(W):
    s=''
    for y in range(H):
        w=max(0,230-p[x,y])/230
        if w>0.15:
            s+='%02d%d'%(y,min(9,max(1,round(w*9)))); n+=1
    out.append(s)
open('cols.txt','w').write('|'.join(out))
print(n, len('|'.join(out)))
