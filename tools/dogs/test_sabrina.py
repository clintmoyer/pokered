#!/usr/bin/env python3
"""Replay Saffron's gates, Dojo, Silph rescue, warp maze and Sabrina.

Requires test_erika.py and test_koga.py checkpoints for this exact ROM. Parties,
money, inventory room and floor-entry warps are fixtures; optional trainers are
marked beaten.
Quest gates, purchases, gifts, mandatory battles, doors, warp pads and save/load
use ordinary game inputs, without patching battle HP, RNG or victory flags.
"""
from collections import deque
import hashlib
import json
import re
import sys
import test_koga as K
from test_koga import E, M, S, A, ITEMS, mid, talk, beaten

def guards_fixture(base):
    E.restore(base)
    assert not E.read('wStatusFlags1')&64
    M.warp(mid('ROUTE_7_GATE'),0,last_map=mid('ROUTE_7'))
    A.navigate('Route7Gate',(2,3));E.walk('right',1)
    E.advance_until(lambda:'thirsty' in E.text());S.close_text()
    assert not E.read('wStatusFlags1')&64 and E.read('wXCoord')==2
    E.write('wPlayerMoney',[5,0,0]);M.warp(mid('CELADON_MART_ROOF'),0)
    talk('CeladonMartRoof',(10,2),'up');E.advance_until(lambda:'FRESH WATER' in E.text());E.press('a')
    E.advance_until(lambda:S.has_item(ITEMS['FRESH_WATER']));S.close_text()
    M.warp(mid('ROUTE_7_GATE'),0,last_map=mid('ROUTE_7'))
    A.navigate('Route7Gate',(2,3));E.walk('right',1)
    E.advance_until(lambda:bool(E.read('wStatusFlags1')&64));S.close_text()
    assert not S.has_item(ITEMS['FRESH_WATER'])
    A.navigate('Route7Gate',(5,3),stop_on_warp=True)
    if E.read('wCurMap')==mid('ROUTE_7_GATE'):E.press('right',8,180)
    assert E.read('wCurMap')==mid('ROUTE_7')
    A.navigate('Route7',(19,10));E.press('right',8,180)
    assert E.read('wCurMap')==mid('SAFFRON_CITY')
    A.navigate('SaffronCity',(35,4));E.press('left',8,45)
    assert E.read('wCurMap')==mid('SAFFRON_CITY') and E.read('wXCoord')==35
    E.photo('sabrina-city-gym-blocked')
    print('PASS: the guards reject passage, accept a purchased drink, and share access; Rockets block the gym.',flush=True)
    return E.state()

def psychic_fixture(base):
    E.restore(base);M.warp(mid('MR_PSYCHICS_HOUSE'),0,last_map=mid('SAFFRON_CITY'))
    talk('MrPsychicsHouse',(5,4),'up')
    E.advance_until(lambda:M.event('EVENT_GOT_TM29'));S.close_text()
    assert S.has_item(ITEMS['TM29'])
    E.press('up',4,20);E.press('a');E.advance_until(lambda:'MIND HOWL' in E.text());S.close_text()
    print('PASS: Mr. Psychic gives TM29 MIND HOWL once.',flush=True)
    return E.state()

def dojo_fixture(base):
    E.restore(base);S.train(['HYPNO','BLASTOISE'],[40,40])
    beaten('EVENT_BEAT_FIGHTING_DOJO_TRAINER_',4)
    M.warp(mid('FIGHTING_DOJO'),0,last_map=mid('SAFFRON_CITY'))
    talk('FightingDojo',(5,4),'up');E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:M.event('EVENT_BEAT_KARATE_MASTER') and E.read('wFightingDojoCurScript')==0,'sabrina-dojo-master');S.close_text()
    mastered=E.state()
    for slot,position,direction,event in [('HITMONLEE',(4,2),'up','EVENT_GOT_HITMONLEE'),('HITMONCHAN',(5,2),'up','EVENT_GOT_HITMONCHAN')]:
        E.restore(mastered);talk('FightingDojo',position,direction)
        E.advance_until(lambda:'YES' in E.text());E.press('a')
        E.advance_until(lambda:'give a nickname' in E.text());E.press('down',8,45);E.press('a')
        E.advance_until(lambda:M.event(event));S.close_text()
        assert E.read('wPartyCount')==3 and E.read('wPartyMon3Species')==E.IDS[slot] and E.read('wPartyMon3Level')==30
        other=(5,2) if slot=='HITMONLEE' else (4,2)
        talk('FightingDojo',other,'up')
        E.advance_until(lambda:'greedy' in E.text());S.close_text()
        assert E.read('wPartyCount')==3
        E.photo('sabrina-dojo-'+slot.lower())
    print('PASS: the Dojo master unlocks both gift choices; each branch gives its dog and enforces one gift.',flush=True)
    return mastered

def elevator(floor):
    # Enter this room through its real elevator door before calling.
    talk('SilphCoElevator',(3,1),'up');E.advance_until(lambda:'1F' in E.text())
    target=floor-1
    for _ in range(20):
        current=E.read('wCurrentMenuItem')+E.read('wListScrollOffset')
        if current==target:break
        E.press('down' if current<target else 'up',8,45)
    else:raise AssertionError(('Silph floor selection',floor,E.text()))
    E.press('a');S.close_text();A.navigate('SilphCoElevator',(1,3),stop_on_warp=True)
    if E.read('wCurMap')==mid('SILPH_CO_ELEVATOR'):E.press('down',8,180)
    assert E.read('wCurMap')==mid(f'SILPH_CO_{floor}F')

def card_fixture(base):
    E.restore(base);S.train(['HYPNO','DUGTRIO','BLASTOISE','RAICHU'],[42]*4)
    # Fuji's rescue already removed the guard at Silph's front door.
    assert M.event('EVENT_RESCUED_MR_FUJI')
    M.warp(mid('MR_PSYCHICS_HOUSE'),0,last_map=mid('SAFFRON_CITY'))
    M.warp(mid('SAFFRON_CITY'),7,last_map=mid('SAFFRON_CITY'))
    A.navigate('SaffronCity',(18,21),cleared=[(18,22)],stop_on_warp=True)
    assert E.read('wCurMap')==mid('SILPH_CO_1F')
    A.navigate('SilphCo1F',(20,0),stop_on_warp=True)
    assert E.read('wCurMap')==mid('SILPH_CO_ELEVATOR');elevator(5)
    beaten('EVENT_BEAT_SILPH_CO_5F_TRAINER_',4)
    A.navigate('SilphCo5F',(9,15),stop_on_warp=True)
    assert E.read('wCurMap')==mid('SILPH_CO_9F')
    E.walk('left',1);E.walk('right',1)
    E.gb.tick(240);assert E.read('wCurMap')==mid('SILPH_CO_5F')
    E.walk('down',1)
    talk('SilphCo5F',(20,16),'right')
    E.advance_until(lambda:S.has_item(ITEMS['CARD_KEY']));S.close_text()
    A.navigate('SilphCo5F',(9,15),stop_on_warp=True)
    assert E.read('wCurMap')==mid('SILPH_CO_9F')
    E.walk('left',1);E.walk('right',1)
    E.gb.tick(240);assert E.read('wCurMap')==mid('SILPH_CO_5F')
    E.walk('up',1)
    A.navigate('SilphCo5F',(20,0),stop_on_warp=True);elevator(3)
    beaten('EVENT_BEAT_SILPH_CO_3F_TRAINER_',2)
    A.navigate('SilphCo3F',(18,8));E.press('left',4,20);keyed=E.state()
    K.remove_item(ITEMS['CARD_KEY']);E.press('a');E.advance_until(lambda:'CARD KEY' in E.text());S.close_text()
    assert not M.event('EVENT_SILPH_CO_3_UNLOCKED_DOOR2')
    E.restore(keyed);E.press('a');E.advance_until(lambda:M.event('EVENT_SILPH_CO_3_UNLOCKED_DOOR2'));S.close_text()
    talk('SilphCo3F',(10,8),'left',cleared=[(16,8),(17,8),(16,9),(17,9)])
    E.advance_until(lambda:M.event('EVENT_SILPH_CO_3_UNLOCKED_DOOR1'));S.close_text()
    assert S.has_item(ITEMS['CARD_KEY'])
    A.navigate('SilphCo3F',(11,11),cleared=[(8,8),(9,8),(8,9),(9,9)],stop_on_warp=True)
    assert E.read('wCurMap')==mid('SILPH_CO_7F')
    E.photo('sabrina-silph-rival-room')
    print('PASS: Silph entry, elevator travel, Card Key pickup, key rejection/unlock, and the real 3F-to-7F warp pad.',flush=True)
    return E.state()

def rival_fixture(base,name,starter,rival):
    E.restore(base);S.train(['RAICHU','HYPNO','DUGTRIO',starter],[42]*4)
    E.write('wPlayerStarter',E.IDS[{'VENUSAUR':'BULBASAUR','CHARIZARD':'CHARMANDER','BLASTOISE':'SQUIRTLE'}[starter]])
    E.write('wRivalStarter',E.IDS[rival])
    A.navigate('SilphCo7F',(3,3));E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:M.event('EVENT_BEAT_SILPH_CO_RIVAL') and E.read('wSilphCo7FCurScript')==0,name+'-silph-rival');S.close_text()
    print('PASS: '+name+' Silph rival variant and route to the president.',flush=True)
    return E.state()

def silph_fixture(base):
    E.restore(base);count=E.read('wPartyCount')
    talk('SilphCo7F',(2,5),'left')
    E.advance_until(lambda:'give a nickname' in E.text());E.press('down',8,45);E.press('a')
    E.advance_until(lambda:bool(E.read('wStatusFlags4')&1));S.close_text()
    assert E.read('wPartyCount')==count+1 and E.read(f'wPartyMon{count+1}Species')==E.IDS['LAPRAS'] and E.read(f'wPartyMon{count+1}Level')==30
    E.press('left',4,20);E.press('a');S.close_text();assert E.read('wPartyCount')==count+1
    E.photo('sabrina-leontide-gift')
    M.warp(mid('SILPH_CO_9F'),3)
    beaten('EVENT_BEAT_SILPH_CO_9F_TRAINER_',3)
    talk('SilphCo9F',(2,8),'right')
    E.advance_until(lambda:M.event('EVENT_SILPH_CO_9_UNLOCKED_DOOR1'));S.close_text()
    talk('SilphCo9F',(3,15),'up',cleared=[(2,8),(3,8),(2,9),(3,9)])
    E.advance_until(lambda:all(M.word(f'wPartyMon{i}HP')==M.word(f'wPartyMon{i}MaxHP') for i in range(1,count+2)));S.close_text()
    M.warp(mid('SILPH_CO_7F'),4)
    A.navigate('SilphCo7F',(5,7),stop_on_warp=True)
    assert E.read('wCurMap')==mid('SILPH_CO_11F')
    A.navigate('SilphCo11F',(3,12));E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:M.event('EVENT_BEAT_SILPH_CO_11F_TRAINER_0'),'sabrina-president-guard');S.close_text()
    talk('SilphCo11F',(6,14),'up')
    E.advance_until(lambda:M.event('EVENT_SILPH_CO_11_UNLOCKED_DOOR'));S.close_text()
    A.navigate('SilphCo11F',(6,13),cleared=[(6,12),(7,12),(6,13),(7,13)])
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:M.event('EVENT_BEAT_SILPH_CO_GIOVANNI'),'sabrina-giovanni');S.close_text()
    S.checkpoint('sabrina-giovanni')
    # The unused warp at (5,5) sits on ordinary floor and does not activate.
    talk('SilphCo11F',(6,5),'right',cleared=[(5,5),(6,9),(6,12),(7,12),(6,13),(7,13)])
    E.advance_until(lambda:M.event('EVENT_GOT_MASTER_BALL'));S.close_text()
    assert A.item_count(ITEMS['MASTER_BALL'])==1
    E.press('right',4,20);E.press('a');S.close_text();assert A.item_count(ITEMS['MASTER_BALL'])==1
    E.photo('sabrina-silph-rescued')
    print('PASS: LEONTIDE gift, nurse healing, 7F-to-11F pad, guard, final key door, Giovanni, and one Master Ball.',flush=True)
    return E.state()

def copycat_talk():
    # Copycat wanders. Follow her current tile and interact from a free neighbour.
    for _ in range(50):
        x=E.read('wSprite01StateData2MapX')-4;y=E.read('wSprite01StateData2MapY')-4
        for position,direction in [((x,y+1),'up'),((x+1,y),'left'),((x-1,y),'right'),((x,y-1),'down')]:
            if not (0<=position[0]<8 and 0<=position[1]<8):continue
            try:A.navigate('CopycatsHouse2F',position,cleared=[(4,3),(4,6)])
            except AssertionError as error:
                if not (error.args and isinstance(error.args[0],tuple) and error.args[0][0]=='No map path'):raise
                continue
            E.press(direction,4,20);E.press('a')
            if 'Hi!' in E.text():return
    raise AssertionError(('Could not approach Copycat',E.text()))

def copycat_fixture(base):
    E.restore(base)
    # Make inventory room for the purchase and the TM, which precedes removal
    # of the doll in the original exchange script.
    for item in ('TM34','TM11'):K.remove_item(ITEMS[item])
    K.remove_item(ITEMS['POKE_DOLL'])
    M.warp(mid('COPYCATS_HOUSE_2F'),0,last_map=mid('SAFFRON_CITY'))
    copycat_talk();S.close_text();assert not M.event('EVENT_GOT_TM31')
    M.warp(mid('CELADON_MART_4F'),0);E.write('wPlayerMoney',[5,0,0])
    A.navigate('CeladonMart4F',(5,5));A.buy_stone(ITEMS['POKE_DOLL'],0)
    M.warp(mid('COPYCATS_HOUSE_2F'),0,last_map=mid('SAFFRON_CITY'))
    copycat_talk();E.advance_until(lambda:M.event('EVENT_GOT_TM31'));S.close_text()
    assert A.item_count(ITEMS['TM31'])==1 and not S.has_item(ITEMS['POKE_DOLL'])
    copycat_talk();S.close_text();assert A.item_count(ITEMS['TM31'])==1
    E.photo('sabrina-copycat-exchange')
    print('PASS: Copycat requires a purchased Poké Doll, consumes it, and gives TM31 COPY TRICK once.',flush=True)
    return E.state()

def maze():
    source=(E.ROOT/'data/maps/objects/SaffronGym.asm').read_text()
    warps=[(int(x),int(y),dest,int(index)) for x,y,dest,index in re.findall(r'warp_event\s+(\d+),\s*(\d+),\s*(\w+),\s*(\d+)',source)]
    def room(p):return (0 if p[0]<6 else 1 if p[0]<12 else 2,0 if p[1]<6 else 1 if p[1]<12 else 2)
    start=room((E.read('wXCoord'),E.read('wYCoord')));goal=(1,1)
    queue=deque([start]);paths={start:[]}
    while queue:
        current=queue.popleft()
        if current==goal:break
        for x,y,dest,index in warps:
            if dest!='SAFFRON_GYM' or room((x,y))!=current:continue
            target=warps[index-1][:2];next_room=room(target)
            if next_room not in paths:paths[next_room]=paths[current]+[((x,y),target)];queue.append(next_room)
    assert goal in paths
    for pad,target in paths[goal]:
        A.navigate('SaffronGym',pad,stop_on_warp=True)
        assert (E.read('wXCoord'),E.read('wYCoord'))==target,(pad,target,E.read('wXCoord'),E.read('wYCoord'))
    return len(paths[goal])

def sabrina_fixture(base,name,starter):
    E.restore(base);S.train(['BEEDRILL','PARASECT',starter],[44]*3)
    beaten('EVENT_BEAT_SAFFRON_GYM_TRAINER_',7)
    M.warp(mid('SILPH_CO_1F'),0,last_map=mid('SAFFRON_CITY'))
    E.walk('up',1)
    A.navigate('SilphCo1F',(10,17),stop_on_warp=True)
    if E.read('wCurMap')==mid('SILPH_CO_1F'):E.press('down',8,180)
    assert E.read('wCurMap')==mid('SAFFRON_CITY')
    A.navigate('SaffronCity',(34,3),cleared=[(34,4),(18,22),(19,22)],stop_on_warp=True)
    assert E.read('wCurMap')==mid('SAFFRON_GYM')
    pads=maze();talk('SaffronGym',(9,9),'up');E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:bool(E.read('wObtainedBadges')&32),name+'-sabrina');S.close_text()
    assert E.read('wObtainedBadges')==0x3f and M.event('EVENT_BEAT_SABRINA') and M.event('EVENT_GOT_TM46') and S.has_item(ITEMS['TM46'])
    E.press('up',4,20);E.press('a');E.advance_until(lambda:'This demo ends' in E.text());S.close_text()
    E.photo(name+'-sabrina-complete')
    print(f'PASS: {name} crosses {pads} real gym pads and earns the Marsh Badge and TM46 AURA PULSE.',flush=True)
    return E.state()

def main():
    try:
        if '--from-card' in sys.argv:card=S.load_checkpoint('sabrina-card')
        else:
            base=S.load_checkpoint('koga-complete')
            city=guards_fixture(base);psychic=psychic_fixture(city);dojo_fixture(psychic)
            card=card_fixture(psychic);S.checkpoint('sabrina-card')
        rivals={name:rival_fixture(card,name,starter,rival) for name,starter,rival in [('groen','VENUSAUR','CHARMANDER'),('shiba','CHARIZARD','SQUIRTLE'),('newf','BLASTOISE','BULBASAUR')]}
        silph=silph_fixture(rivals['newf']);S.checkpoint('sabrina-silph')
        silph=copycat_fixture(silph)
        completed={name:sabrina_fixture(silph,name,starter) for name,starter in [('groen','VENUSAUR'),('shiba','CHARIZARD'),('newf','BLASTOISE')]}
        E.restore(completed['newf']);S.checkpoint('sabrina-complete')
        E.save_reload(completed['newf'],expected_map=mid('SAFFRON_GYM'),expected_badges=0x3f)
        assert M.event('EVENT_BEAT_SILPH_CO_GIOVANNI') and M.event('EVENT_GOT_MASTER_BALL') and E.read('wStatusFlags1')&64
        (E.QA/'sabrina-results.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(E.ROM).hexdigest(),'drink_gate_and_purchase':True,'dojo_choices':2,'card_key_and_elevator':True,'silph_rivals':list(rivals),'leontide_gift_and_nurse':True,'president_rescue_and_master_ball':True,'copycat_doll_purchase_and_exchange':True,'gym_pad_routes_and_sabrina':list(completed),'save_load_six_badges':True,'fixture':'trained parties, money, inventory room, floor-entry warps, optional trainers marked beaten; actual purchases, gates, gifts, mandatory battles, doors and warp pads'},indent=2)+'\n')
    finally:E.gb.stop();E.tmp.cleanup()

if __name__=='__main__':main()
