import os,re,json,shutil,collections
from xml.sax.saxutils import escape as esc
SP=os.path.dirname(os.path.abspath(__file__))
W=os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
XML=os.path.join(W,"prefabs.xml")
BAK=os.path.join(W,"prefabs.xml.BEFORE-DENSIFY")
ch=json.load(open(os.path.join(SP,"densify.json")))
raw=open(XML,encoding="utf-8-sig").read(); LINES=raw.split("\n")
drop=[c["line"] for c in ch]
assert len(set(drop))==len(drop), "a filler line was targeted twice"
cnt=collections.Counter(LINES)
for d in drop: assert cnt[d]==1, "line not unique in file: %r"%d
if not os.path.exists(BAK): shutil.copy2(XML,BAK)
ds=set(drop)
out=[l for l in LINES if l not in ds]
removed=len(LINES)-len(out)
assert removed==len(ch), "expected to remove %d, removed %d"%(len(ch),removed)
MODNAME={"AAA":"MPLogue Prefabs","AAB":"Voltralux POI Pack","AAC":"Zeebark POI Pack",
         "AAD":"WinterDawn Fortress","AAF":"Svarii POI Package","AAG":"Caleseche",
         "AAH":"ShadowModernHouse","AAI":"Cog's POIs"}
body=["  <!-- ===== MOD POI PACKS - local densification (%d), Astoria east/central towns ===== -->"%len(ch)]
for mod in sorted({c["mod"] for c in ch}):
    g=sorted([c for c in ch if c["mod"]==mod],key=lambda q:(q["name"],q["x"]))
    body.append("  <!-- %s (%d) -->"%(MODNAME.get(mod,mod),len(g)))
    for c in g:
        assert 0<=c["rot"]<=3
        body.append('  <decoration type="model" name="%s" position="%d,%d,%d" rotation="%d" y_is_groundlevel="true" />'
                    %(esc(c["name"]),c["x"],c["y"],c["z"],c["rot"]))
i=max(j for j,l in enumerate(out) if "</prefabs>" in l)
out[i:i]=body
open(XML,"wb").write(b"\xef\xbb\xbf"+"\r\n".join(out).encode("utf-8"))
print("removed %d filler lines, added %d mod POIs"%(removed,len(ch)))
print("decorations now:",sum(1 for l in out if "<decoration" in l))
