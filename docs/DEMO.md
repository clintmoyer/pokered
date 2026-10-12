# Pokedogs: first-gym demo

This is a local development fork of pret/pokered. Do not create a GitHub repository or push changes. Make local commits at useful milestones.

## Baseline

- Upstream commit: `af519899719f0754965776faac0e836a3b906e6d`.
- RGBDS: `1.0.4` (also recorded in `.rgbds-version`).
- Unmodified Red SHA-1: `ea9bcae617fdf159b045185467ae58b2e4a48b9a`.
- Unmodified Blue SHA-1: `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`.
- Development branch: `demo/first-gym`.

## Design

Keep the 15 Gen 1 types and the original battle rules, including one combined Special stat. Species names remain at most ten characters; the full breed name appears in Pokédex prose. Keep internal species and move IDs stable so existing scripts and field-move hooks continue to work.

The demo covers Pallet Town, Route 1, Viridian City, Route 22, Route 2, Viridian Forest, Pewter City, and Brock. Later areas are unfinished and retain upstream content.

The starter families are Grass Groenendael (`GROENPUP`, `GROEN`, `GROENHOUND`), Fire Shiba Inu (`SHIBAPUP`, `SHIBA`, `SHIBLAZE`), and Water Newfoundland (`NEWFPUP`, `NEWFIE`, `NEWFTIDE`). Each evolves at levels 16 and 36. All final starters have 425 base-stat points across HP, Attack, Defense, Speed, and Special.

The opening wild roster uses Beagle, Papillon, and Boxer families. Boxer is available before Brock to support the Shiba route. The gym uses Rock Bulldog and Mastiff forms. Twenty dog forms receive names, stats, Pokédex entries, learnsets, and front/back sprites.

New dog moves initially reuse existing effects and animation routines. Every move in the demo dogs' level-up learnsets has a dog-themed display name. HMs preserve their original IDs and field behavior. The larger 151-form conversion is a later milestone.

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
```

The emulator replay starts a new game, selects all three starters, checks their full breed names, and completes the tutorial rival battles. Brock checks use a scripted warp and trained-party fixtures: level-14 Groenendael and Newfoundland puppies, and a level-12 Boxer leading a level-14 Shiba team. They exercise the actual battle, badge, and TM reward scripts. Save/load uses the game's Save menu and Continue in a fresh emulator. Evolution checks use Rare Candy fixtures at levels 15 and 35.

## Art and remaining work

Original draft artwork was generated with the built-in imagegen tool. The two source atlases and exact prompts are in `assets/dogs/`; conversion instructions are in `tools/dogs/convert_sprites.py`. Battle sprites and the shared dog menu icon use the original four-shade format. The title's random species list now contains only demo dogs; the original animated opening and logo remain for a later art pass.

New moves reuse upstream effect and animation routines. Other breeds, later encounters, broader balance work, custom move animations, and new sound design remain future work. The demo does not change the name buffers or save-file layout.
