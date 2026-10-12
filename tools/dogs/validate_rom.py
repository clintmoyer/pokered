#!/usr/bin/env python3
"""Check compiled dog data and sprite constraints, including ID alignment."""
from pathlib import Path
import re
from PIL import Image
from data import DOGS, MOVES

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
    front= symbols[dog['slot'].capitalize()+'PicFront']
    back= symbols[dog['slot'].capitalize()+'PicBack']
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
    assert rom[position] == 0, name
    position += 1
    learned=[]
    while rom[position]:
        level,move=rom[position:position+2]
        assert move in [move_ids[value[0]] for value in MOVES.values()], (name,level,move)
        learned.append((level,move)); position+=2
    assert learned == [(level,move_ids[MOVES[move][0]]) for level,move in dog['learnset']], (name,learned)
    for view,size in [('front',(56,56)),('back',(32,32))]:
        im=Image.open(ROOT/f'gfx/pokemon/{view}'/(dog['slot'].lower()+('b' if view == 'back' else '')+'.png')).convert('L')
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
    assert bank_table[species_ids[dog['slot']]] == symbols[dog['slot'].capitalize()+'PicFront'][0]

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
print(f'PASS: {len(DOGS)} dog records and banks, {len(MOVES)} complete move records, seven Misty encounter tables, {checked} chapter trainer parties, all starter catches, and sprite encoding.')
