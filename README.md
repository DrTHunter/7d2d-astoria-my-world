# 7 Days to Die — Astoria 8K, POI overhaul

A heavily populated edit of the **Astoria 8K** world for 7 Days to Die (tested on V 3.2.0 b10).

259 modded points of interest were added to the map, almost all of them by **replacing
Tier‑0 filler** — the non‑enterable rubble piles, burnt shells and empty gravel lots that
otherwise take up city blocks and give you nothing to do. Thirteen custom player builds sit
on levelled pads next to the main city, and the player spawn was moved into one of them.

---

## ⚠️ Credit — the base map is not mine

The world itself (terrain, biomes, road network, road splats, the original POI layout) is
**Astoria 8K by Grim**, published on Nexus Mods:

> **https://www.nexusmods.com/7daystodie/mods/7017**

All of `dtm.raw`, `biomes.png`, `splat3.png`, `splat4.png`, `regions.png`, `main.ttw` and the
original `prefabs.xml` are that author's work. This repository is a modification of it, not a
replacement — please go and endorse the original.

If you are the author of Astoria 8K and would prefer this not be mirrored here, open an issue
and I will take it down.

---

## Required mods

The world's `prefabs.xml` references POIs from these packs. **Install all of them first** or
those POIs will silently fail to spawn and you will get holes in the map.

| Pack | Nexus |
|---|---|
| Astoria 8K (base map) | [7017](https://www.nexusmods.com/7daystodie/mods/7017) |
| MPLogue Prefabs | [3436](https://www.nexusmods.com/7daystodie/mods/3436) |
| Voltralux's POI Pack | [4916](https://www.nexusmods.com/7daystodie/mods/4916) |
| Zeebark POI Pack | [6577](https://www.nexusmods.com/7daystodie/mods/6577) |
| WinterDawn Fortress | [9420](https://www.nexusmods.com/7daystodie/mods/9420) |
| Svarii's POI Package | [9899](https://www.nexusmods.com/7daystodie/mods/9899) |
| Caleseche | [10496](https://www.nexusmods.com/7daystodie/mods/10496) |
| ShadowModernHouse | [10509](https://www.nexusmods.com/7daystodie/mods/10509) |
| Cog's POIs | [10928](https://www.nexusmods.com/7daystodie/mods/10928) |

---

## Install

The heightmap is **not in this repository** — `dtm.raw` is 128 MB, over GitHub's 100 MB file
limit. It ships gzipped as a release asset, which also keeps it out of every clone:

> **[Download `dtm.raw.gz` from the v1.0 release](../../releases/tag/v1.0)** (90.6 MB)

Clone the repo, drop `dtm.raw.gz` into the world folder, then run this from the repo root in
PowerShell:

```powershell
$w = "$env:APPDATA\7DaysToDie\GeneratedWorlds\Astoria 8K"
New-Item -ItemType Directory -Force $w | Out-Null
Copy-Item "GeneratedWorlds\Astoria 8K\*" $w -Recurse -Force
Copy-Item "LocalPrefabs\*" "$env:APPDATA\7DaysToDie\LocalPrefabs" -Recurse -Force

# expand the heightmap you downloaded from the release into the world folder
$in  = [IO.File]::OpenRead("$w\dtm.raw.gz")
$out = [IO.File]::Create("$w\dtm.raw")
$gz  = New-Object IO.Compression.GzipStream($in, [IO.Compression.CompressionMode]::Decompress)
$gz.CopyTo($out); $gz.Close(); $out.Close(); $in.Close()
Remove-Item "$w\dtm.raw.gz"
```

`dtm.raw` must end up exactly **134,217,728 bytes** — the world will not load correctly
otherwise. Then start a new game and pick *Astoria 8K*.

The 13 custom builds load from `LocalPrefabs`. If any of them fail to appear, check the log
for a missing‑prefab warning and move that folder to `Mods/<anything>/Prefabs/` instead —
you also need to do that if you are hosting a dedicated server, since `LocalPrefabs` is not
distributed to clients.

---

## What changed

Original map: **13,011** decorations. This edit: **13,064**.

### 122 modded POIs from the packs above
73 dropped into real street‑tile lot slots in towns across the map, replacing Tier‑0 filler;
49 placed in the wilderness on flat, road‑adjacent ground. Full list with coordinates in
[`docs/ADDED_POIS.md`](docs/ADDED_POIS.md).

### 124 more around the map's east/central towns
Extra copies concentrated where you actually play, again all replacing junk lots — 56 in the
31‑tile city at (2656, −677), 36 in the 13‑tile town at (1714, −848), the rest spread over
seven more clusters. Capped at two copies of any POI in the area, never twice in one town,
copies at least 300 m apart. See [`docs/ADDED_POIS_local.md`](docs/ADDED_POIS_local.md).

### 13 custom builds on levelled pads
Astoria has **nowhere** a 103×103 building can sit on flat empty ground — RWG flattened every
large plateau and then built a town on it. So `dtm.raw` was edited to level a pad under each
build, with a 24 m cosine ramp back to natural terrain. 0.27 % of the map's terrain was
touched; land steeper than 45° in the modified area actually *decreased*, from 15,872 m² to
7,401 m². Details in [`docs/MY_PREFABS.md`](docs/MY_PREFABS.md).

### Spawn
`spawnpoints.xml` now holds a single point at **X 2415, Z −817**, inside `Prison-perimiter`.
The original ten points are in `GeneratedWorlds/Astoria 8K/backups/`.

### 19 broken references repaired
V 3.2.0 removed several prefabs the original map used — `remnant_lot_industrial_01`,
`cave_15`, `aaa_subway` and some orphaned parts. These were remapped to current equivalents
or dropped.

---

## The interactive map

[`docs/ADDED_POIS_map.html`](docs/ADDED_POIS_map.html) — open it from a clone, pan and zoom,
hover a pin for the POI's pack, size and what it replaced, click to copy its `teleport`
command. Filter by name or by pack in the right‑hand rail.

The map is a stack of switchable layers, in the **Layers** panel top right. Every layer is
the whole 8192 × 8192 world drawn north‑up, so they all line up with each other and with the
pins without any offset:

| | Layer | From |
|---|---|---|
| **base** | your own maps | whatever you pass to `--maps`, one chip each |
| **base** | Biomes | `biomes.png`, with a legend of what each colour is and how much of the map it covers |
| **base** | Terrain zones | `regions.png` |
| overlay | Roads | `splat3.png` — grey asphalt, tan gravel. On by default; it sharpens the road network on any base |
| overlay | Biomes | the biome colours as a tint over whatever base you are on |
| overlay | Terrain zones | the same for the terrain banding |

Base maps are chips, the same as the POI pack chips in the rail — click one to switch to it.
The number keys **1**–**9** pick one directly, and the **MAP** button by the zoom controls
steps to the next (**M**, or shift+**M** to go back).
Whichever base you are on, the overlays stay exactly as you left them — turning them on once
keeps them over every map you switch to. Overlays each have an opacity slider. **G** toggles a 512 m coordinate grid (1024 m lines drawn heavier), and
the world X/Z under the cursor is read out under the title. POI pins, footprints and spawn
markers each toggle separately. Your layer choices are remembered between visits.

### Using your own map renders

Drop any full‑world renders you have into a folder and point the generator at it:

```powershell
python tools\mapgen.py --maps "C:\Users\you\Desktop\maps"
```

Each image becomes a base map chip, and **the first one in natural filename order is the one
the map opens on**. The chip's label is its filename, so a `1_` prefix forced into the name to
win that order shows up in the label too — giving the main render a name that already sorts
first reads better than numbering it.

They must be square and north‑up covering the whole world, which every 7 Days to Die map
export already is; the generator warns if one is not square, because a stretched map will
not line up with the pins. Imports are saved as WebP, and are never scaled up past the
resolution you exported at.

Useful flags:

- `--size 4096` — build the generated roads, biome and terrain layers at 4096 px instead of 2048. It does not enlarge your own renders beyond their own resolution.
- `--quality 90` — WebP quality for the imported maps, 82 by default.
- `--inline` — bake every layer into the HTML as one portable file with no `docs/maps/` alongside it.

`--maps` is what builds the base map chips, so pass it every time you rebuild. Running
`python tools\mapgen.py` with no arguments regenerates the page with only the Biomes and
Terrain zones bases and drops your own renders from the viewer — it warns on stderr when
you do.

---

## Stopping zombies spawning in your base

A Land Claim Block cannot be baked into a world file — it needs an owner, and an unowned one
claims nothing. Place one yourself. In the F1 console:

```
giveself keystoneBlock
```

Quoting the game's own description:

> LCBs will also prevent Sleeper and Biome respawns, but allow Blood Moon or Screamer spawns.

So it stops POI sleepers and wandering biome zombies inside the claimed area, but **not**
blood moons or screamers. It prevents *respawns* — clear the POI once after you first enter
and the LCB keeps them from coming back.

---

## Using this on an existing save

New POIs only appear in chunks the save has not generated yet. For an existing save, rebuild
the affected areas from the F1 console (this destroys anything you built inside the box and
resets loot containers):

```
chunkreset 1272 -1128 2086 -614     # 13-tile town
chunkreset 2172 -1428 3136 136      # 31-tile city
chunkreset 1920 -1412 2509 -358     # the custom-build cluster
```

The rest are listed in `docs/ADDED_POIS_local.md`. Starting a fresh game is cleaner.

---

## Reverting

`GeneratedWorlds/Astoria 8K/backups/` holds each stage of `prefabs.xml`
(`.ORIGINAL-BACKUP` is Grim's untouched file) plus the original `spawnpoints.xml` and
`map_info.xml`. For terrain, re-download `dtm.raw` from the Nexus page — the copy here is
the edited one, and the original is unmodified upstream.

---

## `tools/`

The Python used to build this: street‑tile lot‑slot resolution from `POIMarker*` data,
POI placement and collision checking against the full 8192×8192 heightmap, the terrain
levelling pass, and the map renderer. Not polished, but reproducible.

`mapgen.py` builds the interactive map above: it turns the world's own PNGs into map layers
via `maplayers.py`, then fills `map_template.html` with those layers and the POI, pack and
spawn data in `mapdata.json`. `render2.py` is the separate one‑shot PNG renderer that
produced `docs/ADDED_POIS_map.png`.

Rotation for lot swaps uses the law derived from 8,758 matched placements across Navezgane
and the shipped Pregen worlds:

```
rotation = (marker_rotation + tile_rotation + RotationToFaceNorth) mod 4
```

---

## Licence

The tooling in `tools/` and the documentation are free to use. The world and prefab data
belong to their respective authors — see credits above.
