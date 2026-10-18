from PIL import Image
import json,sys
im=Image.open(sys.argv[1]).convert('L'); p=im.load()
W,H=im.size
# find level centers from row darkness peaks
rows=[sum(255-p[x,y] for x in range(W)) for y in range(H)]
# group rows into bands of consecutive rows with darkness >2500 (plus weak top ones)
bands=[];cur=[]
for y in range(H):
    if rows[y]>2000: cur.append(y)
    else:
        if cur: bands.append(cur); cur=[]
if cur: bands.append(cur)
centers=[sum(y*rows[y] for y in b)/sum(rows[y] for y in b) for b in bands]
# include y=5 band (weak) manually check
print('centers',[round(c,1) for c in centers],file=sys.stderr)
# presence matrix: for each x, each band, max darkness
M=[]
for x in range(W):
    col=[]
    for b in bands:
        lo=min(b)-1; hi=max(b)+1
        col.append(max(255-p[x,y] for y in range(lo,hi+1)))
    M.append(col)
json.dump({'centers':centers,'M':M},open('matrix.json','w'))
