from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m18/work/record.jpg').convert('L')
w,h=im.size; p=im.load()
col=[(255-p[x,83])+(255-p[x,84]) for x in range(w)]
# local minima
mins=[]
for x in range(1,w-1):
  if col[x]<=col[x-1] and col[x]<=col[x+1] and col[x]<200:
    # parabolic subpixel
    a,b,c=col[x-1],col[x],col[x+1]
    den=a-2*b+c
    off=0.5*(a-c)/den if den else 0
    mins.append(x+off)
mins=[0.6]+mins if col[0]<col[1]+50 else mins
print(len(mins)); print([round(m,2) for m in mins])
n=len(mins); xs=list(range(n))
mx=sum(xs)/n; my=sum(mins)/n
sl=sum((a-mx)*(b-my) for a,b in zip(xs,mins))/sum((a-mx)**2 for a in xs)
print('slope',sl,'icpt',my-sl*mx)
res=[round(m-(my-sl*mx+sl*k),2) for k,m in enumerate(mins)]
print(res)
# also widths of dark blocks (count of px with col>300) per day
