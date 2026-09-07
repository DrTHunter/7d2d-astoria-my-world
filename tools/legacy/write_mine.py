import os,json,shutil,re
from xml.sax.saxutils import escape as esc
SP=os.path.dirname(os.path.abspath(__file__))
W=os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
XML=os.path.join(W,"prefabs.xml"); SPW=os.path.join(W,"spawnpoints.xml")
cfg=json.load(open(os.path.join(SP,"cluster.json"))); pl=cfg["placed"]
# ---- prefabs.xml ----
bak=XML+".BEFORE-MYPREFABS"
if not os.path.exists(bak): shutil.copy2(XML,bak)
raw=open(XML,encoding="utf-8-sig").read(); LINES=raw.split("\n")
assert "MY PREFABS" not in raw, "already added"
body=["  <!-- ===== MY PREFABS (%d) - levelled pads, cluster near X 2415 Z -817 ===== -->"%len(pl)]
for p in sorted(pl,key=lambda q:q["name"]):
    body.append('  <decoration type="model" name="%s" position="%d,%d,%d" rotation="%d" y_is_groundlevel="true" />'
                %(esc(p["name"]),p["x"],p["y"],p["z"],p["rot"]))
i=max(j for j,l in enumerate(LINES) if "</prefabs>" in l)
LINES[i:i]=body
open(XML,"wb").write(b"\xef\xbb\xbf"+"\r\n".join(LINES).encode("utf-8"))
print("prefabs.xml: added %d of your builds -> %d decorations"%(len(pl),sum(1 for l in LINES if "<decoration" in l)))
# ---- spawnpoints.xml ----
pr=[p for p in pl if p["name"]=="Prison-perimiter"][0]
cx,cz=pr["x"]+pr["w"]//2, pr["z"]+pr["d"]//2
sbak=SPW+".ORIGINAL-BACKUP"
if not os.path.exists(sbak): shutil.copy2(SPW,sbak)
out=('<?xml version="1.0" encoding="UTF-8"?>\r\n<spawnpoints>\r\n'
     '  <!-- single spawn: inside Prison-perimiter -->\r\n'
     '  <spawnpoint position="%d,0,%d" rotation="0,0,0" />\r\n</spawnpoints>\r\n'%(cx,cz))
open(SPW,"wb").write(b"\xef\xbb\xbf"+out.encode("utf-8"))
print("spawnpoints.xml: single spawn at %d,%d (prison centre); original backed up"%(cx,cz))
json.dump({"spawn":[cx,cz],"prison":pr},open(os.path.join(SP,"spawn.json"),"w"),indent=1)
