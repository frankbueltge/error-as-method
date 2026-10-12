import json
g=json.load(open('scratch/grey.json'))
data=json.dumps(g,separators=(',',':'))
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nineteen and a Half Hours</title>
<style>:root{--paper:#f2efe8;--ink:#1b1a17;--faint:#8a857a}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--paper:#f2efe8;--ink:#1b1a17;--faint:#8a857a}}
html,body{margin:0;background:var(--paper)}body{display:flex;justify-content:center}
svg{display:block;width:1100px;height:800px;max-width:100%;height:auto}</style></head><body>
<svg id="s" viewBox="0 0 1100 800" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The 75 by 23 pixels of the record, enlarged, above rulers counting 1,464 hours, 61 days and 75 pixel columns."></svg>
<script>
const G=DATA;
const NS="http://www.w3.org/2000/svg",s=document.getElementById("s");
const el=(t,a,p=s)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e};
const X0=100,W=960,Y0=86,CH=23,R=23,CW=W/75,H=CH*R,HR=1464,hx=h=>X0+W*h/HR;
el("rect",{x:0,y:0,width:1100,height:800,fill:"#f2efe8"});
const txt=(x,y,t,o={})=>{const e=el("text",Object.assign({x,y,fill:"#1b1a17","font-family":"Georgia, 'Times New Roman', serif","font-size":13},o));e.textContent=t;return e};
txt(X0,48,"Nineteen and a Half Hours",{"font-size":22});
txt(X0+W,48,"1,464 hours \\u00b7 61 days \\u00b7 75 \\u00d7 23 pixels",{"text-anchor":"end",fill:"#6f6a60","font-size":13,"font-style":"italic"});
// the pixels, as found (JPEG artefacts included)
const f=el("g",{"shape-rendering":"crispEdges"});
for(let y=0;y<R;y++)for(let x=0;x<75;x++){const v=G[y][x];if(v>246)continue;
 el("rect",{x:(X0+x*CW).toFixed(2),y:Y0+y*CH,width:(CW+0.4).toFixed(2),height:CH+0.4,fill:`rgb(${v},${v-3},${v-8})`},f);}
// faint grid of the pixel lattice
const gl=el("g",{stroke:"#1b1a17","stroke-opacity":0.06,"stroke-width":0.5});
for(let x=0;x<=75;x++)el("line",{x1:X0+x*CW,x2:X0+x*CW,y1:Y0,y2:Y0+H},gl);
for(let y=0;y<=R;y++)el("line",{x1:X0,x2:X0+W,y1:Y0+y*CH,y2:Y0+y*CH},gl);
// rulers
const ry=Y0+H+26;
// hours: one hairline each
const hg=el("g",{stroke:"#1b1a17","stroke-width":0.35});
for(let h=0;h<=HR;h++)el("line",{x1:hx(h),x2:hx(h),y1:ry,y2:ry+(h%24?10:18)},hg);
// pixel columns: alternating bands, each holding 19 or 20 hours
for(let x=0;x<75;x++){const a=Math.ceil(x*HR/75),b=Math.ceil((x+1)*HR/75);
 el("rect",{x:X0+x*CW,y:ry+30,width:CW,height:8,fill:x%2?"#1b1a17":"#b9b3a6","fill-opacity":x%2?0.75:0.6});
 txt(X0+(x+.5)*CW,ry+54,String(b-a),{"text-anchor":"middle","font-size":8.5,fill:"#6f6a60","font-family":"ui-monospace, Menlo, monospace"});}
txt(X0-6,ry+11,"hours",{"text-anchor":"end","font-size":10,fill:"#6f6a60","font-style":"italic"});
txt(X0-6,ry+38,"pixels",{"text-anchor":"end","font-size":10,fill:"#6f6a60","font-style":"italic"});
txt(X0-6,ry+54,"hours each",{"text-anchor":"end","font-size":8.5,fill:"#6f6a60","font-style":"italic"});
txt(X0,ry+86,"Every hour was a dot. At this size each column of pixels had to hold nineteen or twenty of them,",{"font-size":13,fill:"#3a3732","font-style":"italic"});
txt(X0,ry+104,"and kept only their spread: a steady band, and once, near the forty-fourth day, a rise.",{"font-size":13,fill:"#3a3732","font-style":"italic"});
</script></body></html>'''
open('work/index.html','w').write(html.replace('DATA',data))
