#!/usr/bin/env python3
"""Replay starter selection and rival fights, then exercise Brock with level-16 fixtures.

The Brock fixture uses a scripted warp and a trained party, avoiding hours of grinding.
It does not bypass the battle, badge script, TM reward, or actual save/load routines.
"""
from pathlib import Path
import io,json,re,shutil,sys,tempfile
from pyboy import PyBoy
from PIL import Image
from data import DOGS,MOVES

ROOT=Path(__file__).resolve().parents[2]
QA=ROOT/'build/qa'; QA.mkdir(parents=True,exist_ok=True)
SYMS={}
for line in (ROOT/'pokered.sym').read_text().splitlines():
    m=re.match(r'([\da-fA-F]+):([\da-fA-F]+) (\S+)',line)
    if m: SYMS[m[3]]=(int(m[1],16),int(m[2],16))
CHARS={}
for c,v in re.findall(r'^\s*charmap "([^"\n]+)",\s*\$([\da-fA-F]+)',(ROOT/'constants/charmap.asm').read_text(),re.M):
    CHARS.setdefault(int(v,16),c)
def constants(path):
    return {k:int(v,16) for k,v in re.findall(r'^\s*const (\w+)\s*; \$?([\da-fA-F]{2})\b',(ROOT/path).read_text(),re.M)}
IDS=constants('constants/pokemon_constants.asm'); MIDS=constants('constants/move_constants.asm')
ROM=(ROOT/'pokered.gbc').read_bytes()
def rom_offset(label):
    bank,address=SYMS[label]; return bank*0x4000+address%0x4000 if bank else address

tmp=tempfile.TemporaryDirectory(prefix='pokedogs-test-')
rom_path=Path(tmp.name)/'demo.gb'; shutil.copyfile(ROOT/'pokered.gbc',rom_path)
gb=PyBoy(str(rom_path),window='null',sound_emulated=False); gb.set_emulation_speed(0)
def read(name): return gb.memory[SYMS[name][1]]
def write(name,value):
    addr=SYMS[name][1]
    if isinstance(value,(list,bytes,bytearray)): gb.memory[addr:addr+len(value)]=list(value)
    else: gb.memory[addr]=value
def text():
    addr=SYMS['wTileMap'][1]
    return '\n'.join(''.join(CHARS.get(gb.memory[addr+y*20+x],' ') for x in range(20)) for y in range(18))
def press(button,hold=8,wait=180):
    gb.button_press(button); gb.tick(hold); gb.button_release(button); gb.tick(wait)
def advance_until(predicate,limit=120):
    for _ in range(limit):
        if predicate(): return
        press('a')
    photo('failure')
    raise AssertionError(f"Timed out at map {read('wCurMap')}, ({read('wXCoord')}, {read('wYCoord')}): "+text())
def photo(name):
    gb.tick(1); gb.screen.image.resize((640,576),Image.Resampling.NEAREST).save(QA/(name+'.png'))
def state():
    f=io.BytesIO(); gb.save_state(f); return f.getvalue()
def restore(value): gb.load_state(io.BytesIO(value))
def walk(button,steps): press(button,steps*16,180)

def bootstrap():
    gb.tick(2000); press('start',wait=330)
    assert 'NEW GAME' in text(), text()
    press('a'); write('wOptions',1)
    advance_until(lambda:'NEW NAME' in text()); press('down',wait=20); press('a')
    advance_until(lambda:'NEW NAME' in text()); press('down',wait=20); press('a')
    advance_until(lambda:read('wCurMap')==38 and gb.memory[SYMS['wTileMap'][1]]==0x10)
    walk('right',2); walk('up',5); walk('right',2)
    assert read('wCurMap')==37, (read('wCurMap'),read('wXCoord'),read('wYCoord'))
    walk('down',5); walk('left',4); walk('down',2)
    assert read('wCurMap')==0, (read('wCurMap'),read('wXCoord'),read('wYCoord'))
    walk('right',5); walk('up',5)
    advance_until(lambda:read('wCurMap')==40 and read('wOaksLabCurScript')==6 and read('wJoyIgnore')==0)
    return state()

def choose_starter(x,name,breed,expected_rival):
    walk('down',1); walk('right',x-5); press('up',4,20); press('a',wait=240)
    assert name in text() and breed+'.' in text(), text()
    photo(name.lower()+'-pokedex')
    advance_until(lambda:'YES' in text() and name+'?' in text())
    press('a')
    advance_until(lambda:'give a nickname' in text())
    press('down',wait=20); press('a')
    advance_until(lambda:read('wOaksLabCurScript')==10 and read('wJoyIgnore')==0)
    assert read('wPartyCount')==1 and read('wPlayerStarter')==IDS[expected_rival[0]]
    assert read('wRivalStarter')==IDS[expected_rival[1]]
    walk('down',1); walk('left',x-5); walk('down',1)
    advance_until(lambda:read('wIsInBattle')==2)
    for _ in range(110):
        if read('wIsInBattle')==0 and read('wOaksLabCurScript')==18 and read('wJoyIgnore')==0: break
        press('a',wait=240)
        if 'FIGHT' in text(): photo(name.lower()+'-rival')
    else: raise AssertionError('Rival battle did not finish: '+text())
    print('PASS: '+name+' selection, full breed Pokédex, rival typing, and tutorial battle.',flush=True)
    return state()

def trained_party(slots,levels):
    write('wPartyCount',len(slots)); write('wPartySpecies',[IDS[s] for s in slots]+[255])
    for n,(slot,level) in enumerate(zip(slots,levels),1):
        dog=next(d for d in DOGS if d['slot']==slot); sid=IDS[slot]
        dex=ROM[rom_offset('PokedexOrder')+sid-1]
        header=ROM[rom_offset('BaseStats')+(dex-1)*28:][:28]
        # Fixed DV=8 in every non-HP stat; the derived HP DV is zero.
        stats=[dog['stats'][0]*2*level//100+level+10]+[(v+8)*2*level//100+5 for v in dog['stats'][1:]]
        learned=list(dog['base'])+[m for l,m in dog['learnset'] if l<=level]
        learned=learned[-4:]; move_ids=[MIDS[MOVES[m][0]] for m in learned]
        exp=max(0,6*level**3//5-15*level**2+100*level-140)
        values=bytearray(44)
        values[0]=sid; values[1:3]=stats[0].to_bytes(2,'big'); values[3]=level
        values[5:7]=header[6:8]; values[7]=dog['catch']
        values[8:8+len(move_ids)]=bytes(move_ids); values[14:17]=exp.to_bytes(3,'big')
        values[12:14]=bytes(gb.memory[SYMS['wPlayerID'][1]:SYMS['wPlayerID'][1]+2])
        values[27:29]=b'\x88\x88'; values[29:29+len(learned)]=bytes(MOVES[m][6] for m in learned)
        values[33]=level
        for i,v in enumerate(stats): values[34+i*2:36+i*2]=v.to_bytes(2,'big')
        write(f'wPartyMon{n}',values)
        nick=ROM[rom_offset('MonsterNames')+(sid-1)*10:][:10]+b'\x50'
        write(f'wPartyMon{n}Nick',nick)
    # Standard shop items for battle recovery and later capture checks.
    write('wNumBagItems',2); write('wBagItems',[0x14,5,0x04,5,255])

def brock_fixture(start,name,slots,levels,attack_index):
    restore(start); trained_party(slots,levels)
    write('wDestinationWarpID',0); write('hWarpDestinationMap',0x36)
    write('wStatusFlags3',read('wStatusFlags3')|8)
    # Mark the gym's junior trainer beaten so this fixture isolates Brock.
    addr=SYMS['wEventFlags'][1]+0x72//8; gb.memory[addr] |= 1 << (0x72%8)
    gb.tick(360)
    assert read('wCurMap')==0x36, (name,read('wCurMap'),text())
    write('wLastMap',2) # Pewter City is the gym's normal outdoor return map.
    photo(name+'-gym-entry')
    # Spawn at the door and follow the clear central aisle to Brock.
    walk('up',11); press('up',4,20); press('a')
    photo(name+'-gym-approach')
    advance_until(lambda:read('wIsInBattle')==2)
    lead=next(d for d in DOGS if d['slot']==slots[0])
    learned=(list(lead['base'])+[m for l,m in lead['learnset'] if l<=levels[0]])[-4:]
    attack_name=MOVES[learned[attack_index]][1]
    for _ in range(180):
        if read('wObtainedBadges')&1 and read('wIsInBattle')==0: break
        screen=text()
        if 'Abandon learning' in screen:
            press('a')
        elif 'YES' in screen and 'NO' in screen:
            press('b') # Keep the current lead when Brock sends his second dog.
        elif 'FNT' in screen and 'SHIBA' in screen and 'TYPE/' not in screen:
            if not any(('\u25b2' in row or '\u25b7' in row) and 'SHIBA' in row for row in screen.splitlines()):
                press('down',wait=30)
            press('a',wait=240)
        elif 'FIGHT' in screen and 'TYPE/' not in screen:
            press('a',wait=90)
        elif 'TYPE/' in screen:
            for _ in range(8):
                rows=text().splitlines()
                target=next(i for i,row in enumerate(rows) if attack_name in row)
                cursor=next((i for i,row in enumerate(rows) if '\u25b2' in row),None)
                if cursor==target: break
                press('down',wait=60)
            assert cursor==target, (attack_name,text())
            photo(name+'-brock-battle')
            press('a',wait=360)
        else: press('a',wait=180)
    else: raise AssertionError('Brock failed: '+name+' '+text())
    # Finish the TM explanation and capture the completed gym.
    for _ in range(18): press('b')
    assert read('wObtainedBadges')&1
    event=gb.memory[SYMS['wEventFlags'][1]+0x76//8]
    assert event&(1<<(0x76%8)) and event&(1<<(0x77%8)), event
    bag=gb.memory[SYMS['wBagItems'][1]:SYMS['wBagItems'][1]+read('wNumBagItems')*2]
    assert 0xEA in bag[::2], bag # TM34
    photo(name+'-badge')
    print('PASS: '+name+' Brock battle, Boulder Badge, and TM34 GUARD HOWL.',flush=True)
    return state()

def start_option(label):
    press('start',wait=90)
    for _ in range(12):
        rows=text().splitlines()
        target=next(i for i,row in enumerate(rows) if label in row)
        cursor=next((i for i,row in enumerate(rows) if '\u25b2' in row),None)
        if cursor==target: break
        press('down',wait=40)
    else: raise AssertionError('Start menu selection failed: '+text())
    press('a')

def save_reload(value,expected_map=0x36,expected_badges=1):
    global gb
    restore(value)
    start_option('SAVE')
    advance_until(lambda:'YES' in text())
    press('a',wait=600)
    assert read('wSaveFileStatus')==2, (read('wSaveFileStatus'),text())
    photo('saved-game')
    gb.stop()
    gb=PyBoy(str(rom_path),window='null',sound_emulated=False); gb.set_emulation_speed(0)
    gb.tick(2000); press('start',wait=330)
    assert 'CONTINUE' in text(), text()
    press('a',wait=600)
    assert read('wCurMap')==expected_map and read('wObtainedBadges')&expected_badges==expected_badges
    photo('saved-continue')
    print('PASS: in-game save and fresh-emulator Continue preserve the badge and gym location.',flush=True)

def evolution_check(value,slot,level,target):
    restore(value); trained_party([slot],[level])
    write('wNumBagItems',1); write('wBagItems',[0x28,1,255])
    start_option('ITEM')
    press('a'); press('a'); press('a')
    advance_until(lambda:read('wPartyMon1Species')==IDS[target],limit=100)
    for _ in range(8): press('b')
    addr=SYMS['wPartyMon1Nick'][1]
    nickname=''.join(CHARS.get(b,'?') for b in gb.memory[addr:addr+11] if b!=0x50)
    expected=next(d['name'] for d in DOGS if d['slot']==target)
    assert nickname==expected, (nickname,expected)
    photo(expected.lower()+'-evolution')
    print(f'PASS: {slot} evolves into {target} at level {level+1}, with its new default name.',flush=True)

def main():
    try:
        if '--brock-only' in sys.argv:
            starts={name:(QA/(name.lower()+'-after-rival.state')).read_bytes() for name in ['GROENPUP','SHIBAPUP','NEWFPUP']}
        elif '--from-snapshot' in sys.argv:
            lab=(QA/'lab-choice.state').read_bytes()
        else: lab=bootstrap()
        if '--brock-only' not in sys.argv:
            starts={}
            for x,name,breed,pair in [(8,'GROENPUP','GROENENDAEL',('BULBASAUR','CHARMANDER')),(6,'SHIBAPUP','SHIBA INU',('CHARMANDER','SQUIRTLE')),(7,'NEWFPUP','NEWFOUNDLAND',('SQUIRTLE','BULBASAUR'))]:
                restore(lab); starts[name]=choose_starter(x,name,breed,pair)
                (QA/(name.lower()+'-after-rival.state')).write_bytes(starts[name])
        completed={}
        for name,slots,levels,index in [('groen',['IVYSAUR'],[16],1),('shiba',['MANKEY','CHARMELEON'],[14,16],2),('newf',['WARTORTLE'],[16],1)]:
            completed[name]=brock_fixture(starts[{'groen':'GROENPUP','shiba':'SHIBAPUP','newf':'NEWFPUP'}[name]],name,slots,levels,index)
        save_reload(completed['newf'])
        for slot,level,target in [('BULBASAUR',15,'IVYSAUR'),('IVYSAUR',35,'VENUSAUR'),('CHARMANDER',15,'CHARMELEON'),('CHARMELEON',35,'CHARIZARD'),('SQUIRTLE',15,'WARTORTLE'),('WARTORTLE',35,'BLASTOISE')]:
            evolution_check(completed['newf'],slot,level,target)
        (QA/'emulator-results.json').write_text(json.dumps({'starters':list(starts),'brock':['groen','shiba','newf'],'brock_fixture':'trained level-16 adolescent starter; Shiba supported by level-14 Boxer','save_load':True,'starter_evolutions':6},indent=2)+'\n')
    finally:
        gb.stop(); tmp.cleanup()

if __name__ == "__main__":
    main()
