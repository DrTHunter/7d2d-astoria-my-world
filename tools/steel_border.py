"""Upgrade the Ranger Station's perimeter fence to steel, keeping its look.

chain-link segments -> steelShapes:barsCentered (same axis), corners and posts -> steelShapes:poleCentered,
corrugated-sheet panels -> steelShapes:<same shape> painted Corrugated_metal (paint 57) where they were
unpainted, existing paint kept. Gate, pedestrian door and barbed wire are left as they are.

    python steel_border.py            # report only
    python steel_border.py --apply    # write out2/StarterBase_Ranger_Station.{tts,blocks.nim}
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tts import Prefab, Nim, btype, brot, bmeta, bval
SRC = r"C:/Users/drtre/AppData/Roaming/Vortex/7daystodie/mods/Astoria-8K-Complete/Prefabs/POIs/"   # the Modded mod's prefab folder
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out2'); os.makedirs(OUT, exist_ok=True)
NAME = 'StarterBase_Ranger_Station'
PAINT_CORRUGATED = 57
EXCLUDE = [(21, 33, 24, 36), (37, 45, 49, 54)]   # x0,x1,z0,z1: the pen inside the yard, the shed by the south-east fence
KEEP = ('chainlinkGateDoubleWide', 'chainlinkFenceDoor')
WALL_SHAPES = {'billboard', 'shantywall02', 'shantywall03', 'shantywall04', 'pillar0.05'}
apply = '--apply' in sys.argv

p = Prefab(SRC + NAME + '.tts'); nim = Nim(SRC + NAME + '.blocks.nim')
name2id = nim.name2id
def name(v): return nim.id2name.get(btype(v), '') if btype(v) else ''
def excluded(x, z): return any(x0 <= x <= x1 and z0 <= z <= z1 for x0, x1, z0, z1 in EXCLUDE)

chain, cols = [], set()
for z in range(p.sz):
    for y in range(p.sy):
        for x in range(p.sx):
            n = name(p.at(x, y, z))
            if n.startswith('chainlink') and not excluded(x, z):
                chain.append((x, y, z)); cols.add((x, z))
panels = []
for z in range(p.sz):
    for y in range(p.sy):
        for x in range(p.sx):
            n = name(p.at(x, y, z))
            if n.startswith('corrugatedMetalShapes:') and n.split(':')[1] in WALL_SHAPES and not excluded(x, z) and \
               any((x + dx, z + dz) in cols for dx in (-1, 0, 1) for dz in (-1, 0, 1)):
                panels.append((x, y, z))

print(f"border: {len(chain)} chain-link blocks on {len(cols)} columns, {len(panels)} corrugated panel blocks")
print("chain-link by name:", dict(collections.Counter(name(p.at(*c)) for c in chain)))
print("panels by shape:", dict(collections.Counter(name(p.at(*c)).split(':')[1] for c in panels)))
skipped = collections.Counter()
for z in range(p.sz):
    for y in range(p.sy):
        for x in range(p.sx):
            n = name(p.at(x, y, z))
            if n.startswith('corrugatedMetalShapes:') and n.split(':')[1] not in WALL_SHAPES and not excluded(x, z) and any((x + dx, z + dz) in cols for dx in (-1, 0, 1) for dz in (-1, 0, 1)):
                skipped[(n.split(':')[1], x, z)] += 1
print("touching the fence but left alone (shape, x, z):", sorted(skipped))
print("panels already painted:", sum(1 for c in panels if p.idx(*c) in p.tex), "of", len(panels))

# id table additions
def get_id(n):
    if n in name2id: return name2id[n]
    i = max(nim.id2name) + 1
    assert i < 65536
    nim.id2name[i] = n; name2id[n] = i; return i
BARS = get_id('steelShapes:barsCentered'); POLE = get_id('steelShapes:poleCentered')

conv = collections.Counter()
for (x, y, z) in chain:
    i = p.idx(x, y, z); v = p.blocks[i]; n = name(v); r = brot(v) % 4
    if n in KEEP: conv['kept ' + n] += 1; continue
    if 'Corner' in n or n.startswith('chainlinkFencePole'):
        p.blocks[i] = bval(POLE, 0, 0); conv[n + ' -> steelShapes:poleCentered'] += 1
    else:
        axis_rot = 0 if r in (0, 2) else 1          # chain-link rot 0/2 runs along x, 1/3 along z; same for bars
        p.blocks[i] = bval(BARS, axis_rot, 0); conv[n + ' -> steelShapes:barsCentered'] += 1
    p.damage[i] = 0
painted_new = 0
for (x, y, z) in panels:
    i = p.idx(x, y, z); v = p.blocks[i]; n = name(v)
    shape = n.split(':')[1]; nid = get_id('steelShapes:' + shape)
    p.blocks[i] = bval(nid, brot(v), bmeta(v)); p.damage[i] = 0
    if i not in p.tex:
        p.tex[i] = bytes([PAINT_CORRUGATED] * 6) + b'\x00\x00'; painted_new += 1
    conv[n + ' -> steelShapes:' + shape] += 1
print("\nconversions:")
for k, c in sorted(conv.items()): print(f"  {c:4d}  {k}")
print(f"panels newly painted Corrugated_metal: {painted_new}")

# map of the result at y=5 and y=7
def ch(v):
    n = name(v)
    if not n: return '.'
    if n.startswith('steelShapes:bars'): return 'S'
    if n.startswith('steelShapes:pole'): return 'o'
    if n.startswith('steelShapes:'): return 's'
    if 'chainlink' in n: return 'C'
    if n.startswith('corrugatedMetal'): return 'M'
    if 'barbed' in n.lower(): return 'X'
    if n.startswith(('terr', 'tree')): return ','
    return '#'
for y in (5, 7):
    print(f"--- y={y}: S steel bars, o steel post, s steel panel, C chain-link left, M corrugated left, X barbed wire ---")
    for z in range(p.sz): print(f"{z:3d} " + ''.join(ch(p.at(x, y, z)) for x in range(p.sx)))

if apply:
    p.save(os.path.join(OUT, NAME + '.tts'))
    used = {btype(v) for v in p.blocks if btype(v)}
    nim.save(os.path.join(OUT, NAME + '.blocks.nim'), used)
    q = Prefab(os.path.join(OUT, NAME + '.tts')); n2 = Nim(os.path.join(OUT, NAME + '.blocks.nim'))
    assert (q.sx, q.sy, q.sz) == (p.sx, p.sy, p.sz) and q.blocks == p.blocks and q.tex == p.tex and q.trailer == p.trailer
    assert all(btype(v) in n2.id2name for v in q.blocks if btype(v))
    print(f"\nwritten to {OUT}: re-read OK, {len(n2.id2name)} names in the id table, "
          f"{sum(1 for n in n2.id2name.values() if 'chainlink' in n)} chain-link names still referenced")
