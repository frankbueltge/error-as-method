from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m22/work/record.jpg').convert('L')
W,H=im.size;px=im.load()
s=[sum(255-px[x,y] for y in (82,83,84,85)) for x in range(W)]
# troughs: local regions below 300
gaps=[];x=3
while x<W:
  if s[x]<330 and s[x-1]>=330:
    a=x
    while x<W and s[x]<330: x+=1
    b=x
    w=[(330-s[k]) for k in range(a,b)]
    c=sum(k*wk for k,wk in zip(range(a,b),w))/sum(w)
    gaps.append((round(c,2),b-a,round(sum(w))))
  x+=1
print(len(gaps));print(gaps)
n=len(gaps);ks=list(range(n));cs=[g[0] for g in gaps]
mk=sum(ks)/n;mc=sum(cs)/n
sl=sum((k-mk)*(c-mc) for k,c in zip(ks,cs))/sum((k-mk)**2 for k in ks)
print('slope',sl,'icpt',mc-sl*mk)
print([round(c-(mc-sl*mk)-sl*k,2) for k,c in zip(ks,cs)])
