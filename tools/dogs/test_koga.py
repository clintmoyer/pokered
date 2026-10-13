#!/usr/bin/env python3
"""Replay the Scope/Flute, Safari rewards, Strength, Koga, and Surf chapter.

Trained parties, money, Repel and room warps are fixtures. Optional trainers are
marked beaten when navigating; required battles and quest flags are earned via
ordinary game inputs. No battle stats, damage, HP, RNG or victory flags are patched.
Run test_erika.py first to produce a matching four-badge checkpoint.
"""
import hashlib
import json
import sys
import test_erika as A
from test_erika import E, M, S, ITEMS, MAPS

def mid(code):return MAPS[code][0]

def talk(filename,position,direction,cleared=()):
    A.navigate(filename,position,cleared);E.press(direction,4,20);E.press('a')

def beaten(prefix,count):
    for i in range(count):M.event(prefix+str(i),True)

def remove_item(item):
    items=[v for key,qty in zip(S.bag()[::2],S.bag()[1::2]) if key!=item for v in (key,qty)]
    E.write('wNumBagItems',len(items)//2);E.write('wBagItems',items+[255])

def battle_option(label):
    # The battle menu has two columns; a row-only selector confuses ITEM and RUN.
    for _ in range(8):
        rows=E.text().splitlines()
        if label=='BALL':
            cursor=next(((row.index('▲'),y) for y,row in enumerate(rows) if '▲' in row),None)
            if cursor==(1,14):E.press('a');return
            if cursor and cursor[0]>1:E.press('left',8,45)
            if cursor and cursor[1]>14:E.press('up',8,45)
            continue
        selected=next((row.split('▲',1)[1].strip().split()[0] for row in rows if '▲' in row),None)
        if selected and selected.startswith(label):E.press('a');return
        E.press('left' if label in ('FIGHT','ITEM','BALL') else 'right',8,45)
        E.press('up' if label in ('FIGHT','PKMN','BALL') else 'down',8,45)
    raise AssertionError(('Battle menu',label,E.text()))

def rocket_fixture(base):
    E.restore(base);S.train(['WARTORTLE','HYPNO','PRIMEAPE'],[32,32,32])
    M.warp(mid('GAME_CORNER'),0,last_map=6)
    talk('GameCorner',(9,6),'up')
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:E.read('wGameCornerCurScript')==0 and E.read('wJoyIgnore')==0,'koga-poster-guard')
    S.close_text();talk('GameCorner',(9,5),'up',cleared=[(9,5)])
    E.advance_until(lambda:M.event('EVENT_FOUND_ROCKET_HIDEOUT'));S.close_text()
    A.navigate('GameCorner',(17,4));assert E.read('wCurMap')==mid('ROCKET_HIDEOUT_B1F')
    E.photo('koga-hideout-entry')
    print('PASS: the poster guard battle and switch open the Rocket Hideout.',flush=True)
    M.warp(mid('ROCKET_HIDEOUT_ELEVATOR'),0)
    talk('RocketHideoutElevator',(1,2),'up');E.advance_until(lambda:'key' in E.text())
    assert not S.has_item(ITEMS['LIFT_KEY']);S.close_text()
    M.warp(mid('ROCKET_HIDEOUT_B4F'),0)
    talk('RocketHideoutB4F',(11,3),'up')
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:M.event('EVENT_BEAT_ROCKET_HIDEOUT_4_TRAINER_2'),'koga-lift-key-guard')
    S.close_text();E.press('up',4,20);E.press('a')
    E.advance_until(lambda:M.event('EVENT_ROCKET_DROPPED_LIFT_KEY'));S.close_text()
    talk('RocketHideoutB4F',(10,3),'up')
    E.advance_until(lambda:S.has_item(ITEMS['LIFT_KEY']));S.close_text()
    E.photo('koga-lift-key')
    print('PASS: the lift refuses travel without its key; the defeated guard drops the key.',flush=True)
    M.warp(mid('ROCKET_HIDEOUT_ELEVATOR'),0)
    talk('RocketHideoutElevator',(1,2),'up');E.advance_until(lambda:'B4F' in E.text())
    M.select_row('B4F');E.press('a');S.close_text()
    A.navigate('RocketHideoutElevator',(2,1));E.press('up',8,360)
    assert E.read('wCurMap')==mid('ROCKET_HIDEOUT_B4F')
    for position in [(23,13),(26,13)]:
        talk('RocketHideoutB4F',position,'up');E.advance_until(lambda:E.read('wIsInBattle')==2)
        index=0 if position[0]==23 else 1
        M.fight_until(lambda:M.event(f'EVENT_BEAT_ROCKET_HIDEOUT_4_TRAINER_{index}'),'koga-door-guard-'+str(index));S.close_text()
    E.gb.tick(180);assert M.event('EVENT_ROCKET_HIDEOUT_4_DOOR_UNLOCKED')
    # The floor block replacing the closed door is walkable at these four cells.
    talk('RocketHideoutB4F',(24,3),'right',cleared=[(24,10),(25,10),(24,11),(25,11)])
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:M.event('EVENT_BEAT_ROCKET_HIDEOUT_GIOVANNI'),'koga-giovanni');S.close_text()
    talk('RocketHideoutB4F',(25,3),'up',cleared=[(25,3)])
    E.advance_until(lambda:S.has_item(ITEMS['SILPH_SCOPE']));S.close_text()
    E.photo('koga-silph-scope')
    print('PASS: both door guards, Giovanni, and the Scope pickup complete the hideout.',flush=True)
    return E.state()

def tower_rival_fixture(base,name,starter,rival):
    E.restore(base);S.train(['HYPNO','RAICHU','WARTORTLE'],[32,32,32])
    E.write('wPlayerStarter',E.IDS[starter]);E.write('wRivalStarter',E.IDS[rival])
    M.warp(mid('POKEMON_TOWER_2F'),1,last_map=4)
    A.navigate('PokemonTower2F',(14,6));E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:M.event('EVENT_BEAT_POKEMON_TOWER_RIVAL') and E.read('wPokemonTower2FCurScript')==0,name+'-tower-rival')
    S.close_text();print('PASS: '+name+' Tower rival variant.',flush=True)
    return E.state()

def tower_fixture(base):
    E.restore(base);S.train(['BLASTOISE','HYPNO','RAICHU'],[36,36,36])
    beaten('EVENT_BEAT_POKEMONTOWER_6_TRAINER_',3)
    M.warp(mid('POKEMON_TOWER_6F'),0,last_map=4)
    before=A.item_count(ITEMS['RARE_CANDY'])
    talk('PokemonTower6F',(6,7),'down')
    E.advance_until(lambda:A.item_count(ITEMS['RARE_CANDY'])==before+1);S.close_text()
    A.navigate('PokemonTower6F',(10,15),cleared=[(6,8)]);scoped=E.state()
    remove_item(ITEMS['SILPH_SCOPE'])
    E.walk('down',1);E.advance_until(lambda:'FIGHT' in E.text())
    assert 'GHOST' in E.text();E.photo('koga-unidentified-ghost')
    battle_option('RUN')
    E.advance_until(lambda:E.read('wIsInBattle')==0);S.close_text()
    assert not M.event('EVENT_BEAT_GHOST_MAROWAK')
    E.restore(scoped);E.walk('down',1)
    E.advance_until(lambda:'FIGHT' in E.text())
    E.photo('koga-revealed-scottdig')
    assert E.read('wEnemyMonSpecies')==E.IDS['MAROWAK']
    # The guardian's mother cannot be adopted even after the Scope reveals her.
    battle_option('ITEM');A.select_item(ITEMS['POKE_BALL']);E.press('a');E.press('a')
    E.advance_until(lambda:'dodged' in E.text() or 'missed' in E.text());E.photo('koga-ghost-cannot-catch')
    assert S.has_item(ITEMS['SILPH_SCOPE'])
    S.checkpoint('koga-mother-start')
    M.fight_until(lambda:M.event('EVENT_BEAT_GHOST_MAROWAK'),'koga-guardian-mother');S.close_text()
    A.navigate('PokemonTower6F',(9,16));E.press('down',8,180)
    assert E.read('wCurMap')==mid('POKEMON_TOWER_7F')
    for index,(position,direction) in enumerate([((10,11),'left'),((10,9),'right'),((10,7),'left')]):
        talk('PokemonTower7F',position,direction);E.advance_until(lambda:E.read('wIsInBattle')==2)
        M.fight_until(lambda:M.event(f'EVENT_BEAT_POKEMONTOWER_7_TRAINER_{index}') and E.read('wPokemonTower7FCurScript')==0,'koga-tower-rocket-'+str(index));S.close_text()
    talk('PokemonTower7F',(10,4),'up')
    E.advance_until(lambda:E.read('wCurMap')==mid('MR_FUJIS_HOUSE'));S.close_text()
    assert M.event('EVENT_RESCUED_MR_FUJI')
    talk('MrFujisHouse',(3,2),'up')
    E.advance_until(lambda:S.has_item(ITEMS['POKE_FLUTE']));S.close_text()
    E.photo('koga-fuji-flute');print('PASS: Scope reveal, uncatchable mother, three Tower Rockets, Fuji rescue and flute reward.',flush=True)
    return E.state()

def flute_fixture(base,route):
    E.restore(base);S.train(['HYPNO','PRIMEAPE','WARTORTLE'],[34,34,34])
    M.warp(mid('ROUTE_12_GATE_1F'),0,last_map=mid('ROUTE_12'))
    M.warp(mid('ROUTE_'+str(route)),2,last_map=6 if route==16 else 4)
    prefix=f'EVENT_BEAT_ROUTE_{route}_TRAINER_'
    beaten(prefix,7 if route==12 else 6)
    filename='Route'+str(route);position=(10,61) if route==12 else (25,10)
    direction='down' if route==12 else 'right'
    A.navigate(filename,position);E.press(direction,4,20)
    before=E.state();remove_item(ITEMS['POKE_FLUTE']);E.press('a')
    E.advance_until(lambda:'sleeping' in E.text());S.close_text()
    assert not M.event(f'EVENT_BEAT_ROUTE{route}_SNORLAX')
    E.restore(before);E.start_option('ITEM');A.select_item(ITEMS['POKE_FLUTE']);E.press('a');E.press('a')
    E.advance_until(lambda:E.read('wIsInBattle')==1)
    assert E.read('wEnemyMonSpecies')==E.IDS['SNORLAX']
    M.fight_until(lambda:M.event(f'EVENT_BEAT_ROUTE{route}_SNORLAX'),'koga-neomast-route-'+str(route));S.close_text()
    E.photo('koga-neomast-route-'+str(route)+'-open')
    print('PASS: the flute wakes NEOMAST and clears Route '+str(route)+'.',flush=True)
    return E.state()

def safari_fixture(base):
    E.restore(base);S.train(['BLASTOISE','RATICATE'],[36,32]);E.write('wPlayerMoney',[5,0,0])
    M.warp(mid('SAFARI_ZONE_GATE'),0,last_map=7)
    E.walk('up',3);E.advance_until(lambda:'YES' in E.text());E.press('a')
    E.advance_until(lambda:E.read('wCurMap')==mid('SAFARI_ZONE_CENTER'));S.close_text()
    assert E.read('wNumSafariBalls')==30 and M.event('EVENT_IN_SAFARI_ZONE')
    assert list(E.gb.memory[E.SYMS['wPlayerMoney'][1]:E.SYMS['wPlayerMoney'][1]+3])==[4,0x95,0]
    admission=E.state();safari_capture_fixture(admission);E.restore(admission)
    for filename,target,expected in [('SafariZoneCenter',(29,10),'SAFARI_ZONE_EAST'),('SafariZoneEast',(0,4),'SAFARI_ZONE_NORTH'),('SafariZoneNorth',(2,35),'SAFARI_ZONE_WEST')]:
        current=E.read('wCurMap')
        A.navigate(filename,target)
        if E.read('wCurMap')==current:E.press('right' if target[0]==29 else 'left' if target[0]==0 else 'down',8,180)
        assert E.read('wCurMap')==mid(expected),(filename,E.read('wCurMap'))
    talk('SafariZoneWest',(19,8),'up');E.advance_until(lambda:S.has_item(ITEMS['GOLD_TEETH']));S.close_text()
    A.navigate('SafariZoneWest',(3,3));assert E.read('wCurMap')==mid('SAFARI_ZONE_SECRET_HOUSE')
    talk('SafariZoneSecretHouse',(3,4),'up');E.advance_until(lambda:M.event('EVENT_GOT_HM03'));S.close_text()
    assert S.has_item(ITEMS['HM03']);E.photo('koga-secret-house-hm03')
    print('PASS: the paid Safari run traverses all four areas, collects teeth, and awards HM03 within its step limit.',flush=True)
    # Return through the normal gate; the two rewards remain in the ordinary bag.
    M.warp(mid('SAFARI_ZONE_GATE'),2,last_map=7)
    E.advance_until(lambda:'YES' in E.text());E.press('a');S.close_text()
    assert not M.event('EVENT_IN_SAFARI_ZONE')
    M.warp(mid('WARDENS_HOUSE'),0,last_map=7)
    talk('WardensHouse',(2,4),'up');E.advance_until(lambda:M.event('EVENT_GOT_HM04'));S.close_text()
    assert S.has_item(ITEMS['HM04']) and not S.has_item(ITEMS['GOLD_TEETH'])
    A.teach_hm(ITEMS['HM04'],'STRENGTH',1);A.teach_hm(ITEMS['HM03'],'SURF',0)
    A.navigate('WardensHouse',(7,4));E.press('right',4,20);ready=E.state()
    E.write('wObtainedBadges',E.read('wObtainedBadges')&~8)
    A.field_move('HAUL',1);E.advance_until(lambda:'BADGE' in E.text());S.close_text()
    E.restore(ready);A.field_move('HAUL',1);S.close_text()
    for _ in range(3):
        E.walk('right',1)
        if E.read('wXCoord')==8:break # the original engine requires two push attempts
    assert E.read('wXCoord')==8 and E.read('wYCoord')==4
    talk('WardensHouse',(8,4),'up');E.advance_until(lambda:S.has_item(ITEMS['RARE_CANDY']));S.close_text()
    E.photo('koga-warden-boulder')
    print('PASS: teeth exchange, reusable HMs, Rainbow-gated HAUL, boulder movement and Candy pickup.',flush=True)
    return E.state()

def safari_capture_fixture(base):
    E.restore(base);A.navigate('SafariZoneCenter',(23,19))
    E.write('wRepelRemainingSteps',0)
    count=E.read('wPartyCount')
    for step in range(120):
        if E.read('wPartyCount')==count+1:break
        if E.read('wIsInBattle'):
            E.advance_until(lambda:('BAIT' in E.text() and 'ROCK' in E.text()) or E.read('wIsInBattle')==0 or E.read('wPartyCount')==count+1)
            if 'BAIT' in E.text() and 'ROCK' in E.text():battle_option('BALL')
        else:E.press('right' if step%2 else 'left',8,90)
    else:raise AssertionError(('Safari adoption',E.text(),E.read('wNumSafariBalls')))
    E.advance_until(lambda:'give a nickname' in E.text());E.press('down',8,45);E.press('a');S.close_text()
    dog=next(d for d in M.DOGS if E.IDS[d['slot']]==E.read(f'wPartyMon{count+1}Species'))
    assert M.event('EVENT_IN_SAFARI_ZONE') and E.read('wNumSafariBalls')<30
    E.photo('koga-safari-adoption')
    print('PASS: actual Safari grass encounters and Safari Balls adopt '+dog['name']+'.',flush=True)

def koga_fixture(base,name,starter):
    E.restore(base);S.train(['HYPNO','DUGTRIO',starter],[40,40,40])
    beaten('EVENT_BEAT_FUCHSIA_GYM_TRAINER_',6)
    M.warp(mid('FUCHSIA_GYM'),0,last_map=7)
    talk('FuchsiaGym',(4,11),'up');E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:bool(E.read('wObtainedBadges')&16),name+'-koga');S.close_text()
    assert E.read('wObtainedBadges')==0x1f and M.event('EVENT_BEAT_KOGA') and M.event('EVENT_GOT_TM06') and S.has_item(ITEMS['TM06'])
    E.press('a');E.advance_until(lambda:'Visit SAFFRON' in E.text());S.close_text();E.photo(name+'-koga-complete')
    print('PASS: '+name+' earns the Soul Badge and TM06 VENOM MARK.',flush=True)
    return E.state()

def surf_fixture(before,after):
    E.restore(before);S.train(['BLASTOISE'],[40]);A.teach_hm(ITEMS['HM03'],'SURF')
    M.warp(mid('FUCHSIA_GOOD_ROD_HOUSE'),1,last_map=7);A.navigate('FuchsiaGoodRodHouse',(2,0));E.press('up',8,180)
    # The backyard water is directly north of this row.
    A.navigate('FuchsiaCity',(31,22));E.press('up',4,20)
    A.field_move('DOG PADDLE');E.advance_until(lambda:'BADGE' in E.text());S.close_text()
    assert E.read('wWalkBikeSurfState')==0
    E.restore(after);S.train(['BLASTOISE'],[40]);A.teach_hm(ITEMS['HM03'],'SURF')
    M.warp(mid('FUCHSIA_GOOD_ROD_HOUSE'),1,last_map=7);A.navigate('FuchsiaGoodRodHouse',(2,0));E.press('up',8,180)
    A.navigate('FuchsiaCity',(31,22));E.press('up',4,20)
    A.field_move('DOG PADDLE');E.advance_until(lambda:E.read('wWalkBikeSurfState')==2)
    S.close_text();E.photo('koga-dog-paddle');E.walk('up',1)
    for _ in range(5):
        E.walk('down',1)
        if E.read('wWalkBikeSurfState')==0:break
    assert E.read('wWalkBikeSurfState')==0
    print('PASS: DOG PADDLE requires the Soul Badge, enters water and lands normally.',flush=True)

def main():
    try:
        base=S.load_checkpoint('erika-complete')
        rivals={}
        if '--from-flute' in sys.argv:tower=S.load_checkpoint('koga-flute')
        else:
            rocket=S.load_checkpoint('koga-scope') if '--from-scope' in sys.argv else rocket_fixture(base)
            E.restore(rocket);S.checkpoint('koga-scope')
            for name,starter,rival in [('groen','BULBASAUR','CHARMANDER'),('shiba','CHARMANDER','SQUIRTLE'),('newf','SQUIRTLE','BULBASAUR')]:rivals[name]=tower_rival_fixture(rocket,name,starter,rival)
            tower=tower_fixture(rivals['newf']);S.checkpoint('koga-flute')
        if '--from-route12' in sys.argv:opened=S.load_checkpoint('koga-route12')
        else:flute_fixture(tower,16);opened=flute_fixture(tower,12);S.checkpoint('koga-route12')
        safari=safari_fixture(opened);S.checkpoint('koga-safari')
        completed={name:koga_fixture(safari,name,starter) for name,starter in [('groen','VENUSAUR'),('shiba','CHARIZARD'),('newf','BLASTOISE')]}
        E.restore(completed['newf']);S.checkpoint('koga-complete')
        surf_fixture(safari,completed['newf']);E.save_reload(completed['newf'],expected_map=mid('FUCHSIA_GYM'),expected_badges=0x1f)
        for slot in json.loads((E.ROOT/'data/dogs/koga.json').read_text())['new_forms']:
            dog=next(d for d in M.DOGS if d['slot']==slot)
            if dog['evolution']:E.evolution_check(completed['newf'],slot,dog['evolution'][0]-1,dog['evolution'][1])
        (E.QA/'koga-results.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(E.ROM).hexdigest(),'scope_and_lift_key':True,'tower_rivals':list(rivals),'ghost_and_fuji':True,'flute_routes':[12,16],'safari_rewards_and_adoption':True,'strength_boulder':True,'koga':list(completed),'surf_soul_gate':True,'save_load_five_badges':True,'fixture':'trained parties, money, room warps, optional trainers marked beaten, Repel during walking'},indent=2)+'\n')
    finally:E.gb.stop();E.tmp.cleanup()

if __name__=='__main__':main()
