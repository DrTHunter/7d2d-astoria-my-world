# Astoria 8K - local densification

124 extra mod-POI copies added around the player's area (X 2006, Z -989).
Each replaced a Tier-0 remnant/rubble/empty lot in a real street-tile slot.
Rules: max 2 copies of any POI in the area, never twice in the same town,
copies at least 300 m apart. Rotation from the verified tile-marker law.

Decorations 13051 -> 13051 (124 filler out, 124 POIs in). Backup: `prefabs.xml.BEFORE-DENSIFY`.

## Chunk reset - REQUIRED for your existing save

287 of these sit in chunks your save already generated, so they will NOT appear
until those chunks are rebuilt. In the F1 console, one line per town:

    chunkreset 1272 -1128 2086 -614                # 13 tiles, +36 POIs, 325 m away
    chunkreset 2172 -1428 3136 136                 # 31 tiles, +56 POIs, 721 m away
    chunkreset 1272 -1578 1486 -1214               # 2 tiles, +2 POIs, 748 m away
    chunkreset 3222 -1278 3736 -764                # 5 tiles, +1 POIs, 1503 m away
    chunkreset 972 -3078 1636 -2414                # 13 tiles, +8 POIs, 1874 m away
    chunkreset 522 72 1186 1036                    # 17 tiles, +14 POIs, 1930 m away
    chunkreset 2472 -3378 3286 -2564               # 23 tiles, +7 POIs, 2142 m away

WARNING: chunkreset rebuilds terrain and POIs in that box. It destroys anything
you built there and resets loot containers. Your bedroll at 2672,-738 is inside
the big city box - move it first or expect to re-place it.

## What went where

### 31-tile town at (2656, -677) - 721 m away, +56 POIs

| POI | pack | X | Y | Z | size | replaced |
|---|---|---|---|---|---|---|
| 7Days_Swinger_Pad_by_MPLogue | MPLogue | 2677 | 57 | -413 | 42x42 | `remnant_burnt_02` |
| Ambulance_Station_Zeebark | Zeebark | 2667 | 57 | -547 | 42x42 | `remnant_carwash_01` |
| Bar_Bistro_Zeebark | Zeebark | 2709 | 57 | -547 | 42x42 | `remnant_commercial_strip_03` |
| Boxing_Gym_Voltralux | Voltralux | 2598 | 57 | -698 | 42x42 | `remnant_burnt_05` |
| Camera_Shop_Zeebark | Zeebark | 2478 | 57 | -496 | 25x25 | `remnant_downtown_filler_26` |
| Camping_Store_Zeebark | Zeebark | 2355 | 57 | -397 | 25x25 | `remnant_downtown_filler_14` |
| Cemetery_Zeebark | Zeebark | 2812 | 57 | -921 | 42x42 | `remnant_house_15` |
| Charity_Bar_Duplex_Zeebark | Zeebark | 2505 | 57 | -487 | 25x25 | `rubble_downtown_filler_21` |
| Chippys_Chippy_Zeebark | Zeebark | 2204 | 57 | -308 | 25x25 | `remnant_downtown_filler_12` |
| Church_Zeebark | Zeebark | 2303 | 57 | -343 | 25x25 | `rubble_downtown_filler_02` |
| Cinema_Zeebark | Zeebark | 2505 | 57 | -462 | 25x25 | `remnant_downtown_filler_27` |
| Coffee_Shop_Zeebark | Zeebark | 2436 | 57 | -397 | 25x25 | `remnant_downtown_filler_24` |
| Community_Center_Zeebark | Zeebark | 2656 | 57 | -471 | 42x42 | `remnant_burnt_09` |
| Community_Hall_Zeebark | Zeebark | 2806 | 57 | -471 | 42x42 | `remnant_house_13` |
| Cool_Shooz_Duplex_Zeebark | Zeebark | 2204 | 57 | -283 | 25x25 | `remnant_downtown_filler_30` |
| Crack_a_Book_Zeebark | Zeebark | 2530 | 57 | -413 | 42x42 | `remnant_downtown_strip_20` |
| DiaLogueTowers_by_MPLogue | MPLogue | 2508 | 59 | -341 | 60x60 | `remnant_skyscraper_04` |
| Eternal_Rests_Voltralux | Voltralux | 2513 | 57 | -633 | 42x42 | `remnant_commercial_strip_05` |
| FacePalmInc_by_MPLogue | MPLogue | 2504 | 57 | 37 | 42x42 | `remnant_business_04` |
| Fastfood_Roosters_Voltralux | Voltralux | 2513 | 57 | -549 | 42x42 | `remnant_waste_02` |
| Garden_Centre_Zeebark | Zeebark | 2437 | 57 | -171 | 42x42 | `remnant_downtown_strip_01` |
| Gun_Shop_Kendo_Voltralux | Voltralux | 2204 | 57 | -345 | 25x25 | `rubble_downtown_filler_15` |
| House_Atomic_01_Voltralux | Voltralux | 2760 | 57 | -413 | 42x42 | `remnant_burnt_10` |
| Ice_Skating_Rink_Zeebark | Zeebark | 2699 | 57 | -795 | 60x60 | `remnant_waste_18` |
| Jail_Break_Pizza_Zeebark | Zeebark | 2303 | 57 | -303 | 25x25 | `remnant_downtown_filler_17` |
| Little_Italy_Voltralux | Voltralux | 2360 | 57 | -151 | 60x60 | `remnant_library_01` |
| MidCenturyModernHouse02_by_MPLogue | MPLogue | 2848 | 57 | -627 | 42x42 | `remnant_house_14` |
| Mile_End_Prison_Zeebark | Zeebark | 2654 | 57 | -646 | 60x60 | `remnant_business_02` |
| Mirror_Shop_Zeebark | Zeebark | 2436 | 57 | -372 | 25x25 | `remnant_downtown_filler_22` |
| Oasis_Apartments_Voltralux | Voltralux | 2679 | 57 | -1071 | 42x42 | `remnant_waste_19` |
| Pet_Salon_Zeebark | Zeebark | 2476 | 57 | -397 | 25x25 | `remnant_downtown_filler_18` |
| Pop_n_Pills_Zeebark | Zeebark | 2328 | 57 | -303 | 25x25 | `remnant_downtown_filler_15` |
| Pubic_Libary_by_MPLogue | MPLogue | 2443 | 57 | -260 | 60x60 | `remnant_skyscraper_05` |
| Quad_Zeebark | Zeebark | 2204 | 57 | -257 | 25x25 | `remnant_downtown_filler_28` |
| Quick_Cabs_Voltralux | Voltralux | 2380 | 57 | -397 | 42x42 | `remnant_downtown_strip_19` |
| Rainbow_Pit_by_MPLogue | MPLogue | 2892 | 57 | -746 | 42x42 | `remnant_house_09` |
| Reptile_Store_Zeebark | Zeebark | 2586 | 57 | -495 | 25x25 | `rubble_downtown_filler_18` |
| Retro_Diner_Zeebark | Zeebark | 2824 | 57 | -746 | 42x42 | `remnant_house_06` |
| Shotgun_Messiah_Zeebark | Zeebark | 2529 | 57 | -171 | 42x42 | `remnant_downtown_strip_18` |
| Stuff_N_Books_Zeebark | Zeebark | 2862 | 57 | -926 | 42x42 | `remnant_house_11` |
| The_Holly_Residence_Zeebark | Zeebark | 2866 | 57 | -1013 | 42x42 | `remnant_house_16` |
| Time_Out Diner_Zeebark | Zeebark | 2622 | 57 | -1376 | 25x25 | `lot_industrial_14` |
| Yard_Sale_Zeebark | Zeebark | 2862 | 57 | -858 | 42x42 | `remnant_house_12` |
| ZBites_Zeebark | Zeebark | 2777 | 57 | -943 | 25x25 | `rubble_downtown_filler_24` |
| Zden_Nightclub_Zeebark | Zeebark | 2751 | 57 | -547 | 42x42 | `remnant_business_05` |
| Zee_Antiques_Zeebark | Zeebark | 2390 | 57 | -496 | 25x25 | `remnant_downtown_filler_11` |
| Zee_Bliss_Zeebark | Zeebark | 2416 | 57 | -496 | 25x25 | `remnant_downtown_filler_25` |
| Zee_Hardware_Zeebark | Zeebark | 2437 | 57 | -113 | 42x42 | `remnant_downtown_strip_16` |
| Zee_Plantz_Zeebark | Zeebark | 2654 | 57 | -1013 | 25x25 | `rubble_downtown_filler_23` |
| Zmart_Zeebark | Zeebark | 2778 | 57 | -1013 | 25x25 | `rubble_downtown_filler_25` |
| church_01_svarii | Svarii | 2588 | 57 | -151 | 60x60 | `remnant_church_01` |
| farnsworth_residence_svarii | Svarii | 2700 | 57 | -471 | 42x42 | `remnant_burnt_01` |
| graveyard_01_svarii | Svarii | 2478 | 57 | -1245 | 25x25 | `lot_vacant_04` |
| house_burnt_01_exd_svarii | Svarii | 2759 | 57 | -1278 | 25x25 | `lot_industrial_13` |
| house_old_cottage_oneHalf_svarii | Svarii | 2519 | 57 | -1336 | 25x25 | `lot_industrial_15` |
| park_residential_01_exd_svarii | Svarii | 2441 | 57 | -496 | 25x25 | `remnant_downtown_filler_16` |

### 23-tile town at (2879, -2944) - 2142 m away, +7 POIs

| POI | pack | X | Y | Z | size | replaced |
|---|---|---|---|---|---|---|
| Ambulance_Station_Zeebark | Zeebark | 2965 | 35 | -2731 | 42x42 | `remnant_burnt_08` |
| Crack_a_Book_Zeebark | Zeebark | 2530 | 36 | -2797 | 42x42 | `remnant_downtown_strip_01` |
| Fastfood_Roosters_Voltralux | Voltralux | 3104 | 36 | -2638 | 42x42 | `remnant_carwash_01` |
| Pubic_Libary_by_MPLogue | MPLogue | 2699 | 36 | -2662 | 60x60 | `remnant_hospital_01` |
| Quick_Cabs_Voltralux | Voltralux | 2737 | 36 | -2721 | 42x42 | `remnant_downtown_strip_02` |
| Retro_Diner_Zeebark | Zeebark | 3208 | 36 | -2959 | 42x42 | `remnant_house_09` |
| church_01_svarii | Svarii | 2660 | 36 | -2851 | 60x60 | `remnant_library_02` |

### 17-tile town at (840, 549) - 1930 m away, +14 POIs

| POI | pack | X | Y | Z | size | replaced |
|---|---|---|---|---|---|---|
| Alamo_Restaurant_Voltralux | Voltralux | 896 | 36 | 512 | 42x42 | `remnant_commercial_strip_04` |
| Eternal_Rests_Voltralux | Voltralux | 715 | 36 | 418 | 42x42 | `remnant_carwash_01` |
| Hallucigen_Inc_Voltralux | Voltralux | 729 | 36 | 337 | 42x42 | `remnant_downtown_strip_09` |
| Liberty_Apartments_Voltralux | Voltralux | 788 | 36 | 299 | 60x60 | `remnant_library_01` |
| Mafia_Museum_Voltralux | Voltralux | 729 | 36 | 279 | 42x42 | `remnant_downtown_strip_08` |
| Phabbers_Cafe_Zeebark | Zeebark | 789 | 36 | 422 | 42x42 | `remnant_business_05` |
| The_Holly_Residence_Zeebark | Zeebark | 802 | 36 | 198 | 42x42 | `remnant_burnt_06` |
| Umbrella_Corp_VoltraLux | Voltralux | 568 | 36 | 126 | 100x100 | `remnant_industrial_large_02` |
| Zden_Nightclub_Zeebark | Zeebark | 810 | 36 | 661 | 42x42 | `remnant_burnt_08` |
| Zee_Antiques_Zeebark | Zeebark | 942 | 36 | 139 | 25x25 | `rubble_downtown_filler_12` |
| Zee_Bliss_Zeebark | Zeebark | 909 | 36 | 114 | 25x25 | `rubble_downtown_filler_15` |
| Zee_Plantz_Zeebark | Zeebark | 917 | 36 | 139 | 25x25 | `rubble_downtown_filler_13` |
| park_azaroth_svarii | Svarii | 979 | 36 | 139 | 25x25 | `rubble_downtown_filler_14` |
| park_residential_01_exd_svarii | Svarii | 896 | 36 | 229 | 25x25 | `rubble_downtown_filler_05` |

### 13-tile town at (1713, -847) - 325 m away, +36 POIs

| POI | pack | X | Y | Z | size | replaced |
|---|---|---|---|---|---|---|
| 7Days_Swinger_Pad_by_MPLogue | MPLogue | 1929 | 36 | -1073 | 42x42 | `remnant_house_17` |
| Alamo_Restaurant_Voltralux | Voltralux | 1551 | 36 | -697 | 42x42 | `remnant_burnt_08` |
| Boxing_Gym_Voltralux | Voltralux | 1471 | 36 | -927 | 42x42 | `lot_vacant_05` |
| Camera_Shop_Zeebark | Zeebark | 1877 | 36 | -903 | 25x25 | `remnant_downtown_filler_20` |
| Camping_Store_Zeebark | Zeebark | 1852 | 36 | -943 | 25x25 | `remnant_downtown_filler_16` |
| Charity_Bar_Duplex_Zeebark | Zeebark | 1877 | 36 | -1093 | 25x25 | `rubble_downtown_filler_13` |
| Chippys_Chippy_Zeebark | Zeebark | 1879 | 36 | -864 | 25x25 | `rubble_downtown_filler_03` |
| Church_Zeebark | Zeebark | 1827 | 36 | -943 | 25x25 | `remnant_downtown_filler_19` |
| Cinema_Zeebark | Zeebark | 1852 | 36 | -1093 | 25x25 | `remnant_downtown_filler_09` |
| Cocktail_Bar_Zeebark | Zeebark | 1813 | 36 | -972 | 25x25 | `rubble_downtown_filler_14` |
| Coffee_Shop_Zeebark | Zeebark | 1827 | 36 | -1093 | 25x25 | `remnant_downtown_filler_21` |
| Computer_Store_Zeebark | Zeebark | 1788 | 36 | -972 | 25x25 | `remnant_downtown_filler_01` |
| Cool_Shooz_Duplex_Zeebark | Zeebark | 1763 | 36 | -972 | 25x25 | `remnant_downtown_filler_23` |
| FacePalmInc_by_MPLogue | MPLogue | 1779 | 36 | -945 | 42x42 | `remnant_downtown_strip_05` |
| Fanz_Duplex_Zeebark | Zeebark | 1813 | 36 | -822 | 25x25 | `remnant_downtown_filler_18` |
| Gun_Shop_Kendo_Voltralux | Voltralux | 1879 | 36 | -1014 | 25x25 | `rubble_downtown_filler_16` |
| Hallucigen_Inc_Voltralux | Voltralux | 1780 | 36 | -878 | 42x42 | `remnant_downtown_strip_07` |
| Jail_Break_Pizza_Zeebark | Zeebark | 1755 | 36 | -1053 | 25x25 | `remnant_downtown_filler_08` |
| KickFlipz_Skate_Store_Voltralux | Voltralux | 1877 | 36 | -943 | 25x25 | `remnant_downtown_filler_14` |
| MidCenturyModernHouse01_by_MPLogue | MPLogue | 2010 | 36 | -863 | 42x42 | `remnant_house_18` |
| MidCenturyModernHouse02_by_MPLogue | MPLogue | 1962 | 36 | -776 | 42x42 | `remnant_house_09` |
| Mirror_Shop_Zeebark | Zeebark | 1755 | 36 | -903 | 25x25 | `remnant_downtown_filler_24` |
| Pet_Salon_Zeebark | Zeebark | 1788 | 36 | -822 | 25x25 | `remnant_downtown_filler_22` |
| Pop_n_Pills_Zeebark | Zeebark | 1729 | 36 | -904 | 25x25 | `remnant_downtown_filler_07` |
| Quad_Zeebark | Zeebark | 1763 | 36 | -822 | 25x25 | `remnant_downtown_filler_02` |
| Rainbow_Pit_by_MPLogue | MPLogue | 1962 | 36 | -708 | 42x42 | `remnant_house_06` |
| Reptile_Store_Zeebark | Zeebark | 1729 | 36 | -863 | 25x25 | `remnant_downtown_filler_05` |
| Retro_Cafe_Zeebark | Zeebark | 1621 | 36 | -946 | 25x25 | `rubble_downtown_filler_11` |
| Time_Out Diner_Zeebark | Zeebark | 1646 | 36 | -822 | 25x25 | `rubble_downtown_filler_17` |
| Video_Rental_Voltralux | Voltralux | 1877 | 36 | -1053 | 25x25 | `remnant_downtown_filler_04` |
| Wagon_Trail_Cafe_Zeebark | Zeebark | 1606 | 36 | -839 | 25x25 | `remnant_downtown_filler_06` |
| ZBites_Zeebark | Zeebark | 1559 | 36 | -828 | 25x25 | `lot_industrial_06` |
| Zmart_Zeebark | Zeebark | 1519 | 36 | -931 | 25x25 | `lot_industrial_07` |
| graveyard_01_svarii | Svarii | 1364 | 36 | -686 | 25x25 | `lot_industrial_08` |
| house_burnt_01_exd_svarii | Svarii | 1422 | 36 | -926 | 25x25 | `lot_industrial_09` |
| house_old_cottage_oneHalf_svarii | Svarii | 1324 | 36 | -789 | 25x25 | `lot_industrial_10` |

### 13-tile town at (1309, -2728) - 1874 m away, +8 POIs

| POI | pack | X | Y | Z | size | replaced |
|---|---|---|---|---|---|---|
| Bar_Bistro_Zeebark | Zeebark | 1370 | 78 | -2896 | 42x42 | `remnant_carwash_01` |
| Cemetery_Zeebark | Zeebark | 1558 | 78 | -2809 | 42x42 | `remnant_house_09` |
| Community_Center_Zeebark | Zeebark | 1558 | 78 | -2877 | 42x42 | `remnant_house_11` |
| Little_Italy_Voltralux | Voltralux | 1160 | 78 | -2701 | 60x60 | `remnant_hospital_01` |
| RPD_Voltralux | Voltralux | 1340 | 78 | -2568 | 100x100 | `remnant_industrial_large_02` |
| Shotgun_Messiah_Zeebark | Zeebark | 1237 | 78 | -2721 | 42x42 | `remnant_downtown_strip_05` |
| Stuff_N_Books_Zeebark | Zeebark | 1305 | 78 | -2896 | 42x42 | `remnant_commercial_strip_03` |
| farnsworth_residence_svarii | Svarii | 1252 | 78 | -2582 | 42x42 | `remnant_burnt_05` |

### 5-tile town at (3509, -1021) - 1503 m away, +1 POIs

| POI | pack | X | Y | Z | size | replaced |
|---|---|---|---|---|---|---|
| Central_Station_Voltralux | Voltralux | 3268 | 36 | -1074 | 100x100 | `remnant_industrial_large_01` |

### 2-tile town at (1379, -1396) - 748 m away, +2 POIs

| POI | pack | X | Y | Z | size | replaced |
|---|---|---|---|---|---|---|
| Community_Hall_Zeebark | Zeebark | 1358 | 57 | -1538 | 42x42 | `remnant_house_06` |
| House_Atomic_01_Voltralux | Voltralux | 1392 | 57 | -1496 | 42x42 | `remnant_house_09` |
