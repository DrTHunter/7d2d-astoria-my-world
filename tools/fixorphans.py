"""Resolve the 19 placements referencing prefabs that no longer exist in V 3.2.0.

  remnant_lot_industrial_01      9x  -> remnant_industrial_large_01/_02 (same 100x100, T0, industrial)
  cave_15                        1x  -> cave_17 (25x25 wilderness cave; cave_15 was cut in 3.x)
  part_remnant_lot_industrial_01 7x  -> removed (child parts of a prefab that no longer exists)
  part_gardener_truck            1x  -> removed (same)
  aaa_subway                     1x  -> removed (Compopack prefab, no vanilla successor, size unknown)

Rotation for replacements uses the verified law:
    rotation = (marker_rotation + tile_rotation + RotationToFaceNorth) mod 4
"""
import os, re, shutil, collections
import numpy as np

SP   = os.path.dirname(os.path.abspath(__file__))
W    = os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
DATA = r"C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\Data\Prefabs"
MODS = os.path.expandvars(r"%APPDATA%\7DaysToDie\Mods")
XML  = os.path.join(W, "prefabs.xml")

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

raw   = open(XML, encoding="utf-8-sig").read()
LINES = raw.split("\n")
DEC   = re.compile(r'name="([^"]+)"\s+position="(-?\d+),(-?\d+),(-?\d+)"\s+rotation="(\d+)"')
dec   = [(m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)))
         for m in DEC.finditer(raw)]

# lot slots, for the exact facing of each 100x100 industrial lot
def trip(s): return [tuple(int(v) for v in g.split(",")) for g in s.split("#")]
def tw(S, X, Z, k, mx, mz, sw, sd):
    if k == 0: return X + mx,            Z + mz,            sw, sd
    if k == 2: return X + (S - mx - sw), Z + (S - mz - sd), sw, sd
    if k == 1: return X + (S - mz - sd), Z + mx,            sd, sw
    return           X + mz,             Z + (S - mx - sw), sd, sw
slots = {}
for n, x, y, z, r in dec:
    d = TILES.get(n)
    if not d: continue
    S = trip(d["PrefabSize"])[0][0]
    st, sz = trip(d["POIMarkerStart"]), trip(d["POIMarkerSize"])
    rots = [int(v) for v in d["POIMarkerPartRotations"].split(",")]
    typ = d["POIMarkerType"].split(",")
    for i, (mk, s) in enumerate(zip(st, sz)):
        if typ[i].strip() != "POISpawn": continue
        wx, wz, ww, wd = tw(S, x, z, r, mk[0], mk[2], s[0], s[2])
        slots[(wx, wz)] = (ww, wd, (rots[i] + r) % 4)

DROP    = {"part_remnant_lot_industrial_01", "part_gardener_truck", "aaa_subway"}
REPLACE = {"remnant_lot_industrial_01": ["remnant_industrial_large_01", "remnant_industrial_large_02"],
           "cave_15": ["cave_17"]}
for lst in REPLACE.values():
    for n in lst:
        assert n in P, f"replacement {n} does not exist in 3.2.0"

# occupancy of everything that is staying, for a collision check on the replacements
def size(n):
    ps = P.get(n, {}).get("PrefabSize")
    return [int(v) for v in ps.split(",")] if ps else None
N = 8192
occ = np.zeros((N, N), bool)
targets = DROP | set(REPLACE)
for n, x, y, z, r in dec:
    if n in targets or n in TILES or n.startswith("part_"): continue
    s = size(n)
    if not s: continue
    w, d = (s[2], s[0]) if r % 2 else (s[0], s[2])
    X, Z = x + 4096, z + 4096
    if X < 0 or Z < 0 or X + w > N or Z + d > N: continue
    occ[Z:Z + d, X:X + w] = True

out, changed, removed, clashes = [], [], [], []
counter = collections.Counter()
for ln in LINES:
    m = DEC.search(ln)
    if not m:
        out.append(ln); continue
    n, x, y, z, r = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
    if n in DROP:
        removed.append((n, x, z)); continue
    if n in REPLACE:
        opts = REPLACE[n]
        new = opts[counter[n] % len(opts)]; counter[n] += 1
        s = size(new)
        slot = slots.get((x, z))
        if slot:                                    # exact facing from the lot marker
            rot = (slot[2] + int(P[new].get("RotationToFaceNorth", "2"))) % 4
            assert (slot[0], slot[1]) == (s[0], s[2]), f"{new} does not fit slot at {x},{z}"
        else:                                       # no slot: inherit, adjusting for RTFN
            rot = (r - 2 + int(P[new].get("RotationToFaceNorth", "2"))) % 4
        w, d = (s[2], s[0]) if rot % 2 else (s[0], s[2])
        X, Z = x + 4096, z + 4096
        if occ[Z:Z + d, X:X + w].any(): clashes.append((new, x, z))
        occ[Z:Z + d, X:X + w] = True
        out.append(ln.replace(f'name="{n}"', f'name="{new}"')
                     .replace(f'rotation="{r}"', f'rotation="{rot}"'))
        changed.append((n, new, x, z, r, rot, "slot" if slot else "inherited"))
        continue
    out.append(ln)

print(f"replaced: {len(changed)}   removed: {len(removed)}   total handled: {len(changed)+len(removed)}")
assert len(changed) + len(removed) == 19, "expected exactly 19 orphaned placements"
print(f"collisions introduced: {len(clashes)} {clashes}")
assert not clashes
print("\nreplacements:")
for a, b, x, z, ro, rn, how in changed:
    print(f"   {a:30} -> {b:28} X={x:6} Z={z:6}  rot {ro} -> {rn}  ({how})")
print("\nremoved:")
for n, x, z in removed:
    print(f"   {n:32} X={x:6} Z={z:6}")

shutil.copy2(XML, XML + ".BEFORE-ORPHAN-FIX")
open(XML, "wb").write(b"\xef\xbb\xbf" + "\r\n".join(out).encode("utf-8"))
print(f"\nwrote prefabs.xml  ({len(LINES)} -> {len(out)} lines)")
