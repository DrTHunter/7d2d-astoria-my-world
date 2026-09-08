# Astoria 8K — my world

My version of the **Astoria 8K** map for *7 Days to Die* **V 3.2.0 (b10)**: the junk cleared out,
1,812 POIs swapped in, and eight zombie-free starter bases in two walled compounds.

📍 **[Browse every POI on the interactive map →](https://drthunter.github.io/astoria-8k-poi-map/)**
&nbsp;·&nbsp; [how the map page works](https://github.com/DrTHunter/astoria-8k-poi-map)

| | |
|---|--:|
| POIs in the world | **13,108** |
| …that aren't in the stock map | **2,109** |
| Traders, one for every town | **38** |
| Starter bases, no zombies inside | **8** + 2 horde bunkers |

---

# Setup

**You will not break your game.** Everything here is one switch in Vortex. Turn it off and your
game is exactly as it was, and Navezgane and random worlds keep working the whole time.

**Nothing gets edited, patched or overwritten.** The whole thing lives in its own folder.

## First — which one do you want?

There are two. **Pick one.** They're the same map with the same 13,108 buildings in the same places.

| | **Astoria 8K — Modded** | **Astoria 8K — Vanilla** |
|---|---|---|
| Download size | 638 MB | 116 MB |
| The buildings | the modders' originals, with all their custom furniture, signs and textures | the same buildings, rebuilt out of ordinary game blocks |
| Looks | the best it gets | 91% of the POIs are pixel-for-pixel identical anyway |
| Shows in the world list as | `Astoria 8K Modded` | `Astoria 8K Vanilla` |
| Anti-cheat / servers | fine | fine |

**If you're not sure, take the Vanilla one.** It's five times smaller and you honestly won't notice
the difference in most buildings — the layouts, the loot and the zombies are identical.

> ⚠️ **Only ever enable ONE of them.** They show up as two clearly different worlds, but both carry
> POI files under the same names — so with both switched on, each building could come from either
> edition and you'd get a mix. Pick one, enable it, leave the other off.

---

## Step 1 — Install Vortex (5 minutes, once)

Vortex is Nexus's free mod manager. It's what turns this into a single on/off switch.

**[Download Vortex here →](https://www.nexusmods.com/vortex)**

Install it, open it, click **Games** in the left sidebar, find **7 Days to Die**, and click
**Manage**. Vortex finds your game on its own.

---

## Step 2 — Download the mod

### The easy way — copy and paste one line

**1.** Hold down the **Windows key** and press **R**. A little box called *Run* opens in the corner.

**2.** Type this and press Enter:

```
powershell
```

**3.** A blue window opens. Copy the line below (click the copy icon in the corner of the box),
right-click inside the blue window to paste it, and press **Enter**.

For **Vanilla** (116 MB — the recommended one):

```powershell
curl.exe -L -o "$([Environment]::GetFolderPath('Desktop'))\Astoria-8K-Vanilla-Complete.zip" https://github.com/DrTHunter/7d2d-astoria-my-world/releases/latest/download/Astoria-8K-Vanilla-Complete.zip
```

For **Modded** (638 MB — the full-fat one):

```powershell
curl.exe -L -o "$([Environment]::GetFolderPath('Desktop'))\Astoria-8K-Complete.zip" https://github.com/DrTHunter/7d2d-astoria-my-world/releases/latest/download/Astoria-8K-Complete.zip
```

You'll see a progress bar. When it finishes, **the zip file is sitting on your Desktop.** Close the
blue window.

*Nothing clever is happening here — `curl` is a download tool that comes with Windows, and this just
tells it to save the file to your Desktop.*

### Or just click a link

Prefer to click? These download the same files straight to your browser's Downloads folder:

- **[Astoria-8K-Vanilla-Complete.zip](https://github.com/DrTHunter/7d2d-astoria-my-world/releases/latest/download/Astoria-8K-Vanilla-Complete.zip)** (116 MB)
- **[Astoria-8K-Complete.zip](https://github.com/DrTHunter/7d2d-astoria-my-world/releases/latest/download/Astoria-8K-Complete.zip)** (638 MB)

Your browser may warn that it's a large file — that's fine, keep it.

---

## Step 3 — Drag it into Vortex

**Don't unzip it.** Vortex wants the zip exactly as it downloaded.

1. Open Vortex
2. **Drag the zip file from your Desktop and drop it onto the Vortex window**
3. Vortex shows it in the list — click **Install**
4. When that finishes, click **Enable**

That's the install. There is no step where you copy files into the game folder.

---

## Step 4 — Play

Start 7 Days to Die. Click **New Game**, and in the world dropdown pick whichever you installed:

- **Astoria 8K Modded**
- **Astoria 8K Vanilla**

Only the one you enabled will be in the list.

You'll spawn in the prison yard, which is a starter base with no zombies in it.

> **Start a NEW game.** 7 Days to Die bakes the buildings into the ground the first time you visit
> an area. If you load an old save, everywhere you've already walked keeps the old layout.

> **If the game was already running while you installed, close it completely and reopen it.** It
> only reads the mod folder at startup.

---

## Turning it off again

Open Vortex, find the mod, click **Disable**. Done — the world vanishes from the list and your game
is stock. Click **Enable** to bring it back.

Your saves aren't touched either way. A save on Astoria 8K just can't be opened while the mod is
off, and works again the second you turn it on.

# Troubleshooting

**Astoria 8K Modded / Astoria 8K Vanilla isn't in the world list.**
The mod isn't enabled in Vortex, or the game was already open when you enabled it. Close the game
completely — all the way to the desktop — and start it again.

**Buildings are missing, or there are empty lots where houses should be.**
Almost always one of two things:

1. **A mod got switched on or off while the game was running.** 7 Days to Die reads the mod folder
   once at startup and remembers where every building lives. Sort your mods out *first*, then
   launch. **Fix: quit the game completely and restart it.**
2. **You're on an old save.** See Step 4.

To check for yourself, open the newest file in your logs folder and search it for
`Could not load prefab` — it names every building the game couldn't place, and the `ERR` line just
above each one says why. To get to the logs: **Windows key + R**, then paste
`%APPDATA%\7DaysToDie\logs` and press Enter.

**I enabled both mods and buildings look wrong.**
Disable one. Both editions ship POI files under the same names, so with both on the game picks
whichever it found first for each building and you end up with a mix. Turn one off, restart the
game.

**The log fills with `Skipping loading of active block data for xcpv_…` / `Object reference not set`.**
About 800 lines across 45 Compopack POIs, and harmless: those POIs carry sign data in a format
V 3.2.0 can't convert, so the building loads and the sign text doesn't. The files are byte-identical
to the pack's originals — it isn't either mod, and it happens on both editions. The world still
reaches *Ready to spawn*; the red overlay is just the log being shown while it loads.

**`Could not load prefab 'xcpv_…_EvilRacc0on'`.**
Three Compopack POIs shipped with a property named `StaticSpawner.Size`, and the `.` in the name
makes V 3.2.0 refuse the whole prefab. Fixed in builds from **1.10.0** — the property is removed and
the build refuses to ship any prefab XML with an illegal property name.

**The modded world won't load, or the log fills with `is not a BlockCompositeTileEntity`.**
You have a build before 8 September 2026. Two separate faults aborted the `blocks.xml` parse — a
shape pointing at an asset bundle that wasn't shipped, 73 blocks defined before the parent they
extend, and 15 blocks whose `DowngradeBlock` target had been pruned away. Any one of these stops
block creation, so most blocks never exist and every POI with a container throws. Re-download; the
fixed build reports **1.12.0** in Vortex.

**The log says `expected data len N. Probably outdated ins file` for `StarterBase_…`.**
Builds before **1.12.0** shipped a placeholder `.ins` (inside-data) file with every prefab I authored,
and the game flags each one. Harmless — the prefab still loads — and gone from 1.12.0 on.

**Vortex says the mod is "not deployed".**
Click **Deploy Mods** at the top of Vortex, or just click Disable then Enable again.

**I have no idea whether it worked.**
Start a new game on Astoria 8K Modded or Astoria 8K Vanilla and look at where you spawn. If you're
standing in a prison yard, it worked. If you're in an ordinary field, it didn't.

---

# What's in this repo

The two mods are on the [Releases page](https://github.com/DrTHunter/7d2d-astoria-my-world/releases/latest) —
they're too big to sit in the repo itself:

```
Astoria-8K-Complete.zip           638 MB  world "Astoria 8K Modded"  - the modders' own blocks and models
Astoria-8K-Vanilla-Complete.zip   116 MB  world "Astoria 8K Vanilla" - the same 987 POIs, stock blocks only
```

And in the repo:

```
vortex/Astoria-StarterBases.zip   just the 8 starter bases, if you want them on their own
world-patch/                      the raw map changes: dtm.patch, prefabs.xml, spawnpoints.xml
tools/install.py                  the old route - patches a Nexus copy of the map in place
docs/                             the full write-up of every change, and every trader's coordinates
```

The git repo holds only the map patch and my own buildings — a 0.2 MB `dtm.patch` rather than a
128 MB heightmap. The two mods, which repackage the packs' POIs and the Astoria map, are Release
assets; credit and links for every author are in the release notes and at the bottom of this page.

<details>
<summary>The older way, if you already patched a Nexus copy of the map</summary>

`Astoria-AllInOne.zip` from the
[v1.1 release](https://github.com/DrTHunter/7d2d-astoria-my-world/releases/tag/v1.0-allinone)
ships the POIs only, and `python tools/install.py` edits the map in
`%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K` in place (`--undo` puts it back). It needs the
Astoria 8K map v1.5.1 from Nexus first.

**Don't run both routes at once** — the patched map in `GeneratedWorlds` is also called
*Astoria 8K*, and its POIs come from the packs, so mixing the two gets confusing fast.
</details>

## Traders

**38 traders, and every town has one within a short walk.** Astoria shipped 24, but they were
distributed by the world generator rather than by town, so several towns had none at all and the
spawn city had two on opposite corners.

Astoria's own traders sit a median 66 m *outside* the town edge, on the approach road, and that is
the shape this follows — for each town without one, a clear, flat 60x60 patch 25–140 m beyond the
edge was scored on distance to the nearest road, how much cut and fill it needs, and whether it
faces the next town along. Every site chosen is on or beside a road; all but two need under a
metre of levelling. An existing town lot was the fallback, and never won.

Three traders that were already in the right place kept their spot and just got a better building.
All **14 distinct trader buildings** are now in use — the five vanilla ones, six of MPLogue's,
Zeebark's, and both of xcpv's settlements — so no two neighbouring towns look alike. Three have
deep basements (MPLogue's Wight bunker goes 31 blocks down), so those went to the sites with the
most ground under them; the shallowest trader still stands on 5 m of rock.

The spawn city gets a third, `trader_xcpv_Settlement_02_Viper7`, 266 m from where you wake up,
because the first walk was otherwise the better part of a kilometre.

Turn on the **Traders** layer on the [interactive map](https://drthunter.github.io/astoria-8k-poi-map/)
to see where they all are.

The full list, with teleport commands: [`docs/TRADERS.md`](docs/TRADERS.md).

## The eight starter bases

Each was cut out of an existing POI. **None has a single sleeper volume**, so nothing spawns inside —
they're safe to move into on day one.

| Cut from | Name | Size |
|---|---|--:|
| `prison_01` | **StarterBase_Prison_Cellblock** — the map spawn is in its yard | 113×109 |
| `farm_17` | **StarterBase_UFO_Farm** | 69×75 |
| `ranger_station_07` | **StarterBase_Ranger_Station** | 70×79 |
| `hotel_03` | **StarterBase_Hotel_Tower** | 127×124 |
| `house_modern_18` | **StarterBase_Modern_House** — compound | 111×105 |
| `house_modern_31` | **StarterBase_Bunker_House** — compound | 69×75 |
| `Ayesoar_Mansion_by_MPLogue` | **StarterBase_Ayesoar_Mansion** — compound | 60×54 |
| `Modern_House_Zeebark` | **StarterBase_Zeebark_Modern_House** — own plot | 60×60 |

The last one ships from Zeebark as a Tier‑5 *infested* POI with **31 badass sleeper volumes**; those
were stripped so it matches the rest. Its geometry is byte-identical to Zeebark's original.

Two walled plots hold them: a **148×204 compound** with three houses, and a **74×74 plot** 14 m east
with the Zeebark house.

### The fence

The compound is fenced the way the Modern House itself is fenced — not a drawing of it, the thing
itself. Every block was cut out of `StarterBase_Modern_House` with its rotation intact:

| | |
|---|---|
| **Fence** | the house's own front bay, tiled along every side — brick pier, five panels of half-brick with iron bars on top, cast cap |
| **Gates** | 6 working 5×3 roll-up doors set into the line between two piers, with a driveway out through the yard. The bar course runs across the top of each opening and a cast lintel ties the two flanking pier caps together, so a gate reads as a portal rather than a gap |
| **Entrance buildings** | the 16 m building embedded in the house's front line, once per full side — brick back wall *on* the fence, windowed facade and door one row inside, yard in front. Each one stands hard against its gate's own pier, so the guard shack watches the drive-through |
| **Security posts** | the module from the house's west fence, at every pedestrian entrance: carport outside, the fence with its door and the *Staff Only* / *Private Property* signs, the booth just inside — standing 4 m proud of the line so the booth clears the ring road |
| **Yard** | an 18 m apron in front of the S, N and W sides and Plot 2's east side, on regraded ground |

The E side faces Plot 2 across a road, and Plot 2's other three sides are boxed in by the road out
and a cabin, so those are the fence and gates only.

Every fence block carries the same paint the Modern House gives it — `0x3f` on the brick piers,
`0x32` on the half-brick panels and the caps, `0x18` on the window, the bars and the steel gate
panels. The first build of these strips wrote no paint layer at all, which is why the piers and
gates came out the wrong colour against the house they were cut from;
[`tools/refence.py`](tools/refence.py) puts it back, reading the scheme off a capture of the house's
own fence. The rebuilt strips are in [`world-patch/fence/`](world-patch/fence/), the originals
beside them in `world-patch/fence-backup/`.

The two buildings carry block rotations up to 27, so nothing was rotated by hand: each side is
authored facing south and the game rotates it (S 0, E 1, N 2, W 3); the post is authored facing
west (W 0, S 1, E 2, N 3). The convention was derived from `trader_rekt`, whose gate sits on its
west edge at rotation 0 with `RotationToFaceNorth` 3 — quarter turns are counter-clockwise.

Every block is stock, and this time both editions get exactly the same fence.

### Where the two editions differ

Not on the compound any more — the fence is the Modern House's own, and that house is stock blocks
throughout. The editions differ only in the POI packs' own buildings elsewhere on the map.

### Roads

The ring road inside is asphalt with a concrete kerb down each side, on a gravel base. A cobbled
path leads out of each entrance, and the two roads that join the compound to the real road network
were shortened 2 m so they meet the wall's new outer face cleanly rather than running under it.

Two entrances had to move: the north gate opened straight onto `xcpv_Trailer_01_ZZTong` and one east
gate onto `cabin_16`, so both were shifted along the wall to the nearest clear ground.

### Two horde bunkers

Both are TFP's own `aaa_horde_base` — a 25 m concrete pillbox with iron bars, entered through a
roof hatch, no sleeper volumes, every block stock — shipped here as **StarterBase_Horde_Bunker** so it
doesn't depend on the game's `Test` folder being on the prefab search path.

| Where | Position | Notes |
|---|---|---|
| **In the compound** | X 2126 Z −412, the northeast nook | The mansion moved 10 m south and the north ring road was cut short of the corner to open a 25×25 pocket — there wasn't one before |
| **Behind the prison** | X 2418 Z −746 | 66 m from the map spawn, 3 m off the prison's back wall, 12 m short of the ranger station — between two starter bases, clear of the prison gate, which faces south |

Teleports for all of them: [`docs/TELEPORTS_mine.txt`](docs/TELEPORTS_mine.txt).

## What was done to the map

- **1,812 junk POIs replaced.** Astoria shipped with 1,070 Tier‑0 filler lots — the non-enterable
  rubble RWG scatters everywhere — plus a lot of repetition (one downtown filler appeared **18
  times**). Those, and every 7th-and-beyond copy of a vanilla POI, now hold a Compopack POI: **820
  distinct** ones, never more than 4 copies of any single POI across the whole 8 km map. **1,769 of
  them have sleeper volumes**, so they're lootable and questable — the rubble wasn't.
- **Terrain re-graded** under the two plots and the roads: 112,881 cells, 0.17 % of the map.
- The detail, including how the placement rules were derived and checked:
  [`docs/REPOPULATED.md`](docs/REPOPULATED.md) and [`docs/MY_PREFABS.md`](docs/MY_PREFABS.md).
  Every single swap is listed in [`docs/REPOPULATED_pois.csv`](docs/REPOPULATED_pois.csv).

## Credit

The POIs in the all-in-one mod are other people's work. The buildings were designed by the authors
of the [Compopack](https://www.nexusmods.com/7daystodie/mods/5438),
[Zeebark](https://www.nexusmods.com/7daystodie/mods/6577),
[Voltralux](https://www.nexusmods.com/7daystodie/mods/4916),
[MPLogue](https://www.nexusmods.com/7daystodie/mods/3436),
[Svarii](https://www.nexusmods.com/7daystodie/mods/9899),
[Cog](https://www.nexusmods.com/7daystodie/mods/10928),
[WinterDawn](https://www.nexusmods.com/7daystodie/mods/9420),
[Caleseche](https://www.nexusmods.com/7daystodie/mods/10496) and
[ShadowModernHouse](https://www.nexusmods.com/7daystodie/mods/10509) packs, and the map itself by
the author of [Astoria 8K](https://www.nexusmods.com/7daystodie/mods/7017). All that was done here
is to repackage the parts this map uses into one install. Go give them endorsements.
