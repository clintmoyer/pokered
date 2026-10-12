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
; Evolutions
	db 0
; Learnset
	db 30, STOMP
	db 35, TAIL_WHIP
	db 40, FURY_ATTACK
	db 48, HORN_DRILL
	db 55, LEER
	db 64, TAKE_DOWN
	db 0

KangaskhanEvosMoves:
; Evolutions
	db 0
; Learnset
	db 26, BITE
	db 31, TAIL_WHIP
	db 36, MEGA_PUNCH
	db 41, LEER
	db 46, DIZZY_PUNCH
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
; Evolutions
	db 0
; Learnset
	db 18, DISABLE
	db 22, HEADBUTT
	db 27, GROWL
	db 33, WATER_GUN
	db 37, WITHDRAW
	db 44, AMNESIA
	db 55, PSYCHIC_M
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
; Evolutions
	db 0
; Learnset
	db 28, STOMP
	db 0

LickitungEvosMoves:
; Evolutions
	db 0
; Learnset
	db 7, STOMP
	db 15, DISABLE
	db 23, DEFENSE_CURL
	db 31, SLAM
	db 39, SCREECH
	db 0

ExeggcuteEvosMoves:
; Evolutions
	db EVOLVE_ITEM, LEAF_STONE, 1, EXEGGUTOR
	db 0
; Learnset
	db 25, REFLECT
	db 28, LEECH_SEED
	db 32, STUN_SPORE
	db 37, POISONPOWDER
	db 42, SOLARBEAM
	db 48, SLEEP_POWDER
	db 0

GrimerEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 38, MUK
	db 0
; Learnset
	db 30, POISON_GAS
	db 33, MINIMIZE
	db 37, SLUDGE
	db 42, HARDEN
	db 48, SCREECH
	db 55, ACID_ARMOR
	db 0

GengarEvosMoves:
; Evolutions
	db 0
; Learnset
	db 29, HYPNOSIS
	db 38, DREAM_EATER
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
; Evolutions
	db EVOLVE_LEVEL, 42, RHYDON
	db 0
; Learnset
	db 30, STOMP
	db 35, TAIL_WHIP
	db 40, FURY_ATTACK
	db 45, HORN_DRILL
	db 50, LEER
	db 55, TAKE_DOWN
	db 0

LaprasEvosMoves:
; Evolutions
	db 0
; Learnset
	db 16, SING
	db 20, MIST
	db 25, BODY_SLAM
	db 31, CONFUSE_RAY
	db 38, ICE_BEAM
	db 46, HYDRO_PUMP
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
; Evolutions
	db EVOLVE_ITEM, WATER_STONE, 1, CLOYSTER
	db 0
; Learnset
	db 18, SUPERSONIC
	db 23, CLAMP
	db 30, AURORA_BEAM
	db 39, LEER
	db 50, ICE_BEAM
	db 0

TentacoolEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 30, TENTACRUEL
	db 0
; Learnset
	db 7, SUPERSONIC
	db 13, WRAP
	db 18, POISON_STING
	db 22, WATER_GUN
	db 27, CONSTRICT
	db 33, BARRIER
	db 40, SCREECH
	db 48, HYDRO_PUMP
	db 0

GastlyEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 25, HAUNTER
	db 0
; Learnset
	db 27, HYPNOSIS
	db 35, DREAM_EATER
	db 0

ScytherEvosMoves:
; Evolutions
	db 0
; Learnset
	db 17, LEER
	db 20, FOCUS_ENERGY
	db 24, DOUBLE_TEAM
	db 29, SLASH
	db 35, SWORDS_DANCE
	db 42, AGILITY
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
; Evolutions
	db 0
; Learnset
	db 25, SEISMIC_TOSS
	db 30, GUILLOTINE
	db 36, FOCUS_ENERGY
	db 43, HARDEN
	db 49, SLASH
	db 54, SWORDS_DANCE
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
; Evolutions
	db EVOLVE_LEVEL, 37, SLOWBRO
	db 0
; Learnset
	db 18, DISABLE
	db 22, HEADBUTT
	db 27, GROWL
	db 33, WATER_GUN
	db 40, AMNESIA
	db 48, PSYCHIC_M
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
; Evolutions
	db 0
; Learnset
	db 24, SING
	db 30, GROWL
	db 38, MINIMIZE
	db 44, DEFENSE_CURL
	db 48, LIGHT_SCREEN
	db 54, DOUBLE_EDGE
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
; Evolutions
	db 0
; Learnset
	db 15, CONFUSION
	db 23, LIGHT_SCREEN
	db 31, DOUBLESLAP
	db 39, MEDITATE
	db 47, SUBSTITUTE
	db 0

HitmonleeEvosMoves:
; Evolutions
	db 0
; Learnset
	db 33, ROLLING_KICK
	db 38, JUMP_KICK
	db 43, FOCUS_ENERGY
	db 48, HI_JUMP_KICK
	db 53, MEGA_KICK
	db 0

HitmonchanEvosMoves:
; Evolutions
	db 0
; Learnset
	db 33, FIRE_PUNCH
	db 38, ICE_PUNCH
	db 43, THUNDERPUNCH
	db 48, MEGA_PUNCH
	db 53, COUNTER
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
; Evolutions
	db 0
; Learnset
	db 13, STUN_SPORE
	db 20, LEECH_LIFE
	db 30, SPORE
	db 39, SLASH
	db 48, GROWTH
	db 0

PsyduckEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 33, GOLDUCK
	db 0
; Learnset
	db 28, TAIL_WHIP
	db 31, DISABLE
	db 36, CONFUSION
	db 43, FURY_SWIPES
	db 52, HYDRO_PUMP
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
; Evolutions
	db 0
; Learnset
	db 36, LEER
	db 39, CONFUSE_RAY
	db 43, FIRE_PUNCH
	db 48, SMOKESCREEN
	db 52, SMOG
	db 55, FLAMETHROWER
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
; Evolutions
	db EVOLVE_LEVEL, 35, WEEZING
	db 0
; Learnset
	db 32, SLUDGE
	db 37, SMOKESCREEN
	db 40, SELFDESTRUCT
	db 45, HAZE
	db 48, EXPLOSION
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
; Evolutions
	db EVOLVE_LEVEL, 34, DEWGONG
	db 0
; Learnset
	db 30, GROWL
	db 35, AURORA_BEAM
	db 40, REST
	db 45, TAKE_DOWN
	db 50, ICE_BEAM
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
; Evolutions
	db 0
; Learnset
	db 21, STOMP
	db 28, TAIL_WHIP
	db 35, LEER
	db 44, RAGE
	db 51, TAKE_DOWN
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
; Evolutions
	db 0
; Learnset
	db 7, LEER
	db 15, FURY_ATTACK
	db 23, SWORDS_DANCE
	db 31, AGILITY
	db 39, SLASH
	db 0

VenonatEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 31, VENOMOTH
	db 0
; Learnset
	db 24, POISONPOWDER
	db 27, LEECH_LIFE
	db 30, STUN_SPORE
	db 35, PSYBEAM
	db 38, SLEEP_POWDER
	db 43, PSYCHIC_M
	db 0

DragoniteEvosMoves:
; Evolutions
	db 0
; Learnset
	db 10, THUNDER_WAVE
	db 20, AGILITY
	db 35, SLAM
	db 45, DRAGON_RAGE
	db 60, HYPER_BEAM
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
; Evolutions
	db EVOLVE_LEVEL, 31, DODRIO
	db 0
; Learnset
	db 20, GROWL
	db 24, FURY_ATTACK
	db 30, DRILL_PECK
	db 36, RAGE
	db 40, TRI_ATTACK
	db 44, AGILITY
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
; Evolutions
	db 0
; Learnset
	db 18, LICK
	db 23, DOUBLESLAP
	db 31, ICE_PUNCH
	db 39, BODY_SLAM
	db 47, THRASH
	db 58, BLIZZARD
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
; Evolutions
	db 0
; Learnset
	db 51, BLIZZARD
	db 55, AGILITY
	db 60, MIST
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
; Evolutions
	db 0
; Learnset
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
; Evolutions
	db EVOLVE_LEVEL, 28, KINGLER
	db 0
; Learnset
	db 20, VICEGRIP
	db 25, GUILLOTINE
	db 30, STOMP
	db 35, CRABHAMMER
	db 40, HARDEN
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
; Evolutions
	db EVOLVE_LEVEL, 30, DRAGONAIR
	db 0
; Learnset
	db 10, THUNDER_WAVE
	db 20, AGILITY
	db 30, SLAM
	db 40, DRAGON_RAGE
	db 50, HYPER_BEAM
	db 0

DragonairEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 55, DRAGONITE
	db 0
; Learnset
	db 10, THUNDER_WAVE
	db 20, AGILITY
	db 35, SLAM
	db 45, DRAGON_RAGE
	db 55, HYPER_BEAM
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
; Evolutions
	db EVOLVE_LEVEL, 32, SEADRA
	db 0
; Learnset
	db 19, SMOKESCREEN
	db 24, LEER
	db 30, WATER_GUN
	db 37, AGILITY
	db 45, HYDRO_PUMP
	db 0

SeadraEvosMoves:
; Evolutions
	db 0
; Learnset
	db 19, SMOKESCREEN
	db 24, LEER
	db 30, WATER_GUN
	db 41, AGILITY
	db 52, HYDRO_PUMP
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
; Evolutions
	db EVOLVE_LEVEL, 24, PARASECT
	db 0
; Learnset
	db 13, STUN_SPORE
	db 20, LEECH_LIFE
	db 27, SPORE
	db 34, SLASH
	db 41, GROWTH
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
; Evolutions
	db 0
; Learnset
	db 20, GROWL
	db 24, FURY_ATTACK
	db 30, DRILL_PECK
	db 39, RAGE
	db 45, TRI_ATTACK
	db 51, AGILITY
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
; Evolutions
	db 0
; Learnset
	db 24, POISONPOWDER
	db 27, LEECH_LIFE
	db 30, STUN_SPORE
	db 38, PSYBEAM
	db 43, SLEEP_POWDER
	db 50, PSYCHIC_M
	db 0

DewgongEvosMoves:
; Evolutions
	db 0
; Learnset
	db 30, GROWL
	db 35, AURORA_BEAM
	db 44, REST
	db 50, TAKE_DOWN
	db 56, ICE_BEAM
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
; Evolutions
	db 0
; Learnset
	db 28, TAIL_WHIP
	db 31, DISABLE
	db 39, CONFUSION
	db 48, FURY_SWIPES
	db 59, HYDRO_PUMP
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
; Evolutions
	db 0
; Learnset
	db 35, BODY_SLAM
	db 41, HARDEN
	db 48, DOUBLE_EDGE
	db 56, HYPER_BEAM
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
; Evolutions
	db 0
; Learnset
	db 30, POISON_GAS
	db 33, MINIMIZE
	db 37, SLUDGE
	db 45, HARDEN
	db 53, SCREECH
	db 60, ACID_ARMOR
	db 0

MissingNo8AEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

KinglerEvosMoves:
; Evolutions
	db 0
; Learnset
	db 20, VICEGRIP
	db 25, GUILLOTINE
	db 34, STOMP
	db 42, CRABHAMMER
	db 49, HARDEN
	db 0

CloysterEvosMoves:
; Evolutions
	db 0
; Learnset
	db 50, SPIKE_CANNON
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
; Evolutions
	db 0
; Learnset
	db 32, SLUDGE
	db 39, SMOKESCREEN
	db 43, SELFDESTRUCT
	db 49, HAZE
	db 53, EXPLOSION
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
; Evolutions
	db EVOLVE_TRADE, 1, GENGAR
	db 0
; Learnset
	db 29, HYPNOSIS
	db 38, DREAM_EATER
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
; Evolutions
	db 0
; Learnset
	db 7, SUPERSONIC
	db 13, WRAP
	db 18, POISON_STING
	db 22, WATER_GUN
	db 27, CONSTRICT
	db 35, BARRIER
	db 43, SCREECH
	db 50, HYDRO_PUMP
	db 0

MissingNo9CEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

GoldeenEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 33, SEAKING
	db 0
; Learnset
	db 19, SUPERSONIC
	db 24, HORN_ATTACK
	db 30, FURY_ATTACK
	db 37, WATERFALL
	db 45, HORN_DRILL
	db 54, AGILITY
	db 0

SeakingEvosMoves:
; Evolutions
	db 0
; Learnset
	db 19, SUPERSONIC
	db 24, HORN_ATTACK
	db 30, FURY_ATTACK
	db 39, WATERFALL
	db 48, HORN_DRILL
	db 54, AGILITY
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
; Evolutions
	db EVOLVE_LEVEL, 40, RAPIDASH
	db 0
; Learnset
	db 30, TAIL_WHIP
	db 32, STOMP
	db 35, GROWL
	db 39, FIRE_SPIN
	db 43, TAKE_DOWN
	db 48, AGILITY
	db 0

RapidashEvosMoves:
; Evolutions
	db 0
; Learnset
	db 30, TAIL_WHIP
	db 32, STOMP
	db 35, GROWL
	db 39, FIRE_SPIN
	db 47, TAKE_DOWN
	db 55, AGILITY
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
; Evolutions
	db 0
; Learnset
	db 33, SUPERSONIC
	db 38, BITE
	db 45, TAKE_DOWN
	db 54, HYPER_BEAM
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
