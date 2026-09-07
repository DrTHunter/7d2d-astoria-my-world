import os,re,json,collections,math
W=os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
DATA=r"C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\Data\Prefabs"
MODS=os.path.expandvars(r"%APPDATA%\7DaysToDie\Mods")
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
dec=[(m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5)))
     for m in re.finditer(r'name="([^"]+)"\s+position="(-?\d+),(-?\d+),(-?\d+)"\s+rotation="(\d+)"',raw)]
PX,PZ=2006,-989            # player
BX,BZ=2672,-738            # bedroll
tiles=[(n,x,z,r) for n,x,y,z,r in dec if n in TILES]
print(f"street tiles in world: {len(tiles)}")
# cluster tiles into towns (grid-adjacent, 150m tiles)
cells={(x//150,z//150):(n,x,z,r) for n,x,z,r in tiles}
seen=set();towns=[]
for c in cells:
    if c in seen:continue
    stack=[c];comp=[]
    seen.add(c)
    while stack:
        cur=stack.pop();comp.append(cur)
        for dx in(-1,0,1):
            for dz in(-1,0,1):
                nb=(cur[0]+dx,cur[1]+dz)
                if nb in cells and nb not in seen:
                    seen.add(nb);stack.append(nb)
    xs=[cells[k][1] for k in comp];zs=[cells[k][2] for k in comp]
    towns.append({"n":len(comp),"cx":sum(xs)/len(xs)+75,"cz":sum(zs)/len(zs)+75,
                  "x0":min(xs),"x1":max(xs)+150,"z0":min(zs),"z1":max(zs)+150,
                  "cells":comp})
towns.sort(key=lambda t:-t["n"])
def dist(t,x,z):return math.hypot(t["cx"]-x,t["cz"]-z)
print(f"\ndistinct town clusters: {len(towns)}")
print("\nNearest clusters to the player at X=%d Z=%d:"%(PX,PZ))
near=sorted(towns,key=lambda t:dist(t,PX,PZ))[:10]
for t in near:
    print(f"   {t['n']:3} tiles  centre ({t['cx']:7.0f},{t['cz']:7.0f})  "
          f"span X {t['x0']}..{t['x1']}  Z {t['z0']}..{t['z1']}   {dist(t,PX,PZ):6.0f} m away")
json.dump([{k:v for k,v in t.items() if k!='cells'} for t in towns],open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"towns.json"),"w"),indent=1)
