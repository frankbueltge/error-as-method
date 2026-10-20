"""figure.py: draws figure.svg from results.json, the same chart as the face."""
import json
R=json.load(open("results.json"))["rows"]
X0,CW=170,110; out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 335" font-family="Georgia,serif" font-size="13">',
'<rect width="760" height="335" fill="#f6f3ec"/>',
'<text x="20" y="26" font-size="16" fill="#1d1b18">Torn, Reversed: sixteen variants of one work, by blind distance and a judge\'s verdict</text>',
f'<rect x="{X0+3*CW}" y="44" width="{2*CW}" height="112" fill="#c99a2e" opacity=".18"/>',f'<text x="{X0+3*CW+8}" y="62" fill="#6b665c">information</text>']
cols=["broken","distance 0","distance 1","distance 2","distance 3"]
for i,c in enumerate(cols):
  out.append(f'<line x1="{X0+i*CW}" x2="{X0+i*CW}" y1="44" y2="285" stroke="#d7d1c4"/>'); out.append(f'<text x="{X0+i*CW+CW/2}" y="305" text-anchor="middle" fill="#6b665c">{c}</text>')
out.append(f'<line x1="{X0}" x2="{X0+5*CW}" y1="160" y2="160" stroke="#d7d1c4"/>')
out+= [f'<text x="{X0-12}" y="105" text-anchor="end" fill="#1d1b18">judged to work</text>',f'<text x="{X0-12}" y="230" text-anchor="end" fill="#1d1b18">judged not to</text>']
slots={}
for k,r in R.items():
  if r["arm"]=="C": continue
  ci=0 if r["x_broken"]=="yes" else r["x_distance"]+1; ry=100 if r["w_works"]=="yes" else 225
  n=slots[(ci,ry)]=slots.get((ci,ry),0)+1; cx=X0+ci*CW+20+((n-1)%4)*23; cy=ry-30+((n-1)//4)*30
  col="#2f6f62" if r["arm"]=="A" else "#a5432e"
  out.append(f'<circle cx="{cx}" cy="{cy+15}" r="9" fill="{col}"/><text x="{cx}" y="{cy+34}" text-anchor="middle" font-size="9" fill="#6b665c">{k}</text>')
out.append('<circle cx="30" cy="322" r="5" fill="#2f6f62"/><text x="40" y="326" font-size="12" fill="#6b665c">asked for a variation (4 fresh makers)</text>')
out.append('<circle cx="290" cy="322" r="5" fill="#a5432e"/><text x="300" y="326" font-size="12" fill="#6b665c">blind mutation of the code (12, seed 144)</text></svg>')
open("figure.svg","w").write("\n".join(out))
