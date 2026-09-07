import os, re, json, collections, numpy as np
import xml.etree.ElementTree as ET

SP   = os.path.dirname(os.path.abspath(__file__))
W    = os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
DATA = r"C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\Data\Prefabs"
MODS = os.path.expandvars(r"%APPDATA%\7DaysToDie\Mods")
NEW  = os.path.join(W, "prefabs.xml")
OLD  = os.path.join(W, "prefabs.xml.ORIGINAL-BACKUP")
fail = []

def read_props(p):
    t = open(p, encoding="utf-8", errors="replace").read(); d = {}
    for m in re.finditer(r'name="([A-Za-z0-9_]+)"\s+value="([^"]*)"', t): d.setdefault(m.group(1), m.group(2))
    return d
P, TILES = {}, {}
for root in (DATA, MODS):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith(".xml"): continue
            b = f[:-4]
            if not os.path.exists(os.path.join(dp, b + ".tts")): continue
            d = read_props(os.path.join(dp, f)); P[b] = d
            if "POIMarkerStart" in d and "streettile" in (d.get("Tags") or ""): TILES[b] = d

# 1 -------------------------------------------------------------- XML + counts
root = ET.parse(NEW).getroot()
n_new, n_old = len(root), len(ET.parse(OLD).getroot())
print(f"1. XML parses. decorations {n_old} -> {n_new}  (expected {n_old - 73 + 122})")
if n_new != n_old - 73 + 122: fail.append("decoration count")

from xml.sax.saxutils import unescape
def parse(path):
    txt = open(path, encoding="utf-8-sig").read()
    return [(unescape(n), int(x), int(y), int(z), int(r)) for n, x, y, z, r in
            re.findall(r'name="([^"]+)"\s+position="(-?\d+),(-?\d+),(-?\d+)"\s+rotation="(\d+)"', txt)]
dec_new, dec_old = parse(NEW), parse(OLD)
town = json.load(open(os.path.join(SP, "town_placements.json")))
wild = json.load(open(os.path.join(SP, "wild_placements.json")))
present = {(n, x, z) for n, x, y, z, r in dec_new}
missing = [t["name"] for t in town + wild if (t["name"], t["x"], t["z"]) not in present]
print(f"   all 122 mod POIs present in file: {not missing}")
if missing: fail.append(f"missing {missing[:5]}")

gone = {(c["occ"], c["x"], c["z"]) for c in town}
still = [g for g in gone if g in present]
print(f"   all 73 replaced fillers removed: {not still}")
if still: fail.append("filler still present")

# 2 ---------------------------------------------------------- slot + rotation
def trip(s): return [tuple(int(v) for v in g.split(",")) for g in s.split("#")]
def to_world(S, X, Z, k, mx, mz, sw, sd):
    if k == 0: return X + mx,            Z + mz,            sw, sd
    if k == 2: return X + (S - mx - sw), Z + (S - mz - sd), sw, sd
    if k == 1: return X + (S - mz - sd), Z + mx,            sd, sw
    return           X + mz,             Z + (S - mx - sw), sd, sw
slots = {}
for n, x, y, z, r in dec_new:
    d = TILES.get(n)
    if not d: continue
    S = trip(d["PrefabSize"])[0][0]
    st, sz = trip(d["POIMarkerStart"]), trip(d["POIMarkerSize"])
    rots = [int(v) for v in d["POIMarkerPartRotations"].split(",")]
    typ = d["POIMarkerType"].split(",")
    for i, (mk, s) in enumerate(zip(st, sz)):
        if typ[i].strip() != "POISpawn": continue
        wx, wz, ww, wd = to_world(S, x, z, r, mk[0], mk[2], s[0], s[2])
        slots[(wx, wz)] = (ww, wd, (rots[i] + r) % 4)

tab = collections.defaultdict(collections.Counter)
for n, x, y, z, r in dec_new:
    if n in TILES or n.startswith("part_"): continue
    s = slots.get((x, z)); ps = P.get(n, {}).get("PrefabSize")
    if not s or not ps: continue
    a, _, b = [int(v) for v in ps.split(",")]
    if {a, b} != {s[0], s[1]}: continue
    tab[int(P[n].get("RotationToFaceNorth", "2"))][(r - s[2]) % 4] += 1
tot = sum(sum(c.values()) for c in tab.values())
bad = sum(v for rt, c in tab.items() for k, v in c.items() if k != rt)
print(f"\n2. rotation law over the FINISHED file: {tot} POIs in resolved slots, {bad} violate it")
for rt in sorted(tab):
    t = sum(tab[rt].values())
    print(f"      RTFN={rt}: n={t:5}  correct {100*tab[rt][rt]/t:5.1f}%")
if bad: fail.append(f"{bad} rotation violations")

slotted = [c for c in town if c["how"] == "slot"]
off = [c for c in slotted if slots.get((c["x"], c["z"]), (0,0,-1))[2] !=
       (c["rot"] - int(P[c["name"]].get("RotationToFaceNorth", "2"))) % 4]
print(f"   the {len(slotted)} slot-placed swaps all satisfy the law: {not off}")
if off: fail.append("slot swap rotation")
for c in town:
    if c["how"] == "inherited":
        print(f"   inherited-rotation swap: {c['name']:26} over {c['occ']:28} rot={c['rot']}")

# 3 ------------------------------------------------------------- collisions
def size(n):
    ps = P.get(n, {}).get("PrefabSize")
    return None if not ps else [int(v) for v in ps.split(",")]
N = 8192
# town POIs live INSIDE street tiles by design, so tiles are a separate mask that
# only the wilderness placements must avoid.
occ_poi  = np.zeros((N, N), bool)
occ_tile = np.zeros((N, N), bool)
mine = {(t["name"], t["x"], t["z"]) for t in town + wild}
for n, x, y, z, r in dec_new:
    if (n, x, z) in mine or n.startswith("part_"): continue
    s = size(n)
    if not s: continue
    w, d = (s[2], s[0]) if r % 2 else (s[0], s[2])
    X, Z = x + 4096, z + 4096
    if X < 0 or Z < 0 or X + w > N or Z + d > N: continue
    (occ_tile if n in TILES else occ_poi)[Z:Z + d, X:X + w] = True
clash = []
new = np.zeros((N, N), bool)
for t in town + wild:
    X, Z, w, d = t["x"] + 4096, t["z"] + 4096, t["w"], t["d"]
    if occ_poi[Z:Z + d, X:X + w].any(): clash.append((t["name"], "an existing POI"))
    if new[Z:Z + d, X:X + w].any():     clash.append((t["name"], "another new POI"))
    new[Z:Z + d, X:X + w] = True
for t in wild:
    X, Z, w, d = t["x"] + 4096, t["z"] + 4096, t["w"], t["d"]
    if occ_tile[Z:Z + d, X:X + w].any(): clash.append((t["name"], "a street tile"))
print(f"\n3. footprint collisions: {len(clash)}   "
      f"(town POIs vs POIs; wilderness POIs vs POIs and tiles)")
for c in clash[:8]: print("     ", c)
if clash: fail.append("collisions")

# 4 ------------------------------------------------------------------ terrain
h = np.load(os.path.join(SP, "h.npy"))
def relief(t):
    s = h[t["z"]+4096:t["z"]+4096+t["d"], t["x"]+4096:t["x"]+4096+t["w"]]
    return float(s.max() - s.min())
rt = [relief(t) for t in town]; rw = [relief(t) for t in wild]
print(f"\n4. ground relief under town POIs : median {np.median(rt):.2f} m  max {max(rt):.2f} m")
print(f"   ground relief under wild POIs : median {np.median(rw):.2f} m  max {max(rw):.2f} m")
tn = {t["name"] for t in town}
low = [(t["name"], "town lot" if t["name"] in tn else "WILDERNESS",
        round(float(h[t["z"]+4096:t["z"]+4096+t["d"], t["x"]+4096:t["x"]+4096+t["w"]].min()), 1))
       for t in town + wild
       if h[t["z"]+4096:t["z"]+4096+t["d"], t["x"]+4096:t["x"]+4096+t["w"]].min() < 20]
print(f"   POIs on ground below 20 m: {len(low)}")
for n, kind, m in low: print(f"      {n:30} {kind:11} min {m} m")
# only a wilderness POI below 20 m is a water risk; town lots are flattened tile ground
if [l for l in low if l[1] == "WILDERNESS"]: fail.append("wilderness POI on low ground")

# 5 --------------------------------------------------------------- district
# count by tile INSTANCE (its world corner), not by tile type name
inst = []
for n, x, y, z, r in dec_new:
    if n in TILES: inst.append((x, z, n))
def owner(px, pz):
    for x, z, n in inst:
        if x <= px < x + 150 and z <= pz < z + 150: return (x, z, n)
    return None
per = collections.Counter()
dist = collections.Counter()
for c in town:
    if c["how"] != "slot": continue
    o = owner(c["x"], c["z"])
    if o:
        per[(o[0], o[1])] += 1
        dist[o[2].replace("rwg_tile_", "").split("_")[0]] += 1
crowd = sum(1 for v in per.values() if v > 1)
print(f"\n5. tile instances receiving >1 new POI: {crowd}  (cap was 1)")
print("   new POIs by district: " + ", ".join(f"{k} {v}" for k, v in dist.most_common()))
if crowd: fail.append("tile crowding")
print("\n" + ("ALL CHECKS PASSED" if not fail else "FAILURES: " + "; ".join(fail)))
