import os,re,json,collections,math
W=os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
DATA=r"C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\Data\Prefabs"
MODS=os.path.expandvars(r"%APPDATA%\7DaysToDie\Mods")
SP=os.path.dirname(os.path.abspath(__file__))
def rp(p):
    t=open(p,encoding="utf-8",errors="replace").read();d={}
    for m in re.finditer(r'name="([A-Za-z0-9_]+)"\s+value="([^"]*)"',t):d.setdefault(m.group(1),m.group(2))
    return d
P,TILES={},{}
for root in (DATA,MODS):
    for dp,dn,fn in os.walk(root):
        for f in fn:
            if not f.endswith(".xml"):continue
            b=f[:-4]
            if not os.path.exists(os.path.join(dp,b+".tts")):continue
            d=rp(os.path.join(dp,f));P[b]=d
            if "POIMarkerStart" in d and "streettile" in (d.get("Tags") or ""):TILES[b]=d
raw=open(os.path.join(W,"prefabs.xml"),encoding="utf-8-sig").read()
LINES=raw.split("\n")
dec=[]
for m in re.finditer(r'^.*<decoration[^>]*name="([^"]+)"\s+position="(-?\d+),(-?\d+),(-?\d+)"\s+rotation="(\d+)".*$',raw,re.M):
    dec.append((m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5)),m.group(0)))
def trip(s):return [tuple(int(v) for v in g.split(",")) for g in s.split("#")]
def to_world(S,X,Z,k,mx,mz,sw,sd):
    if k==0:return X+mx,Z+mz,sw,sd
    if k==2:return X+(S-mx-sw),Z+(S-mz-sd),sw,sd
    if k==1:return X+(S-mz-sd),Z+mx,sd,sw
    return X+mz,Z+(S-mx-sw),sd,sw
slots={}
for n,x,y,z,r,_ in dec:
    d=TILES.get(n)
    if not d:continue
    S=trip(d["PrefabSize"])[0][0]
    st,sz=trip(d["POIMarkerStart"]),trip(d["POIMarkerSize"])
    rots=[int(v) for v in d["POIMarkerPartRotations"].split(",")]
    typ=d["POIMarkerType"].split(",")
    for i,(mk,s) in enumerate(zip(st,sz)):
        if typ[i].strip()!="POISpawn":continue
        wx,wz,ww,wd=to_world(S,x,z,r,mk[0],mk[2],s[0],s[2])
        if ww!=wd:continue
        slots[(wx,wz)]={"w":ww,"d":wd,"srot":(rots[i]+r)%4,"tile":n,"tx":x,"tz":z}
occ=collections.defaultdict(list)
for n,x,y,z,r,ln in dec:
    if n not in TILES and not n.startswith("part_"):occ[(x,z)].append((n,y,r,ln))
JUNK=re.compile(r'^(remnant_|rubble_|lot_)',re.I)
MODNAMES={p["name"] for p in json.load(open(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "work"), "placements_numbered.json")))}
PX,PZ=2006,-989
towns=json.load(open(os.path.join(SP,"towns.json")))
targets=[t for t in towns if math.hypot(t["cx"]-PX,t["cz"]-PZ)<=2200]
print("target clusters within 2200 m: %d  (%d tiles total)"%(len(targets),sum(t["n"] for t in targets)))
def inarea(x,z):
    return any(t["x0"]-20<=x<=t["x1"]+20 and t["z0"]-20<=z<=t["z1"]+20 for t in targets)
free=collections.Counter();modhere=collections.Counter();allfree=collections.Counter()
lots=[]
for (x,z),s in slots.items():
    for n,y,r,ln in occ.get((x,z),[]):
        ps=P.get(n,{}).get("PrefabSize")
        if not ps:continue
        w,_,d2=[int(v) for v in ps.split(",")]
        if (w,d2)!=(s["w"],s["d"]):continue
        if n in MODNAMES:
            if inarea(x,z):modhere[s["w"]]+=1
            continue
        if not JUNK.match(n):continue
        allfree[s["w"]]+=1
        if inarea(x,z):
            free[s["w"]]+=1
            lots.append(dict(s,x=x,z=z,occ=n,y=y,line=ln))
print("\nJunk lots still available:")
print("  size |  in target area | whole map")
for k in sorted(set(allfree)|set(free)):
    print(f"  {k:>3}x{k:<3}|  {free[k]:>13} | {allfree[k]:>8}")
print(f"  TOTAL|  {sum(free.values()):>13} | {sum(allfree.values()):>8}")
print("\nmod POIs already sitting in the target area:",sum(modhere.values()),dict(modhere))
json.dump(lots,open(os.path.join(SP,"open_lots.json"),"w"),indent=1)
