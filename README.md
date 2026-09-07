# Astoria 8K — my world

My version of the **Astoria 8K** map for *7 Days to Die* **V 3.2.0 (b10)**: the junk cleared out,
1,812 POIs swapped in, and eight zombie-free starter bases in two walled compounds.

📍 **[Browse every POI on the interactive map →](https://drthunter.github.io/astoria-8k-poi-map/)**
&nbsp;·&nbsp; [how the map page works](https://github.com/DrTHunter/astoria-8k-poi-map)

| | |
|---|--:|
| POIs in the world | **13,081** |
| …that aren't in the stock map | **2,088** |
| Starter bases, no zombies inside | **8** |

---

# Setup — read this bit, it's short

**You will not break your game.** Everything below is either managed by Vortex (one switch, on or
off) or backed up automatically and undoable with one command.

**You can still play vanilla whenever you like.** Flip the mods off in Vortex and play Navezgane or
a random world exactly as before. The Astoria map just sits there doing nothing until you pick it.

You need to do four things. Give it 20 minutes.

## 1. Install Vortex

**[Download Vortex →](https://www.nexusmods.com/vortex)** (from Nexus — it's free)

Install it, open it, and let it find 7 Days to Die under **Games**. Click **Manage** on it.

This is the whole reason we're using Vortex: every mod becomes a switch you can turn **on to play
with me** and **off to play vanilla**. No moving files around, nothing to break.

## 2. Get the POI packs

These are the actual buildings. Download each from Nexus — Vortex picks them up automatically if
you use the **Mod Manager Download** button on the page, otherwise drag the downloaded file onto the
Vortex window.

| Pack | POIs it supplies |
|---|--:|
| **[Compopack Classic All-In-One (No Traders)](https://www.nexusmods.com/7daystodie/mods/5438)** | **1,812** ← the big one |
| [Zeebark POI Pack](https://www.nexusmods.com/7daystodie/mods/6577) | 125 |
| [Voltralux's POI Pack](https://www.nexusmods.com/7daystodie/mods/4916) | 50 |
| [MPLogue Prefabs](https://www.nexusmods.com/7daystodie/mods/3436) | 41 |
| [Svarii's POI Package](https://www.nexusmods.com/7daystodie/mods/9899) | 21 |
| [Cog's POIs](https://www.nexusmods.com/7daystodie/mods/10928) | 6 |
| [WinterDawn Fortress](https://www.nexusmods.com/7daystodie/mods/9420) | 1 |
| [Caleseche](https://www.nexusmods.com/7daystodie/mods/10496) | 1 |
| [ShadowModernHouse](https://www.nexusmods.com/7daystodie/mods/10509) | 1 |

In Vortex, hit **Install** then **Enable** on each one.

> **All of us need the same list, me included.** MPLogue and Zeebark change core game data
> (`blocks.xml`, `shapes.xml`, `materials.xml`), so if one person is missing them the block IDs
> won't line up and the world will look wrong.

## 3. Get my starter bases

Download **[`vortex/Astoria-StarterBases.zip`](vortex/Astoria-StarterBases.zip)** from this repo
(click the file, then the **Download** button — it's only 0.5 MB).

**Drag it onto the Vortex window** → **Install** → **Enable**. That's it. It's a normal mod now, with
its own on/off switch like the others.

## 4. Get the map, then patch it

**a.** Install the base map:
**[Astoria 8K — Full World Map](https://www.nexusmods.com/7daystodie/mods/7017)** (Nexus 7017,
**version 1.5.1**). This one is *not* a Vortex mod — extract it by hand so the files land here:

```
%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K\
```

(Paste `%APPDATA%\7DaysToDie` into Explorer's address bar to get there.) The folder has to be named
exactly **Astoria 8K**.

**b.** Download this repo — green **Code** button → **Download ZIP** — unzip it anywhere, then
double-click into the folder and run:

```
python tools/install.py
```

It finds your game on its own, checks your Astoria files are the right version, **backs them up**,
applies my changes, then checks the result. If anything looks wrong it stops and changes nothing.

*(No Python? Get it from [python.org](https://www.python.org/downloads/) — tick **"Add Python to
PATH"** during install.)*

## 5. Play

Start a **new** game, pick **Astoria 8K**. You'll spawn in the prison yard.

> **An existing save won't show any of this.** The game bakes buildings into the ground the first
> time you visit an area, so anywhere you've already been keeps the old layout. Start fresh.

---

# Switching back to vanilla

**To play vanilla:** open Vortex and click **Disable** on the POI packs and on
Astoria-StarterBases. Play Navezgane or a random world. Done — nothing else to do.

**To play with me again:** click **Enable** on them.

**To remove my changes from the map itself** (you almost never need to — the map is only used if you
choose it):

```
python tools/install.py --undo
```

That puts the original Astoria files straight back from the backups the installer made.

---

# Troubleshooting

**Buildings are missing / there are empty lots where houses should be.**
Almost always one of two things:

1. **A mod was turned on or off while the game was running.** 7 Days to Die reads the mod folders
   once when it starts and remembers where every building lives. Sort your mods out *first*, then
   launch. If Vortex moves a mod folder while you're playing, everything in it silently disappears.
   **Fix: quit the game completely and restart it.**
2. **You're on an old save.** See step 5.

To check, open the newest file in `%APPDATA%\7DaysToDie\logs\` and search for `does not exist` — it
names every building the game couldn't find.

**The installer says "MISMATCH".** Your Astoria download isn't v1.5.1. Get that exact version. The
installer deliberately refuses rather than half-patching your map.

---

# What's in this repo

```
vortex/Astoria-StarterBases.zip   my 8 starter bases + their walls and roads, ready for Vortex
world-patch/                      the map changes: dtm.patch, prefabs.xml, spawnpoints.xml
tools/install.py                  applies them; --undo puts the stock map back
docs/                             the full write-up of every change
```

**This repo doesn't redistribute anyone else's work.** The base map and the POI packs come from
Nexus; what's stored here is the *difference* between stock Astoria and mine, plus my own buildings.
That's why the map patch is 0.2 MB instead of a 128 MB file.

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

Two walled plots hold them: a **146×202 compound** with three houses, and a **74×74 plot** 14 m east
with the Zeebark house. The wall is copied block-for-block from the Modern House's own front wall —
brick pillars every 6 m, dark metal panels, iron railings — with **seven working roll-up gates** and
a paved ring road inside each, joined to the real road network.

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
