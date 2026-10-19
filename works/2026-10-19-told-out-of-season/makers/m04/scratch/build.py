from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m04/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
X0,X1=2,297
rows=[]
for x in range(X0,X1+1):
    s=''
    for y in range(H):
        v=max(0,215-p[x,y])/215.0
        q=min(9,int(round(v*9))) if v>0.12 else 0
        s+=str(q)
    rows.append(s)
data='|'.join(rows)
tpl=open('/tmp/claude-0/s137/mk/m04/scratch/template.html').read()
open('/tmp/claude-0/s137/mk/m04/work/index.html','w').write(tpl.replace('__DATA__',data))
print(len(data))
