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
