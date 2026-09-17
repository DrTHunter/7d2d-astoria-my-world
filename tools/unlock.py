#!/usr/bin/env python3
"""Unlock every door, gate and safe in a folder of prefabs.

    python tools/unlock.py <prefab dir> [<prefab dir> ...] [--apply] [--blocks blocks.xml ...]

Two things keep a player out of a POI block, and they live in different places:

  Doors and gates (TEFeatureLockable) carry their lock in the prefab's tile-entity
  list - a bool in the Lockable feature record. The prefab editor writes 1 for a
  door it locked; a door with no record at all is unlocked. The bool is set to 0.

  Safes, chests and ATMs (TEFeatureLockPickable) are locked by the block itself,
  no record involved - the game locks them when the POI is placed. The only
  unlocked form is the block the game leaves behind after a successful lockpick,
  its DowngradeBlock (cntGunSafe -> cntGunSafeInsecure). Same model, same loot
  list, no lock. The block is swapped and the name added to the .blocks.nim.

Trailer layout of a V2.0 .tts after the block arrays, as far as this needs it:
  uint16[water]   one mass per set bit in the second flag plane
  uint16 count    tile entities, then per entity: uint16 len, byte type, byte[len]
  ...             whatever follows is carried through untouched
Inside a Composite (type 25) entity the Lockable feature is found by its id:
  2a 4a 24 ae | 0c 00 00 00 | 12 00 | isLocked | ...
"""
import os, sys, struct, glob, argparse
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tts import Prefab, Nim, btype, brot, bmeta, bval

LOCKABLE_SIG = bytes.fromhex('2a4a24ae0c0000001200')
COMPOSITE = 25
STOCK_BLOCKS = r"C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\Data\Config\blocks.xml"


def load_blocks(paths):
    """name -> (features, downgrade). Extends inherits by property path, minus what param1 excludes."""
    raw = {}
    for path in paths:
        for b in ET.parse(path).getroot().iter('block'):
            nm = b.get('name')
            if not nm:
                continue
            ext = down = None
            feats, drop = set(), set()
            for pr in b.findall('property'):
                if pr.get('name') == 'Extends':
                    ext = pr.get('value')
                    # param1 names the parent properties NOT to inherit, e.g. CompositeFeatures.TEFeatureLockPickable
                    drop = {x.split('.', 1)[1] for x in (pr.get('param1') or '').split(',') if x.startswith('CompositeFeatures.')}
                elif pr.get('name') == 'DowngradeBlock':
                    down = pr.get('value')
                elif pr.get('class') == 'CompositeFeatures':
                    feats = {f.get('class') for f in pr.findall('property') if f.get('class')}
            raw[nm] = (ext, feats, down, drop)
    out = {}

    def resolve(nm, seen=()):
        if nm in out:
            return out[nm]
        ext, feats, down, drop = raw.get(nm, (None, set(), None, set()))
        if ext and ext not in seen:
            pf, pd = resolve(ext, seen + (nm,))
            feats = feats | (pf - drop)
            down = down or pd
        out[nm] = (feats, down)
        return out[nm]

    for nm in raw:
        resolve(nm)
    return out


def split_trailer(p):
    tr = p.trailer
    lead = sum(bin(b).count('1') for b in p.bitB) * 2
    cnt, = struct.unpack_from('<H', tr, lead)
    o = lead + 2
    recs = []
    for _ in range(cnt):
        ln, ty = struct.unpack_from('<HB', tr, o)
        recs.append([ty, bytearray(tr[o + 3:o + 3 + ln])])
        o += 3 + ln
    return tr[:lead], recs, tr[o:]


def join_trailer(lead, recs, tail):
    out = bytearray(lead) + struct.pack('<H', len(recs))
    for ty, pl in recs:
        out += struct.pack('<HB', len(pl), ty) + pl
    return bytes(out) + tail


def unlock_prefab(tts_path, blocks, apply):
    p = Prefab(tts_path)
    nim_path = tts_path[:-4] + '.blocks.nim'
    nim = Nim(nim_path)
    id2name = nim.id2name
    name2id = nim.name2id
    lead, recs, tail = split_trailer(p)
    assert join_trailer(lead, recs, tail) == p.trailer, tts_path

    doors_unlocked, doors_already, swapped, unknown = [], 0, {}, set()

    for ty, pl in recs:
        if ty != COMPOSITE:
            continue
        x, y, z = struct.unpack_from('<iii', pl, 2)
        name = id2name.get(btype(p.at(x, y, z)))
        feats, _ = blocks.get(name, (set(), None))
        if 'TEFeatureLockable' not in feats:
            continue
        k = pl.find(LOCKABLE_SIG)
        if k < 0 or pl[k + 10] not in (0, 1):
            unknown.add(name)
            continue
        if pl[k + 10] == 1:
            pl[k + 10] = 0
            doors_unlocked.append((name, x, y, z))
        else:
            doors_already += 1

    next_id = max(id2name) + 1
    for i, v in enumerate(p.blocks):
        name = id2name.get(btype(v))
        if not name:
            continue
        feats, down = blocks.get(name, (set(), None))
        if 'TEFeatureLockPickable' not in feats:
            continue
        target = down
        while target and 'TEFeatureLockPickable' in blocks.get(target, (set(), None))[0]:
            target = blocks[target][1]
        if not target:
            unknown.add(name)
            continue
        if target not in name2id:
            name2id[target] = next_id
            id2name[next_id] = target
            next_id += 1
        p.blocks[i] = bval(name2id[target], brot(v), bmeta(v))
        swapped[(name, target)] = swapped.get((name, target), 0) + 1

    if apply and (doors_unlocked or swapped):
        p.trailer = join_trailer(lead, recs, tail)
        p.save(tts_path)
        nim.save(nim_path, {btype(v) for v in p.blocks if btype(v)})
    return doors_unlocked, doors_already, swapped, unknown


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dirs', nargs='+')
    ap.add_argument('--apply', action='store_true', help='write the files (default: report only)')
    ap.add_argument('--blocks', action='append', default=[],
                    help='blocks.xml to read; default is the stock one. Pass a mod\'s Config/blocks.xml too if the prefabs use its blocks')
    ap.add_argument('--glob', default='*.tts')
    a = ap.parse_args()
    blocks = load_blocks([STOCK_BLOCKS] + a.blocks)
    total_doors = total_swaps = 0
    for d in a.dirs:
        for f in sorted(glob.glob(os.path.join(d, a.glob))):
            doors, already, swaps, unknown = unlock_prefab(f, blocks, a.apply)
            if not (doors or swaps or unknown):
                continue
            n = sum(swaps.values())
            total_doors += len(doors)
            total_swaps += n
            print(f"{os.path.basename(f)[:-4]}: {len(doors)} doors unlocked ({already} were open already), {n} safes swapped")
            for (src, dst), c in sorted(swaps.items()):
                print(f"    {c} x {src} -> {dst}")
            for u in sorted(unknown):
                print(f"    !! could not unlock {u}")
    print(f"\n{'wrote' if a.apply else 'would write'}: {total_doors} doors unlocked, {total_swaps} safes swapped")


if __name__ == '__main__':
    main()
