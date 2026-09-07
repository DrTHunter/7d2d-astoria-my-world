"""Move town-typed mod POIs out of the wilderness and into Astoria's junk city lots.

Rotation law, derived from 8,758 matched placements across Navezgane, the four
shipped Pregen worlds and Astoria itself:

    rotation = (marker_rotation + tile_rotation + RotationToFaceNorth) mod 4

Rebuilds prefabs.xml from prefabs.xml.ORIGINAL-BACKUP in a single pass.
"""
import os, re, json, math, collections

SP   = os.path.dirname(os.path.abspath(__file__))
W    = os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
DATA = r"C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\Data\Prefabs"
MODS = os.path.expandvars(r"%APPDATA%\7DaysToDie\Mods")
SRC  = os.path.join(W, "prefabs.xml.ORIGINAL-BACKUP")

# ---------------------------------------------------------------- prefab props
def read_props(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    d = {}
    for m in re.finditer(r'name="([A-Za-z0-9_]+)"\s+value="([^"]*)"', t):
        d.setdefault(m.group(1), m.group(2))
    return d

P, TILES = {}, {}
for root in (DATA, MODS):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith(".xml"):
                continue
            b = f[:-4]
            if not os.path.exists(os.path.join(dp, b + ".tts")):
                continue
            d = read_props(os.path.join(dp, f))
            P[b] = d
            if "POIMarkerStart" in d and "streettile" in (d.get("Tags") or ""):
                TILES[b] = d

def size(n):
    ps = P.get(n, {}).get("PrefabSize")
    if not ps:
        return None
    a, b, c = [int(v) for v in ps.split(",")]
    return a, b, c

def rtfn(n):
    return int(P.get(n, {}).get("RotationToFaceNorth", "2"))

# ---------------------------------------------------------------- world source
raw = open(SRC, encoding="utf-8-sig").read()   # universal newlines -> "\n" only
LINES = raw.split("\n")
LINE = re.compile(r'^.*<decoration[^>]*name="([^"]+)"\s+position="(-?\d+),(-?\d+),(-?\d+)"'
                  r'\s+rotation="(\d+)".*$', re.M)
placements = []          # (name, x, y, z, rot, full_line)
for m in LINE.finditer(raw):
    placements.append((m.group(1), int(m.group(2)), int(m.group(3)),
                       int(m.group(4)), int(m.group(5)), m.group(0)))
print(f"source decorations: {len(placements)}")

# ------------------------------------------------------- lot slots from tiles
def trip(s):
    return [tuple(int(v) for v in g.split(",")) for g in s.split("#")]

def to_world(S, X, Z, k, mx, mz, sw, sd):
    if k == 0: return X + mx,             Z + mz,             sw, sd
    if k == 2: return X + (S - mx - sw),  Z + (S - mz - sd),  sw, sd
    if k == 1: return X + (S - mz - sd),  Z + mx,             sd, sw
    return           X + mz,              Z + (S - mx - sw),  sd, sw

slots = {}                                    # (x,z) -> dict
for n, x, y, z, r, _ in placements:
    d = TILES.get(n)
    if not d:
        continue
    S = trip(d["PrefabSize"])[0][0]
    st, sz = trip(d["POIMarkerStart"]), trip(d["POIMarkerSize"])
    rots = [int(v) for v in d["POIMarkerPartRotations"].split(",")]
    typ  = d["POIMarkerType"].split(",")
    for i, (mk, s) in enumerate(zip(st, sz)):
        if typ[i].strip() != "POISpawn":
            continue
        wx, wz, ww, wd = to_world(S, x, z, r, mk[0], mk[2], s[0], s[2])
        if ww != wd:
            continue
        slots[(wx, wz)] = {"w": ww, "d": wd, "srot": (rots[i] + r) % 4,
                           "tile": n, "tx": x, "tz": z}
print(f"resolved lot slots: {len(slots)}")

occ = collections.defaultdict(list)
for n, x, y, z, r, ln in placements:
    if n not in TILES and not n.startswith("part_"):
        occ[(x, z)].append((n, y, r, ln))

JUNK = re.compile(r'^(remnant_|rubble_|lot_)', re.I)
open_lots = collections.defaultdict(list)     # size -> [slot dicts]
for (x, z), s in slots.items():
    for n, y, r, ln in occ.get((x, z), []):
        sz_ = size(n)
        if not sz_ or sz_[0] != s["w"] or sz_[2] != s["d"]:
            continue
        if not JUNK.match(n):
            continue
        open_lots[s["w"]].append(dict(s, x=x, z=z, occ=n, y=y, line=ln))
for k in sorted(open_lots):
    print(f"   junk lots {k}x{k}: {len(open_lots[k])}")

# 100x100 Tier-0 remnants have no marker slot; use the inheritance form of the law
big = []
for n, x, y, z, r, ln in placements:
    sz_ = size(n)
    if sz_ and (sz_[0], sz_[2]) == (100, 100) and JUNK.match(n):
        big.append({"x": x, "z": z, "y": y, "occ": n, "orot": r, "line": ln})
print(f"   100x100 junk remnants: {len(big)}")

# ------------------------------------------------------------ the 122 mod POIs
pl = json.load(open(os.path.join(SP, "placements_numbered.json")))
TOWN = {"downtown", "commercial", "industrial", "residential",
        "countryresidential", "countrytown", "rpd", "kendo", "culdesac"}
PREF = [("downtown",          ["downtown", "commercial"]),
        ("rpd",               ["commercial", "downtown"]),
        ("kendo",             ["countrytown", "commercial"]),
        ("commercial",        ["commercial", "downtown"]),
        ("industrial",        ["industrial", "commercial"]),
        ("countryresidential",["countryresidential", "countrytown", "residential"]),
        ("countrytown",       ["countrytown", "residential", "commercial"]),
        ("culdesac",          ["residential"]),
        ("residential",       ["residential", "countryresidential"])]

town, wild = [], []
for p in pl:
    tags = {t.strip().lower() for t in (P.get(p["name"], {}).get("Tags") or "").split(",")}
    w, _, d = size(p["name"])
    if (tags & TOWN) and w == d:
        p["tags"] = tags
        town.append(p)
    else:
        wild.append(p)
town.sort(key=lambda q: -q["w"])
print(f"\ntown-typed & square: {len(town)}   staying wild: {len(wild)}")

# ----------------------------------------------------------------- assignment
used_tiles = collections.Counter()
taken = set()
chosen, unplaced = [], []
bigq = sorted(big, key=lambda b: (b["x"], b["z"]))

for p in town:
    w = p["w"]
    if w == 100:
        if not bigq:
            unplaced.append(p); continue
        b = bigq.pop(0)
        rot = (b["orot"] - rtfn(b["occ"]) + rtfn(p["name"])) % 4
        chosen.append({**p, "x": b["x"], "y": b["y"], "z": b["z"], "rot": rot,
                       "occ": b["occ"], "line": b["line"], "tile": "(remnant swap)",
                       "how": "inherited"})
        continue
    prefs = []
    for tag, order in PREF:
        if tag in p["tags"]:
            prefs = order; break
    pool = [s for s in open_lots.get(w, []) if (s["x"], s["z"]) not in taken]
    pick = None
    for pref in prefs + [None]:
        cand = [s for s in pool if pref is None or ("rwg_tile_" + pref) in s["tile"]]
        cand = [s for s in cand if used_tiles[(s["tx"], s["tz"])] < 1]
        if not cand:
            continue
        # spread: maximise distance to already-chosen new POIs
        def score(s):
            if not chosen:
                return 0
            return -min((s["x"] - c["x"]) ** 2 + (s["z"] - c["z"]) ** 2 for c in chosen)
        cand.sort(key=score)
        pick = cand[0]; break
    if not pick:
        unplaced.append(p); continue
    taken.add((pick["x"], pick["z"]))
    used_tiles[(pick["tx"], pick["tz"])] += 1
    rot = (pick["srot"] + rtfn(p["name"])) % 4
    chosen.append({**p, "x": pick["x"], "y": pick["y"], "z": pick["z"], "rot": rot,
                   "occ": pick["occ"], "line": pick["line"], "tile": pick["tile"],
                   "how": "slot"})

print(f"assigned into town lots: {len(chosen)}   could not place: {len(unplaced)}")
if unplaced:
    print("   ", [u["name"] for u in unplaced])
wild += unplaced

extrap = [c["name"] for c in chosen if rtfn(c["name"]) == 1]
print(f"\nplacements relying on the unobserved RTFN=1 case: {len(extrap)}")
for n in extrap:
    print("   ", n)

# ---------------------------------------------------------------- emit new xml
from xml.sax.saxutils import escape as esc
drop = {c["line"] for c in chosen}
assert len(drop) == len(chosen), "a filler line was targeted twice"
out = [ln for ln in LINES if ln not in drop]
removed = len(LINES) - len(out)
print(f"\nfiller lines removed: {removed}")
assert removed == len(chosen), f"expected to remove {len(chosen)} filler lines, removed {removed}"

MODNAME = {"AAA": "MPLogue Prefabs", "AAB": "Voltralux POI Pack", "AAC": "Zeebark POI Pack",
           "AAD": "WinterDawn Fortress", "AAF": "Svarii POI Package", "AAG": "Caleseche",
           "AAH": "ShadowModernHouse", "AAI": "Cog's POIs"}

def block(title, items):
    L = ["  <!-- ===== %s ===== -->" % title]
    for mod in sorted({i["mod"] for i in items}):
        g = sorted([i for i in items if i["mod"] == mod], key=lambda q: q["name"])
        L.append("  <!-- %s (%d) -->" % (MODNAME.get(mod, mod), len(g)))
        for i in g:
            L.append('  <decoration type="model" name="%s" position="%d,%d,%d" '
                     'rotation="%d" y_is_groundlevel="true" />'
                     % (esc(i["name"]), i["x"], i["y"], i["z"], i["rot"]))
    return L

body = block("MOD POI PACKS - town lots (%d), replacing Tier-0 filler" % len(chosen), chosen)
body += block("MOD POI PACKS - wilderness (%d)" % len(wild), wild)
i = max(j for j, ln in enumerate(out) if "</prefabs>" in ln)
out[i:i] = body
open(os.path.join(W, "prefabs.xml"), "wb").write(
    b"\xef\xbb\xbf" + "\r\n".join(out).encode("utf-8"))

def plain(items):
    return [{k: (sorted(v) if isinstance(v, set) else v) for k, v in i.items()} for i in items]
json.dump(plain(chosen), open(os.path.join(SP, "town_placements.json"), "w"), indent=1)
json.dump(plain(wild),   open(os.path.join(SP, "wild_placements.json"), "w"), indent=1)
print(f"wrote prefabs.xml  ({len(chosen)} in town, {len(wild)} in the wild)")
