# Pokedogs: four-gym demo

This is a development fork of pret/pokered on the `dogs` branch of the existing clintmoyer/pokered repository. Make local commits at useful milestones and push this branch when requested. Do not create a new GitHub repository.

## Baseline

- Upstream commit: `af519899719f0754965776faac0e836a3b906e6d`.
- RGBDS: `1.0.4` (also recorded in `.rgbds-version`).
- Unmodified Red SHA-1: `ea9bcae617fdf159b045185467ae58b2e4a48b9a`.
- Unmodified Blue SHA-1: `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`.
- Development branch: `dogs`.

## Design

Keep the 15 Gen 1 types and the original battle rules, including one combined Special stat. Species names remain at most ten characters; the full breed name appears in Pokédex prose. Keep internal species and move IDs stable so existing scripts and field-move hooks continue to work.

The demo covers Pallet Town through Brock, Mt. Moon, Cerulean City, the northern routes and Bill, Misty, Routes 5 and 6, Vermilion City, the S.S. Anne, Route 11, Diglett's Cave, Lt. Surge, Routes 9 and 10, Rock Tunnel, Lavender, Routes 8 and 7, Celadon, the northern Route 16 path and Fly house, and Erika. Later story areas, including the Rocket Hideout and Pokémon Tower battles, are unfinished. The complete planned roster is documented in [FULL_GAME_PLAN.md](FULL_GAME_PLAN.md).

The starter families are Grass Groenendael (`GROENPUP`, `GROEN`, `GROENHOUND`), Fire Shiba Inu (`SHIBAPUP`, `SHIBA`, `SHIBLAZE`), and Water Newfoundland (`NEWFPUP`, `NEWFIE`, `NEWFTIDE`). Each evolves at levels 16 and 36. All final starters have 425 base-stat points across HP, Attack, Defense, Speed, and Special.

All three Groenendael forms use a dedicated black and charcoal Super Game Boy palette for their front and back sprites, while retaining Grass typing. The original four-shade sprite artwork is unchanged.

The opening wild roster uses Beagle, Papillon, and Boxer families. Boxer is available before Brock to support the Shiba route. The gym uses Rock Bulldog and Mastiff forms. Ninety-one dog forms across thirty-nine breed families receive names, stats, Pokédex entries, learnsets, and front/back sprites. The Vermilion chapter adds Border Terrier, Boston Terrier, Staffordshire Bull Terrier, Schnauzer, Bloodhound, and Chihuahua families.

All 165 move slots now use the finalized dog move names and parameters, with existing effect and animation routines. HMs preserve their original IDs and field behavior. Dig, Teleport, and Softboiled field-menu labels are also renamed to match their new battle names. The remaining 60 dog forms are planned but unimplemented.

The seven new wild tables are version-independent. Route 25 offers all three starter puppies (approximately 10% Groenendael, 5% Shiba Inu, and 5% Newfoundland) at level 10. Route 24 supplies Grass Lagotto puppies; Mt. Moon supplies Electric Pomeranian puppies. The Lagotto puppy and adolescent remain pure Grass to serve as Water counters; the adult gains Ground typing.

Misty uses level-18 OTTERPUP and level-21 OTTERMIND, awards the Cascade Badge, and gives TM11 WAKE CHARGE. Her dialogue explains the preserved HM01 unlock. The Mt. Moon seller gives SPRINGPUP; Route 4 also supplies it as a repeatable wild encounter. Bill's separation sequence, S.S. Ticket, and PC previews remain functional with dog art and entries.

Routes 5 and 6 offer Boston Terrier puppies, with Electric Schnauzer and Chihuahua puppies on Route 6. Route 11 offers Bloodhound and Staffordshire Bull Terrier puppies. Diglett's Cave supplies Ground Border Terriers, including adults at levels 24 and 26. All four new wild tables are version-independent and supply repeatable sources for the new families.

The S.S. Ticket gate, ship trainers, three rival variants, captain's HM01 reward, and departure sequence retain the original story scripts. HM01 teaches BRAMBLE BITE, preserves its Cut function, remains reusable, and requires the Cascade Badge to remove bushes. Groenendael and Shiba can learn it; Newfoundland players can use an early Beagle or another compatible companion. The nearby in-game trades now use chapter dogs, with repeatable wild sources for both sides. The fan club's Bicycle Voucher and the Old Rod reward remain available; the Old Rod encounters SPRINGPUP through its stable species slot.

Lt. Surge uses level-21 SCHNAUPUP, level-21 CHIPUP, and level-24 POMSPARK. The original tree barrier and trash-can locks remain functional. Victory grants the Thunder Badge and TM24 VOLT BARK, and unlocks SKYBOUND outside battle. Surge's advice directs the player toward Rock Tunnel and Celadon.


HM05 remains Oak's aide's reward for ten registered forms in the Route 2 gate. BEACON BARK retains Flash's illumination and Boulder Badge requirement. Rock Tunnel has dog encounters and trainer teams on both floors, including repeatable KEESPUP and ELKPUP encounters for both fossil families. Routes 9 and 10 add Australian Cattle Dog, Australian Shepherd, Samoyed, and Portuguese Water Dog puppies, and the tunnel adds Scottish Terriers. Lavender's NPC dogs and species dialogue are updated; the Tower story is a later slice.

Routes 8 and 7 add Akita, Irish Setter, Finnish Spitz, Komondor, German Shepherd, and Belgian Tervuren encounters. The Celadon mansion gives a level-25 TERVPUP, also repeatably catchable on Route 7. Water, Thunder, and Fire Stones produce TIDETERV, SPARKTERV, and FLAMETERV; all three stones remain unlimited department-store purchases. The version-independent Game Corner roster offers POODPUP, SAMOPUP, CATTLEDOG, AKITAFIRE, TERVPUP, and SHEPHGUARD as optional prizes, with wild/evolution sources for all of them.

The northern Route 16 path retains its Cut tree, gate, and HM02 giver. SKYBOUND retains Fly's visited-town menu, travel animation, and Thunder Badge requirement. Erika uses level-29 SUNSETTER, level-24 KOMONDOR, and level-29 TRUFFHOUND. Victory gives the Rainbow Badge, preserves the future HAUL field unlock, and awards TM21 BRIAR FANG. Erika's advice marks the current endpoint.

## Build

Install RGBDS 1.0.4, a C compiler, and make as described in `INSTALL.md`.

```sh
make -j4 demo
```

The emulator-ready result is `build/pokedogs-demo.gb`. Existing `red`, `blue`, and `blue_debug` targets remain available. `make compare` checks the upstream reference hashes and is expected to fail after modifications.

## Verification

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
```

Emulator tests use temporary save files and record screenshots under `build/qa/`.

```sh
.venv/bin/python tools/dogs/validate_rom.py
.venv/bin/python tools/dogs/test_emulator.py
.venv/bin/python tools/dogs/test_misty.py
.venv/bin/python tools/dogs/test_surge.py
.venv/bin/python tools/dogs/test_erika.py
.venv/bin/python tools/dogs/validate_plan.py
```

The emulator replay starts a new game, selects all three starters, checks their full breed names, and completes the tutorial rival battles. Brock checks use a scripted warp and trained-party fixtures: level-16 Groenendael and Newfoundland adolescents, and a level-14 Boxer leading a level-16 Shiba team. They exercise the actual battle, badge, and TM reward scripts. Save/load uses the game's Save menu and Continue in a fresh emulator. Evolution checks use Rare Candy fixtures at levels 15 and 35.

The Misty replay uses trained level-20 parties and map warps. It exercises all three Cerulean rival teams, the three starter routes against Misty (Grass/Electric companions support Fire/Water), both badge and TM reward flags, the real purchase and Bill scripts, Bill's dog PC previews, two-badge save/load, and five additional evolutions. Optional gym trainers are marked beaten in boss fixtures; compiled checks independently inspect all 41 chapter trainer parties. These checks do not replace a continuous playthrough or prove natural difficulty.

The Surge replay earns Bill's ticket and both preceding badges through their actual scripts, then tests ticket rejection and admission, all three ship rival teams with trained level-22 parties, the captain's HM01 reward, HM teaching without consumption, Cascade Badge gating, actual tree removal and gym entry, both trash-can lock scripts, all three starter routes against Surge with a trained Ground companion, ship departure, three-badge save/load, and seven new evolutions. Map warps isolate chapter checks; optional gym trainers are marked beaten. The test reads the randomized lock locations without changing them, then interacts with the correct cans. Compiled checks inspect all 131 chapter trainer placements, eighteen encounter tables, the three ship rival teams, five trades, palettes, and Cut compatibility.


The Erika replay verifies Oak's aide's nine/ten-form reward threshold, HM05 teaching and Boulder Badge gating, illumination through an actual walk across both Rock Tunnel floors, Cut through the northern Route 16 entrance, HM02 teaching and Thunder Badge gating, a real Fly trip to visited Vermilion, the mansion gift, repeated stone purchases and all three Tervuren branches, the diner Coin Case and a Game Corner prize, all three starter routes against Erika, the Rainbow Badge/TM21 reward, four-badge save/load, and fourteen level evolutions. Erika fixtures use level-28 starters and Flying companions; Shiba also has a Yorkshire Terrier, and Newfoundland has a level-26 Beagle for Cut. Capture counts, money, trained parties and map warps are fixtures. Cave and optional gym trainers are marked beaten during traversal, and Repel is renewed to isolate the path checks from wild fights. Compiled checks also verify all six prize species/levels/prices, stone inventory, branch conditions, and HM compatibility.

## Regeneration

The finalized JSON files feed the implementation through `data/dogs/implemented.json`. After editing the appropriate data or source atlases, run:

```sh
.venv/bin/python tools/dogs/generate_data.py
.venv/bin/python tools/dogs/generate_misty.py
.venv/bin/python tools/dogs/generate_surge.py
.venv/bin/python tools/dogs/generate_erika.py
.venv/bin/python tools/dogs/convert_sprites.py
.venv/bin/python tools/dogs/generate_sprite_banks.py
.venv/bin/python tools/dogs/export_plan.py
make -j4 demo
```

Sprite pairs are packed eight species per bank. A banked lookup returns each pair's bank without consuming scarce ROM0 space; original species IDs and save layout remain stable.

## Art and remaining work

Original draft artwork was generated with the built-in imagegen tool. The source atlases and exact prompts are in `assets/dogs/`; conversion instructions are in `tools/dogs/convert_sprites.py`. Battle sprites, the shared dog menu icon, and the six-frame generic overworld dog use the original four-shade format. The title's random species list now contains only demo dogs; the original animated opening and logo remain for a later art pass.

New moves reuse upstream effect and animation routines. The remaining 60 forms, later encounters, collection-source and legendary-retry implementation, continuous playthroughs, broader balance work, custom move animations, and new sound design remain future work. The demo does not change the name buffers or save-file layout.
