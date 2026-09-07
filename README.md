# Astoria 8K — my world

My version of the **Astoria 8K** map for *7 Days to Die* **V 3.2.0 (b10)**: the junk cleared out, a
few thousand POIs swapped in, and eight zombie-free starter bases in two walled compounds.

**[Browse every POI on the interactive map →](https://drthunter.github.io/astoria-8k-poi-map/)**

| | |
|---|--:|
| POIs in the world | **13,081** |
| …not in the stock map | **2,088** |
| Starter bases (no sleeper volumes) | **8** |
| Terrain cells re-graded | 112,881 |

---

# Installing it (for my friends)

You need **five things**. Steps 1–3 are downloads from Nexus; steps 4–5 are one command.

Everything below happens in your 7 Days to Die data folder. On Windows that is:

```
%APPDATA%\7DaysToDie
```

Paste that into Explorer's address bar and it will take you there.

## 1. The game

**7 Days to Die V 3.2.0 (b10)**. Other versions will not match — the patch checks and refuses.

## 2. The base map

**[Astoria 8K — Game Version 2.0 — Full World Map](https://www.nexusmods.com/7daystodie/mods/7017)**
(Nexus mod 7017, **version 1.5.1**). Extract it so the files land here:

```
%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K\
    biomes.png   dtm.raw   main.ttw   map_info.xml
    prefabs.xml  regions.png  spawnpoints.xml  splat3.png  splat4.png
```

Do **not** rename the folder — it must be exactly `Astoria 8K`.

## 3. The POI packs

These supply the buildings. Every one goes in `%APPDATA%\7DaysToDie\Mods\`.
**Without them you get empty lots where 2,088 POIs should be.**

| Pack | POIs used | Also needed for |
|---|--:|---|
| **[Compopack Classic All-In-One (No Traders)](https://www.nexusmods.com/7daystodie/mods/5438)** | 1,812 | by far the biggest share — most of the map |
| [Zeebark POI Pack](https://www.nexusmods.com/7daystodie/mods/6577) | 125 | blocks for one starter base |
| [Voltralux's POI Pack](https://www.nexusmods.com/7daystodie/mods/4916) | 50 | |
| [MPLogue Prefabs](https://www.nexusmods.com/7daystodie/mods/3436) | 41 | blocks for one starter base |
| [Svarii's POI Package](https://www.nexusmods.com/7daystodie/mods/9899) | 21 | |
| [Cog's POIs](https://www.nexusmods.com/7daystodie/mods/10928) | 6 | |
| [WinterDawn Fortress](https://www.nexusmods.com/7daystodie/mods/9420) | 1 | |
| [Caleseche](https://www.nexusmods.com/7daystodie/mods/10496) | 1 | |
| [ShadowModernHouse](https://www.nexusmods.com/7daystodie/mods/10509) | 1 | |

**All of us must run the same list**, including the host. MPLogue and Zeebark ship `blocks.xml`,
`shapes.xml` and `materials.xml`, which change core game data — if one person is missing them the
block IDs will not line up.

## 4. Get this repo

```
git clone https://github.com/DrTHunter/7d2d-astoria-my-world.git
```

or **Code → Download ZIP** and unzip it anywhere.

## 5. Run the installer

```
python tools/install.py
```

It finds your game folder on its own. It will:

- check your stock Astoria files are v1.5.1 (**it stops if they are not** — nothing is touched)
- copy them to `*.stock-backup` so you can always go back
- patch `dtm.raw` (112,881 cells — the levelled pads and the roads)
- replace `prefabs.xml` and `spawnpoints.xml`
- verify all three against known checksums
- install `Mods\Astoria-StarterBases`

Re-running it is safe. To undo, delete the three files and rename the `.stock-backup` copies back.

## 6. Start a **new** save

Pick **Astoria 8K**. You will spawn in the prison yard at `2430, -800`.

> **An existing save will not show any of this.** 7 Days to Die bakes POIs into a chunk the first
> time it generates, so anything you have already explored keeps the old layout. Start fresh.

---

# What is actually in here

```
mods/Astoria-StarterBases/   the eight starter bases + their walls and roads (my own builds)
world-patch/                 dtm.patch, prefabs.xml, spawnpoints.xml, manifest.json
tools/install.py             applies the patch to a stock Astoria world
docs/                        the full write-up of every change
```

**This repo does not redistribute anyone else's work.** The base map and the POI packs come from
Nexus (links above); what is stored here is the patch that turns a stock Astoria into mine, plus my
own prefabs. That is also why `dtm.patch` is 0.2 MB instead of a 128 MB file.

## The eight starter bases

Each was cut out of an existing POI. **None of them has a single sleeper volume**, so nothing spawns
inside — they are safe to move into on day one.

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

The last one ships from Zeebark as a Tier‑5 `infested` POI with **31 badass sleeper volumes**; those
were stripped so it matches the rest. Its geometry is byte-identical to Zeebark's original.

Two walled plots hold them: a **146×202 compound** with three houses, and a **74×74 plot** 14 m east
with the Zeebark house. The wall is copied block-for-block from the Modern House's own front wall —
brick pillars every 6 m, dark metal panels, iron railings — with **seven working roll-up gates** and
a paved ring road inside each, linked to the real road network.

Teleports for everything: [`docs/TELEPORTS_mine.txt`](docs/TELEPORTS_mine.txt).

## What was done to the map

- **1,812 junk POIs replaced.** Astoria shipped with 1,070 Tier‑0 filler lots — `remnant_*`,
  `rubble_*`, `lot_vacant_*`, the non-enterable rubble RWG scatters everywhere — plus a lot of
  repetition (one downtown filler appeared **18 times**). Those, and every 7th-and-beyond copy of a
  vanilla POI, now hold a Compopack POI: **820 distinct** ones, never more than 4 copies of any
  single POI across the whole 8 km map. **1,769 of them have sleeper volumes**, so they are lootable
  and questable — the rubble was not.
- **Terrain re-graded** under the two plots and the roads: 112,881 cells, 0.17 % of the map.
- Full detail, including how the placement rules were derived and verified:
  [`docs/REPOPULATED.md`](docs/REPOPULATED.md) and [`docs/MY_PREFABS.md`](docs/MY_PREFABS.md).
  Every swap is listed in [`docs/REPOPULATED_pois.csv`](docs/REPOPULATED_pois.csv).

## If something is missing in game

Almost always one of two things:

1. **A mod was added or removed while the game was running.** 7 Days to Die scans the prefab folders
   once at startup and remembers where each POI lives. Install everything, *then* start the game.
   If Vortex renames a mod folder mid-session, every POI in it silently vanishes.
2. **You are on an old save.** See step 6.

To confirm, search your log in `%APPDATA%\7DaysToDie\logs\` for `does not exist` — it names every
prefab the game could not find.
