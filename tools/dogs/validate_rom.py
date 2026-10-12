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
    assert record[2] == power and record[4] == accuracy*255//100 and record[5] == pp, (slot,record)

for dog in DOGS:
    sid=species_ids[dog['slot']]
    name=decode(rom[offset('MonsterNames')+(sid-1)*10:][:10])
    assert name == dog['name'] and len(name) <= 10, (sid,name,dog['name'])
    dex=rom[offset('PokedexOrder')+sid-1]
    record=rom[offset('BaseStats')+(dex-1)*28:][:28]
    assert tuple(record[1:6]) == dog['stats'], (name,record[1:6])
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
    assert len(learned) == len(dog['learnset']), (name,learned)
    for view,size in [('front',(56,56)),('back',(32,32))]:
        im=Image.open(ROOT/f'gfx/pokemon/{view}'/(dog['slot'].lower()+('b' if view == 'back' else '')+'.png')).convert('L')
        assert im.size == size, (name,view,im.size)
        assert set(im.tobytes()) <= {0,85,170,255}, (name,view)

assert rom[0x134:0x13f] == b'POKEMON RED\x00', 'Unexpected cartridge title'
print(f'PASS: {len(DOGS)} compiled dog records, evolutions, name-table alignment, {len(MOVES)} move records, and sprite encoding.')
