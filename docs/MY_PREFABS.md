# Your prefabs + spawn - Astoria 8K

13 of your LocalPrefabs placed as a cluster around the prison, each on a levelled pad.
`Spotlight-down` (1x1x1 decoration) and `Parts/UFOHomeBASE` (duplicate of UFOhomeBase) skipped.

## Spawn

New players spawn at **X 2415, Z -817** - the centre of Prison-perimiter, ground 58 m.
`spawnpoints.xml` now has this one point only; the original 10 are in `spawnpoints.xml.ORIGINAL-BACKUP`.

## Land claim block

A claim block cannot be baked into the world - it needs an owner, and an unowned one claims nothing.
Place it yourself on arrival. In the F1 console:

    giveself keystoneBlock

or `creativemenu` and search for it. Straight from the game's own text:

> LCBs will also prevent Sleeper and Biome respawns, but allow Blood Moon or Screamer spawns.

So it stops POI sleepers and wandering biome zombies inside the claim, but **not** blood moons or
screamers. Clear the prison once after first entry; the LCB stops them coming back.

## Chunk reset

Your save has already generated this area, so run this once in the F1 console:

    chunkreset 1920 -1412 2509 -358

That covers the whole cluster. It rebuilds terrain from the edited dtm.raw and stamps the builds.

## The builds

| Build | X | Y | Z | size | pad level | cut | fill | from prison |
|---|---|---|---|---|---|---|---|---|
| Prison-perimiter | 2364 | 59 | -868 | 103x103 | 58 m | 4.9 m | 4.0 m | 72 m |
| BunkerPerimiter | 2376 | 60 | -752 | 92x109 | 59 m | 4.5 m | 3.8 m | 76 m |
| House | 2280 | 54 | -772 | 64x67 | 53 m | 6.0 m | 3.4 m | 142 m |
| Tower1 | 2256 | 58 | -828 | 42x44 | 57 m | 1.9 m | 5.5 m | 159 m |
| AyasterMansion | 2292 | 55 | -692 | 49x54 | 54 m | 4.2 m | 4.2 m | 175 m |
| IncredibleTower | 2364 | 59 | -988 | 105x105 | 58 m | 4.9 m | 3.7 m | 178 m |
| Farm1 | 2244 | 43 | -924 | 64x65 | 42 m | 4.3 m | 5.1 m | 202 m |
| UFOhomeBase | 2380 | 60 | -616 | 81x69 | 59 m | 4.2 m | 3.7 m | 204 m |
| bakerywithbunkergarage | 2236 | 40 | -980 | 44x44 | 39 m | 2.7 m | 1.7 m | 242 m |
| CoolHouse1 | 2152 | 39 | -1120 | 65x62 | 38 m | 4.0 m | 3.2 m | 401 m |
| DriveThroughPeremiter | 2048 | 58 | -572 | 102x103 | 57 m | 2.7 m | 5.4 m | 441 m |
| RangerStation | 1964 | 59 | -460 | 65x62 | 58 m | 3.7 m | 3.2 m | 575 m |
| RogueNerds | 1960 | 35 | -1372 | 62x62 | 34 m | 3.3 m | 2.3 m | 718 m |

## Backups

- `dtm.raw.ORIGINAL-BACKUP` - terrain before levelling
- `prefabs.xml.BEFORE-MYPREFABS` - before your 13 were added
- `prefabs.xml.BEFORE-DENSIFY` - before the 124 local mod POIs
- `prefabs.xml.ORIGINAL-BACKUP` - the untouched original
- `spawnpoints.xml.ORIGINAL-BACKUP` - the original 10 spawn points

`dtm_processed.raw` was deleted; the game rebuilds it on next load.
