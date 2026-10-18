import json
def e(K1,cats,K3,L1q,L2q,K4):
    return {"K1":K1,"K1_cats":cats,"K3":K3,"L1":"yes" if L1q else "no","L1_quote":L1q,"L2":"yes" if L2q else "no","L2_quote":L2q,"K4":K4}
L=["light"]
FP="Fort Peck, Montana, 634 m"
a={
"p01":e(["Sunlight on level ground","Sun Wheel","how much light"],L,"is","Fort Peck ... at 634 m on the plains of north-eastern Montana","","Sun Wheel, Fort Peck"),
"p02":e(["Sixty-one Suns","the sun's path","the measured sunlight on level ground"],L,"is","Fort Peck, Montana, 634 m","","Sixty-one Suns"),
"p03":e([],[],"none","Fort Peck, Montana · 634 m","","Sixty-One Turns"),
"p04":e(["1,464 hours of sunlight on level ground"],L,"is","","","Sixty-One Noons"),
"p05":e(["Sixty-One Days of Light","Sunlight on level ground","light per day"],L,"is","Sunlight on level ground at Fort Peck, Montana, 634 m above sea level","Values are read back from a small dot plot and are approximate","Sixty-One Days of Light"),
"p06":e(["one hour of sunlight on level ground","What the Ground Received"],L,"is","Fort Peck, Montana · 634 m","","What the Ground Received"),
"p07":e(["Where the Light Reached"],L,"is","","","Where the Light Reached"),
"p08":e(["Printed by Their Own Light","as high as its light reached"],L,"is","","","Printed by Their Own Light"),
"p09":e(["The Light Draws In","Sunlight on level ground","light per day","sun time"],L,"is","Sunlight on level ground at Fort Peck, Montana, 634 m","the record as it arrived: 1,464 hours, left to right","The Light Draws In"),
"p10":e(["light from the record's own values"],L,"none","Fort Peck, Montana · 634 m","","Sixty-One Turns"),
"p11":e(["Sun Print","Sixty-one days of sunlight on a level surface","more light"],L,"is","","","Sun Print"),
"p12":e(["Sixty-One Days of Light"],L,"is","Fort Peck, Montana · 634 m","Brightness is each hour's value as read back from a 300-pixel picture, where one pixel held about five hours.","Sixty-One Days of Light"),
"p13":e([],[],"none","","",""),
"p14":e([],[],"none","","",""),
"p15":e([],[],"none","","","Sixty-One Exposures"),
"p16":e(["Sunlight falling on a level surface","where the sun stands","the light gathers"],L,"is","Fort Peck, north-eastern Montana, 634 m above the sea","The values were read back from a small dotted plot and are approximate, hour by hour.","Sixty-One Turns"),
"p17":e(["Gathered Light"],L,"is","","","Gathered Light"),
"p18":e([],[],"none","","","Sixty-One Turns"),
"p19":e([],[],"none","","","The Night Widens"),
"p20":e([],[],"none","Fort Peck, Montana · 634 m","","APERTURE"),
"p21":e(["Contact sheet for an unnamed light"],L,"is","","","Contact Sheet for an Unnamed Light"),
"p22":e(["Sixty-One Suns","as far out as that hour's light reached"],L,"is","","","Sixty-One Suns"),
"p23":e([],[],"none","FORT PECK, MONTANA · 634 M","",""),
"p24":e(["Light Rings, Fort Peck"],L,"is","Light Rings, Fort Peck / Montana, 634 m above sea level.","","Light Rings, Fort Peck"),
}
json.dump(a,open('/tmp/claude-0/s133/cd/answers.json','w'),indent=1,ensure_ascii=False)
print(len(a))
