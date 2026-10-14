from PIL import Image
import json,sys
g=Image.open(sys.argv[1]).convert('L')
W,H=g.size
out=[]
for x in range(W):
    d=[(255-g.getpixel((x,y)))/255 for y in range(H)]
    # top edge: first y where darkness crosses 0.5, interpolated
    def edge(seq):
        for i in range(1,len(seq)):
            if seq[i]>=0.5 and seq[i-1]<0.5:
                return i-1+(0.5-seq[i-1])/(seq[i]-seq[i-1])
        return 0.0 if seq[0]>=0.5 else None
    t=edge(d); b=edge(d[::-1]); b=H-1-b if b is not None else None
    m=sum(d); c=sum(i*v for i,v in enumerate(d))/m
    out.append([round(t,2),round(b,2),round(c,2),[round(v,2) for v in d]])
    print(x, round(t,2), round(b,2), round(b-t,2), round(c,2))
json.dump(out,open(sys.argv[2],'w'))
