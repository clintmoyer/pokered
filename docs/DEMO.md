# Pokedogs: full adventure and postgame

This is a development fork of pret/pokered on the `dogs` branch of the existing clintmoyer/pokered repository. Make local commits at useful milestones and push this branch when requested. Do not create a new GitHub repository.

## Baseline

- Upstream commit: `af519899719f0754965776faac0e836a3b906e6d`.
- RGBDS: `1.0.4` (also recorded in `.rgbds-version`).
- Unmodified Red SHA-1: `ea9bcae617fdf159b045185467ae58b2e4a48b9a`.
- Unmodified Blue SHA-1: `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`.
- Development branch: `dogs`.

## Design

Keep the 15 Gen 1 types and the original battle rules, including one combined Special stat. Species names remain at most ten characters; the full breed name appears in Pokédex prose. Keep internal species and move IDs stable so existing scripts and field-move hooks continue to work.

The demo covers Pallet Town through Brock, Mt. Moon, Cerulean City, the northern routes and Bill, Misty, Routes 5 and 6, Vermilion City, the S.S. Anne, Route 11, Diglett's Cave, Lt. Surge, Routes 9 and 10, Rock Tunnel, Lavender, Routes 8 and 7, Celadon, the northern Route 16 path and Fly house, Erika, the Rocket Hideout, Pokémon Tower, Routes 12–15 and 17–19, Fuchsia City, the Safari Zone, Koga, Saffron City, the Fighting Dojo, Silph Co., Sabrina, Routes 20 and 21, Seafoam Islands, Cinnabar Island, the lab, the Pokémon Mansion, Blaine, the Power Plant, Viridian Gym, both Route 22 rival encounters, Route 23, Victory Road, Indigo Plateau, the Elite Four, the Champion the Hall of Fame, and all three floors of Cerulean Cave. All 151 dog forms are implemented, with single-ROM collection access audited from the compiled ROM. See [COLLECTION.md](COLLECTION.md) for an obtainable path to every form. The complete planned roster is documented in [FULL_GAME_PLAN.md](FULL_GAME_PLAN.md).

The starter families are Grass Groenendael (`GROENPUP`, `GROEN`, `GROENHOUND`), Fire Shiba Inu (`SHIBAPUP`, `SHIBA`, `SHIBLAZE`), and Water Newfoundland (`NEWFPUP`, `NEWFIE`, `NEWFTIDE`). Each evolves at levels 16 and 36. All final starters have 425 base-stat points across HP, Attack, Defense, Speed, and Special.

All three Groenendael forms use a dedicated black and charcoal Super Game Boy palette for their front and back sprites, while retaining Grass typing. The original four-shade sprite artwork is unchanged.

The opening wild roster uses Beagle, Papillon, and Boxer families. Boxer is available before Brock to support the Shiba route. The gym uses Rock Bulldog and Mastiff forms. 151 dog forms across 79 breed families receive names, stats, Pokédex entries, learnsets, and front/back sprites. The Vermilion chapter adds Border Terrier, Boston Terrier, Staffordshire Bull Terrier, Schnauzer, Bloodhound, and Chihuahua families.

All 165 move slots now use the finalized dog move names and parameters, with existing effect and animation routines. HMs preserve their original IDs and field behavior. Dig, Teleport, and Softboiled field-menu labels are also renamed to match their new battle names. The final two forms are PSIGUARD, a Psychic Caucasian Shepherd Dog, and MUDIMYTH, a Psychic/Grass Mudi.

The seven new wild tables are version-independent. Route 25 offers all three starter puppies (approximately 10% Groenendael, 5% Shiba Inu, and 5% Newfoundland) at level 10. Route 24 supplies Grass Lagotto puppies; Mt. Moon supplies Electric Pomeranian puppies. The Lagotto puppy and adolescent remain pure Grass to serve as Water counters; the adult gains Ground typing.

Misty uses level-18 OTTERPUP and level-21 OTTERMIND, awards the Cascade Badge, and gives TM11 WAKE CHARGE. Her dialogue explains the preserved HM01 unlock. The Mt. Moon seller gives SPRINGPUP; Route 4 also supplies it as a repeatable wild encounter. Bill's separation sequence, S.S. Ticket, and PC previews remain functional with dog art and entries.

Routes 5 and 6 offer Boston Terrier puppies, with Electric Schnauzer and Chihuahua puppies on Route 6. Route 11 offers Bloodhound and Staffordshire Bull Terrier puppies. Diglett's Cave supplies Ground Border Terriers, including adults at levels 24 and 26. All four new wild tables are version-independent and supply repeatable sources for the new families.

The S.S. Ticket gate, ship trainers, three rival variants, captain's HM01 reward, and departure sequence retain the original story scripts. HM01 teaches BRAMBLE BITE, preserves its Cut function, remains reusable, and requires the Cascade Badge to remove bushes. Groenendael and Shiba can learn it; Newfoundland players can use an early Beagle or another compatible companion. The nearby in-game trades now use chapter dogs, with repeatable wild sources for both sides. The fan club's Bicycle Voucher and the Old Rod reward remain available; the Old Rod encounters SPRINGPUP through its stable species slot.

Lt. Surge uses level-21 SCHNAUPUP, level-21 CHIPUP, and level-24 POMSPARK. The original tree barrier and trash-can locks remain functional. Victory grants the Thunder Badge and TM24 VOLT BARK, and unlocks SKYBOUND outside battle. Surge's advice directs the player toward Rock Tunnel and Celadon.


HM05 remains Oak's aide's reward for ten registered forms in the Route 2 gate. BEACON BARK retains Flash's illumination and Boulder Badge requirement. Rock Tunnel has dog encounters and trainer teams on both floors, including repeatable KEESPUP and ELKPUP encounters for both fossil families. Routes 9 and 10 add Australian Cattle Dog, Australian Shepherd, Samoyed, and Portuguese Water Dog puppies, and the tunnel adds Scottish Terriers. Lavender's NPC dogs and species dialogue are updated; the Tower story continues in the Koga chapter.

Routes 8 and 7 add Akita, Irish Setter, Finnish Spitz, Komondor, German Shepherd, and Belgian Tervuren encounters. The Celadon mansion gives a level-25 TERVPUP, also repeatably catchable on Route 7. Water, Thunder, and Fire Stones produce TIDETERV, SPARKTERV, and FLAMETERV; all three stones remain unlimited department-store purchases. The version-independent Game Corner roster offers POODPUP, SAMOPUP, CATTLEDOG, AKITAFIRE, TERVPUP, and SHEPHGUARD as optional prizes, with wild/evolution sources for all of them.

The northern Route 16 path retains its Cut tree, gate, and HM02 giver. SKYBOUND retains Fly's visited-town menu, travel animation, and Thunder Badge requirement. Erika uses level-29 SUNSETTER, level-24 KOMONDOR, and level-29 TRUFFHOUND. Victory gives the Rainbow Badge, unlocks HAUL outside battle, and awards TM21 BRIAR FANG. Erika's advice directs the player to the Game Corner poster and Lavender Tower.

The Rocket Hideout keeps its poster guard, switch, arrow floors, Lift Key drop, keyed elevator, two door guards, Giovanni fight and Silph Scope pickup. Giovanni uses level-25 STONEMAST, level-24 BULLTPUP and level-29 GREATDANE. Tower rivals retain three starter variants. Channelers use Ghost Weimaraners; the Scope reveals the uncatchable SCOTTDIG mother, and the three upper-floor Rockets guard Fuji. Rescuing Fuji awards the Poké Flute. Both sleeping NEOMAST encounters clear the original roadblocks, and a rare Route 18 wild source provides a repeatable collection fallback.

Routes 12–15 and Cycling Road have dog encounters and teams. The Safari Zone retains its fee, thirty balls, step limit, four areas and catch/flee mechanics, with identical Red/Blue dog tables. It supplies Bichon Frise, Bull Terrier, Bernese Mountain Dog, Saint Bernard, Cavalier, Great Dane, Lhasa Apso, Malinois, Border Collie, Ridgeback and Lundehund families. The latter evolves at levels 30 and 50; all other new ordinary two-form families evolve at 24, and Weimaraners evolve at 16/32. Good and Super Rod groups are dog-only and repeatable. The shared Routes 19/20 Surf table includes Spanish Water Dog, Irish Water Spaniel, Chesapeake Bay Retriever, Barbet and American Water Spaniel families.

The Secret House awards reusable HM03 DOG PADDLE. Returning the Gold Teeth gives reusable HM04 HAUL. HAUL preserves the Rainbow Badge check and boulder movement; DOG PADDLE preserves the Soul Badge check, water movement and landing. Koga uses level-37 PUGHAZE, level-39 SHARPEI, level-37 CATTLEGARD and level-43 PUGHAZE, awards the Soul Badge and TM06 VENOM MARK, and directs the player to Saffron and Silph. Fuchsia's zoo displays dog sprites, breed entries and updated signs.

Saffron retains the shared thirsty-guard flag and drink requirement; Celadon roof vending purchases unlock city access. The Fighting Dojo master uses level-37 DOBERGUARD and ROTTGUARD, with the original choice of one level-30 gift. Both breeds also have rare, repeatable level-30 Safari Zone North encounters, so the gift choice does not exclude either dog. Mr. Psychic gives TM29 MIND HOWL, and Copycat's Poké Doll exchange gives TM31 COPY TRICK. City and house dogs and species dialogue are updated.

All eleven Silph floors retain their stairs, elevator, warp pads, Card Key doors, nurse, rival encounter and rescue scripts. The three rival teams preserve the selected starter relationship and use mature dog forms. Silph's worker gives one level-30 LEONTIDE (Leonberger), also repeatably encountered while surfing on Routes 19/20. Giovanni uses level-37 AUSSGUARD, level-35 GREATDANE, level-37 BULLTANK and level-41 CATTLEGARD. Defeating him removes the city's Rocket guards, opens Sabrina's gym and lets the president award one Master Ball.

Sabrina's warp maze and seven trainers use the original map and scripts. Her team is level-38 POODMIND, level-37 LHASA, level-38 CRESTWING and level-43 POODMIND. The Marsh Badge and TM46 AURA PULSE retain their reward IDs and level-70 obedience effect. Sabrina directs the player toward Seafoam and Cinnabar. Her gym guide recommends Bug attacks; the original Gen 1 Ghost/Psychic matchup remains in force.

Seafoam's five floors have shared Red/Blue dog tables, including repeatable Siberian Husky and rare Irish Wolfhound encounters. The original two boulders drop through three floors to stop the eastern current; the lower four-boulder puzzle stops the western current. Surf, Strength, stairs, dungeon falls and cave exits retain their original mechanics. The level-50 FROSTMAUL guardian uses an overworld dog sprite and Alaskan Malamute battle art. Catching it removes the encounter permanently. If it is fled from or defeated, a subsequent Hall of Fame entry restores its flag and object before saving. This retry hook is implemented for all five guardians: FROSTMAUL, STORMLAEK, SUNMAST, PSIGUARD and MUDIMYTH.

Routes 20 and 21 have dog trainer teams, with a shared coastal Surf table and a new Route 21 grass/Surf table. Cinnabar's lab preserves all three level-30 fossil revivals: Dome gives ELKPUP, Helix gives KEESPUP and Old Amber gives WOLFGALE. The first two have repeatable Rock Tunnel sources and WOLFGALE has rare Seafoam encounters, so revival is a bonus. All three lab trades use repeatably obtainable dogs and remove the old trade-evolution dialogue. The TM35 gift is WILD TRICK, and the lab's stone and guardian hints match the dog roster.

The Mansion retains all four floors, alternating statue switches, the third-floor fall, diaries and Secret Key pickup. Its version-independent encounters include Chow Chow, and its six trainer placements use dog teams. Cinnabar's gym rejects entry without the Secret Key. The six quiz answers retain their original flags, with questions rewritten around dog growth, types, stones, stats and moves. Wrong answers still start trainer battles; correct answers open their corresponding doors. Blaine uses level-42 AKITAFIRE, level-40 SUNSPITZ, level-42 CHOWFLARE and level-47 AKITAFIRE. The Volcano Badge retains its Special-stat boost and TM38 teaches FLAME POUNCE. Blaine directs the player back to Viridian and toward the optional Power Plant.

The Power Plant retains its Route 10 Surf approach, eight item-disguised wild encounters, and TM25 STORM HOWL/TM33 PACK SHIELD pickups. Its shared Red/Blue table adds repeatable level-28/32/36 DALMSPARK (Dalmatian) encounters. The level-50 STORMLAEK guardian is a Belgian Laekenois with Electric/Flying typing, a wiry fawn palette and an overworld dog sprite. Catching it removes it permanently; fleeing or defeating it allows another challenge after a Hall of Fame entry. The two retry checks use the permanent caught Pokédex bits independently, including after a caught dog is released.

Viridian Gym retains the gate requiring all seven earlier badges, its spinner floors and eight trainer placements. Giovanni uses level-45 BULLTANK, level-42 BORDERDIG, level-44 CATTLEGARD, level-45 AUSSGUARD and level-50 BULLTANK. The Earth Badge permits obedience at all levels, and TM27 teaches FAULT FANG with the original Ground one-hit-KO effect and accuracy. His departure and the late Route 22 rival spawn retain their original scripts. All three late rival teams have six mature dog forms at levels 45–53, preserving the starter relationship; all three early rival variants are also dog-only. The gym guide directs the player through Route 23 and Victory Road to the League. Route 22's early wild table remains available for opening support.

Route 23 keeps all eight badge gates, including the Boulder check in the entrance building and the Surf crossing between the Soul and Marsh checks. Its dog grass encounters and all three Victory Road tables are identical in Red and Blue. Victory Road retains its three switch floors, movable boulders, stairs, third-floor hole and final exit. Eleven trainer placements use mature dog teams. The level-50 SUNMAST guardian has Tibetan Mastiff art, Fire/Flying typing and a dark brown palette. Its retry hook restores an uncaught encounter after a Hall of Fame entry; caught guardians remain gone even after release.

Indigo Plateau retains its nurse, shop and League entrance. Lorelei uses GOLDTIDE, CHESSTIDE, BASSET, HUSKY and LEONTIDE at levels 53–56. Bruno uses STONEMAST, ROTTGUARD, DOBERGUARD, STONEMAST and STAFFGUARD at levels 53–58. Agatha uses WEIMWRAITH, IGGALE, XOLO, DACHSHUND and WEIMWRAITH at levels 55–60. Lance uses BARBTIDE, two LUNDEWYRM, WOLFGALE and a final LUNDEWYRM at levels 56–62. The final dog's fourth move is the ace move: WHITEOUT YIP, SKY PAW, VENOM MARK and WYRM BARK respectively. Each ace move is in that dog's learnset or TM compatibility. Changing the old third-slot overrides preserves the rest of the learned moves and avoids duplicate signatures.

The Champion has all three six-dog teams at levels 59–65, ending in the rival's fully grown starter. WINDWHIP retains GALE FANG; the starter retains its own learned SUN HOWL, FLAME POUNCE or TIDAL BARK. The original five-battle sequence, locked exits, loss/restart behavior, Oak's arrival, six-dog Hall of Fame record, automatic save, Pallet Town return and League reset remain functional. The Hall of Fame opens Cerulean Cave and restores any uncaught guardians before saving.

## Cerulean Cave and collection completion

The original Cave guard admits the Champion after the earned Hall of Fame entry. All three floors have shared Red/Blue dog encounters. PSIGUARD waits in the basement at level 60; MUDIMYTH waits in the 2F maze at level 50. Both have distinct front/back sprites, full breed Pokédex entries, the planned five stats and learnsets, and explicit TM/HM compatibility. MUDIMYTH uses Mew's separate base-stat path and the common dog sprite bank lookup.

All five guardians return after a later Hall of Fame entry if they were defeated or fled from. Once caught, their Pokédex-owned bit keeps them gone even after release. MUDIMYTH uses a reserved event bit and script byte, and an appended toggle flag inside the existing 256-bit array, preserving earlier save offsets and object/item IDs. The original three 2F item flags keep their IDs.

The compiled collection audit follows actual map/wild pointers, encounter terrain and levels, rod groups, static guardians, and evolution bytes in Red, Blue and Debug. It reaches all 151 forms from 124 directly encounterable forms and 72 level/stone evolution edges. All base breeds have repeatable encounters or a retryable guardian; unlimited Celadon stones cover all three Tervuren branches. Starter, fossil and Dojo choices do not prevent completion. The Celadon game designer now awards the diploma only at 151 forms.

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
.venv/bin/python tools/dogs/test_koga.py
.venv/bin/python tools/dogs/test_sabrina.py
.venv/bin/python tools/dogs/test_blaine.py
.venv/bin/python tools/dogs/test_giovanni.py --early
.venv/bin/python tools/dogs/test_giovanni.py
.venv/bin/python tools/dogs/test_league.py
.venv/bin/python tools/dogs/test_postgame.py
.venv/bin/python tools/dogs/validate_collection.py --report
.venv/bin/python tools/dogs/validate_plan.py
```

The emulator replay starts a new game, selects all three starters, checks their full breed names, and completes the tutorial rival battles. Brock checks use a scripted warp and trained-party fixtures: level-16 Groenendael and Newfoundland adolescents, and a level-14 Boxer leading a level-16 Shiba team. They exercise the actual battle, badge, and TM reward scripts. Save/load uses the game's Save menu and Continue in a fresh emulator. Evolution checks use Rare Candy fixtures at levels 15 and 35.

The Misty replay uses trained level-20 parties and map warps. The Shiba rival fixture has both Electric and Grass support. It exercises all three Cerulean rival teams, the three starter routes against Misty (Grass/Electric companions support Fire/Water), both badge and TM reward flags, the real purchase and Bill scripts, Bill's dog PC previews, two-badge save/load, and five additional evolutions. Optional gym trainers are marked beaten in boss fixtures; compiled checks independently inspect all 41 chapter trainer parties. These checks do not replace a continuous playthrough or prove natural difficulty.

The Surge replay earns Bill's ticket and both preceding badges through their actual scripts, then tests ticket rejection and admission, all three ship rival teams with trained level-22 parties, the captain's HM01 reward, HM teaching without consumption, Cascade Badge gating, actual tree removal and gym entry, both trash-can lock scripts, all three starter routes against Surge with a trained Ground companion, ship departure, three-badge save/load, and seven new evolutions. Map warps isolate chapter checks; optional gym trainers are marked beaten. The test reads the randomized lock locations without changing them, then interacts with the correct cans. Compiled checks inspect all 327 chapter trainer placements, 49 encounter tables, the three ship rival teams, five trades, palettes, and Cut compatibility.


The Erika replay verifies Oak's aide's nine/ten-form reward threshold, HM05 teaching and Boulder Badge gating, illumination through an actual walk across both Rock Tunnel floors, Cut through the northern Route 16 entrance, HM02 teaching and Thunder Badge gating, a real Fly trip to visited Vermilion, the mansion gift, repeated stone purchases and all three Tervuren branches, the diner Coin Case and a Game Corner prize, all three starter routes against Erika, the Rainbow Badge/TM21 reward, four-badge save/load, and fourteen level evolutions. Erika fixtures use level-28 starters and Flying companions, with level-32 Flying support for Newfoundland; Groenendael and Shiba also have a Yorkshire Terrier, and Newfoundland has a level-26 Beagle for Cut. Capture counts, money, trained parties and map warps are fixtures. Cave and optional gym trainers are marked beaten during traversal, and Repel is renewed to isolate the path checks from wild fights. Compiled checks also verify all six prize species/levels/prices, stone inventory, branch conditions, and HM compatibility.

The Koga replay consumes a matching-ROM checkpoint from the Erika replay. It tests the poster switch, Lift Key rejection/drop, keyed elevator, both door guards and Giovanni's Scope reward; three Tower rival variants; the Scope gate, uncatchable mother, upper-floor Rockets, Fuji and flute; both sleeping dogs; a real Safari grass encounter and capture with Safari Balls; a paid Safari walk to the Gold Teeth and Secret House; HM teaching, Rainbow-gated boulder movement, three starter teams against Koga, the Soul Badge/TM06 reward, Soul-gated Surf and landing, five-badge save/load and 20 new level evolutions. Story parties are level 32, with level-36 Water/Psychic/Electric support for the mother and upper-floor Rockets; Koga parties have a level-40 starter, Bloodhound and Border Terrier. Money, room warps, Repel and optional trainers are fixtures. Evolution checks also verify the recalculated five stats after the bank relocation. These checks do not prove a continuous playthrough or full-game collection. Compiled checks additionally enforce every new family's repeatable source, all fishing groups and the actual coastal encounter pointers.

The Sabrina replay uses a matching-ROM checkpoint from the Koga replay. It checks drink rejection, an actual vending purchase and city entry, the occupied gym entrance, Mr. Psychic's reward, the Dojo master and both exclusive gift branches, Silph entry and elevator travel, Card Key rejection and persistent unlocks, real warp-pad travel, all three rival variants, Leonberger adoption, nurse recovery, the boardroom guard, Giovanni, the president's one-time reward, a purchased Poké Doll and Copycat's one-time TM exchange, post-rescue gym access, four real jumps through Sabrina's warp maze, all three starter teams, the Marsh Badge/TM46 reward and six-badge save/load. Parties, money, inventory room, floor-entry warps and optional trainer flags are fixtures. Sabrina fixtures use level-48 Bug support and a level-44 starter; the support levels keep the scripted replay reliable without changing battle balance. The prior Surge fixture uses an adult level-24 Border Terrier obtainable in Diglett's Cave, matching its new evolution threshold.

The Blaine replay uses a matching-ROM Sabrina checkpoint. It pushes the boulders through three floors, follows actual dungeon falls, checks the strong-current ride before the eastern dam is complete, uses Surf, solves the lower boulder puzzle and reaches the guardian island. It exits Seafoam through a floor-entry fixture and uses actual Surf movement across Route 20 to land on Cinnabar. It tests the level-50 guardian's capture, flee and defeat branches, then enters the Hall of Fame through a map-warp fixture to exercise the real retry/save hook: only an uncaught guardian returns. This isolated check does not test the League challenge. The replay also walks the Mansion's stairs and third-floor fall, toggles its actual switches, collects the Secret Key, tests locked/keyed gym entry, a wrong-answer battle and six correct quiz doors, three level-48 starter teams with Water/Ground support against Blaine, the badge/TM38 rewards, seven-badge save/load, all three fossil revivals and the one-time TM35 gift. Parties, inventory room, fossil items, floor-entry warps, optional trainer flags and Repel are fixtures. Navigation reads the loaded blocks and respects cave elevation collisions; no puzzle, capture or victory flags are injected.

The Giovanni replay uses matching-ROM Sabrina and Blaine checkpoints. It follows the actual Surf route from the northern Route 10 shore into the Power Plant, catches a naturally encountered Dalmatian, triggers all eight disguised dogs, and picks up both TMs. It tests STORMLAEK capture, flee and defeat, and both real Hall of Fame retry hooks while confirming that the already-caught FROSTMAUL remains gone. It tests the gym gate with six and seven badges earned in prior replays; a room-entry warp and actual gym exit position the fixture north of Viridian's ledge. It checks three actual gym trainer battles with corridor-opening movement, six spinner rides to the leader and two back to the guide, three level-52 starter parties with Water/Ground support against Giovanni, the Earth Badge/TM27 rewards, Giovanni's departure, three late rival variants and their earned spawn/trigger/departure, and eight-badge save/load with the caught dogs and all HMs intact. Late rival parties are trained level 56. The separate early replay starts three new games, earns the parcel/Pokédex rewards, and uses level-12 parties to check all three early rival variants. Entry warps, trained parties, capture balls, inventory room, optional trainer flags and Repel are fixtures. Hall of Fame entry warps isolate retry behavior; these checks do not establish League progress, natural difficulty, or a continuous playthrough.

The League replay uses matching-ROM Blaine and Giovanni checkpoints. It tests a new game's Boulder rejection, seven earned badges failing the Earth checkpoint, all eight badge checks, actual Surf and landing, Victory Road entry, the three switch floors, the boulder and player fall, a cave trainer, SUNMAST capture/flee/defeat, and arrival through the cave exit at Indigo Plateau. It checks the nurse and real purchases of Full Restores and Revives, then runs all five League battles for all three starter relationships with level-64 parties. Party order, healing, revival and PP restoration use the game menus between rounds. It validates each loaded enemy team's species, levels and legal ace moves, the Champion cutscene, six saved dog names/levels in the Hall of Fame, the game's automatic save and fresh-emulator Continue in Pallet. The capture/flee/defeat branches go through earned Hall of Fame entries, independently checking the third guardian retry and preserving the two previously caught guardians. A level-5 party fixture deliberately loses to Bruno after a won Lorelei round, checking blackout, lobby reset and a restarted challenge. Parties, money, PP supplies, capture balls, entry warps, optional cave trainers and Repel are fixtures; these checks do not establish natural difficulty or an uninterrupted new-game playthrough.

The postgame replay uses matching-ROM League checkpoints. It approaches the cave through Cerulean, earns any outstanding Cerulean rival and Nugget Bridge scripts, Surfs from Route 24, and checks eight badges being rejected before the Champion and access after the earned Hall of Fame. It walks all six 2F stairs and Surfs the basement to PSIGUARD. Both guardians are tested with actual capture, flee and defeat inputs, including typing and five-stat formula checks from their actual DVs. Four complete five-battle League rematches test both caught, either caught, and neither caught, then use fresh-emulator Continue to check persistence, all five HMs, and an actual 2F Full Restore pickup staying removed. Restored guardians are actually encountered and recaptured. A separate Cave Save/Continue preserves both captured dogs in the party. Explicit 150/151-owned-bit fixtures test diploma rejection and display; they do not represent a legitimate complete collection. Cave parties are trained level 75 so Repel covers the level-67 wild table; League rematches use the earlier level-64 fixture. Entry positioning, parties, capture balls, optional bridge trainer flags and Repel are fixtures. Mandatory rewards, guardian flags, captures and League victories are earned through inputs.

## Regeneration

The finalized JSON files feed the implementation through `data/dogs/implemented.json`. After editing the appropriate data or source atlases, run:

```sh
.venv/bin/python tools/dogs/generate_data.py
.venv/bin/python tools/dogs/generate_misty.py
.venv/bin/python tools/dogs/generate_surge.py
.venv/bin/python tools/dogs/generate_erika.py
.venv/bin/python tools/dogs/generate_koga.py
.venv/bin/python tools/dogs/generate_sabrina.py
.venv/bin/python tools/dogs/generate_blaine.py
.venv/bin/python tools/dogs/generate_giovanni.py
.venv/bin/python tools/dogs/generate_league.py
.venv/bin/python tools/dogs/generate_postgame.py
.venv/bin/python tools/dogs/convert_sprites.py
.venv/bin/python tools/dogs/generate_sprite_banks.py
.venv/bin/python tools/dogs/export_plan.py
make -j4 demo
```

Sprite pairs are packed eight species per bank. A banked lookup returns each pair's bank without consuming scarce ROM0 space; original species IDs and save layout remain stable. Evolution code and learnset tables share a separate bank with move names; the evolved-stat read explicitly copies from the base-stat bank.

## Art and remaining work

Original draft artwork was generated with the built-in imagegen tool. The source atlases and exact prompts are in `assets/dogs/`; conversion instructions are in `tools/dogs/convert_sprites.py`. Battle sprites, the shared dog menu icon, and the six-frame generic overworld dog use the original four-shade format. The title's random species list now contains only demo dogs; the original animated opening and logo remain for a later art pass.

All 151 forms and five guardian retries are implemented. New moves reuse upstream effect and animation routines. Continuous playthroughs with each starter, a legitimate 151-form save, broader balance work, custom move animations, and new sound design remain future work. The demo does not change the name buffers or save-file layout.
