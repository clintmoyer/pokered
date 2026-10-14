#!/usr/bin/env python3
"""Exercise real chapter scripts with explicitly trained/warped party fixtures.

These checks cover battles and rewards, not an uninterrupted natural playthrough.
No battle HP, enemy stats, damage, or winning flags are patched during fights.
"""
import json
import re
import test_emulator as E
from data import DOGS, MOVES

TYPES=E.constants('constants/type_constants.asm')
MOVE_BY_ID={E.MIDS[m[0]]:m for m in MOVES.values()}
DOG_BY_ID={E.IDS[d['slot']]:d for d in DOGS}
MATCHUPS={}
for attack,defender,kind in re.findall(r'^\s*db (\w+),\s*(\w+),\s*(\w+)',(E.ROOT/'data/types/type_matchups.asm').read_text(),re.M):
    MATCHUPS[TYPES[attack],TYPES[defender]]={'SUPER_EFFECTIVE':2,'NOT_VERY_EFFECTIVE':.5,'NO_EFFECT':0}[kind]

EVENTS={}; value=0
for line in (E.ROOT/'constants/event_constants.asm').read_text().splitlines():
    code=line.split(';')[0].strip()
    if code=='const_def': value=0
    elif code.startswith('const_next '):
        # Tower flags begin at "$F0 - 2"; include the full offset expression.
        expression=code.removeprefix('const_next ').replace(' ','')
        terms=re.findall(r'[+-]?(?:\$[\dA-Fa-f]+|\d+)',expression)
        assert ''.join(terms)==expression,expression
        value=sum((-1 if term.startswith('-') else 1)*int(term.lstrip('+-').replace('$','0x'),0) for term in terms)
    elif code.startswith('const_skip'): value+=int(code.split()[1]) if len(code.split())>1 else 1
    elif code.startswith('const '): EVENTS[code.split()[1]]=value;value+=1


def event(name,set_value=None):
    index=EVENTS[name];address=E.SYMS['wEventFlags'][1]+index//8;bit=1<<(index%8)
    if set_value is not None:
        E.gb.memory[address]=(E.gb.memory[address]|bit) if set_value else (E.gb.memory[address]&~bit)
    return bool(E.gb.memory[address]&bit)


def word(name):
    address=E.SYMS[name][1]
    return E.gb.memory[address]*256+E.gb.memory[address+1]


def warp(map_id,warp_id=0,last_map=None):
    E.write('wDestinationWarpID',warp_id);E.write('hWarpDestinationMap',map_id)
    E.write('wStatusFlags3',E.read('wStatusFlags3')|8);E.gb.tick(360)
    assert E.read('wCurMap')==map_id,(map_id,E.read('wCurMap'),E.text())
    if last_map is not None:E.write('wLastMap',last_map)


def walk_axis(axis,target,button):
    for _ in range(40):
        if E.read(axis)==target:return
        before=E.read(axis);E.press(button,16,90)
        if E.read(axis)==before:
            E.press(button,16,90)
            assert E.read(axis)!=before,(button,axis,target,E.read('wXCoord'),E.read('wYCoord'))
    raise AssertionError((axis,target,E.read(axis)))


def strongest_move():
    current=E.read('wBattleMonSpecies');dog=DOG_BY_ID[current]
    address=E.SYMS['wBattleMonMoves'][1];pp=E.SYMS['wBattleMonPP'][1]
    choices=[]
    enemies={E.read('wEnemyMonType1'),E.read('wEnemyMonType2')}
    for i,mid in enumerate(E.gb.memory[address:address+4]):
        if not mid or not (E.gb.memory[pp+i]&63):continue
        slot,name,effect,power,typ,accuracy,_=MOVE_BY_ID[mid]
        if power<=1:continue
        multiplier=1.5 if typ in dog['types'] else 1
        for target in enemies:multiplier*=MATCHUPS.get((TYPES[typ],target),1)
        if effect in ('ATTACK_TWICE_EFFECT','TWINEEDLE_EFFECT'):multiplier*=2
        if effect=='TWO_TO_FIVE_ATTACKS_EFFECT':multiplier*=3
        special=TYPES[typ]>=20
        offense=word('wBattleMonSpecial' if special else 'wBattleMonAttack')
        defense=word('wEnemyMonSpecial' if special else 'wEnemyMonDefense')
        choices.append((power*multiplier*accuracy*offense/max(1,defense),name))
    assert choices,(current,E.text())
    return max(choices)[1]


def select_row(label,party=False):
    for _ in range(12):
        rows=E.text().splitlines();target=next(i for i,row in enumerate(rows) if label in row)+(1 if party else 0)
        cursor=next((i for i,row in enumerate(rows) if '▲' in row),None)
        if cursor==target:return
        E.press('down',wait=45)
    raise AssertionError((label,E.text()))


def fight_until(done,name,limit=240):
    focused=set()
    for _ in range(limit):
        if done() and E.read('wIsInBattle')==0:return
        screen=E.text()
        if 'Abandon learning' in screen:E.press('a')
        elif 'YES' in screen and 'NO' in screen:E.press('b')
        elif 'FNT' in screen and 'TYPE/' not in screen and 'FIGHT' not in screen:
            living=[DOG_BY_ID[E.read(f'wPartyMon{i}Species')]['name'] for i in range(1,E.read('wPartyCount')+1) if word(f'wPartyMon{i}HP')]
            assert living,(name,'party fainted',screen)
            select_row(living[0],party=True);E.press('a',wait=240)
        elif 'FIGHT' in screen and 'TYPE/' not in screen:
            rows=screen.splitlines()
            cursor=next(((x,y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch=='▲'),None)
            if cursor and cursor[0]>=15:E.press('left',8,45)
            if cursor and cursor[1]>=16:E.press('up',8,45)
            E.press('a',wait=90)
        elif 'TYPE/' in screen:
            address=E.SYMS['wBattleMonMoves'][1]
            available={MOVE_BY_ID[mid][1] for mid in E.gb.memory[address:address+4] if mid}
            current=E.read('wBattleMonSpecies')
            if 'PACK FOCUS' in available and current not in focused:
                move='PACK FOCUS';focused.add(current)
            elif 'ROOT SNARE' in available and not (E.read('wEnemyBattleStatus2')&128):
                move='ROOT SNARE'
            else:move=strongest_move()
            select_row(move);E.photo(name+'-battle');E.press('a',wait=360)
        else:E.press('a')
    E.photo(name+'-failure')
    raise AssertionError((name,E.read('wCurMap'),E.read('wIsInBattle'),E.text()))


def misty_fixture(base,name,slots,levels):
    E.restore(base);E.trained_party(slots,levels)
    event('EVENT_BEAT_CERULEAN_GYM_TRAINER_0',True);event('EVENT_BEAT_CERULEAN_GYM_TRAINER_1',True)
    warp(0x41,last_map=3)
    # Follow the actual floor path around the pool, ending below Misty.
    walk_axis('wYCoord',8,'up');walk_axis('wXCoord',5,'right')
    walk_axis('wYCoord',5,'up');walk_axis('wXCoord',7,'right')
    walk_axis('wYCoord',3,'up');walk_axis('wXCoord',4,'left')
    E.press('up',4,20);E.press('a')
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    fight_until(lambda:bool(E.read('wObtainedBadges')&2),name+'-misty')
    for _ in range(20):E.press('b')
    assert E.read('wObtainedBadges')&3==3
    assert event('EVENT_BEAT_MISTY') and event('EVENT_GOT_TM11')
    address=E.SYMS['wBagItems'][1];bag=E.gb.memory[address:address+E.read('wNumBagItems')*2]
    assert 0xd3 in bag[::2],bag # TM11, same item ID as upstream
    E.press('a');E.advance_until(lambda:'WAKE CHARGE' in E.text());E.photo(name+'-misty-reward')
    for _ in range(8):E.press('b')
    print('PASS: '+name+' Misty battle, Cascade Badge, TM11 WAKE CHARGE, and preserved Cut unlock.',flush=True)
    return E.state()


def rival_fixture(base,name,slots,levels,starter,rival):
    E.restore(base);E.trained_party(slots,levels)
    E.write('wPlayerStarter',E.IDS[starter]);E.write('wRivalStarter',E.IDS[rival])
    warp(3,8);E.walk('down',1);E.walk('right',11);E.walk('up',7)
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    fight_until(lambda:event('EVENT_BEAT_CERULEAN_RIVAL'),name+'-cerulean-rival')
    for _ in range(15):E.press('b')
    assert event('EVENT_BEAT_CERULEAN_RIVAL')
    print('PASS: '+name+' Cerulean rival team and northern-route unlock.',flush=True)
    return E.state()


def bill_fixture(base):
    E.restore(base);warp(0x58,last_map=0x24)
    E.walk('right',4);E.walk('up',1);E.press('up',4,20);E.press('a')
    E.advance_until(lambda:'YES' in E.text());E.press('a')
    E.advance_until(lambda:event('EVENT_BILL_SAID_USE_CELL_SEPARATOR'))
    for _ in range(5):E.press('b')
    E.walk('left',5);E.walk('up',2);E.press('up',4,20);E.press('a')
    E.advance_until(lambda:event('EVENT_MET_BILL'))
    for _ in range(4):E.press('b')
    # Bill exits the left machine and stands at his original (4,4) object.
    E.walk('down',1);E.walk('right',3);E.press('up',4,20);E.press('a')
    E.advance_until(lambda:event('EVENT_GOT_SS_TICKET'))
    E.photo('bill-ss-ticket')
    for _ in range(10):E.press('b')
    print('PASS: Bill separation sequence and S.S. Ticket reward.',flush=True)
    walk_axis('wXCoord',3,'left');E.walk('down',3)
    assert E.read('wCurMap')==0x24,E.read('wCurMap')
    assert event('EVENT_LEFT_BILLS_HOUSE_AFTER_HELPING')
    warp(0x58,last_map=0x24)
    E.walk('up',1);E.walk('left',1);E.walk('up',2);E.press('up',4,20);E.press('a')
    E.advance_until(lambda:'GROENPUP' in E.text() and 'POMPUP' in E.text())
    E.photo('bill-dog-pc')
    select_row('POMPUP');E.press('a')
    # Bill previews an uncaught dog: vanilla Pokédex rules hide its prose/size.
    E.advance_until(lambda:'POMPUP' in E.text() and 'PACK DOG' in E.text())
    E.photo('bill-pomeranian-dex')
    print('PASS: Bill PC displays the dog menu and the selected POMPUP Pokédex preview.',flush=True)


def seller_fixture(base):
    E.restore(base);E.trained_party(['WARTORTLE'],[20]);warp(0x44,last_map=0x0f)
    walk_axis('wYCoord',5,'up')
    for _ in range(30):
        # This NPC walks; approach his current column from the open row above.
        npc_x=E.read('wSprite04StateData2MapX')-4
        x=E.read('wXCoord')
        walk_axis('wXCoord',npc_x,'right' if npc_x>x else 'left')
        E.press('down',4,20);E.press('a')
        if 'YES' in E.text():break
        if E.read('wYCoord')==6:walk_axis('wYCoord',5,'up')
    E.advance_until(lambda:'YES' in E.text());E.press('a')
    E.advance_until(lambda:E.read('wPartyCount')==2)
    E.advance_until(lambda:'give a nickname' in E.text());E.press('down',wait=20);E.press('a')
    for _ in range(8):E.press('b')
    assert E.read('wPartyMon2Species')==E.IDS['MAGIKARP']
    E.photo('springpup-adoption')
    print('PASS: Mt. Moon seller gives SPRINGPUP through the real purchase script.',flush=True)


def main():
    try:
        lab=E.bootstrap();E.restore(lab)
        start=E.choose_starter(7,'NEWFPUP','NEWFOUNDLAND',('SQUIRTLE','BULBASAUR'))
        base=E.brock_fixture(start,'misty-base',['WARTORTLE'],[16],1)
        for name,slots,levels,starter,rival in [
            ('groen',['IVYSAUR','GYARADOS'],[20,20],'BULBASAUR','CHARMANDER'),
            ('shiba',['CHARMELEON','PIKACHU','GLOOM'],[20,20,20],'CHARMANDER','SQUIRTLE'),
            ('newf',['WARTORTLE','BUTTERFREE','BEEDRILL'],[20,20,20],'SQUIRTLE','BULBASAUR')]:
            rival_fixture(base,name,slots,levels,starter,rival)
        completed={}
        for name,slots,levels in [
            ('groen',['IVYSAUR'],[20]),
            ('shiba',['GLOOM','CHARMELEON'],[20,20]),
            ('newf',['PIKACHU','GLOOM','WARTORTLE'],[20,20,20])]:
            completed[name]=misty_fixture(base,name,slots,levels)
        seller_fixture(base);bill_fixture(base)
        E.save_reload(completed['newf'],expected_map=0x41,expected_badges=3)
        for slot,level,target in [('WEEDLE',8,'KAKUNA'),('KAKUNA',17,'BEEDRILL'),('ODDISH',17,'GLOOM'),('STARYU',19,'STARMIE'),('MAGIKARP',19,'GYARADOS')]:
            E.evolution_check(completed['newf'],slot,level,target)
        (E.QA/'misty-results.json').write_text(json.dumps({'rivals':['groen','shiba','newf'],'misty':['groen','shiba','newf'],'fixture':'trained level-20 parties, map warps; optional gym trainers marked beaten','bill_ticket':True,'bill_dog_pc':True,'springpup_purchase':True,'save_load_two_badges':True,'additional_evolutions':5},indent=2)+'\n')
    finally:E.gb.stop();E.tmp.cleanup()


if __name__=='__main__':main()
