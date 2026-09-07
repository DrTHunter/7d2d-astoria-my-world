# Astoria 8K — my world

My version of the **Astoria 8K** map for *7 Days to Die* **V 3.2.0 (b10)**: the junk cleared out,
1,812 POIs swapped in, and eight zombie-free starter bases in two walled compounds.

📍 **[Browse every POI on the interactive map →](https://drthunter.github.io/astoria-8k-poi-map/)**
&nbsp;·&nbsp; [how the map page works](https://github.com/DrTHunter/astoria-8k-poi-map)

| | |
|---|--:|
| POIs in the world | **13,095** |
| …that aren't in the stock map | **2,100** |
| Traders, one for every town | **38** |
| Starter bases, no zombies inside | **8** |

---

# Setup — read this bit, it's short

**You will not break your game.** Everything below is either managed by Vortex (one switch, on or
off) or backed up automatically and undoable with one command.

**You can still play vanilla whenever you like.** Flip the mods off in Vortex and play Navezgane or
a random world exactly as before. The Astoria map just sits there doing nothing until you pick it.

**Two steps. Give it 15 minutes — nearly all of it is one download.**

## 1. Install Vortex

**[Download Vortex →](https://www.nexusmods.com/vortex)** (from Nexus — it's free)

Install it, open it, and let it find 7 Days to Die under **Games**. Click **Manage** on it.

This is the whole reason we're using Vortex: the mod becomes a switch you can turn **on to play
with me** and **off to play vanilla**. No moving files around, nothing to break.

## 2. Install the one mod

**[Download `Astoria-8K-Complete.zip` from Releases →](https://github.com/DrTHunter/7d2d-astoria-my-world/releases/latest)**
(601 MB)

**Drag it onto the Vortex window** → **Install** → **Enable**.

Start the game and pick **Astoria 8K** from the world list. That's the whole setup.

That one file carries the map itself, the 981 POIs it places, the 640 block definitions those POIs
use, the Unity assets behind them, my eight starter bases and all 38 traders. **You do not need the
Astoria map from Nexus, and you do not need the nine POI packs** — if you already installed any of
them, disable them in Vortex, or the same POI ends up defined twice and which copy you get is
anyone's guess.

> **Start a new game.** The game bakes buildings into the ground the first time you visit an area,
> so an existing save keeps the old layout wherever you've already been. You'll spawn in the prison
> yard.

<details>
<summary>Why there's no longer anything to patch</summary>

7 Days to Die resolves worlds through `PathAbstractions.WorldsSearchPaths`, and that includes mod
folders — so `Mods/<mod>/Worlds/<name>/` is a first-class world source, exactly like
`GeneratedWorlds/`. Earlier versions shipped only the POIs and had to edit the Nexus map in place
with a script; this one carries the world itself, so enabling the mod *is* the install.

The world folder ships the 9 files the game needs. The `*_processed` and `*_half` caches are left
out on purpose — the game rebuilds them on first load.
</details>

<details>
<summary>How it stays at 601 MB instead of the 1,531 MB the nine downloads used to be</summary>

- **Only what the map places.** The packs hold ~2,900 prefabs between them; Astoria places 981.
- **No `.mesh` files** — 479 MB of distant-view imposters, and optional: 11 vanilla POIs and 31 of
  the packs' own ship without one. Distant silhouettes pop in a little closer; nothing else changes.
- **Config pruned to 640 blocks** from the 1,550 the packs define, following each kept block's
  `Extends` and upgrade chains so nothing dangles. That also dropped 200 MB of asset bundles only
  unused blocks referenced.

Verified against a simulated install of vanilla + this one mod: 0 of 1,794 POIs fail to resolve,
0 undefined blocks, 0 dangling `Extends`, 0 missing bundles.
</details>

<details>
<summary>If you already have the Nexus map patched (the old way)</summary>

Use `Astoria-AllInOne.zip` from the
[v1.1 release](https://github.com/DrTHunter/7d2d-astoria-my-world/releases/tag/v1.0-allinone)
plus `python tools/install.py`, which patches the map in `GeneratedWorlds` in place. **Don't enable
both** — you'd have two worlds named *Astoria 8K* in two different search paths and no way to say
which one the game picks.
</details>

---

# Switching back to vanilla

**To play vanilla:** open Vortex and click **Disable** on *Astoria 8K — Complete*. That's it. The
world disappears from the list along with every POI, block and asset it brought, and your game is
stock again. Play Navezgane or a random world exactly as before.

**To play with me again:** click **Enable**.

Nothing outside the mod folder is ever touched, so there is nothing to undo and no backup to
restore. Your saves stay where they are — a save on Astoria 8K simply can't be loaded while the mod
is off, and works again the moment you turn it back on.

*(Only relevant if you used the old patch-the-map route: `python tools/install.py --undo` puts the
original Astoria files back from the installer's backups.)*

---

# Troubleshooting

**Buildings are missing / there are empty lots where houses should be.**
Almost always one of two things:

1. **A mod was turned on or off while the game was running.** 7 Days to Die reads the mod folders
   once when it starts and remembers where every building lives. Sort your mods out *first*, then
   launch. If Vortex moves a mod folder while you're playing, everything in it silently disappears.
   **Fix: quit the game completely and restart it.**
2. **You're on an old save.** See the note in step 2.

To check, open the newest file in `%APPDATA%\7DaysToDie\logs\` and search for `does not exist` — it
names every building the game couldn't find.

**The world isn't in the list.** The mod isn't enabled, or the game was already running when you
enabled it — quit all the way out and restart.

**Two worlds called Astoria 8K.** You have both this mod *and* the old patched map in
`%APPDATA%\7DaysToDie\GeneratedWorlds\`. Pick one: either disable the mod, or delete the
`GeneratedWorlds\Astoria 8K` folder. With both present the game picks one and won't tell you which.

**The installer says "MISMATCH"** *(old patch route only)*. Your Astoria download isn't v1.5.1. Get
that exact version. The installer deliberately refuses rather than half-patching your map.

---

# What's in this repo

```
Releases: Astoria-8K-Complete.zip  the whole thing: map + 981 POIs + blocks + assets  <- use this
Releases: Astoria-AllInOne.zip     POIs only, for the older patch-the-map route
vortex/Astoria-StarterBases.zip    just the 8 starter bases, if you want them on their own
world-patch/                       the map changes: dtm.patch, prefabs.xml, spawnpoints.xml
tools/install.py                   applies them; --undo puts the stock map back
docs/                              the full write-up of every change
```

The git repo itself holds only the map patch and my own buildings — the 0.2 MB `dtm.patch` instead
of a 128 MB file. The two mods, which do repackage the nine packs' POIs and the Astoria map, are
Release assets; credit and links for every author are in their release notes and at the bottom of
this page.

**Want this without any mods at all?** There's a second version where every POI has been rewritten
to use only vanilla blocks — same 13,095 POIs, nothing to install but the map:
**[7d2d-astoria-vanilla](https://github.com/DrTHunter/7d2d-astoria-vanilla)**.

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
