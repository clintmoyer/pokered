# Pokedogs: full-game design

The first release keeps Kanto's maps and story progression, the 15 Gen 1 types,
the five-stat system with combined Special, and the original species and move IDs.
All 151 species slots become dog forms across 79 breed families. Puppy, adolescent,
and adult forms remain the same breed; elemental features are fictional.
Names fit the existing ten-character species and twelve-character move buffers.
The full breed name appears in Pokédex prose, wrapped across lines when needed.

## Authoritative roster and move pool

- [Full 151-form roster](ROSTER.md), with names, breed identities, typing, stats,
  evolution conditions, and acquisition locations.
- [Roster CSV](ROSTER.csv), including initial moves, level-up progression,
  family signature moves, and explicit TM/HM compatibility.
- [All 165 move slots](MOVES.csv), including names, types, power, accuracy, PP,
  effects, and preserved HM functions.
- Editable sources: `data/dogs/roster.json` and `data/dogs/moves.json`.
  Regenerate the views with `python3 tools/dogs/export_plan.py` and check the plan
  with `python3 tools/dogs/validate_plan.py`.

These are finalized design baselines. Balance can be tuned against playthroughs.
`data/dogs/implemented.json` lists the forms actually converted in the current ROM;
the full collection plan does not imply all 151 are already implemented.

Stats give breeds different roles: fast coursing hounds, sturdy guardians,
rescue swimmers, special attackers, and supporting companions. Evolution and
learnset progression are explicit per form. Ordinary breed signatures may be
shared by related battle roles; they are not 151 exclusive moves. Existing moves
are reworked into a shared dog move library. New display names do not imply new
engine mechanics: existing effect and animation routines are reused for version 1.
Fixed damage, charging, priority, recoil, transformation, and other special-ID
behavior remain attached to their original slots. HUNT FOCUS instead raises Attack
one stage to avoid the original Focus Energy effect's inverted critical-hit behavior.
Custom animations and new cries are a subsequent presentation pass.
WYRM FANG and WYRM BARK repurpose the old Splash and Tri Attack slots into
ordinary Dragon attacks, giving the Lundehund family attacks beyond fixed damage.

## Collection contract: all 151 in one ROM

Every base family has a repeatable wild source or a retryable special encounter.
There are no Red/Blue encounter exclusives, external trades, event distributions,
or permanently exclusive rewards required to complete the Pokédex.

- All three starter puppies also appear at levels 10–12 on Route 25. The initial
  choice still determines the rival's starter. Their evolutions remain 16 and 36.
- Ordinary evolution is by level; all original trade evolutions are removed.
  TERVPUP has Water Stone, Thunder Stone, and Fire Stone branches, with unlimited
  stones sold at Celadon. TERVPUP is also repeatably catchable on Route 7, so all
  three branches can be collected in one save.
- KEESPUP and ELKPUP have repeatable Rock Tunnel B1F encounters; WOLFGALE has a
  Victory Road 1F encounter. Fossil choice and revival can provide an early or
  higher-level gift, but do not exclude either family from the collection.
- Both Fighting Dojo dogs are also catchable on Route 23. The original gift
  choice can remain without locking the other form out.
- Adoptable SPRINGPUP replaces the Mt. Moon seller's gift and also appears on
  Route 4. Other story gifts remain bonuses rather than exclusive sources.
- NEOMAST retains the sleeping-roadblock role. The three legendary guardians
  retain their original encounter sites. PSIGUARD inhabits Cerulean Cave B1F;
  MUDIMYTH gains a standard, post-Champion encounter on Cerulean Cave 2F.
- For special encounters, fleeing or defeating the dog makes it available again
  after the next Hall of Fame entry. Catching it permanently completes that
  encounter. No save-file manipulation is required.

Location, terrain, level range, milestone gate, and retry policy are recorded in
each form's acquisition record. These are implementation requirements. The plan
validator checks the graph; later ROM checks must verify actual encounter tables,
event scripts, branch conditions, stones, and respawn flags against that graph.

## TM and HM contracts

Keep all 50 TM items and all five HM IDs, badge checks, and field hooks.
TMs teach the redesigned move assigned to their existing move slot. Rewards,
shop inventories, and compatibility must be audited together, and every TM must
have at least one obtainable compatible dog. TMs are consumed once; HMs remain
reusable and retain the original deletion restrictions.

| HM | Dog move | Field behavior | Early obtainable carriers |
|---|---|---|---|
| HM01 CUT | BRAMBLE BITE | Remove bushes; Cascade Badge | Groenendael, Shiba Inu, Beagle |
| HM02 FLY | SKYBOUND | Return to visited towns; Thunder Badge | Adult Papillon, Whippet, Greyhound |
| HM03 SURF | DOG PADDLE | Cross water; Soul Badge | Newfoundland, Otterhound |
| HM04 STRENGTH | HAUL | Push boulders; Rainbow Badge | Boxer, Beagle, Bulldog |
| HM05 FLASH | BEACON BARK | Illuminate caves; Boulder Badge | Papillon, Pomeranian, Poodle |

HM acquisition locations and unlocking badges remain the original ones.
Carriers are reachable without their own field function. HOMEBOUND (Teleport),
BURROW RUSH (Dig), and RESCUE REST (Softboiled) also retain their field behavior.
Their field-menu labels and explanatory text must match the redesigned names.

## Delivery order and acceptance

1. Extend the opening through Route 3, Mt. Moon, Route 4, Cerulean, the northern
   routes and Bill, and Misty. Convert all reachable wild/trainer rosters, the
   seller, rival fight, dialogue about species and moves, and Misty's TM11 reward.
   Supply Grass and Electric counters before the gym and access to all starters
   on Route 25. Remove Brock's demo-ending text.
2. Extend through Vermilion and Erika, implementing Cut, Flash, and Fly along the
   way. Finish further families, trainer teams, trades, gifts, and both fossil
   families' repeatable sources.
3. Extend through Fuchsia, Saffron, Cinnabar, and Viridian, with Surf, Strength,
   Safari encounters, Tower events, sleeping dogs, and late-game progression.
4. Finish Elite Four, Champion, legendary retries, Cerulean Cave, and collection
   completion. Add the remaining presentation assets and sound pass.

Each slice needs a successful build, compiled-data checks, actual boss battle and
badge/TM reward checks, save/load, evolution checks, and sprite inspection. Full
release acceptance additionally requires continuous playthroughs with all three
starters and a legitimate 151-entry collection in one save. Fixture-based boss
checks alone do not establish natural difficulty or complete collection access.
The original intro, logo, Super Game Boy border, cries, and unconverted later
content remain visible until their respective implementation milestones.
