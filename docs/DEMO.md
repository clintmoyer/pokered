# Pokedogs: two-gym demo

This is a development fork of pret/pokered on the `dogs` branch of the existing clintmoyer/pokered repository. Make local commits at useful milestones and push this branch when requested. Do not create a new GitHub repository.

## Baseline

- Upstream commit: `af519899719f0754965776faac0e836a3b906e6d`.
- RGBDS: `1.0.4` (also recorded in `.rgbds-version`).
- Unmodified Red SHA-1: `ea9bcae617fdf159b045185467ae58b2e4a48b9a`.
- Unmodified Blue SHA-1: `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`.
- Development branch: `dogs`.

## Design

Keep the 15 Gen 1 types and the original battle rules, including one combined Special stat. Species names remain at most ten characters; the full breed name appears in Pokédex prose. Keep internal species and move IDs stable so existing scripts and field-move hooks continue to work.

The demo covers Pallet Town through Brock, then Route 3, Route 4, Mt. Moon, Cerulean City, Routes 24 and 25, Bill, and Misty. Later areas are unfinished and retain upstream species and story content. The complete planned roster is documented in [FULL_GAME_PLAN.md](FULL_GAME_PLAN.md).

The starter families are Grass Groenendael (`GROENPUP`, `GROEN`, `GROENHOUND`), Fire Shiba Inu (`SHIBAPUP`, `SHIBA`, `SHIBLAZE`), and Water Newfoundland (`NEWFPUP`, `NEWFIE`, `NEWFTIDE`). Each evolves at levels 16 and 36. All final starters have 425 base-stat points across HP, Attack, Defense, Speed, and Special.

The opening wild roster uses Beagle, Papillon, and Boxer families. Boxer is available before Brock to support the Shiba route. The gym uses Rock Bulldog and Mastiff forms. Forty-eight dog forms across twenty breed families receive names, stats, Pokédex entries, learnsets, and front/back sprites. New families include Yorkshire Terrier, Whippet, Greyhound, Dachshund, Pomeranian, Jack Russell Terrier, Cocker Spaniel, Italian Greyhound, Lagotto Romagnolo, Poodle, Otterhound, and English Springer Spaniel.

All 165 move slots now use the finalized dog move names and parameters, with existing effect and animation routines. HMs preserve their original IDs and field behavior. Dig, Teleport, and Softboiled field-menu labels are also renamed to match their new battle names. The remaining 103 dog forms are planned but unimplemented.

The seven new wild tables are version-independent. Route 25 offers all three starter puppies (approximately 10% Groenendael, 5% Shiba Inu, and 5% Newfoundland) at level 10. Route 24 supplies Grass Lagotto puppies; Mt. Moon supplies Electric Pomeranian puppies. The Lagotto puppy and adolescent remain pure Grass to serve as Water counters; the adult gains Ground typing.

Misty uses level-18 OTTERPUP and level-21 OTTERMIND, awards the Cascade Badge, and gives TM11 WAKE CHARGE. Her dialogue explains the preserved HM01 unlock. The Mt. Moon seller gives SPRINGPUP; Route 4 also supplies it as a repeatable wild encounter. Bill's separation sequence, S.S. Ticket, and PC previews remain functional with dog art and entries.

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
.venv/bin/python tools/dogs/validate_plan.py
```

The emulator replay starts a new game, selects all three starters, checks their full breed names, and completes the tutorial rival battles. Brock checks use a scripted warp and trained-party fixtures: level-16 Groenendael and Newfoundland adolescents, and a level-14 Boxer leading a level-16 Shiba team. They exercise the actual battle, badge, and TM reward scripts. Save/load uses the game's Save menu and Continue in a fresh emulator. Evolution checks use Rare Candy fixtures at levels 15 and 35.

The Misty replay uses trained level-20 parties and map warps. It exercises all three Cerulean rival teams, the three starter routes against Misty (Grass/Electric companions support Fire/Water), both badge and TM reward flags, the real purchase and Bill scripts, Bill's dog PC previews, two-badge save/load, and five additional evolutions. Optional gym trainers are marked beaten in boss fixtures; compiled checks independently inspect all 41 chapter trainer parties. These checks do not replace a continuous playthrough or prove natural difficulty.

## Regeneration

The finalized JSON files feed the implementation through `data/dogs/implemented.json`. After editing the appropriate data or source atlases, run:

```sh
.venv/bin/python tools/dogs/generate_data.py
.venv/bin/python tools/dogs/generate_misty.py
.venv/bin/python tools/dogs/convert_sprites.py
.venv/bin/python tools/dogs/generate_sprite_banks.py
.venv/bin/python tools/dogs/export_plan.py
make -j4 demo
```

Sprite pairs are packed eight species per bank. A banked lookup returns each pair's bank without consuming scarce ROM0 space; original species IDs and save layout remain stable.

## Art and remaining work

Original draft artwork was generated with the built-in imagegen tool. The source atlases and exact prompts are in `assets/dogs/`; conversion instructions are in `tools/dogs/convert_sprites.py`. Battle sprites, the shared dog menu icon, and the six-frame generic overworld dog use the original four-shade format. The title's random species list now contains only demo dogs; the original animated opening and logo remain for a later art pass.

New moves reuse upstream effect and animation routines. The remaining 103 forms, later encounters, collection-source and legendary-retry implementation, continuous playthroughs, broader balance work, custom move animations, and new sound design remain future work. The demo does not change the name buffers or save-file layout.
