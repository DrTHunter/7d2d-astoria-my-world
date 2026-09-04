"""Fill junk lots around the player with extra copies of the mod POIs.

Rules
  - at most 2 copies of any POI inside the target area (existing ones count)
  - never two copies of the same POI in one town cluster
  - copies of the same POI at least 300 m apart
  - POI tag preference matched to the street-tile type
  - rotation = (slot_rotation + RotationToFaceNorth) mod 4   [verified law]
  - y inherited from the filler being replaced
"""
import os,re,json,math,collections
from xml.sax.saxutils import escape as esc
SP=os.path.dirname(os.path.abspath(__file__))
OLD=os.path.join(os.path.dirname(os.path.abspath(__file__)), "work")
W=os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
DATA=r"C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\Data\Prefabs"
MODS=os.path.expandvars(r"%APPDATA%\7DaysToDie\Mods")
XML=os.path.join(W,"prefabs.xml")
PX,PZ=2006,-989

def rp(p):
    t=open(p,encoding="utf-8",errors="replace").read();d={}
    for m in re.finditer(r'name="([A-Za-z0-9_]+)"\s+value="([^"]*)"',t):d.setdefault(m.group(1),m.group(2))
    return d
P={}
for root in (DATA,MODS):
    for dp,dn,fn in os.walk(root):
        for f in fn:
            if not f.endswith(".xml"):continue
            b=f[:-4]
            if os.path.exists(os.path.join(dp,b+".tts")):P[b]=rp(os.path.join(dp,f))
def rtfn(n):return int(P.get(n,{}).get("RotationToFaceNorth","2"))

raw=open(XML,encoding="utf-8-sig").read(); LINES=raw.split("\n")
lots=json.load(open(os.path.join(SP,"open_lots.json")))
towns=[t for t in json.load(open(os.path.join(SP,"towns.json")))
       if math.hypot(t["cx"]-PX,t["cz"]-PZ)<=2200]
def cluster(x,z):
    for i,t in enumerate(towns):
        if t["x0"]-20<=x<=t["x1"]+20 and t["z0"]-20<=z<=t["z1"]+20:return i
    return None
for L in lots: L["cl"]=cluster(L["x"],L["z"])
lots=[L for L in lots if L["cl"] is not None]

# --- the mod POIs eligible for town lots, and where copies already sit ---
placed=json.load(open(os.path.join(OLD,"placements_numbered.json")))
TOWN={"downtown","commercial","industrial","residential","countryresidential",
      "countrytown","rpd","kendo","culdesac"}
pool=[]
for p in placed:
    d=P.get(p["name"],{}); ps=d.get("PrefabSize")
    if not ps:continue
    w,_,dd=[int(v) for v in ps.split(",")]
    tags={t.strip().lower() for t in (d.get("Tags") or "").split(",")}
    if w==dd and (tags&TOWN): pool.append({"name":p["name"],"mod":p["mod"],"w":w,"tags":tags})
seen={p["name"] for p in pool}
print("unique town-typed mod POIs available:",len(pool),
      dict(collections.Counter(p["w"] for p in pool)))
existing=collections.defaultdict(list)   # name -> [(x,z,cluster)]
for p in placed:
    c=cluster(p["x"],p["z"])
    if c is not None and p["name"] in seen: existing[p["name"]].append((p["x"],p["z"],c))

PREF=[("downtown",["downtown","commercial"]),("rpd",["commercial","downtown"]),
      ("kendo",["countrytown","commercial"]),("commercial",["commercial","downtown"]),
      ("industrial",["industrial","commercial"]),
      ("countryresidential",["countryresidential","countrytown","residential"]),
      ("countrytown",["countrytown","residential","commercial"]),
      ("culdesac",["residential"]),("residential",["residential","countryresidential"])]
CAP=2; MINDIST=300
bysize=collections.defaultdict(list)
for L in lots: bysize[L["w"]].append(L)
for k in bysize: bysize[k].sort(key=lambda L:math.hypot(L["x"]-PX,L["z"]-PZ))

used=collections.defaultdict(list)
for n,v in existing.items(): used[n]=list(v)
taken=set(); chosen=[]
# round-robin so every POI gets a copy before any gets a second
for rnd in range(CAP):
    for p in sorted(pool,key=lambda q:-q["w"]):
        n=p["name"]
        if len(used[n])>=CAP+len([e for e in existing[n]])*0: pass
        if len(used[n])>=CAP: continue
        prefs=next((o for tag,o in PREF if tag in p["tags"]),[])
        pick=None
        for pref in prefs+[None]:
            for L in bysize.get(p["w"],[]):
                if (L["x"],L["z"]) in taken: continue
                if pref and ("rwg_tile_"+pref) not in L["tile"]: continue
                if any(c==L["cl"] for _,_,c in used[n]): continue
                if any(math.hypot(L["x"]-x,L["z"]-z)<MINDIST for x,z,_ in used[n]): continue
                pick=L; break
            if pick: break
        if not pick: continue
        taken.add((pick["x"],pick["z"]))
        used[n].append((pick["x"],pick["z"],pick["cl"]))
        chosen.append({"name":n,"mod":p["mod"],"x":pick["x"],"y":pick["y"],"z":pick["z"],
                       "rot":(pick["srot"]+rtfn(n))%4,"w":p["w"],"d":p["w"],
                       "occ":pick["occ"],"line":pick["line"],"tile":pick["tile"],"cl":pick["cl"]})
print("\nnew copies to place:",len(chosen),dict(collections.Counter(c["w"] for c in chosen)))
print("per town cluster:")
for i,t in enumerate(towns):
    k=sum(1 for c in chosen if c["cl"]==i)
    print(f"   {t['n']:3} tiles ({t['cx']:7.0f},{t['cz']:7.0f})  {math.hypot(t['cx']-PX,t['cz']-PZ):6.0f} m  +{k}")
json.dump(chosen,open(os.path.join(SP,"densify.json"),"w"),indent=1)
