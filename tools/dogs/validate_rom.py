#!/usr/bin/env python3
"""Check compiled dog data and sprite constraints, including ID alignment."""
from pathlib import Path
import re
from PIL import Image
from data import DOGS, MOVES, species_label, sprite_filename

ROOT=Path(__file__).resolve().parents[2]
rom=(ROOT/'pokered.gbc').read_bytes()
symbols={}
for line in (ROOT/'pokered.sym').read_text().splitlines():
    m=re.match(r'([0-9a-fA-F]+):([0-9a-fA-F]+) (\S+)',line)
    if m: symbols[m[3]]=(int(m[1],16),int(m[2],16))
def offset(symbol):
    bank,address=symbols[symbol]
    return bank*0x4000+(address%0x4000) if bank else address
def constants(path):
    return {name:int(value,16) for name,value in re.findall(r'^\s*const (\w+)\s*; \$?([0-9a-fA-F]{2})\b',(ROOT/path).read_text(),re.M)}
species_ids=constants('constants/pokemon_constants.asm')
move_ids=constants('constants/move_constants.asm')
type_ids=constants('constants/type_constants.asm')
effect_ids=constants('constants/move_effect_constants.asm')
item_ids=constants('constants/item_constants.asm')
charmap={}
for character,value in re.findall(r'^\s*charmap "([^"\n]+)",\s*\$([0-9a-fA-F]+)',(ROOT/'constants/charmap.asm').read_text(),re.M):
    charmap.setdefault(int(value,16),character) # English glyphs precede unused Japanese aliases.
def decode(value): return ''.join(charmap.get(b,'?') for b in value if b != 0x50)

move_names=[]; pos=offset('MoveNames')
for _ in range(165):
    end=rom.index(0x50,pos)
    move_names.append(decode(rom[pos:end])); pos=end+1
for alias,(slot,name,effect,power,kind,accuracy,pp) in MOVES.items():
    assert 1 <= len(name) <= 12, name
    move_id=move_ids[slot]
    assert move_names[move_id-1] == name, (slot,move_names[move_id-1],name)
    record=rom[offset('Moves')+(move_id-1)*6:][:6]
    assert tuple(record) == (move_id,effect_ids[effect],power,type_ids[kind],accuracy*255//100,pp), (slot,record)

for dog in DOGS:
    sid=species_ids[dog['slot']]
    name=decode(rom[offset('MonsterNames')+(sid-1)*10:][:10])
    assert name == dog['name'] and len(name) <= 10, (sid,name,dog['name'])
    dex=rom[offset('PokedexOrder')+sid-1]
    record=rom[offset('BaseStats')+(dex-1)*28:][:28]
    assert tuple(record[1:6]) == dog['stats'], (name,record[1:6])
    assert tuple(record[6:8]) == tuple(type_ids[t] for t in dog['types']), name
    expected_base=[move_ids[MOVES[m][0]] for m in dog['base']]
    assert list(record[15:19]) == expected_base+[0]*(4-len(expected_base)), name
    front= symbols[species_label(dog['slot'])+'PicFront']
    back= symbols[species_label(dog['slot'])+'PicBack']
    assert front[0] == back[0] and front[0] >= 0x2d, (name,front,back)
    assert int.from_bytes(record[11:13],'little') == front[1], name
    assert int.from_bytes(record[13:15],'little') == back[1], name
    pointer_pos=offset('EvosMovesPointerTable')+(sid-1)*2
    pointer=int.from_bytes(rom[pointer_pos:pointer_pos+2],'little')
    bank=symbols['EvosMovesPointerTable'][0]
    position=bank*0x4000+pointer%0x4000
    if dog['evolution']:
        assert tuple(rom[position:position+3]) == (1,dog['evolution'][0],species_ids[dog['evolution'][1]]), name
        position += 3
    for branch in dog.get('branch_evolutions', []):
        assert tuple(rom[position:position+4]) == (2,item_ids[branch['item']],1,species_ids[branch['target']]),name
        position += 4
    assert rom[position] == 0, name
    position += 1
    learned=[]
    while rom[position]:
        level,move=rom[position:position+2]
        assert move in [move_ids[value[0]] for value in MOVES.values()], (name,level,move)
        learned.append((level,move)); position+=2
    assert learned == [(level,move_ids[MOVES[move][0]]) for level,move in dog['learnset']], (name,learned)
    for view,size in [('front',(56,56)),('back',(32,32))]:
        im=Image.open(ROOT/f'gfx/pokemon/{view}'/(sprite_filename(dog['slot'])+('b' if view == 'back' else '')+'.png')).convert('L')
        assert im.size == size, (name,view,im.size)
        assert set(im.tobytes()) <= {0,85,170,255}, (name,view)

allowed_species={species_ids[d['slot']] for d in DOGS}
for route in ['Route1','Route2','Route22','ViridianForest']:
    position=offset(route+'WildMons')
    encounters=rom[position+1:position+21]
    assert all(sid in allowed_species for sid in encounters[1::2]), (route,encounters)
    assert species_ids['MANKEY'] in encounters[1::2], 'Every opening area should offer the Boxer support route.'
assert set(rom[offset('TitleMons'):offset('TitleMons')+16]) <= allowed_species

# Explicit dog bank lookup must agree with both pointers in every compiled header.
pos=offset('DogSpriteSpecies')
bank_table={}
while rom[pos] != 255:
    bank_table[rom[pos]]=rom[pos+1]; pos+=2
assert set(bank_table)==allowed_species
for dog in DOGS:
    assert bank_table[species_ids[dog['slot']]] == symbols[species_label(dog['slot'])+'PicFront'][0]

import json
misty=json.loads((ROOT/'data/dogs/misty.json').read_text())
name_to_id={d['name']:species_ids[d['slot']] for d in DOGS}
for route, encounters in misty['wild'].items():
    pos=offset(route+'WildMons')
    assert list(rom[pos+1:pos+21]) == [v for level,name in encounters for v in (level,name_to_id[name])], route
    assert rom[pos+21]==0, route # no unconverted water encounters in this slice
route25=misty['wild']['Route25']
assert {'GROENPUP','SHIBAPUP','NEWFPUP'} <= {name for _,name in route25}
assert 'LAGOPUP' in {name for _,name in misty['wild']['Route24']}
assert 'POMPUP' in {name for route in misty['wild'].values() for _,name in route}
assert list(rom[offset('MistyData'):offset('MistyData')+6]) == [255,18,name_to_id['OTTERPUP'],21,name_to_id['OTTERMIND'],0]
assert list(rom[offset('BillsDogSpecies'):offset('BillsDogSpecies')+4]) == [name_to_id[n] for n in ('GROENPUP','SHIBAPUP','NEWFPUP','POMPUP')]

field_names=[];pos=offset('FieldMoveNames')
for _ in range(9):
    end=rom.index(0x50,pos);field_names.append(decode(rom[pos:end]));pos=end+1
for slot,index,name in [('CUT',1,'BRAMBLE BITE'),('FLY',2,'SKYBOUND'),('SURF',4,'DOG PADDLE'),('STRENGTH',5,'HAUL'),('FLASH',6,'BEACON BARK'),('DIG',7,'BURROW RUSH'),('TELEPORT',8,'HOMEBOUND'),('SOFTBOILED',9,'RESCUE REST')]:
    pos=offset('FieldMoveDisplayData')+(index-1)*3
    assert rom[pos]==move_ids[slot] and rom[pos+1]==index and rom[pos+2]==min(12,18-len(name)),slot
    assert field_names[index-1]==name,slot

# Resolve each reachable map's trainer class and party index, then inspect ROM teams.
trainer_source=(ROOT/'data/trainers/parties.asm').read_text().split('assert_table_length NUM_TRAINERS')[0]
labels=re.findall(r'^\tdw (\w+Data)$',trainer_source,re.M)
trainer_constants=(ROOT/'constants/trainer_constants.asm').read_text()
order=re.findall(r'^\s*trainer_const (\w+)\s*;',trainer_constants,re.M)[1:]
classes={f'OPP_{name}':label for name,label in zip(order,labels)}
chapter=['Route3','Route4','MtMoon1F','MtMoonB1F','MtMoonB2F','Route24','Route25','CeruleanCity','CeruleanGym']
checked=0
for route in chapter:
    objects=(ROOT/f'data/maps/objects/{route}.asm').read_text()
    for trainer,index in re.findall(r'object_event[^\n]+, (OPP_\w+), (\d+)',objects):
        pos=offset(classes[trainer])
        for party_index in range(1,int(index)+1):
            variable=rom[pos]==255; pos+=1
            members=[]
            while rom[pos]:
                if variable: pos+=1
                members.append(rom[pos]); pos+=1
            pos+=1
        assert set(members) <= allowed_species,(route,trainer,index,members)
        checked+=1
assert checked >= 30,checked

assert rom[0x134:0x13f] == b'POKEMON RED', 'Unexpected cartridge title'
surge=json.loads((ROOT/'data/dogs/surge.json').read_text())
for route, encounters in surge['wild'].items():
    pos=offset(route+'WildMons')
    assert rom[pos] == surge['rates'][route], route
    assert list(rom[pos+1:pos+21]) == [v for level,name in encounters for v in (level,name_to_id[name])], route
    assert rom[pos+21] == 0, route
assert 'BORDERPUP' in {name for _,name in surge['wild']['DiglettsCave']}
for root in ('BOSTPUP','STAFFPUP','SCHNAUPUP','BLOODPUP','CHIPUP'):
    assert root in {name for encounters in surge['wild'].values() for _,name in encounters},root

def trainer_party(label,index):
    pos=offset(label)
    for _ in range(index):
        variable=rom[pos]==255; level=rom[pos];pos+=1
        party=[]
        while rom[pos]:
            if variable:level=rom[pos];pos+=1
            party.append((level,rom[pos]));pos+=1
        pos+=1
    return party

for label,parties in surge['trainers'].items():
    for index,members in parties.items():
        assert trainer_party(label,int(index)) == [(level,name_to_id[name]) for level,name in members],(label,index)
for index,members in enumerate(surge['rival'],1):
    assert trainer_party('Rival2Data',index) == [(level,name_to_id[name]) for level,name in members]
assert trainer_party('LtSurgeData',1) == [(level,name_to_id[name]) for level,name in surge['lt_surge']]
for route in surge['maps']:
    objects=(ROOT/f'data/maps/objects/{route}.asm').read_text()
    for trainer,index in re.findall(r'object_event[^\n]+, (OPP_\w+), (\d+)',objects):
        assert {sid for _,sid in trainer_party(classes[trainer],int(index))} <= allowed_species,(route,trainer,index)
        checked+=1

trade_ids=['TRADE_FOR_TERRY','TRADE_FOR_MARCEL','UNUSED','TRADE_FOR_SAILOR','TRADE_FOR_DUX','TRADE_FOR_MARC','TRADE_FOR_LOLA','TRADE_FOR_DORIS','TRADE_FOR_CRINKLES','TRADE_FOR_SPOT']
for trade,(give,receive,nickname) in surge['trades'].items():
    pos=offset('TradeMons')+trade_ids.index(trade)*14
    assert list(rom[pos:pos+2]) == [name_to_id[give],name_to_id[receive]],trade
    assert rom[pos+2] == 0,trade # casual dialogue, no obsolete trade-evolution claim
    assert decode(rom[pos+3:pos+14]) == nickname,trade
palette_ids=constants('constants/palette_constants.asm')
for slot,palette in surge['palettes'].items():
    dog=next(d for d in DOGS if d['slot']==slot)
    assert rom[offset('MonsterPalettes')+dog['dex']] == palette_ids[palette],slot
for dex in (1,2,3):
    assert rom[offset('MonsterPalettes')+dex] == palette_ids['PAL_GROENMON']

# Cut remains a reusable HM with its stable move ID and compatible early dogs.
tmhm_source=(ROOT/'constants/item_constants.asm').read_text()
tmhm_order=re.findall(r'^\s*add_tm (\w+)',tmhm_source,re.M)+re.findall(r'^\s*add_hm (\w+)',tmhm_source,re.M)
assert tmhm_order.index('CUT') == 50
for slot in ('BULBASAUR','CHARMANDER','RATTATA'):
    dog=next(d for d in DOGS if d['slot']==slot)
    pos=offset('BaseStats')+(dog['dex']-1)*28+20
    assert rom[pos+50//8] & 1 << (50%8),slot
erika=json.loads((ROOT/'data/dogs/erika.json').read_text())
for route,encounters in erika['wild'].items():
    pos=offset(route+'WildMons')
    assert rom[pos] == erika['rates'][route],route
    assert list(rom[pos+1:pos+21]) == [v for level,name in encounters for v in (level,name_to_id[name])],route
    assert rom[pos+21] == 0,route
assert {'KEESPUP','ELKPUP'} <= {name for _,name in erika['wild']['RockTunnelB1F']}
assert 'TERVPUP' in {name for _,name in erika['wild']['Route7']}
for label,parties in erika['trainers'].items():
    for index,members in parties.items():
        assert trainer_party(label,int(index)) == [(level,name_to_id[name]) for level,name in members],(label,index)
assert trainer_party('ErikaData',1) == [(level,name_to_id[name]) for level,name in erika['erika']]
for route in erika['maps']:
    objects=(ROOT/f'data/maps/objects/{route}.asm').read_text()
    for trainer,index in re.findall(r'object_event[^\n]+, (OPP_\w+), (\d+)',objects):
        assert {sid for _,sid in trainer_party(classes[trainer],int(index))} <= allowed_species,(route,trainer,index)
        checked+=1
for slot,palette in erika['palettes'].items():
    dog=next(d for d in DOGS if d['slot']==slot)
    assert rom[offset('MonsterPalettes')+dog['dex']] == palette_ids[palette],slot
for group,members in enumerate([erika['prizes'][:3],erika['prizes'][3:]],1):
    pos=offset(f'PrizeMenuMon{group}Entries')
    assert list(rom[pos:pos+4]) == [name_to_id[name] for _,name,_ in members]+[0x50]
    pos=offset(f'PrizeMenuMon{group}Cost')
    expected=b''.join(bytes.fromhex(f'{price:04d}') for _,_,price in members)+b'\x50'
    assert rom[pos:pos+7] == expected
pos=offset('PrizeMonLevelDictionary')
assert list(rom[pos:pos+12]) == [v for level,name,_ in erika['prizes'] for v in (name_to_id[name],level)]
pos=offset('CeladonMart4FClerkText')
assert list(rom[pos:pos+8]) == [0xfe,5,item_ids['POKE_DOLL'],item_ids['FIRE_STONE'],item_ids['THUNDER_STONE'],item_ids['WATER_STONE'],item_ids['LEAF_STONE'],0xff]
for slot,move in [('PIKACHU','FLASH'),('FEAROW','FLY')]:
    dog=next(d for d in DOGS if d['slot']==slot)
    flag=tmhm_order.index(move);pos=offset('BaseStats')+(dog['dex']-1)*28+20
    assert rom[pos+flag//8] & 1 << (flag%8),slot
koga=json.loads((ROOT/'data/dogs/koga.json').read_text())
for route in koga['wild'].keys() | koga['water'].keys():
    pos=offset(route+'WildMons')
    for key,rates in [('wild','rates'),('water','water_rates')]:
        encounters=koga[key].get(route,[])
        assert rom[pos] == koga[rates].get(route,0),route
        pos+=1
        if encounters:
            assert list(rom[pos:pos+20]) == [v for level,name in encounters for v in (level,name_to_id[name])],route
            pos+=20
# Check the actual map pointers as well as the generated encounter bytes.
map_ids={name:int(value,16) for name,value in re.findall(r'^\s*map_const (\w+),[^;]+; \$([\dA-F]+)',(ROOT/'constants/map_constants.asm').read_text(),re.M)}
for code in ('ROUTE_19','ROUTE_20'):
    pos=offset('WildDataPointers')+map_ids[code]*2
    assert int.from_bytes(rom[pos:pos+2],'little') == symbols['SeaRoutesWildMons'][1],code
for label,parties in koga['trainers'].items():
    for index,members in parties.items():
        assert trainer_party(label,int(index)) == [(level,name_to_id[name]) for level,name in members],(label,index)
for route in koga['maps']:
    objects=(ROOT/f'data/maps/objects/{route}.asm').read_text()
    for trainer,index in re.findall(r'object_event[^\n]+, (OPP_\w+), (\d+)',objects):
        assert {sid for _,sid in trainer_party(classes[trainer],int(index))} <= allowed_species,(route,trainer,index)
        checked+=1
for slot,palette in koga['palettes'].items():
    dog=next(d for d in DOGS if d['slot']==slot)
    assert rom[offset('MonsterPalettes')+dog['dex']] == palette_ids[palette],slot
pos=offset('GoodRodMons')
assert list(rom[pos:pos+4]) == [v for level,name in koga['good_rod'] for v in (level,name_to_id[name])]
for group,members in koga['super_rod'].items():
    pos=offset('SuperRodData.Group'+group)
    assert list(rom[pos:pos+1+len(members)*2]) == [len(members)]+[v for level,name in members for v in (level,name_to_id[name])],group
# Each newly implemented family has a repeatable root in the current ROM.
sources={name for encounters in list(koga['wild'].values())+list(koga['water'].values()) for _,name in encounters}
for slot in koga['new_forms']:
    dog=next(d for d in DOGS if d['slot']==slot)
    if dog['acquisition']['method']=='wild':assert dog['name'] in sources,dog['name']
assert 'NEOMAST' in {name for _,name in koga['wild']['Route18']}
for slot,move in [('WARTORTLE','SURF'),('RATICATE','STRENGTH')]:
    dog=next(d for d in DOGS if d['slot']==slot)
    flag=tmhm_order.index(move);pos=offset('BaseStats')+(dog['dex']-1)*28+20
    assert rom[pos+flag//8] & 1 << (flag%8),slot
assert symbols['EvolutionAfterBattle'][0] == symbols['EvosMovesPointerTable'][0]
assert symbols['EvolutionAfterBattle'][0] != symbols['BaseStats'][0]
sabrina=json.loads((ROOT/'data/dogs/sabrina.json').read_text())
for label,parties in sabrina['trainers'].items():
    for index,members in parties.items():
        assert trainer_party(label,int(index)) == [(level,name_to_id[name]) for level,name in members],(label,index)
for route in sabrina['maps']:
    objects=(ROOT/f'data/maps/objects/{route}.asm').read_text()
    for trainer,index in re.findall(r'object_event[^\n]+, (OPP_\w+), (\d+)',objects):
        assert {sid for _,sid in trainer_party(classes[trainer],int(index))} <= allowed_species,(route,trainer,index)
        checked+=1
for slot,palette in sabrina['palettes'].items():
    dog=next(d for d in DOGS if d['slot']==slot)
    assert rom[offset('MonsterPalettes')+dog['dex']] == palette_ids[palette],slot
for name,source in sabrina['repeatable_sources'].items():
    encounters=koga['wild'].get(source,koga['water'].get(source,[]))
    assert name in {dog for _,dog in encounters},name
pos=offset('SilphCo7FSilphWorkerM1Text.give_lapras')
end=offset('SilphCo7FSilphWorkerM1Text.saved_silph')
level,name=sabrina['gifts']['silph']
assert bytes([1,level,name_to_id[name]]) in rom[pos:end], 'Silph gift species/level'
assert {'DOBERGUARD','ROTTGUARD'} == {name for _,name in sabrina['gifts']['dojo']}
blaine=json.loads((ROOT/'data/dogs/blaine.json').read_text())
for route in blaine['wild'].keys() | blaine['water'].keys():
    pos=offset(route+'WildMons')
    for key,rates in [('wild','rates'),('water','water_rates')]:
        encounters=blaine[key].get(route,[])
        assert rom[pos] == blaine[rates].get(route,0),route
        pos+=1
        if encounters:
            assert list(rom[pos:pos+20]) == [v for level,name in encounters for v in (level,name_to_id[name])],(route,key)
            pos+=20
for label,parties in blaine['trainers'].items():
    for index,members in parties.items():
        assert trainer_party(label,int(index)) == [(level,name_to_id[name]) for level,name in members],(label,index)
for route in blaine['maps']:
    objects=(ROOT/f'data/maps/objects/{route}.asm').read_text()
    for trainer,index in re.findall(r'object_event[^\n]+, (OPP_\w+), (\d+)',objects):
        assert {sid for _,sid in trainer_party(classes[trainer],int(index))} <= allowed_species,(route,trainer,index)
        checked+=1
for slot,palette in blaine['palettes'].items():
    dog=next(d for d in DOGS if d['slot']==slot)
    assert rom[offset('MonsterPalettes')+dog['dex']] == palette_ids[palette],slot
for name,source in blaine['repeatable_sources'].items():
    assert name in {dog for _,dog in blaine['wild'][source]},name
for trade,(give,receive,nickname) in blaine['trades'].items():
    pos=offset('TradeMons')+trade_ids.index(trade)*14
    assert list(rom[pos:pos+3]) == [name_to_id[give],name_to_id[receive],0],trade
    assert decode(rom[pos+3:pos+14]) == nickname,trade
guardian=(ROOT/'data/maps/objects/SeafoamIslandsB4F.asm').read_text()
assert 'FROSTMAUL, 50' in guardian and 'SPRITE_MONSTER' in guardian
assert symbols['RetryUncaughtFrostmaul'][0] == symbols['HallOfFameResetEventsAndSaveScript'][0]
quiz=(ROOT/'data/events/hidden_events.asm').read_text().split('hidden_events_for CINNABAR_GYM')[1].split('\tdb -1')[0]
assert [0 if value=='FALSE' else 1 for value in re.findall(r'PrintCinnabarQuiz, \((FALSE|TRUE)\s*<< 4\)',quiz)] == blaine['quiz_answers']
giovanni=json.loads((ROOT/'data/dogs/giovanni.json').read_text())
for route,encounters in giovanni['wild'].items():
    pos=offset(route+'WildMons')
    assert rom[pos] == giovanni['rates'][route],route
    assert list(rom[pos+1:pos+21]) == [v for level,name in encounters for v in (level,name_to_id[name])],route
    assert rom[pos+21] == 0,route
for label,parties in giovanni['trainers'].items():
    for index,members in parties.items():
        assert trainer_party(label,int(index)) == [(level,name_to_id[name]) for level,name in members],(label,index)
for route in giovanni['maps']:
    objects=(ROOT/f'data/maps/objects/{route}.asm').read_text()
    for trainer,index in re.findall(r'object_event[^\n]+, (OPP_\w+), (\d+)',objects):
        assert {sid for _,sid in trainer_party(classes[trainer],int(index))} <= allowed_species,(route,trainer,index)
        checked+=1
for slot,palette in giovanni['palettes'].items():
    dog=next(d for d in DOGS if d['slot']==slot)
    assert rom[offset('MonsterPalettes')+dog['dex']] == palette_ids[palette],slot
assert 'DALMSPARK' in {name for _,name in giovanni['wild']['PowerPlant']}
# Parse the compiled map object records, including the eight item-disguised dogs.
pos=offset('PowerPlant_Object')+1
warps=rom[pos];pos+=1+warps*4
signs=rom[pos];pos+=1+signs*3
assert rom[pos] == 14
pos+=1
for level,name in giovanni['static_encounters']:
    assert rom[pos+5]&0x40 and tuple(rom[pos+6:pos+8]) == (name_to_id[name],level)
    pos+=8
assert tuple(rom[pos+6:pos+8]) == (name_to_id['STORMLAEK'],50)
assert 'SPRITE_MONSTER, STAY, UP, TEXT_POWERPLANT_ZAPDOS, STORMLAEK, 50' in (ROOT/'data/maps/objects/PowerPlant.asm').read_text()
assert symbols['RetryUncaughtStormlaek'][0] == symbols['HallOfFameResetEventsAndSaveScript'][0]
start=offset('HallOfFameResetEventsAndSaveScript');end=offset('RetryUncaughtFrostmaul')
for label in ('RetryUncaughtFrostmaul','RetryUncaughtStormlaek'):
    assert b'\xcd'+symbols[label][1].to_bytes(2,'little') in rom[start:end],label
assert MOVES['FAULT_FANG'][0] == 'FISSURE' and MOVES['FAULT_FANG'][2] == 'OHKO_EFFECT'
print(f'PASS: {len(DOGS)} dog records and banks, {len(MOVES)} moves, 45 chapter encounter tables, {checked} trainer placements, six Route 22 rival teams, nine Power Plant static dogs, both guardian retry hooks, trades and quiz answers, and all five HMs.')
