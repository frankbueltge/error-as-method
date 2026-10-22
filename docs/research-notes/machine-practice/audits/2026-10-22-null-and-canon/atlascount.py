import json,re,sys
d=json.load(open(sys.argv[1]))['entries']
# keywords fixed before the count, one regex per shelf key named by all four shelf agents (exp 28)
K={'ebird':r'ebird|bird sighting|birdwatch','gbif':r'\bgbif\b|biodiversity (record|occurrence)','gutenberg':r'gutenberg',
'maunaloa':r'mauna loa|keeling|co2 (record|concentration)|carbon dioxide (record|concentration)','met':r'metropolitan museum|\bthe met\b open access',
'nyctaxi':r'taxi','osm':r'openstreetmap|\bosm\b','owid':r'our world in data','pageviews':r'wikipedia','usgs-eq':r'earthquake|seismic|seismo',
'wayback':r'wayback|internet archive','silso':r'sunspot','seaice':r'sea ice|sea-ice','gistemp':r'global temperature|temperature anomal|warming stripes',
'oldfaithful':r'old faithful|geyser'}
n=len(d);out={}
for k,rx in K.items():
  hits=[e['title']+' / '+e['artist']+' ('+str(e['year'])+')' for e in d if re.search(rx,(e.get('title','')+' '+e.get('decisive_move','')).lower())]
  out[k]=hits
print('entries',n)
for k,h in out.items(): print(k,len(h),h[:6])
