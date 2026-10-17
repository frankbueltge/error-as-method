from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m06/work/record.jpg').convert('L')
w,h=im.size;px=im.load()
d=[ (255-px[x,83])+(255-px[x,84]) for x in range(w)]
print(' '.join('%d:%d'%(x,v//10) for x,v in enumerate(d)))
# blocks
blocks=[];cur=None
for x,v in enumerate(d):
  if v>150:
    if cur is None: cur=[x,x,0,0]
    cur[1]=x;cur[2]+=v;cur[3]+=v*x
  else:
    if cur: blocks.append(cur);cur=None
if cur: blocks.append(cur)
print(len(blocks))
cs=[b[3]/b[2] for b in blocks]
print([round(c,1) for c in cs])
print([b[1]-b[0]+1 for b in blocks])
print([round(cs[i+1]-cs[i],2) for i in range(len(cs)-1)])
# weighted width
print([round(b[2]/400,1) for b in blocks])
