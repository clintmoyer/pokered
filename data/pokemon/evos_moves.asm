; Evos+moves data structure:
; - Evolution methods:
;    * db EVOLVE_LEVEL, level, species
;    * db EVOLVE_ITEM, used item, min level (1), species
;    * db EVOLVE_TRADE, min level (1), species
; - db 0 ; no more evolutions
; - Learnset (in increasing level order):
;    * db level, move
; - db 0 ; no more level-up moves

EvosMovesPointerTable:
	table_width 2
	dw RhydonEvosMoves
	dw KangaskhanEvosMoves
	dw NidoranMEvosMoves
	dw ClefairyEvosMoves
	dw SpearowEvosMoves
	dw VoltorbEvosMoves
	dw NidokingEvosMoves
	dw SlowbroEvosMoves
	dw IvysaurEvosMoves
	dw ExeggutorEvosMoves
	dw LickitungEvosMoves
	dw ExeggcuteEvosMoves
	dw GrimerEvosMoves
	dw GengarEvosMoves
	dw NidoranFEvosMoves
	dw NidoqueenEvosMoves
	dw CuboneEvosMoves
	dw RhyhornEvosMoves
	dw LaprasEvosMoves
	dw ArcanineEvosMoves
	dw MewEvosMoves
	dw GyaradosEvosMoves
	dw ShellderEvosMoves
	dw TentacoolEvosMoves
	dw GastlyEvosMoves
	dw ScytherEvosMoves
	dw StaryuEvosMoves
	dw BlastoiseEvosMoves
	dw PinsirEvosMoves
	dw TangelaEvosMoves
	dw MissingNo1FEvosMoves
	dw MissingNo20EvosMoves
	dw GrowlitheEvosMoves
	dw OnixEvosMoves
	dw FearowEvosMoves
	dw PidgeyEvosMoves
	dw SlowpokeEvosMoves
	dw KadabraEvosMoves
	dw GravelerEvosMoves
	dw ChanseyEvosMoves
	dw MachokeEvosMoves
	dw MrMimeEvosMoves
	dw HitmonleeEvosMoves
	dw HitmonchanEvosMoves
	dw ArbokEvosMoves
	dw ParasectEvosMoves
	dw PsyduckEvosMoves
	dw DrowzeeEvosMoves
	dw GolemEvosMoves
	dw MissingNo32EvosMoves
	dw MagmarEvosMoves
	dw MissingNo34EvosMoves
	dw ElectabuzzEvosMoves
	dw MagnetonEvosMoves
	dw KoffingEvosMoves
	dw MissingNo38EvosMoves
	dw MankeyEvosMoves
	dw SeelEvosMoves
	dw DiglettEvosMoves
	dw TaurosEvosMoves
	dw MissingNo3DEvosMoves
	dw MissingNo3EEvosMoves
	dw MissingNo3FEvosMoves
	dw FarfetchdEvosMoves
	dw VenonatEvosMoves
	dw DragoniteEvosMoves
	dw MissingNo43EvosMoves
	dw MissingNo44EvosMoves
	dw MissingNo45EvosMoves
	dw DoduoEvosMoves
	dw PoliwagEvosMoves
	dw JynxEvosMoves
	dw MoltresEvosMoves
	dw ArticunoEvosMoves
	dw ZapdosEvosMoves
	dw DittoEvosMoves
	dw MeowthEvosMoves
	dw KrabbyEvosMoves
	dw MissingNo4FEvosMoves
	dw MissingNo50EvosMoves
	dw MissingNo51EvosMoves
	dw VulpixEvosMoves
	dw NinetalesEvosMoves
	dw PikachuEvosMoves
	dw RaichuEvosMoves
	dw MissingNo56EvosMoves
	dw MissingNo57EvosMoves
	dw DratiniEvosMoves
	dw DragonairEvosMoves
	dw KabutoEvosMoves
	dw KabutopsEvosMoves
	dw HorseaEvosMoves
	dw SeadraEvosMoves
	dw MissingNo5EEvosMoves
	dw MissingNo5FEvosMoves
	dw SandshrewEvosMoves
	dw SandslashEvosMoves
	dw OmanyteEvosMoves
	dw OmastarEvosMoves
	dw JigglypuffEvosMoves
	dw WigglytuffEvosMoves
	dw EeveeEvosMoves
	dw FlareonEvosMoves
	dw JolteonEvosMoves
	dw VaporeonEvosMoves
	dw MachopEvosMoves
	dw ZubatEvosMoves
	dw EkansEvosMoves
	dw ParasEvosMoves
	dw PoliwhirlEvosMoves
	dw PoliwrathEvosMoves
	dw WeedleEvosMoves
	dw KakunaEvosMoves
	dw BeedrillEvosMoves
	dw MissingNo73EvosMoves
	dw DodrioEvosMoves
	dw PrimeapeEvosMoves
	dw DugtrioEvosMoves
	dw VenomothEvosMoves
	dw DewgongEvosMoves
	dw MissingNo79EvosMoves
	dw MissingNo7AEvosMoves
	dw CaterpieEvosMoves
	dw MetapodEvosMoves
	dw ButterfreeEvosMoves
	dw MachampEvosMoves
	dw MissingNo7FEvosMoves
	dw GolduckEvosMoves
	dw HypnoEvosMoves
	dw GolbatEvosMoves
	dw MewtwoEvosMoves
	dw SnorlaxEvosMoves
	dw MagikarpEvosMoves
	dw MissingNo86EvosMoves
	dw MissingNo87EvosMoves
	dw MukEvosMoves
	dw MissingNo8AEvosMoves
	dw KinglerEvosMoves
	dw CloysterEvosMoves
	dw MissingNo8CEvosMoves
	dw ElectrodeEvosMoves
	dw ClefableEvosMoves
	dw WeezingEvosMoves
	dw PersianEvosMoves
	dw MarowakEvosMoves
	dw MissingNo92EvosMoves
	dw HaunterEvosMoves
	dw AbraEvosMoves
	dw AlakazamEvosMoves
	dw PidgeottoEvosMoves
	dw PidgeotEvosMoves
	dw StarmieEvosMoves
	dw BulbasaurEvosMoves
	dw VenusaurEvosMoves
	dw TentacruelEvosMoves
	dw MissingNo9CEvosMoves
	dw GoldeenEvosMoves
	dw SeakingEvosMoves
	dw MissingNo9FEvosMoves
	dw MissingNoA0EvosMoves
	dw MissingNoA1EvosMoves
	dw MissingNoA2EvosMoves
	dw PonytaEvosMoves
	dw RapidashEvosMoves
	dw RattataEvosMoves
	dw RaticateEvosMoves
	dw NidorinoEvosMoves
	dw NidorinaEvosMoves
	dw GeodudeEvosMoves
	dw PorygonEvosMoves
	dw AerodactylEvosMoves
	dw MissingNoACEvosMoves
	dw MagnemiteEvosMoves
	dw MissingNoAEEvosMoves
	dw MissingNoAFEvosMoves
	dw CharmanderEvosMoves
	dw SquirtleEvosMoves
	dw CharmeleonEvosMoves
	dw WartortleEvosMoves
	dw CharizardEvosMoves
	dw MissingNoB5EvosMoves
	dw FossilKabutopsEvosMoves
	dw FossilAerodactylEvosMoves
	dw MonGhostEvosMoves
	dw OddishEvosMoves
	dw GloomEvosMoves
	dw VileplumeEvosMoves
	dw BellsproutEvosMoves
	dw WeepinbellEvosMoves
	dw VictreebelEvosMoves
	assert_table_length NUM_POKEMON_INDEXES

RhydonEvosMoves:
; BULLTANK: same breed, growing maturity.
	db 0
	db 7, DUST_KICK
	db 11, PAW_DASH
	db 14, BONE_BASH
	db 18, BURROW_RUSH
	db 24, PACK_RUSH
	db 27, BRACE
	db 30, BONE_FETCH
	db 38, EARTH_STOMP
	db 0

KangaskhanEvosMoves:
; GREATDANE: same breed, growing maturity.
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 27, PAW_COMBO
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, PACK_TOSS
	db 0

NidoranMEvosMoves:
; AUSSPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 16, NIDORINO
	db 0
	db 7, VENOM_DROOL
	db 11, PAW_DASH
	db 14, TOXIC_DANDER
	db 18, VENOM_BARK
	db 24, PACK_RUSH
	db 27, PAW_COMBO
	db 30, VENOM_MARK
	db 38, VENOM_COAT
	db 42, SPAR_RUSH
	db 0

ClefairyEvosMoves:
; SAMOPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, CLEFABLE
	db 0
	db 7, FROST_PAW
	db 11, PAW_DASH
	db 14, FROST_COAT
	db 18, POLAR_HOWL
	db 24, PACK_RUSH
	db 30, FROST_BARK
	db 38, WHITEOUT_YIP
	db 0

SpearowEvosMoves:
; GREYPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, FEAROW
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 27, AIR_NIP
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, SKY_POUNCE
	db 0

VoltorbEvosMoves:
; CHIPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, ELECTRODE
	db 0
	db 7, SPARK_YIP
	db 11, PAW_DASH
	db 14, STATIC_COAT
	db 18, VOLT_PAW
	db 24, PACK_RUSH
	db 30, VOLT_BARK
	db 38, STORM_HOWL
	db 0

NidokingEvosMoves:
; AUSSGUARD: same breed, growing maturity.
	db 0
	db 7, VENOM_DROOL
	db 11, PAW_DASH
	db 14, TOXIC_DANDER
	db 18, VENOM_BARK
	db 24, PACK_RUSH
	db 27, PAW_COMBO
	db 30, VENOM_MARK
	db 38, VENOM_COAT
	db 42, SPAR_RUSH
	db 0

SlowbroEvosMoves:
; BASSET: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, BARK_ECHO
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, DEEP_CALM
	db 0

IvysaurEvosMoves:
; GROEN: same breed, growing maturity.
	db EVOLVE_LEVEL, 36, VENUSAUR
	db 0
	db 7, LEAF_FANG
	db 10, PAW_DASH
	db 13, ROOT_SNARE
	db 18, PACK_FOCUS
	db 24, PACK_RUSH
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 0

ExeggutorEvosMoves:
; BERNBLOOM: same breed, growing maturity.
	db 0
	db 7, LEAF_FANG
	db 11, PAW_DASH
	db 14, ROOT_SNARE
	db 18, THORN_CLAW
	db 24, PACK_RUSH
	db 27, BARK_ECHO
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 42, MIND_GUARD
	db 0

LickitungEvosMoves:
; STBERNARD: same breed, growing maturity.
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, RESCUE_REST
	db 0

ExeggcuteEvosMoves:
; BERNPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, EXEGGUTOR
	db 0
	db 7, LEAF_FANG
	db 11, PAW_DASH
	db 14, ROOT_SNARE
	db 18, THORN_CLAW
	db 24, PACK_RUSH
	db 27, BARK_ECHO
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 42, MIND_GUARD
	db 0

GrimerEvosMoves:
; SHARPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, MUK
	db 0
	db 7, VENOM_DROOL
	db 11, PAW_DASH
	db 14, TOXIC_DANDER
	db 18, VENOM_BARK
	db 24, PACK_RUSH
	db 30, VENOM_MARK
	db 38, VENOM_COAT
	db 0

GengarEvosMoves:
; WEIMWRAITH: same breed, growing maturity.
	db 0
	db 7, GHOST_LICK
	db 11, PAW_DASH
	db 14, ODD_YIP
	db 18, SHADE_HOWL
	db 24, PACK_RUSH
	db 30, GHOST_GLARE
	db 38, SPIRIT_SHIFT
	db 0

NidoranFEvosMoves:
; CATTLEPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 16, NIDORINA
	db 0
	db 7, VENOM_DROOL
	db 11, PAW_DASH
	db 14, TOXIC_DANDER
	db 18, VENOM_BARK
	db 24, PACK_RUSH
	db 27, DUST_KICK
	db 30, VENOM_MARK
	db 38, VENOM_COAT
	db 42, EARTH_STOMP
	db 0

NidoqueenEvosMoves:
; CATTLEGARD: same breed, growing maturity.
	db 0
	db 7, VENOM_DROOL
	db 11, PAW_DASH
	db 14, TOXIC_DANDER
	db 18, VENOM_BARK
	db 24, PACK_RUSH
	db 27, DUST_KICK
	db 30, VENOM_MARK
	db 38, VENOM_COAT
	db 42, EARTH_STOMP
	db 0

CuboneEvosMoves:
; SCOTTPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, MAROWAK
	db 0
	db 7, DUST_KICK
	db 11, PAW_DASH
	db 14, BONE_BASH
	db 18, BURROW_RUSH
	db 24, PACK_RUSH
	db 30, BONE_FETCH
	db 38, EARTH_STOMP
	db 0

RhyhornEvosMoves:
; BULLTPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, RHYDON
	db 0
	db 7, DUST_KICK
	db 11, PAW_DASH
	db 14, BONE_BASH
	db 18, BURROW_RUSH
	db 24, PACK_RUSH
	db 27, BRACE
	db 30, BONE_FETCH
	db 38, EARTH_STOMP
	db 0

LaprasEvosMoves:
; LEONTIDE: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, FROST_PAW
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, MIST_SHAKE
	db 0

ArcanineEvosMoves:
; AKITAFIRE: same breed, growing maturity.
	db 0
	db 7, CINDER_YIP
	db 11, PAW_DASH
	db 14, SOOT_SHAKE
	db 18, EMBER_PAW
	db 24, PACK_RUSH
	db 30, CINDER_BARK
	db 38, FLAME_POUNCE
	db 0

MewEvosMoves:
; Evolutions
	db 0
; Learnset
	db 10, TRANSFORM
	db 20, MEGA_PUNCH
	db 30, METRONOME
	db 40, PSYCHIC_M
	db 0

GyaradosEvosMoves:
; SPRINGTIDE: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 0

ShellderEvosMoves:
; CHESSPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, CLOYSTER
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, FROST_PAW
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, TIDE_GRIP
	db 0

TentacoolEvosMoves:
; SPANPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, TENTACRUEL
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, VENOM_DROOL
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 0

GastlyEvosMoves:
; WEIMPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 16, HAUNTER
	db 0
	db 7, GHOST_LICK
	db 11, PAW_DASH
	db 14, ODD_YIP
	db 18, SHADE_HOWL
	db 24, PACK_RUSH
	db 30, GHOST_GLARE
	db 38, SPIRIT_SHIFT
	db 0

ScytherEvosMoves:
; MALINOIS: same breed, growing maturity.
	db 0
	db 7, SILK_SLOW
	db 11, PAW_DASH
	db 14, SILK_FANG
	db 18, NUMB_POLLEN
	db 24, PACK_RUSH
	db 27, PAW_COMBO
	db 30, THREAD_RUSH
	db 38, SILK_COMBO
	db 42, THREAD_RUSH
	db 0

StaryuEvosMoves:
; OTTERPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 20, STARMIE
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, BARK_ECHO
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 0

BlastoiseEvosMoves:
; NEWFTIDE: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 10, BRACE
	db 13, PAW_COMBO
	db 18, PACK_FOCUS
	db 24, PACK_RUSH
	db 30, WAKE_CHARGE
	db 38, TIDAL_BARK
	db 0

PinsirEvosMoves:
; COLLIEMIND: same breed, growing maturity.
	db 0
	db 7, LEAF_FANG
	db 11, PAW_DASH
	db 14, ROOT_SNARE
	db 18, PACK_FOCUS
	db 24, PACK_RUSH
	db 27, BARK_ECHO
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 0

TangelaEvosMoves:
; KOMONDOR: same breed, growing maturity.
	db 0
	db 7, LEAF_FANG
	db 11, PAW_DASH
	db 14, ROOT_SNARE
	db 18, THORN_CLAW
	db 24, PACK_RUSH
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 42, DREAM_POLLEN
	db 0

MissingNo1FEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo20EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

GrowlitheEvosMoves:
; AKIPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, ARCANINE
	db 0
	db 7, CINDER_YIP
	db 11, PAW_DASH
	db 14, SOOT_SHAKE
	db 18, EMBER_PAW
	db 24, PACK_RUSH
	db 30, CINDER_BARK
	db 38, FLAME_POUNCE
	db 0

OnixEvosMoves:
; STONEMAST: same breed, growing maturity.
	db 0
	db 8, BRACE
	db 11, STONE_PAW
	db 15, GUARD_HOWL
	db 22, PACK_RUSH
	db 30, BOULDER_RUSH
	db 36, PACK_HOWL
	db 0

FearowEvosMoves:
; GREYGALE: same breed, growing maturity.
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 27, AIR_NIP
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, SKY_POUNCE
	db 0

PidgeyEvosMoves:
; WHIPPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 18, PIDGEOTTO
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 27, AIR_NIP
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, GALE_FANG
	db 0

SlowpokeEvosMoves:
; BASSPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, SLOWBRO
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, BARK_ECHO
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, DEEP_CALM
	db 0

KadabraEvosMoves:
; POODLE: same breed, growing maturity.
	db EVOLVE_LEVEL, 36, ALAKAZAM
	db 0
	db 7, BARK_ECHO
	db 11, PAW_DASH
	db 14, CALM_POSE
	db 18, MIND_YIP
	db 24, PACK_RUSH
	db 30, MIND_HOWL
	db 38, AURA_COAT
	db 0

GravelerEvosMoves:
; BULLDOG: same breed, growing maturity.
	db EVOLVE_LEVEL, 36, GOLEM
	db 0
	db 8, BRACE
	db 11, STONE_PAW
	db 15, GUARD_HOWL
	db 22, PACK_RUSH
	db 30, BOULDER_RUSH
	db 36, HAUL
	db 0

ChanseyEvosMoves:
; CAVALIER: same breed, growing maturity.
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, SOFT_NUZZLE
	db 0

MachokeEvosMoves:
; STAFFORD: same breed, growing maturity.
	db EVOLVE_LEVEL, 32, MACHAMP
	db 0
	db 7, PAW_COMBO
	db 11, PAW_DASH
	db 14, SCENT_LOCK
	db 18, BOXING_PAW
	db 24, PACK_RUSH
	db 30, SPAR_RUSH
	db 38, SKY_PAW
	db 0

MrMimeEvosMoves:
; LHASA: same breed, growing maturity.
	db 0
	db 7, BARK_ECHO
	db 11, PAW_DASH
	db 14, CALM_POSE
	db 18, MIND_YIP
	db 24, PACK_RUSH
	db 30, MIND_HOWL
	db 38, AURA_COAT
	db 0

HitmonleeEvosMoves:
; DOBERGUARD: same breed, growing maturity.
	db 0
	db 7, PAW_COMBO
	db 11, PAW_DASH
	db 14, SCENT_LOCK
	db 18, BOXING_PAW
	db 24, PACK_RUSH
	db 30, SPAR_RUSH
	db 38, SKY_PAW
	db 42, RETORT_PAW
	db 0

HitmonchanEvosMoves:
; ROTTGUARD: same breed, growing maturity.
	db 0
	db 7, PAW_COMBO
	db 11, PAW_DASH
	db 14, SCENT_LOCK
	db 18, BOXING_PAW
	db 24, PACK_RUSH
	db 30, SPAR_RUSH
	db 38, SKY_PAW
	db 42, TITAN_PAW
	db 0

ArbokEvosMoves:
; DACHSHUND: same breed, growing maturity.
	db 0
	db 7, VENOM_DROOL
	db 11, PAW_DASH
	db 14, TOXIC_DANDER
	db 18, VENOM_BARK
	db 24, PACK_RUSH
	db 30, VENOM_MARK
	db 38, VENOM_COAT
	db 0

ParasectEvosMoves:
; BICHOBLOOM: same breed, growing maturity.
	db 0
	db 7, SILK_SLOW
	db 11, PAW_DASH
	db 14, SILK_FANG
	db 18, NUMB_POLLEN
	db 24, PACK_RUSH
	db 27, LEAF_FANG
	db 30, THREAD_RUSH
	db 38, SILK_COMBO
	db 0

PsyduckEvosMoves:
; LABPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, GOLDUCK
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 0

DrowzeeEvosMoves:
; BLOODPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, HYPNO
	db 0
	db 7, BARK_ECHO
	db 11, PAW_DASH
	db 14, CALM_POSE
	db 18, MIND_YIP
	db 24, PACK_RUSH
	db 30, MIND_HOWL
	db 38, AURA_COAT
	db 42, LULL_STARE
	db 0

GolemEvosMoves:
; BULLGUARD: same breed, growing maturity.
	db 0
	db 8, BRACE
	db 11, STONE_PAW
	db 15, GUARD_HOWL
	db 22, PACK_RUSH
	db 30, BOULDER_RUSH
	db 36, HAUL
	db 0

MissingNo32EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MagmarEvosMoves:
; CHOWFLARE: same breed, growing maturity.
	db 0
	db 7, CINDER_YIP
	db 11, PAW_DASH
	db 14, SOOT_SHAKE
	db 18, EMBER_PAW
	db 24, PACK_RUSH
	db 30, CINDER_BARK
	db 38, FLAME_POUNCE
	db 0

MissingNo34EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

ElectabuzzEvosMoves:
; Evolutions
	db 0
; Learnset
	db 34, THUNDERSHOCK
	db 37, SCREECH
	db 42, THUNDERPUNCH
	db 49, LIGHT_SCREEN
	db 54, THUNDER
	db 0

MagnetonEvosMoves:
; SCHNAUZER: same breed, growing maturity.
	db 0
	db 7, SPARK_YIP
	db 11, PAW_DASH
	db 14, STATIC_COAT
	db 18, VOLT_PAW
	db 24, PACK_RUSH
	db 27, BRACE
	db 30, VOLT_BARK
	db 38, STORM_HOWL
	db 0

KoffingEvosMoves:
; PUGPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, WEEZING
	db 0
	db 7, VENOM_DROOL
	db 11, PAW_DASH
	db 14, TOXIC_DANDER
	db 18, VENOM_BARK
	db 24, PACK_RUSH
	db 30, VENOM_MARK
	db 38, VENOM_COAT
	db 42, HAZE_BREATH
	db 0

MissingNo38EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MankeyEvosMoves:
; BOXPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, PRIMEAPE
	db 0
	db 7, PAW_COMBO
	db 11, SCENT_LOCK
	db 15, BOXING_PAW
	db 22, PACK_HOWL
	db 28, SPAR_RUSH
	db 34, CLAW_RAKE
	db 0

SeelEvosMoves:
; GOLDPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, DEWGONG
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, FROST_PAW
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, FROST_BARK
	db 0

DiglettEvosMoves:
; BORDERPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, DUGTRIO
	db 0
	db 7, DUST_KICK
	db 11, PAW_DASH
	db 14, BONE_BASH
	db 18, BURROW_RUSH
	db 24, PACK_RUSH
	db 30, BONE_FETCH
	db 38, EARTH_STOMP
	db 42, FAULT_FANG
	db 0

TaurosEvosMoves:
; RIDGEBACK: same breed, growing maturity.
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 27, PAW_COMBO
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, WILD_RUSH
	db 0

MissingNo3DEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo3EEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo3FEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

FarfetchdEvosMoves:
; SALUKI: same breed, growing maturity.
	db 0
	db 7, AIR_NIP
	db 11, PAW_DASH
	db 14, TAIL_GUST
	db 18, WING_PAW
	db 24, PACK_RUSH
	db 30, GALE_FANG
	db 38, SKY_POUNCE
	db 42, ECHO_TRICK
	db 0

VenonatEvosMoves:
; CRESTPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, VENOMOTH
	db 0
	db 7, SILK_SLOW
	db 11, PAW_DASH
	db 14, SILK_FANG
	db 18, NUMB_POLLEN
	db 24, PACK_RUSH
	db 27, BARK_ECHO
	db 30, THREAD_RUSH
	db 38, SILK_COMBO
	db 42, MIND_YIP
	db 0

DragoniteEvosMoves:
; LUNDEWYRM: same breed, growing maturity.
	db 0
	db 7, WYRM_FANG
	db 11, PAW_DASH
	db 14, HUNT_FOCUS
	db 18, WYRM_HOWL
	db 24, PACK_RUSH
	db 30, PACK_RUSH
	db 38, WYRM_BARK
	db 0

MissingNo43EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo44EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo45EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

DoduoEvosMoves:
; BORZPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, DODRIO
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 27, AIR_NIP
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, GALE_HOWL
	db 0

PoliwagEvosMoves:
; PORTPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 16, POLIWHIRL
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, PAW_COMBO
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, TIDE_PAW
	db 0

JynxEvosMoves:
; HUSKY: same breed, growing maturity.
	db 0
	db 7, FROST_PAW
	db 11, PAW_DASH
	db 14, FROST_COAT
	db 18, POLAR_HOWL
	db 24, PACK_RUSH
	db 27, BARK_ECHO
	db 30, FROST_BARK
	db 38, WHITEOUT_YIP
	db 0

MoltresEvosMoves:
; Evolutions
	db 0
; Learnset
	db 51, LEER
	db 55, AGILITY
	db 60, SKY_ATTACK
	db 0

ArticunoEvosMoves:
; FROSTMAUL: same breed, growing maturity.
	db 0
	db 7, FROST_PAW
	db 11, PAW_DASH
	db 14, FROST_COAT
	db 18, POLAR_HOWL
	db 24, PACK_RUSH
	db 27, AIR_NIP
	db 30, FROST_BARK
	db 38, WHITEOUT_YIP
	db 0

ZapdosEvosMoves:
; Evolutions
	db 0
; Learnset
	db 51, THUNDER
	db 55, AGILITY
	db 60, LIGHT_SCREEN
	db 0

DittoEvosMoves:
; XOLO: same breed, growing maturity.
	db 0
	db 7, GHOST_LICK
	db 11, PAW_DASH
	db 14, ODD_YIP
	db 18, SHADE_HOWL
	db 24, PACK_RUSH
	db 30, GHOST_GLARE
	db 38, SPIRIT_SHIFT
	db 0

MeowthEvosMoves:
; BOSTPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, PERSIAN
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, HEAD_BUMP
	db 0

KrabbyEvosMoves:
; IRISPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, KINGLER
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, TIDE_PAW
	db 0

MissingNo4FEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo50EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo51EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

VulpixEvosMoves:
; SPITZPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, NINETALES
	db 0
	db 7, CINDER_YIP
	db 11, PAW_DASH
	db 14, SOOT_SHAKE
	db 18, EMBER_PAW
	db 24, PACK_RUSH
	db 30, CINDER_BARK
	db 38, FLAME_POUNCE
	db 42, EMBER_CIRCLE
	db 0

NinetalesEvosMoves:
; SUNSPITZ: same breed, growing maturity.
	db 0
	db 7, CINDER_YIP
	db 11, PAW_DASH
	db 14, SOOT_SHAKE
	db 18, EMBER_PAW
	db 24, PACK_RUSH
	db 30, CINDER_BARK
	db 38, FLAME_POUNCE
	db 42, EMBER_CIRCLE
	db 0

PikachuEvosMoves:
; POMPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, RAICHU
	db 0
	db 7, SPARK_YIP
	db 11, PAW_DASH
	db 14, STATIC_COAT
	db 18, VOLT_PAW
	db 24, PACK_RUSH
	db 30, VOLT_BARK
	db 38, STORM_HOWL
	db 0

RaichuEvosMoves:
; POMSPARK: same breed, growing maturity.
	db 0
	db 7, SPARK_YIP
	db 11, PAW_DASH
	db 14, STATIC_COAT
	db 18, VOLT_PAW
	db 24, PACK_RUSH
	db 30, VOLT_BARK
	db 38, STORM_HOWL
	db 0

MissingNo56EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo57EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

DratiniEvosMoves:
; LUNDEPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 30, DRAGONAIR
	db 0
	db 7, WYRM_FANG
	db 11, PAW_DASH
	db 14, HUNT_FOCUS
	db 18, WYRM_HOWL
	db 24, PACK_RUSH
	db 30, PACK_RUSH
	db 38, WYRM_BARK
	db 0

DragonairEvosMoves:
; LUNDE: same breed, growing maturity.
	db EVOLVE_LEVEL, 50, DRAGONITE
	db 0
	db 7, WYRM_FANG
	db 11, PAW_DASH
	db 14, HUNT_FOCUS
	db 18, WYRM_HOWL
	db 24, PACK_RUSH
	db 30, PACK_RUSH
	db 38, WYRM_BARK
	db 0

KabutoEvosMoves:
; ELKPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, KABUTOPS
	db 0
	db 7, BRACE
	db 11, PAW_DASH
	db 14, STONE_PAW
	db 18, GUARD_HOWL
	db 24, PACK_RUSH
	db 27, PAW_COMBO
	db 30, BOULDER_RUSH
	db 38, HAUL
	db 42, ROLL_PAW
	db 0

KabutopsEvosMoves:
; ELKGUARD: same breed, growing maturity.
	db 0
	db 7, BRACE
	db 11, PAW_DASH
	db 14, STONE_PAW
	db 18, GUARD_HOWL
	db 24, PACK_RUSH
	db 27, PAW_COMBO
	db 30, BOULDER_RUSH
	db 38, HAUL
	db 42, ROLL_PAW
	db 0

HorseaEvosMoves:
; BARBPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, SEADRA
	db 0
	db 7, WYRM_FANG
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, NIP_FANG
	db 30, RIVER_RUSH
	db 38, WYRM_BARK
	db 42, WYRM_HOWL
	db 0

SeadraEvosMoves:
; BARBTIDE: same breed, growing maturity.
	db 0
	db 7, WYRM_FANG
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, NIP_FANG
	db 30, RIVER_RUSH
	db 38, WYRM_BARK
	db 42, WYRM_HOWL
	db 0

MissingNo5EEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo5FEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

SandshrewEvosMoves:
; JACKPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, SANDSLASH
	db 0
	db 7, DUST_KICK
	db 11, PAW_DASH
	db 14, BONE_BASH
	db 18, BURROW_RUSH
	db 24, PACK_RUSH
	db 30, BONE_FETCH
	db 38, EARTH_STOMP
	db 0

SandslashEvosMoves:
; JACKDIG: same breed, growing maturity.
	db 0
	db 7, DUST_KICK
	db 11, PAW_DASH
	db 14, BONE_BASH
	db 18, BURROW_RUSH
	db 24, PACK_RUSH
	db 30, BONE_FETCH
	db 38, EARTH_STOMP
	db 0

OmanyteEvosMoves:
; KEESPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, OMASTAR
	db 0
	db 7, BRACE
	db 11, PAW_DASH
	db 14, STONE_PAW
	db 18, GUARD_HOWL
	db 24, PACK_RUSH
	db 27, SPLASH_KICK
	db 30, BOULDER_RUSH
	db 38, HAUL
	db 42, RIVER_RUSH
	db 0

OmastarEvosMoves:
; KEESTIDE: same breed, growing maturity.
	db 0
	db 7, BRACE
	db 11, PAW_DASH
	db 14, STONE_PAW
	db 18, GUARD_HOWL
	db 24, PACK_RUSH
	db 27, SPLASH_KICK
	db 30, BOULDER_RUSH
	db 38, HAUL
	db 42, RIVER_RUSH
	db 0

JigglypuffEvosMoves:
; COCKERPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, WIGGLYTUFF
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, DREAM_HOWL
	db 0

WigglytuffEvosMoves:
; COCKER: same breed, growing maturity.
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, DREAM_HOWL
	db 0

EeveeEvosMoves:
; TERVPUP: same breed, growing maturity.
	db EVOLVE_ITEM, WATER_STONE, 1, VAPOREON
	db EVOLVE_ITEM, THUNDER_STONE, 1, JOLTEON
	db EVOLVE_ITEM, FIRE_STONE, 1, FLAREON
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, COPY_TRICK
	db 0

FlareonEvosMoves:
; FLAMETERV: same breed, growing maturity.
	db 0
	db 7, CINDER_YIP
	db 11, PAW_DASH
	db 14, SOOT_SHAKE
	db 18, EMBER_PAW
	db 30, CINDER_BARK
	db 38, FLAME_POUNCE
	db 42, COPY_TRICK
	db 42, FLAME_POUNCE
	db 0

JolteonEvosMoves:
; SPARKTERV: same breed, growing maturity.
	db 0
	db 7, SPARK_YIP
	db 11, PAW_DASH
	db 14, STATIC_COAT
	db 18, VOLT_PAW
	db 30, VOLT_BARK
	db 38, STORM_HOWL
	db 42, COPY_TRICK
	db 42, STORM_HOWL
	db 0

VaporeonEvosMoves:
; TIDETERV: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, COPY_TRICK
	db 42, TIDAL_BARK
	db 0

MachopEvosMoves:
; STAFFPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 16, MACHOKE
	db 0
	db 7, PAW_COMBO
	db 11, PAW_DASH
	db 14, SCENT_LOCK
	db 18, BOXING_PAW
	db 24, PACK_RUSH
	db 30, SPAR_RUSH
	db 38, SKY_PAW
	db 0

ZubatEvosMoves:
; IGPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, GOLBAT
	db 0
	db 7, AIR_NIP
	db 11, PAW_DASH
	db 14, TAIL_GUST
	db 18, WING_PAW
	db 24, PACK_RUSH
	db 27, GHOST_LICK
	db 30, GALE_FANG
	db 38, SKY_POUNCE
	db 42, SHADE_HOWL
	db 0

EkansEvosMoves:
; DACHSPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, ARBOK
	db 0
	db 7, VENOM_DROOL
	db 11, PAW_DASH
	db 14, TOXIC_DANDER
	db 18, VENOM_BARK
	db 24, PACK_RUSH
	db 30, VENOM_MARK
	db 38, VENOM_COAT
	db 0

ParasEvosMoves:
; BICHOPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, PARASECT
	db 0
	db 7, SILK_SLOW
	db 11, PAW_DASH
	db 14, SILK_FANG
	db 18, NUMB_POLLEN
	db 24, PACK_RUSH
	db 27, LEAF_FANG
	db 30, THREAD_RUSH
	db 38, SILK_COMBO
	db 0

PoliwhirlEvosMoves:
; PORTWATER: same breed, growing maturity.
	db EVOLVE_LEVEL, 32, POLIWRATH
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, PAW_COMBO
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, TIDE_PAW
	db 0

PoliwrathEvosMoves:
; PORTGUARD: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, PAW_COMBO
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, TIDE_PAW
	db 0

WeedleEvosMoves:
; YORKPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 9, KAKUNA
	db 0
	db 7, SILK_SLOW
	db 11, PAW_DASH
	db 14, SILK_FANG
	db 18, NUMB_POLLEN
	db 24, PACK_RUSH
	db 27, VENOM_DROOL
	db 30, THREAD_RUSH
	db 38, SILK_COMBO
	db 42, SILK_COMBO
	db 0

KakunaEvosMoves:
; YORKIE: same breed, growing maturity.
	db EVOLVE_LEVEL, 18, BEEDRILL
	db 0
	db 7, SILK_SLOW
	db 11, PAW_DASH
	db 14, SILK_FANG
	db 18, NUMB_POLLEN
	db 24, PACK_RUSH
	db 27, VENOM_DROOL
	db 30, THREAD_RUSH
	db 38, SILK_COMBO
	db 42, SILK_COMBO
	db 0

BeedrillEvosMoves:
; YORKGUARD: same breed, growing maturity.
	db 0
	db 7, SILK_SLOW
	db 11, PAW_DASH
	db 14, SILK_FANG
	db 18, NUMB_POLLEN
	db 24, PACK_RUSH
	db 27, VENOM_DROOL
	db 30, THREAD_RUSH
	db 38, SILK_COMBO
	db 42, SILK_COMBO
	db 0

MissingNo73EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

DodrioEvosMoves:
; BORZGALE: same breed, growing maturity.
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 27, AIR_NIP
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, GALE_HOWL
	db 0

PrimeapeEvosMoves:
; BOXER: same breed, growing maturity.
	db 0
	db 7, PAW_COMBO
	db 11, SCENT_LOCK
	db 15, BOXING_PAW
	db 22, PACK_HOWL
	db 28, SPAR_RUSH
	db 34, CLAW_RAKE
	db 0

DugtrioEvosMoves:
; BORDERDIG: same breed, growing maturity.
	db 0
	db 7, DUST_KICK
	db 11, PAW_DASH
	db 14, BONE_BASH
	db 18, BURROW_RUSH
	db 24, PACK_RUSH
	db 30, BONE_FETCH
	db 38, EARTH_STOMP
	db 42, FAULT_FANG
	db 0

VenomothEvosMoves:
; CRESTWING: same breed, growing maturity.
	db 0
	db 7, SILK_SLOW
	db 11, PAW_DASH
	db 14, SILK_FANG
	db 18, NUMB_POLLEN
	db 24, PACK_RUSH
	db 27, BARK_ECHO
	db 30, THREAD_RUSH
	db 38, SILK_COMBO
	db 42, MIND_YIP
	db 0

DewgongEvosMoves:
; GOLDTIDE: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, FROST_PAW
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, FROST_BARK
	db 0

MissingNo79EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo7AEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

CaterpieEvosMoves:
; PAPIPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 9, METAPOD
	db 0
	db 6, SILK_SLOW
	db 9, WING_PAW
	db 12, BARK_ECHO
	db 16, POLLEN_PUFF
	db 22, PAW_DASH
	db 28, SNUGGLE
	db 0

MetapodEvosMoves:
; PAPILLON: same breed, growing maturity.
	db EVOLVE_LEVEL, 14, BUTTERFREE
	db 0
	db 6, SILK_SLOW
	db 9, WING_PAW
	db 12, BARK_ECHO
	db 16, POLLEN_PUFF
	db 22, PAW_DASH
	db 28, SNUGGLE
	db 0

ButterfreeEvosMoves:
; PAPIFLY: same breed, growing maturity.
	db 0
	db 6, SILK_SLOW
	db 9, WING_PAW
	db 12, BARK_ECHO
	db 16, POLLEN_PUFF
	db 22, PAW_DASH
	db 28, SNUGGLE
	db 0

MachampEvosMoves:
; STAFFGUARD: same breed, growing maturity.
	db 0
	db 7, PAW_COMBO
	db 11, PAW_DASH
	db 14, SCENT_LOCK
	db 18, BOXING_PAW
	db 24, PACK_RUSH
	db 30, SPAR_RUSH
	db 38, SKY_PAW
	db 0

MissingNo7FEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

GolduckEvosMoves:
; LABRADOR: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 0

HypnoEvosMoves:
; BLOODHOUND: same breed, growing maturity.
	db 0
	db 7, BARK_ECHO
	db 11, PAW_DASH
	db 14, CALM_POSE
	db 18, MIND_YIP
	db 24, PACK_RUSH
	db 30, MIND_HOWL
	db 38, AURA_COAT
	db 42, LULL_STARE
	db 0

GolbatEvosMoves:
; IGGALE: same breed, growing maturity.
	db 0
	db 7, AIR_NIP
	db 11, PAW_DASH
	db 14, TAIL_GUST
	db 18, WING_PAW
	db 24, PACK_RUSH
	db 27, GHOST_LICK
	db 30, GALE_FANG
	db 38, SKY_POUNCE
	db 42, SHADE_HOWL
	db 0

MewtwoEvosMoves:
; Evolutions
	db 0
; Learnset
	db 63, BARRIER
	db 66, PSYCHIC_M
	db 70, RECOVER
	db 75, MIST
	db 81, AMNESIA
	db 0

SnorlaxEvosMoves:
; NEOMAST: same breed, growing maturity.
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, NAP_TIME
	db 0

MagikarpEvosMoves:
; SPRINGPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 20, GYARADOS
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 0

MissingNo86EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo87EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MukEvosMoves:
; SHARPEI: same breed, growing maturity.
	db 0
	db 7, VENOM_DROOL
	db 11, PAW_DASH
	db 14, TOXIC_DANDER
	db 18, VENOM_BARK
	db 24, PACK_RUSH
	db 30, VENOM_MARK
	db 38, VENOM_COAT
	db 0

MissingNo8AEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

KinglerEvosMoves:
; IRISTIDE: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, TIDE_PAW
	db 0

CloysterEvosMoves:
; CHESSTIDE: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, FROST_PAW
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, TIDE_GRIP
	db 0

MissingNo8CEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

ElectrodeEvosMoves:
; CHISPARK: same breed, growing maturity.
	db 0
	db 7, SPARK_YIP
	db 11, PAW_DASH
	db 14, STATIC_COAT
	db 18, VOLT_PAW
	db 24, PACK_RUSH
	db 30, VOLT_BARK
	db 38, STORM_HOWL
	db 0

ClefableEvosMoves:
; SAMOYED: same breed, growing maturity.
	db 0
	db 7, FROST_PAW
	db 11, PAW_DASH
	db 14, FROST_COAT
	db 18, POLAR_HOWL
	db 24, PACK_RUSH
	db 30, FROST_BARK
	db 38, WHITEOUT_YIP
	db 0

WeezingEvosMoves:
; PUGHAZE: same breed, growing maturity.
	db 0
	db 7, VENOM_DROOL
	db 11, PAW_DASH
	db 14, TOXIC_DANDER
	db 18, VENOM_BARK
	db 24, PACK_RUSH
	db 30, VENOM_MARK
	db 38, VENOM_COAT
	db 42, HAZE_BREATH
	db 0

PersianEvosMoves:
; BOSTON: same breed, growing maturity.
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, HEAD_BUMP
	db 0

MarowakEvosMoves:
; SCOTTDIG: same breed, growing maturity.
	db 0
	db 7, DUST_KICK
	db 11, PAW_DASH
	db 14, BONE_BASH
	db 18, BURROW_RUSH
	db 24, PACK_RUSH
	db 30, BONE_FETCH
	db 38, EARTH_STOMP
	db 0

MissingNo92EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

HaunterEvosMoves:
; WEIMAR: same breed, growing maturity.
	db EVOLVE_LEVEL, 32, GENGAR
	db 0
	db 7, GHOST_LICK
	db 11, PAW_DASH
	db 14, ODD_YIP
	db 18, SHADE_HOWL
	db 24, PACK_RUSH
	db 30, GHOST_GLARE
	db 38, SPIRIT_SHIFT
	db 0

AbraEvosMoves:
; POODPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 20, KADABRA
	db 0
	db 7, BARK_ECHO
	db 11, PAW_DASH
	db 14, CALM_POSE
	db 18, MIND_YIP
	db 24, PACK_RUSH
	db 30, MIND_HOWL
	db 38, AURA_COAT
	db 0

AlakazamEvosMoves:
; POODMIND: same breed, growing maturity.
	db 0
	db 7, BARK_ECHO
	db 11, PAW_DASH
	db 14, CALM_POSE
	db 18, MIND_YIP
	db 24, PACK_RUSH
	db 30, MIND_HOWL
	db 38, AURA_COAT
	db 0

PidgeottoEvosMoves:
; WHIPPET: same breed, growing maturity.
	db EVOLVE_LEVEL, 36, PIDGEOT
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 27, AIR_NIP
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, GALE_FANG
	db 0

PidgeotEvosMoves:
; WINDWHIP: same breed, growing maturity.
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 27, AIR_NIP
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, GALE_FANG
	db 0

StarmieEvosMoves:
; OTTERMIND: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, BARK_ECHO
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 0

BulbasaurEvosMoves:
; GROENPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 16, IVYSAUR
	db 0
	db 7, LEAF_FANG
	db 10, PAW_DASH
	db 13, ROOT_SNARE
	db 18, PACK_FOCUS
	db 24, PACK_RUSH
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 0

VenusaurEvosMoves:
; GROENHOUND: same breed, growing maturity.
	db 0
	db 7, LEAF_FANG
	db 10, PAW_DASH
	db 13, ROOT_SNARE
	db 18, PACK_FOCUS
	db 24, PACK_RUSH
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 0

TentacruelEvosMoves:
; SPANTIDE: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 27, VENOM_DROOL
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 0

MissingNo9CEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

GoldeenEvosMoves:
; AMERPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, SEAKING
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, DOG_PADDLE
	db 0

SeakingEvosMoves:
; AMERTIDE: same breed, growing maturity.
	db 0
	db 7, SPLASH_KICK
	db 11, PAW_DASH
	db 14, WATER_GUARD
	db 18, WAKE_CHARGE
	db 24, PACK_RUSH
	db 30, RIVER_RUSH
	db 38, TIDAL_BARK
	db 42, DOG_PADDLE
	db 0

MissingNo9FEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNoA0EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNoA1EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNoA2EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

PonytaEvosMoves:
; BASENPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, RAPIDASH
	db 0
	db 7, CINDER_YIP
	db 11, PAW_DASH
	db 14, SOOT_SHAKE
	db 18, EMBER_PAW
	db 24, PACK_RUSH
	db 30, CINDER_BARK
	db 38, FLAME_POUNCE
	db 0

RapidashEvosMoves:
; BASENFLARE: same breed, growing maturity.
	db 0
	db 7, CINDER_YIP
	db 11, PAW_DASH
	db 14, SOOT_SHAKE
	db 18, EMBER_PAW
	db 24, PACK_RUSH
	db 30, CINDER_BARK
	db 38, FLAME_POUNCE
	db 0

RattataEvosMoves:
; BEAGPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 18, RATICATE
	db 0
	db 7, PAW_DASH
	db 11, SCENT_LOCK
	db 15, DREAM_HOWL
	db 22, PACK_RUSH
	db 28, CLAW_RAKE
	db 34, PACK_HOWL
	db 0

RaticateEvosMoves:
; BEAGLE: same breed, growing maturity.
	db 0
	db 7, PAW_DASH
	db 11, SCENT_LOCK
	db 15, DREAM_HOWL
	db 22, PACK_RUSH
	db 28, CLAW_RAKE
	db 34, PACK_HOWL
	db 0

NidorinoEvosMoves:
; AUSSIE: same breed, growing maturity.
	db EVOLVE_LEVEL, 32, NIDOKING
	db 0
	db 7, VENOM_DROOL
	db 11, PAW_DASH
	db 14, TOXIC_DANDER
	db 18, VENOM_BARK
	db 24, PACK_RUSH
	db 27, PAW_COMBO
	db 30, VENOM_MARK
	db 38, VENOM_COAT
	db 42, SPAR_RUSH
	db 0

NidorinaEvosMoves:
; CATTLEDOG: same breed, growing maturity.
	db EVOLVE_LEVEL, 32, NIDOQUEEN
	db 0
	db 7, VENOM_DROOL
	db 11, PAW_DASH
	db 14, TOXIC_DANDER
	db 18, VENOM_BARK
	db 24, PACK_RUSH
	db 27, DUST_KICK
	db 30, VENOM_MARK
	db 38, VENOM_COAT
	db 42, EARTH_STOMP
	db 0

GeodudeEvosMoves:
; BULLPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 25, GRAVELER
	db 0
	db 8, BRACE
	db 11, STONE_PAW
	db 15, GUARD_HOWL
	db 22, PACK_RUSH
	db 30, BOULDER_RUSH
	db 36, HAUL
	db 0

PorygonEvosMoves:
; SHEPHGUARD: same breed, growing maturity.
	db 0
	db 7, PAW_DASH
	db 11, PAW_DASH
	db 14, NIP_FANG
	db 18, PACK_RUSH
	db 24, PACK_RUSH
	db 27, BARK_ECHO
	db 30, CRUSH_FANG
	db 38, CLAW_RAKE
	db 42, AURA_SHIFT
	db 0

AerodactylEvosMoves:
; WOLFGALE: same breed, growing maturity.
	db 0
	db 7, BRACE
	db 11, PAW_DASH
	db 14, STONE_PAW
	db 18, GUARD_HOWL
	db 24, PACK_RUSH
	db 27, AIR_NIP
	db 30, BOULDER_RUSH
	db 38, HAUL
	db 42, SKY_POUNCE
	db 0

MissingNoACEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MagnemiteEvosMoves:
; SCHNAUPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 24, MAGNETON
	db 0
	db 7, SPARK_YIP
	db 11, PAW_DASH
	db 14, STATIC_COAT
	db 18, VOLT_PAW
	db 24, PACK_RUSH
	db 27, BRACE
	db 30, VOLT_BARK
	db 38, STORM_HOWL
	db 0

MissingNoAEEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNoAFEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

CharmanderEvosMoves:
; SHIBAPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 16, CHARMELEON
	db 0
	db 7, CINDER_YIP
	db 10, PAW_COMBO
	db 13, PAW_DASH
	db 18, SCENT_LOCK
	db 24, PACK_RUSH
	db 30, CINDER_BARK
	db 38, FLAME_POUNCE
	db 0

SquirtleEvosMoves:
; NEWFPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 16, WARTORTLE
	db 0
	db 7, SPLASH_KICK
	db 10, BRACE
	db 13, PAW_COMBO
	db 18, PACK_FOCUS
	db 24, PACK_RUSH
	db 30, WAKE_CHARGE
	db 38, TIDAL_BARK
	db 0

CharmeleonEvosMoves:
; SHIBA: same breed, growing maturity.
	db EVOLVE_LEVEL, 36, CHARIZARD
	db 0
	db 7, CINDER_YIP
	db 10, PAW_COMBO
	db 13, PAW_DASH
	db 18, SCENT_LOCK
	db 24, PACK_RUSH
	db 30, CINDER_BARK
	db 38, FLAME_POUNCE
	db 0

WartortleEvosMoves:
; NEWFIE: same breed, growing maturity.
	db EVOLVE_LEVEL, 36, BLASTOISE
	db 0
	db 7, SPLASH_KICK
	db 10, BRACE
	db 13, PAW_COMBO
	db 18, PACK_FOCUS
	db 24, PACK_RUSH
	db 30, WAKE_CHARGE
	db 38, TIDAL_BARK
	db 0

CharizardEvosMoves:
; SHIBLAZE: same breed, growing maturity.
	db 0
	db 7, CINDER_YIP
	db 10, PAW_COMBO
	db 13, PAW_DASH
	db 18, SCENT_LOCK
	db 24, PACK_RUSH
	db 30, CINDER_BARK
	db 38, FLAME_POUNCE
	db 0

MissingNoB5EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

FossilKabutopsEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

FossilAerodactylEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MonGhostEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

OddishEvosMoves:
; LAGOPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 18, GLOOM
	db 0
	db 7, LEAF_FANG
	db 11, PAW_DASH
	db 14, ROOT_SNARE
	db 18, THORN_CLAW
	db 24, PACK_RUSH
	db 27, DUST_KICK
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 0

GloomEvosMoves:
; LAGOTTO: same breed, growing maturity.
	db EVOLVE_LEVEL, 32, VILEPLUME
	db 0
	db 7, LEAF_FANG
	db 11, PAW_DASH
	db 14, ROOT_SNARE
	db 18, THORN_CLAW
	db 24, PACK_RUSH
	db 27, DUST_KICK
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 0

VileplumeEvosMoves:
; TRUFFHOUND: same breed, growing maturity.
	db 0
	db 7, LEAF_FANG
	db 11, PAW_DASH
	db 14, ROOT_SNARE
	db 18, THORN_CLAW
	db 24, PACK_RUSH
	db 27, DUST_KICK
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 0

BellsproutEvosMoves:
; SETTERPUP: same breed, growing maturity.
	db EVOLVE_LEVEL, 16, WEEPINBELL
	db 0
	db 7, LEAF_FANG
	db 11, PAW_DASH
	db 14, ROOT_SNARE
	db 18, THORN_CLAW
	db 24, PACK_RUSH
	db 27, CINDER_YIP
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 42, BLOOM_DANCE
	db 0

WeepinbellEvosMoves:
; IRISHSET: same breed, growing maturity.
	db EVOLVE_LEVEL, 32, VICTREEBEL
	db 0
	db 7, LEAF_FANG
	db 11, PAW_DASH
	db 14, ROOT_SNARE
	db 18, THORN_CLAW
	db 24, PACK_RUSH
	db 27, CINDER_YIP
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 42, BLOOM_DANCE
	db 0

VictreebelEvosMoves:
; SUNSETTER: same breed, growing maturity.
	db 0
	db 7, LEAF_FANG
	db 11, PAW_DASH
	db 14, ROOT_SNARE
	db 18, THORN_CLAW
	db 24, PACK_RUSH
	db 27, CINDER_YIP
	db 30, BRIAR_FANG
	db 38, SUN_HOWL
	db 42, BLOOM_DANCE
	db 0
