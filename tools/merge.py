"""Merge town + wilderness placements, rebuild the occupancy mask, write the report."""
import os, re, json, numpy as np

SP   = os.path.dirname(os.path.abspath(__file__))
W    = os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
DATA = r"C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\Data\Prefabs"
MODS = os.path.expandvars(r"%APPDATA%\7DaysToDie\Mods")

town = json.load(open(os.path.join(SP, "town_placements.json")))
wild = json.load(open(os.path.join(SP, "wild_placements.json")))
h = np.load(os.path.join(SP, "h.npy"))

def relief(t):
    s = h[t["z"]+4096:t["z"]+4096+t["d"], t["x"]+4096:t["x"]+4096+t["w"]]
    return round(float(s.max() - s.min()), 2)

comb = []
for t in town:
    comb.append({"name": t["name"], "mod": t["mod"], "x": t["x"], "y": t["y"], "z": t["z"],
                 "rot": t["rot"], "w": t["w"], "d": t["d"], "relief": relief(t),
                 "where": "town", "occ": t["occ"], "tile": t["tile"]})
for t in wild:
    comb.append({"name": t["name"], "mod": t["mod"], "x": t["x"], "y": t["y"], "z": t["z"],
                 "rot": t["rot"], "w": t["w"], "d": t["d"], "relief": relief(t),
                 "where": "wild", "occ": "", "tile": ""})
json.dump(comb, open(os.path.join(SP, "placements_numbered.json"), "w"), indent=1)
print(f"combined {len(comb)} placements  ({len(town)} town, {len(wild)} wild)")

# ---- rebuild the occupancy mask from the NEW file, excluding our own 122 ----
def read_props(p):
    t = open(p, encoding="utf-8", errors="replace").read(); d = {}
    for m in re.finditer(r'name="([A-Za-z0-9_]+)"\s+value="([^"]*)"', t): d.setdefault(m.group(1), m.group(2))
    return d
P = {}
for root in (DATA, MODS):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith(".xml"): continue
            b = f[:-4]
            if os.path.exists(os.path.join(dp, b + ".tts")): P[b] = read_props(os.path.join(dp, f))
from xml.sax.saxutils import unescape
txt = open(os.path.join(W, "prefabs.xml"), encoding="utf-8-sig").read()
mine = {(c["name"], c["x"], c["z"]) for c in comb}
occ = np.zeros((8192, 8192), bool)
for n, x, y, z, r in re.findall(
        r'name="([^"]+)"\s+position="(-?\d+),(-?\d+),(-?\d+)"\s+rotation="(\d+)"', txt):
    n = unescape(n); x, z, r = int(x), int(z), int(r)
    if (n, x, z) in mine: continue
    ps = P.get(n, {}).get("PrefabSize")
    s = [int(v) for v in ps.split(",")] if ps else [60, 10, 60]
    w, d = (s[2], s[0]) if r % 2 else (s[0], s[2])
    X, Z = x + 4096, z + 4096
    if X < 0 or Z < 0: continue
    occ[Z:Z+d, X:X+w] = True
np.save(os.path.join(SP, "occ.npy"), occ)
print(f"occupancy rebuilt: {100*occ.mean():.2f}% of map")

# ------------------------------------------------------------------- report
MODNAME = {"AAA": "MPLogue Prefabs", "AAB": "Voltralux's POI Pack", "AAC": "Zeebark POI Pack",
           "AAD": "WinterDawn Fortress", "AAF": "Svarii's POI Package", "AAG": "Caleseche",
           "AAH": "ShadowModernHouse", "AAI": "Cog's POIs"}
sk = json.load(open(os.path.join(SP, "skipped.json")))
L = ["# POIs added to Astoria 8K", "",
     f"World: `{W}`", "Untouched original: `prefabs.xml.ORIGINAL-BACKUP`", "",
     f"**{len(town)} POIs placed in town lots**, replacing Tier-0 remnant/rubble/empty-lot filler.",
     f"**{len(wild)} POIs placed in the wilderness** (wilderness/rural-tagged or non-square).",
     f"Decorations 13011 -> 13060 (+122 mod POIs, -73 filler).", "",
     "Rotation follows the law `(marker_rotation + tile_rotation + RotationToFaceNorth) mod 4`,",
     "derived from 8,758 matched placements across Navezgane, the four Pregen worlds and Astoria.",
     "", "Coordinates are each POI's north-west corner. To visit: `teleport <X> <Y> <Z>`.", ""]
for where, title in (("town", "In town (replacing filler)"), ("wild", "In the wilderness")):
    grp = [c for c in comb if c["where"] == where]
    L += [f"## {title} — {len(grp)}", ""]
    for m in sorted({c["mod"] for c in grp}):
        g = sorted([c for c in grp if c["mod"] == m], key=lambda q: q["name"])
        L += [f"### {MODNAME.get(m, m)} ({len(g)})", ""]
        if where == "town":
            L += ["| POI | X | Y | Z | rot | replaced | tile |", "|---|---|---|---|---|---|---|"]
            for c in g:
                L.append(f"| {c['name']} | {c['x']} | {c['y']} | {c['z']} | {c['rot']} | "
                         f"`{c['occ']}` | {c['tile'].replace('rwg_tile_','')} |")
        else:
            L += ["| POI | X | Y | Z | rot | size | ground relief |", "|---|---|---|---|---|---|---|"]
            for c in g:
                L.append(f"| {c['name']} | {c['x']} | {c['y']} | {c['z']} | {c['rot']} | "
                         f"{c['w']}x{c['d']} | {c['relief']} m |")
        L.append("")
L += ["## Deliberately not placed", ""]
for k, v in sorted(sk.items()):
    L += [f"**{k}** — {len(v)}:", "", ", ".join(f"`{n}`" for n in sorted(v)), ""]
open(os.path.join(W, "ADDED_POIS.md"), "w", encoding="utf-8").write("\n".join(L))
print("wrote ADDED_POIS.md")
