#!/usr/bin/env python3
"""
Bring the compound fence up to the seed capture (LocalPrefabs/Fence-part).

The walls were already cut from the Modern House's own fence, so the blocks and
the profile were right, but the script that emitted them wrote no paint layer,
left the bar course open over every vehicle gate, and parked the gatehouse a
long way from the gate it is meant to watch. This fixes those three things in
place. Prefab dimensions never change, so nothing in prefabs.xml moves and the
terrain patch still fits.

    python tools/refence.py --in <prefab dir> --out <prefab dir>
"""
import os
import sys
import shutil
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tts import Prefab, Nim, btype, brot, bval          # noqa: E402

# The seed paints every face of a fence block with a single texture id: brick
# piers 0x3f, the half-brick panels 0x32, every piece of metal 0x18, caps 0x32.
PAINT = {
    'brickShapes:cube':                     b'\x3f' * 6,
    'brickShapes:cubeHalfCentered':         b'\x32' * 6,
    'brickShapes:cubeBaseboard4Sided':      b'\x3f\x32\x3f\x3f\x3f\x3f',
    'corrugatedMetalShapes:windowCentered': b'\x18' * 6,
    'corrugatedMetalShapes:plate':          b'\x18' * 6,
    'corrugatedMetalShapes:doorTrim1m':     b'\x18' * 6,
    'ironBarsCentered':                     b'\x18' * 6,
    'ironBars':                             b'\x18' * 6,
    'steelShapes:securityGateCentered':     b'\x18' * 6,
    'concreteShapes:pillar100Cap':          b'\x32\x00\x00\x00\x00\x00',
    'concreteShapes:plate':                 b'\x32' * 6,
    'concreteShapes:cube':                  b'\x32' * 6,
    'concreteShapes:cubeHalfCentered':      b'\x32' * 6,
}
GATE = 'steelGarageDoor5x3Black'
FENCE = set(PAINT) | {GATE}
SPACING = 6          # piers every six blocks

# Entrance furniture, lifted from the seed's security post with the game's own
# block ids. The wall prefabs never used these, so they have to be added to the
# name table before they can be placed.
FURNITURE = {
    'signPrivateProperty': 24614,
    'signStaffOnly': 24786,
    'signMiscBewareOfDog': 24793,
    'industrialLight01': 20353,
    'motionsensorPOI': 20123,
    'steelShapes:securityGateCentered': 11733,
    'concreteShapes:plate': 7517,
}


class Wall:
    """One wall strip: a fence line running along x at a fixed z."""

    def __init__(self, stem):
        self.stem = stem
        self.p = Prefab(stem + '.tts')
        self.nim = Nim(stem + '.blocks.nim')
        self.name = self.nim.id2name
        self.id = self.nim.name2id
        p = self.p
        self.zl = max(range(p.sz), key=lambda z: sum(
            1 for x in range(p.sx) for y in range(p.sy)
            if self.name.get(btype(p.at(x, y, z)), '') in FENCE))
        self.y0 = self._first_course()
        self.phase = None

    def _first_course(self):
        for y in range(self.p.sy):
            if any(self.nm(x, y) == 'brickShapes:cubeHalfCentered'
                   for x in range(self.p.sx)):
                return y
        raise SystemExit(f'{self.stem}: no panel course found')

    def nm(self, x, y, z=None):
        return self.name.get(btype(self.p.at(x, y, self.zl if z is None else z)), '')

    def set(self, x, y, z, raw):
        self.p.blocks[self.p.idx(x, y, z)] = raw

    def clear(self, x, y, z):
        self.p.blocks[self.p.idx(x, y, z)] = 0
        self.p.tex.pop(self.p.idx(x, y, z), None)

    def piers(self):
        bid = self.id['brickShapes:cube']
        return [x for x in range(self.p.sx)
                if btype(self.p.at(x, self.y0, self.zl)) == bid]

    def gates(self):
        gid = self.id.get(GATE)
        if gid is None:
            return []
        return sorted(i % self.p.sx for i, v in enumerate(self.p.blocks)
                      if btype(v) == gid)

    def gatehouse(self):
        """x-range of everything that lives off the fence line."""
        xs = [x for x in range(self.p.sx) for y in range(self.p.sy)
              for z in range(self.p.sz)
              if z != self.zl and btype(self.p.at(x, y, z)) != 0
              and not self.name.get(btype(self.p.at(x, y, z)), '').startswith('terr')]
        return (min(xs), max(xs)) if xs else None

    def open_runs(self):
        """x-ranges where the fence line is empty top to bottom - the doorways
        the seven SecurityPost prefabs drop into. Never build over one."""
        empty = [all(btype(self.p.at(x, self.y0 + k, self.zl)) == 0 for k in range(4))
                 for x in range(self.p.sx)]
        runs, i = [], 0
        while i < len(empty):
            if empty[i]:
                j = i
                while j < len(empty) and empty[j]:
                    j += 1
                if j - i >= 8:                 # a gate opening is only 5 wide
                    runs.append((i, j - 1))
                i = j
            else:
                i += 1
        return runs


def paint(w):
    """Give every fence block the seed's paint."""
    n = 0
    for i, v in enumerate(w.p.blocks):
        rec = PAINT.get(w.name.get(btype(v), ''))
        if rec and i not in w.p.tex:
            w.p.tex[i] = rec + b'\x00\x00'
            n += 1
    return n


def close_over_gates(w):
    """Carry the top bar course across each gate opening."""
    bars = w.id['ironBarsCentered']
    y = w.y0 + 3
    fixed = 0
    for gx in w.gates():
        rot = None
        for probe in range(max(0, gx - 12), min(w.p.sx, gx + 13)):
            if w.nm(probe, y) == 'ironBarsCentered':
                rot = brot(w.p.at(probe, y, w.zl))
                break
        if rot is None:
            continue
        for x in range(gx - 2, gx + 3):
            if 0 <= x < w.p.sx and btype(w.p.at(x, y, w.zl)) == 0:
                w.set(x, y, w.zl, bval(bars, rot))
                fixed += 1
    return fixed


PIER = ['brickShapes:cube', 'brickShapes:cube', 'brickShapes:cube',
        'brickShapes:cubeBaseboard4Sided', 'concreteShapes:pillar100Cap']
PANEL = ['brickShapes:cubeHalfCentered', 'corrugatedMetalShapes:windowCentered',
         'ironBarsCentered', 'ironBarsCentered', None]


def course_rotations(w):
    """The rotation each course uses, read off the wall's own untouched fence."""
    rot = {}
    piers = set(w.piers())
    for x in range(w.p.sx):
        kind = 'pier' if x in piers else 'panel'
        for k, want in enumerate(PIER if kind == 'pier' else PANEL):
            if want and w.nm(x, w.y0 + k) == want:
                rot.setdefault((kind, k), brot(w.p.at(x, w.y0 + k, w.zl)))
    return rot


def lay_fence(w, xa, xb, anchor, rot):
    """Fill x in [xa, xb] with fence, piers on the grid running through anchor.

    A gate's five-block footprint is never touched: dropping a pier into it
    would wall the roll-up door in.
    """
    reserved = {x for g in w.gates() for x in range(g - 2, g + 3)}
    for x in range(xa, xb + 1):
        if x in reserved:
            continue
        for z in range(w.p.sz):
            for y in range(w.p.sy):
                v = w.p.at(x, y, z)
                if btype(v) and not w.name.get(btype(v), '').startswith('terr'):
                    w.clear(x, y, z)
        kind = 'pier' if (x - anchor) % SPACING == 0 else 'panel'
        for k, nmv in enumerate(PIER if kind == 'pier' else PANEL):
            if nmv is None:
                continue
            w.set(x, w.y0 + k, w.zl, bval(w.id[nmv], rot.get((kind, k), 0)))


def move_gatehouse(w):
    """Slide the gatehouse along the wall so it stands beside the gate.

    The module carries its own stretch of fence line, and in the wall it was cut
    from it starts one block past a pier. So the only candidate positions are
    'one block past an existing pier', which keeps the grid in step; whatever it
    leaves over before the next pier is laid back as plain fence.
    """
    gh, gates = w.gatehouse(), w.gates()
    if not gh or not gates:
        return None
    x0, x1 = gh
    width = x1 - x0 + 1
    gx = gates[0]
    piers = w.piers()
    blocked = w.open_runs()
    rot = course_rotations(w)
    left_pier = max((p for p in piers if p < x0), default=x0 - 1)

    best = None
    for p in piers:
        start, end = p + 1, p + width
        if start < 1 or end > w.p.sx - 2:
            continue
        if end >= gx - 3 and start <= gx + 3:
            continue                       # would sit on the gate itself
        if any(start <= b and a <= end + 2 for a, b in blocked):
            continue                       # a SecurityPost doorway
        if any(start - 3 <= g <= end + 3 for g in gates[1:]):
            continue
        gap = start - (gx + 3) if start > gx else (gx - 3) - end
        if gap < 0:
            continue
        if best is None or gap < best[0]:
            best = (gap, p)
    if best is None or best[1] + 1 == x0:
        return None
    anchor = best[1]
    newx = anchor + 1
    src = {}
    for x in range(x0, x1 + 1):
        for y in range(w.p.sy):
            for z in range(w.p.sz):
                i = w.p.idx(x, y, z)
                src[(x - x0, y, z)] = (w.p.blocks[i], w.p.tex.get(i))
    lay_fence(w, x0, x1, left_pier, rot)
    for (dx, y, z), (raw, tex) in src.items():
        i = w.p.idx(newx + dx, y, z)
        w.p.blocks[i] = raw
        if tex is not None:
            w.p.tex[i] = tex
        else:
            w.p.tex.pop(i, None)
    # tidy the join between the module's far end and the next pier
    tail_end = newx + width - 1
    nxt = anchor + SPACING * ((width + SPACING) // SPACING)
    while nxt <= tail_end:
        nxt += SPACING
    if nxt < w.p.sx:
        lay_fence(w, tail_end + 1, min(nxt, w.p.sx - 1), anchor, rot)
    return (x0, x1, newx, tail_end)


def dress_gates(w):
    """Make each vehicle gate read as a portal, the way the seed's entrance does.

    A cast lintel across the cap course ties the two flanking piers together,
    the seed's ornamental steel gate panels go on the reveals, and the signs,
    light and sensor from its security post go on the outside face.
    """
    y0, zl = w.y0, w.zl
    zo = zl - 1                 # outside face; 1-deep strips have none
    zi = zl + 1 if zl + 1 < w.p.sz else None
    put = 0
    rot = course_rotations(w)
    for gx in w.gates():
        # both reveals stand as full capped piers, so the lintel has something
        # to spring from and the opening reads the same from either side
        for x in (gx - 3, gx + 3):
            if not (0 <= x < w.p.sx):
                continue
            if not all(w.nm(x, y0 + k) == PANEL[k] for k in range(4)):
                continue                    # a gatehouse wall - leave it alone
            for k, nmv in enumerate(PIER):
                w.set(x, y0 + k, zl, bval(w.id[nmv], rot.get(('pier', k), 0)))
            put += 1
        # lintel over the opening, in the pier caps' own material
        for x in range(gx - 2, gx + 3):
            if 0 <= x < w.p.sx and btype(w.p.at(x, y0 + 4, zl)) == 0:
                w.set(x, y0 + 4, zl, bval(w.id['concreteShapes:plate'], 0))
                put += 1
        # ornamental steel panels on the reveals, as on the seed's booth
        if zi is not None:
            for dx in (-3, 3):
                x = gx + dx
                if not (0 <= x < w.p.sx):
                    continue
                for k in (0, 1):
                    if btype(w.p.at(x, y0 + k, zi)) == 0:
                        w.set(x, y0 + k, zi,
                              bval(w.id['steelShapes:securityGateCentered'], 0))
                        put += 1
        if zo is None or zo < 0:
            continue
        for dx, y, nmv in ((-3, y0,     'signPrivateProperty'),
                           (-3, y0 + 1, 'signMiscBewareOfDog'),
                           (+3, y0,     'signStaffOnly'),
                           (+3, y0 + 1, 'industrialLight01'),
                           (+4, y0 + 1, 'motionsensorPOI')):
            x = gx + dx
            if not (0 <= x < w.p.sx) or nmv not in w.id:
                continue
            if btype(w.p.at(x, y, zo)) != 0:
                continue
            w.set(x, y, zo, bval(w.id[nmv], 3))
            put += 1
    return put


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='src', required=True)
    ap.add_argument('--out', dest='dst', required=True)
    ap.add_argument('--only', default='')
    a = ap.parse_args()
    os.makedirs(a.dst, exist_ok=True)
    stems = sorted({f.rsplit('.', 1)[0].replace('.blocks', '')
                    for f in os.listdir(a.src) if f.endswith('.tts') and 'Wall' in f})
    for stem in stems:
        if a.only and a.only not in stem:
            continue
        w = Wall(os.path.join(a.src, stem))
        for nmv, bid in FURNITURE.items():          # so they can be placed
            w.nim.id2name.setdefault(bid, nmv)
        w.name = w.nim.id2name
        w.id = w.nim.name2id
        painted = paint(w)
        closed = close_over_gates(w)
        moved = move_gatehouse(w)
        dressed = dress_gates(w)
        painted += paint(w)
        for ext in ('.xml', '.ins'):
            src = os.path.join(a.src, stem + ext)
            if os.path.exists(src):
                shutil.copyfile(src, os.path.join(a.dst, stem + ext))
        used = {btype(v) for v in w.p.blocks}
        missing = used - set(w.nim.id2name)
        if missing:
            raise SystemExit(f'{stem}: block ids with no name: {sorted(missing)}')
        w.nim.save(os.path.join(a.dst, stem + '.blocks.nim'), used)
        w.p.save(os.path.join(a.dst, stem + '.tts'))
        print(f'{stem:34s} course y={w.y0} painted={painted:5d} '
              f'closed={closed:2d} dressed={dressed:2d} gatehouse={moved}')


if __name__ == '__main__':
    main()
