import numpy as np, os, json
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS=None
SP=os.path.dirname(os.path.abspath(__file__))
W=os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
S=3072; K=8192/S
base=Image.open(os.path.join(SP,"base_game.png")).resize((S,S),Image.LANCZOS)   # already north-up
MARGIN=150; LEG=470
canvas=Image.new("RGB",(S+MARGIN*2+LEG,S+MARGIN*2),(18,20,24))
canvas.paste(base,(MARGIN,MARGIN))
d=ImageDraw.Draw(canvas,"RGBA")
def F(sz,b=False):
    for n in (["seguisb.ttf","segoeuib.ttf","arialbd.ttf"] if b else ["segoeui.ttf","arial.ttf"]):
        try: return ImageFont.truetype("C:/Windows/Fonts/"+n,sz)
        except: pass
    return ImageFont.load_default()
f9,f11,f14,f20,f30=F(15),F(18),F(21,True),F(30,True),F(44,True)
def px(x,z): return (MARGIN+(x+4096)/K, MARGIN+(4096-z)/K)

# coordinate grid
for v in range(-4096,4097,1024):
    a,_=px(v,0); _,b=px(0,v)
    d.line([(a,MARGIN),(a,MARGIN+S)],fill=(255,255,255,38),width=1)
    d.line([(MARGIN,b),(MARGIN+S,b)],fill=(255,255,255,38),width=1)
    d.text((a,MARGIN-30),f"{v}",font=f11,fill=(150,160,175),anchor="mm")
    d.text((MARGIN-38,b),f"{v}",font=f11,fill=(150,160,175),anchor="mm")
d.rectangle([MARGIN,MARGIN,MARGIN+S,MARGIN+S],outline=(90,100,115),width=2)
d.text((MARGIN+S/2,MARGIN-95),"ASTORIA 8K  —  122 mod POIs added",font=f30,fill=(240,244,250),anchor="mm")
d.text((MARGIN+S/2,MARGIN-58),
       "73 in town lots (white ring)   ·   49 in the wilderness   ·   coordinates are each POI's north-west corner",
       font=f14,fill=(140,150,165),anchor="mm")
# north arrow
nx,ny=MARGIN+S-70,MARGIN+70
d.polygon([(nx,ny-42),(nx-15,ny+12),(nx,ny),(nx+15,ny+12)],fill=(240,244,250))
d.text((nx,ny+30),"N",font=f14,fill=(240,244,250),anchor="mm")

COL={"AAA":(255,86,86),"AAB":(78,176,255),"AAC":(255,206,54),"AAD":(178,124,255),
     "AAF":(60,230,150),"AAG":(255,146,44),"AAH":(255,116,214),"AAI":(140,240,86)}
NAME={"AAA":"MPLogue Prefabs","AAB":"Voltralux's POI Pack","AAC":"Zeebark POI Pack",
      "AAD":"WinterDawn Fortress","AAF":"Svarii's POI Package","AAG":"Caleseche",
      "AAH":"ShadowModernHouse","AAI":"Cog's POIs"}
pl=json.load(open(os.path.join(SP,"placements_numbered.json")))   # written by merge.py
order={m:i for i,m in enumerate(["AAA","AAB","AAC","AAD","AAF","AAG","AAH","AAI"])}
pl.sort(key=lambda p:(order[p["mod"]],p["name"]))
for i,p in enumerate(pl,1): p["n"]=i

for p in pl:
    x0,y0=px(p["x"],p["z"]+p["d"]); x1,y1=px(p["x"]+p["w"],p["z"])
    c=COL[p["mod"]]
    d.rectangle([x0,y0,x1,y1],outline=c+(255,),width=2,fill=c+(70,))
for p in pl:                                    # numbers on top
    cx,cy=px(p["x"]+p["w"]/2,p["z"]+p["d"]/2); c=COL[p["mod"]]
    r=11
    if p.get("where")=="town":                  # town swaps get a bright ring
        d.ellipse([cx-r-3,cy-r-3,cx+r+3,cy+r+3],outline=(255,255,255,150),width=2)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(12,14,18,235),outline=c+(255,),width=2)
    d.text((cx,cy+1),str(p["n"]),font=f9,fill=c,anchor="mm")

# spawn points, drawn as squares on top of everything
spawns=json.load(open(os.path.join(SP,"spawns.json")))
for s in spawns:
    cx,cy=px(s["x"],s["z"]); r=14
    d.rectangle([cx-r,cy-r,cx+r,cy+r],fill=(12,14,18,240),outline=(255,255,255,255),width=3)
    d.text((cx,cy+1),str(s["n"]),font=f11,fill=(255,255,255),anchor="mm")

# legend
lx=MARGIN*2+S; ly=MARGIN
d.text((lx,ly),"LEGEND",font=f20,fill=(240,244,250)); ly+=46
for m in order:
    g=[p for p in pl if p["mod"]==m]
    if not g: continue
    c=COL[m]
    d.rectangle([lx,ly+3,lx+16,ly+19],fill=c+(255,))
    d.text((lx+26,ly),f"{NAME[m]}  ({len(g)})",font=f14,fill=(228,234,242)); ly+=30
    for p in g:
        d.text((lx+26,ly),f"{p['n']:>3}. {p['name'][:34]}",font=f9,fill=(158,168,182))
        d.text((lx+330,ly),f"{p['x']}, {p['z']}",font=f9,fill=(120,130,145)); ly+=19
    ly+=12
ly+=10
d.text((lx,ly),"spawn points  (10)",font=f14,fill=(240,244,250)); ly+=30
for s in spawns:
    d.rectangle([lx,ly+2,lx+14,ly+16],fill=(12,14,18),outline=(255,255,255),width=2)
    d.text((lx+7,ly+9),str(s["n"]),font=f9,fill=(255,255,255),anchor="mm")
    d.text((lx+26,ly),f"{s['biome']}",font=f9,fill=(158,168,182))
    d.text((lx+330,ly),f"{s['x']}, {s['z']}",font=f9,fill=(120,130,145)); ly+=21
ly+=16
d.text((lx,ly),"map shading",font=f14,fill=(200,208,220)); ly+=28
for lbl,c in [("asphalt road",(88,88,92)),
              ("gravel road",(150,132,100)),("white ring = swapped into a town lot",(255,255,255))]:
    d.rectangle([lx,ly+3,lx+16,ly+19],fill=c); d.text((lx+26,ly),lbl,font=f9,fill=(158,168,182)); ly+=24
canvas.save(os.path.join(SP,"astoria_poi_map.png"))
canvas.resize((canvas.width//2,canvas.height//2),Image.LANCZOS).save(os.path.join(SP,"astoria_poi_map_half.png"))
json.dump(pl,open(os.path.join(SP,"placements_numbered.json"),"w"),indent=1)
print("saved",canvas.size, round(os.path.getsize(os.path.join(SP,"astoria_poi_map.png"))/1e6,2),"MB")
