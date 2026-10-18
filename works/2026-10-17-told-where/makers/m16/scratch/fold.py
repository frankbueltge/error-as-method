from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m16/work/record.jpg').convert('L');px=im.load()
W,H=im.size
P=4.824;n0=6.16
def prof(rows,d0,d1,nb=24):
  acc=[0]*nb;cnt=[0]*nb
  for x in range(W):
    d=(x-n0)/P
    k=round(d)
    if not(d0<=k<d1): continue
    ph=(d-k)  # -0.5..0.5, 0 = noon
    b=int((ph+0.5)*nb)%nb
    acc[b]+=sum(255-px[x,y] for y in rows);cnt[b]+=1
  return [round(a/c) if c else None for a,c in zip(acc,cnt)]
for rng in ((0,20),(20,40),(40,61)):
  print(rng,'bottom',prof(range(82,86),*rng))
  print(rng,'upper ',prof(range(0,80),*rng))
