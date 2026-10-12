# Pokedogs

A dog-themed Pokémon Red mod. The current demo runs through Erika, with Groenendael, Shiba Inu, and Newfoundland starters, 91 dog forms, all 165 redesigned move entries, original dog sprites, and working Cut, Flash, and Fly.

Build with RGBDS 1.0.4 using `make -j4 demo`, then load `build/pokedogs-demo.gb` in a Game Boy emulator. See [the demo specification](docs/DEMO.md) for scope and verification instructions. Changes are recorded as Git commits on the [`dogs` branch of clintmoyer/pokered](https://github.com/clintmoyer/pokered/tree/dogs).

The [full-game plan](docs/FULL_GAME_PLAN.md) defines all 151 dog forms, the complete move pool, single-ROM collection access, and preserved HM functions.

## Upstream Pokémon Red and Blue [![Build Status][ci-badge]][ci]

This is a disassembly of Pokémon Red and Blue.

It builds the following ROMs:

- Pokemon Red (UE) [S][!].gb `sha1: ea9bcae617fdf159b045185467ae58b2e4a48b9a`
- Pokemon Blue (UE) [S][!].gb `sha1: d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`
- BLUEMONS.GB (debug build) `sha1: 5b1456177671b79b263c614ea0e7cc9ac542e9c4`
- dmgapae0.e69.patch `sha1: 0fb5f743696adfe1dbb2e062111f08f9bc5a293a`
- dmgapee0.e68.patch `sha1: ed4be94dc29c64271942c87f2157bca9ca1019c7`

To set up the repository, see [**INSTALL.md**](INSTALL.md).


## See also

- [**Wiki**][wiki] (includes [tutorials][tutorials])
- [**Symbols**][symbols]
- [**Tools**][tools]

You can find us on [Discord (pret, #pokered)](https://discord.gg/d5dubZ3).

For other pret projects, see [pret.github.io](https://pret.github.io/).

[wiki]: https://github.com/pret/pokered/wiki
[tutorials]: https://github.com/pret/pokered/wiki/Tutorials
[symbols]: https://github.com/pret/pokered/tree/symbols
[tools]: https://github.com/pret/gb-asm-tools
[ci]: https://github.com/pret/pokered/actions
[ci-badge]: https://github.com/pret/pokered/actions/workflows/main.yml/badge.svg
