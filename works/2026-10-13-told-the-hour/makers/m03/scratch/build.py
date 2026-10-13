from PIL import Image
im=Image.open('../work/record.jpg').convert('L'); w,h=im.size; px=im.load()
digits=[]
for y in range(h):
    row=''
    for x in range(w):
        d=max(0,225-px[x,y])/225
        q=min(9,int(round(d*9)))
        if q<=1: q=0
        row+=str(q)
    digits.append(row)
data=''.join(digits)
html=open('template.html').read().replace('__DATA__',data)
open('../work/index.html','w').write(html)
print(len(html))
