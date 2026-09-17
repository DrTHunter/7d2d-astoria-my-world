"""Retire six of the eight starter bases (2026-09-17): drop every StarterBase_* placement except the Ranger Station and UFO Farm,
put the stock buildings they were cut from on the lowest-tier lots of the neighbouring towns, revert the terrain under the
removed builds to the original map, grade a 25x25 pad for the horde bunker beside the UFO Farm, and move the spawn there.
Reads the original Nexus world and the current Modded world, writes out/ next to this script. See docs/MY_PREFABS.md."""
import re, os, json, zlib, struct, hashlib, numpy as np
S = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(S, 'out')
ORIG = r"C:/Users/drtre/AppData/Roaming/Vortex/7daystodie/mods/Astoria 8K - Game Version 2.0 - Full World Map-7017-1-5-1751680868"
MOD  = r"C:/Users/drtre/AppData/Roaming/Vortex/7daystodie/mods/Astoria-8K-Complete/Worlds/Astoria 8K Modded"
KEEP = {'StarterBase_Ranger_Station', 'StarterBase_UFO_Farm'}
SWAPS = {  # (old name, x, z) -> new name ; same lot, same rotation (all RotationToFaceNorth=2)
    ('utility_refinery_02', 2368, -1224): 'hotel_03',
    ('farm_13', 2509, -1550): 'prison_01',
    ('house_old_gambrel_03', 2503, 132): 'house_modern_18',
    ('cabin_13', 2836, -325): 'house_modern_31',
    ('store_autoparts_01', 2594, -646): 'Modern_House_Zeebark',
    ('gas_station_09', 1843, -796): 'Ayesoar_Mansion_by_MPLogue',
}
BUNKER = (2473, -1021)          # 25x25, 7 m off the UFO farm's z=-990 edge, flat original ground
RANGER = (2426, 2495, -710, -632)   # x0,x1,z0,z1 inclusive, pad 58.25
REVERT = [(2258, 2503, -872, -585), (1971, 2279, -632, -319)]  # dtm diff clusters 6 and 7
R_RING = 13

# ---------------- prefabs.xml ----------------
raw = open(os.path.join(MOD, 'prefabs.xml'), 'rb').read()
nl = b'\r\n' if b'\r\n' in raw else b'\n'
lines = raw.split(nl)
pat = re.compile(rb'name="([^"]+)" position="(-?\d+),(-?\d+),(-?\d+)" rotation="(\d)"')
out, removed, swapped, ufo_idx = [], [], [], None
for ln in lines:
    m = pat.search(ln)
    if m:
        name = m.group(1).decode(); x, y, z = int(m.group(2)), int(m.group(3)), int(m.group(4))
        if name.startswith('StarterBase_') and name not in KEEP:
            removed.append(ln.decode().strip()); continue
        key = (name, x, z)
        if key in SWAPS:
            ln = ln.replace(b'name="%s"' % name.encode(), b'name="%s"' % SWAPS[key].encode(), 1)
            swapped.append((name, SWAPS[key], x, y, z, int(m.group(5))))
        if name == 'StarterBase_UFO_Farm': ufo_idx = len(out)
    out.append(ln)
assert ufo_idx is not None and len(swapped) == 6, (ufo_idx, swapped)
bunker_line = b'  <decoration type="model" name="StarterBase_Horde_Bunker" position="%d,57,%d" rotation="0" y_is_groundlevel="true" />' % BUNKER
out.insert(ufo_idx + 1, bunker_line)
open(os.path.join(OUT, 'prefabs.xml'), 'wb').write(nl.join(out))
n_dec = sum(1 for l in out if b'<decoration' in l)
print(f"prefabs.xml: removed {len(removed)} StarterBase decorations, swapped 6 lots, added 1 horde bunker -> {n_dec} decorations")
for s in swapped: print(f"   {s[0]:<22} -> {s[1]:<28} at {s[2]},{s[4]} rot{s[5]}")
json.dump({'removed': removed, 'swapped': swapped}, open(os.path.join(OUT, 'changes.json'), 'w'), indent=1)

# ---------------- dtm.raw ----------------
o = np.fromfile(os.path.join(ORIG, 'dtm.raw'), dtype='<u2').reshape(8192, 8192)
m = np.fromfile(os.path.join(MOD, 'dtm.raw'), dtype='<u2').reshape(8192, 8192)
new = m.copy()
def sl(x0, x1, z0, z1): return (slice(z0 + 4096, z1 + 4096 + 1), slice(x0 + 4096, x1 + 4096 + 1))
x0, x1, z0, z1 = RANGER
keep = np.zeros_like(o, dtype=bool); keep[sl(x0 - R_RING, x1 + R_RING, z0 - R_RING, z1 + R_RING)] = True
for box in REVERT:
    s = sl(*box); mask = ~keep[s]
    v = new[s]; v[mask] = o[s][mask]
print(f"dtm: reverted {int(((new != m) & ~keep).sum())} cells to the original in the two build zones")
# re-blend the ranger ring on the sides that now face original terrain (x <= 2495); east ramp to the city tile stays as graded
PAD = int(58.25 * 256)
zz, xx = np.mgrid[z0 - R_RING:z1 + R_RING + 1, x0 - R_RING:x1 + R_RING + 1]
kx = np.maximum(np.maximum(x0 - xx, xx - x1), 0); kz = np.maximum(np.maximum(z0 - zz, zz - z1), 0)
k = np.maximum(kx, kz)
ring = (k >= 1) & (xx <= x1)
t = k / R_RING
s = sl(x0 - R_RING, x1 + R_RING, z0 - R_RING, z1 + R_RING)
target = o[s].astype(float)                       # post-revert terrain = original on these sides
blend = PAD * (1 - t) + target * t
v = new[s]; v[ring] = np.round(blend[ring]).astype('<u2')
print(f"dtm: re-blended {int(ring.sum())} ring cells around the ranger station")
# horde bunker pad beside the UFO farm
bx, bz = BUNKER; BP = int(56.25 * 256); RB = 6
zz, xx = np.mgrid[bz - RB:bz + 24 + RB + 1, bx - RB:bx + 24 + RB + 1]
k = np.maximum(np.maximum(np.maximum(bx - xx, xx - (bx + 24)), 0), np.maximum(np.maximum(bz - zz, zz - (bz + 24)), 0))
s = sl(bx - RB, bx + 24 + RB, bz - RB, bz + 24 + RB); t = k / RB
cur = new[s].astype(float); blend = BP * (1 - t) + cur * t
v = new[s]; v[:] = np.round(blend).astype('<u2')
print(f"dtm: bunker pad {bx}..{bx+24},{bz}..{bz+24} at 56.25 m, {int((new[s] != m[s]).sum())} cells touched (max change {abs(new[s].astype(int)-m[s].astype(int)).max()/256:.2f} m)")
new.tofile(os.path.join(OUT, 'dtm.raw'))
diff = new != o
print(f"dtm: {int(diff.sum())} cells differ from the original map now (was {int((m != o).sum())})")
# seam check: max step between 4-neighbours inside a window around the ranger keep zone and the bunker
def maxstep(x0, x1, z0, z1, a):
    w = a[sl(x0, x1, z0, z1)].astype(int)
    return max(abs(np.diff(w, axis=0)).max(), abs(np.diff(w, axis=1)).max()) / 256
print(f"seam check, max step between neighbouring cells: ranger zone {maxstep(2400, 2515, -735, -607, new):.2f} m (original terrain there {maxstep(2400, 2515, -735, -607, o):.2f} m, modded before {maxstep(2400, 2515, -735, -607, m):.2f} m); bunker zone {maxstep(2460, 2510, -1035, -985, new):.2f} m")
print(f"hotel box now equals original: {bool((new[sl(2286,2412,-736,-613)] == o[sl(2286,2412,-736,-613)]).all())}; prison box: {bool((new[sl(2374,2486,-857,-749)] == o[sl(2374,2486,-857,-749)]).all())}; compound box: {bool((new[sl(1994,2245,-604,-387)] == o[sl(1994,2245,-604,-387)]).all())}")
print(f"ranger pad still flat 58.25: {bool((new[sl(*RANGER)] == PAD).all())}; UFO pad untouched: {bool((new[sl(2429,2497,-990,-916)] == m[sl(2429,2497,-990,-916)]).all())}")
# dtm.patch for world-patch (D2DT v1)
idx = np.flatnonzero(diff.ravel()).astype('<u4'); vals = new.ravel()[idx].astype('<u2')
blob = b'D2DT' + struct.pack('<II', 1, len(idx)) + idx.tobytes() + vals.tobytes()
open(os.path.join(OUT, 'dtm.patch'), 'wb').write(zlib.compress(blob, 9))

# ---------------- spawn ----------------
h = new.astype(float) / 256
best = None
for x in range(2420, 2500):
    for z in range(-1045, -993):
        if bx - 3 <= x + 3 and x - 3 <= bx + 27 and bz - 3 <= z + 3 and z - 3 <= bz + 27: continue
        w = h[sl(x - 3, x + 3, z - 3, z + 3)]; rng = w.max() - w.min()
        d = ((x - 2455) ** 2 + (z + 1003) ** 2) ** 0.5
        sc = rng * 20 + d
        if best is None or sc < best[0]: best = (sc, x, z, rng, w.mean())
_, sx, sz, rng, mean = best
print(f"spawn: {sx},{sz} - 7x7 patch is within {rng:.2f} m, ground {mean:.2f} m; {abs(sx-2463)} m from the farm centre line, bunker at {bx}..{bx+24},{bz}..{bz+24}")
open(os.path.join(OUT, 'spawnpoints.xml'), 'wb').write(
    ('\ufeff<?xml version="1.0" encoding="UTF-8"?>\r\n<spawnpoints>\r\n  <!-- single spawn: in front of StarterBase_UFO_Farm, beside the horde bunker -->\r\n'
     f'  <spawnpoint position="{sx},0,{sz}" rotation="0,0,0" />\r\n</spawnpoints>\r\n').encode('utf-8'))
json.dump({'spawn': [sx, sz], 'bunker': BUNKER}, open(os.path.join(OUT, 'sites.json'), 'w'))
for f in ('prefabs.xml', 'spawnpoints.xml', 'dtm.raw'):
    print(f"md5 {f}: {hashlib.md5(open(os.path.join(OUT, f), 'rb').read()).hexdigest()}")
