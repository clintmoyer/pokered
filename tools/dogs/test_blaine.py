#!/usr/bin/env python3
"""Replay Seafoam, Cinnabar's lab, the Mansion, quiz doors and Blaine.

Requires a matching-ROM Sabrina checkpoint. Trained parties, inventory room,
fossil items, room-entry warps, Repel and optional trainer flags are fixtures.
Puzzles, gifts, quest gates, encounters, mandatory battles and saving use inputs.
The Hall of Fame entry warp isolates the guardian retry hook, not League progress.
"""
import hashlib
import json
import re
import sys
import test_sabrina as T
from test_sabrina import E,M,S,A,K,ITEMS,mid,beaten
TOGGLES=[name.strip() for name in re.findall(r'^\s*toggle_object_state ([^,\n]+),',(E.ROOT/'data/maps/toggleable_objects.asm').read_text(),re.M)]

def hidden_object(name):
    if name not in TOGGLES:return False
    index=TOGGLES.index(name)
    return bool(E.gb.memory[E.SYMS['wToggleableObjectFlags'][1]+index//8] & 1<<(index%8))

def nav(name,position,cleared=(),warp=False):
    blocked=[(18,4)] if name=='CinnabarIsland' and not S.has_item(ITEMS['SECRET_KEY']) and position!=(18,4) else []
    holes={'SeafoamIslands1F':[(17,6),(24,6)],'SeafoamIslandsB1F':[(18,6),(23,6)],'SeafoamIslandsB2F':[(19,6),(22,6)],'SeafoamIslandsB3F':[(3,16),(6,16)]}
    blocked += [p for p in holes.get(name,[]) if p!=position]
    # Strength stays active. Avoid the current boulder positions while walking,
    # so the navigator never pushes another box on its way to the next stance.
    source=(E.ROOT/f'data/maps/objects/{name}.asm').read_text()
    objects=re.findall(r'object_event\s+(\d+),\s*(\d+),\s*(\w+)',source)
    object_names=re.findall(r'const_export (\w+)',source)
    cleared=list(cleared)
    for index,(x,y,sprite) in enumerate(objects,1):
        if sprite=='SPRITE_BOULDER':
            cleared.append((int(x),int(y)))
            if not hidden_object(object_names[index-1]):
                blocked.append((E.read(f'wSprite{index:02d}StateData2MapX')-4,E.read(f'wSprite{index:02d}StateData2MapY')-4))
    A.navigate(name,position,cleared=cleared,stop_on_warp=warp,live_blocks=True,
               allowed_tiles=(0x14,) if E.read('wWalkBikeSurfState')==2 else (),blocked_tiles=blocked)

def talk(name,position,direction,cleared=()):
    nav(name,position,cleared);E.press(direction,4,20);E.press('a')

def add_item(item):
    assert not S.has_item(item) and E.read('wNumBagItems')<20
    items=S.bag()+[item,1];E.write('wNumBagItems',len(items)//2);E.write('wBagItems',items+[255])

def room_for_rewards():
    for i in range(1,51):K.remove_item(ITEMS[f'TM{i:02d}'])

def push(direction,count=1):
    for _ in range(count):
        before=(E.read('wXCoord'),E.read('wYCoord'))
        for attempt in range(4):
            E.press(direction,8,90)
            if (E.read('wXCoord'),E.read('wYCoord'))!=before:break
        else:raise AssertionError(('Boulder did not move',direction,before))

def haul():
    A.field_move('HAUL',1);S.close_text()

def seafoam_fixture(base):
    E.restore(base);room_for_rewards();S.train(['BLASTOISE','RATICATE','RAICHU'],[48,48,48])
    A.teach_hm(ITEMS['HM03'],'SURF',0);A.teach_hm(ITEMS['HM04'],'STRENGTH',1)
    M.warp(mid('SEAFOAM_ISLANDS_1F'),0,last_map=mid('ROUTE_20'));haul()
    nav('SeafoamIslands1F',(18,11));push('up',4)
    nav('SeafoamIslands1F',(19,6),cleared=[(18,10)]);push('left')
    assert M.event('EVENT_SEAFOAM1_BOULDER1_DOWN_HOLE')
    M.warp(mid('SEAFOAM_ISLANDS_1F'),5,last_map=mid('ROUTE_20'));haul()
    nav('SeafoamIslands1F',(26,8));push('up')
    nav('SeafoamIslands1F',(27,6),cleared=[(26,7)]);push('left',2)
    assert M.event('EVENT_SEAFOAM1_BOULDER2_DOWN_HOLE')
    for entry,position,hole,stance,direction,index in [
        (1,(16,6),(18,6),(17,6),'right',1),
        (6,(21,6),(23,6),(24,6),'left',2)]:
        M.warp(mid('SEAFOAM_ISLANDS_B1F'),entry);haul()
        nav('SeafoamIslandsB1F',position);push('right')
        assert M.event(f'EVENT_SEAFOAM2_BOULDER{index}_DOWN_HOLE')
        # Follow the boulder down: these raised B2F platforms have no stairs.
        nav('SeafoamIslandsB1F',hole,warp=True)
        assert E.read('wCurMap')==mid('SEAFOAM_ISLANDS_B2F');haul()
        nav('SeafoamIslandsB2F',stance);push(direction)
        assert M.event(f'EVENT_SEAFOAM3_BOULDER{index}_DOWN_HOLE')
        E.press(direction,8,240);E.gb.tick(720)
        if index==1:
            assert E.read('wCurMap')==mid('SEAFOAM_ISLANDS_B4F')
            assert not M.event('EVENT_SEAFOAM3_BOULDER2_DOWN_HOLE')
            print('PASS: the unfinished eastern dam forces a real current ride to B4F.',flush=True)
        else:assert E.read('wCurMap')==mid('SEAFOAM_ISLANDS_B3F')
    print('PASS: both boulders drop through three floors and stop the eastern Seafoam current.',flush=True)
    assert E.read('wWalkBikeSurfState')==2
    S.checkpoint('blaine-east-dam')
    nav('SeafoamIslandsB3F',(23,9));assert E.read('wWalkBikeSurfState')==0
    M.warp(mid('SEAFOAM_ISLANDS_B3F'),0)
    haul();nav('SeafoamIslandsB3F',(6,14));push('left',3);push('down')
    assert M.event('EVENT_SEAFOAM4_BOULDER1_DOWN_HOLE')
    moved=[(5,14),(3,15)]
    nav('SeafoamIslandsB3F',(9,15),cleared=moved);push('up',2)
    moved += [(9,14)]
    nav('SeafoamIslandsB3F',(8,13),cleared=moved);push('down')
    moved += [(8,14)]
    nav('SeafoamIslandsB3F',(9,15),cleared=moved);push('left',2)
    nav('SeafoamIslandsB3F',(6,14),cleared=moved);push('down')
    assert M.event('EVENT_SEAFOAM4_BOULDER2_DOWN_HOLE')
    nav('SeafoamIslandsB3F',(3,16),cleared=moved,warp=True)
    assert E.read('wCurMap')==mid('SEAFOAM_ISLANDS_B4F')
    nav('SeafoamIslandsB4F',(6,2));E.photo('blaine-frostmaul-island')
    print('PASS: real Surf travel, the four-boulder puzzle, both lower holes, and the guardian island.',flush=True)
    return E.state()

def city_entry():
    M.warp(mid('CINNABAR_MART'),0,last_map=mid('CINNABAR_ISLAND'))
    E.walk('up',1);nav('CinnabarMart',(3,7),warp=True)
    if E.read('wCurMap')==mid('CINNABAR_MART'):E.press('down',8,180)
    assert E.read('wCurMap')==mid('CINNABAR_ISLAND')

def switch(name,position):
    before=M.event('EVENT_MANSION_SWITCH_ON')
    talk(name,position,'up');E.advance_until(lambda:'YES' in E.text());E.press('a')
    E.advance_until(lambda:M.event('EVENT_MANSION_SWITCH_ON')!=before);S.close_text()

def mansion_fixture(base):
    E.restore(base);room_for_rewards();S.train(['BLASTOISE','DUGTRIO'],[48,48])
    city_entry();assert not S.has_item(ITEMS['SECRET_KEY'])
    nav('CinnabarIsland',(18,4));E.advance_until(lambda:'locked' in E.text());S.close_text()
    assert E.read('wYCoord')==5 and E.read('wCurMap')==mid('CINNABAR_ISLAND')
    for floor,count in [(1,1),(2,1),(3,2),(4,2)]:beaten(f'EVENT_BEAT_MANSION_{floor}_TRAINER_',count)
    nav('CinnabarIsland',(6,3),warp=True);assert E.read('wCurMap')==mid('POKEMON_MANSION_1F')
    nav('PokemonMansion1F',(5,10),warp=True);assert E.read('wCurMap')==mid('POKEMON_MANSION_2F')
    nav('PokemonMansion2F',(6,1),warp=True);assert E.read('wCurMap')==mid('POKEMON_MANSION_3F')
    switch('PokemonMansion3F',(10,6));assert M.event('EVENT_MANSION_SWITCH_ON')
    nav('PokemonMansion3F',(16,14),warp=True);assert E.read('wCurMap')==mid('POKEMON_MANSION_1F')
    nav('PokemonMansion1F',(21,23),warp=True);assert E.read('wCurMap')==mid('POKEMON_MANSION_B1F')
    switch('PokemonMansionB1F',(18,26));assert not M.event('EVENT_MANSION_SWITCH_ON')
    switch('PokemonMansionB1F',(20,4));assert M.event('EVENT_MANSION_SWITCH_ON')
    talk('PokemonMansionB1F',(5,14),'up')
    E.advance_until(lambda:S.has_item(ITEMS['SECRET_KEY']));S.close_text();E.photo('blaine-secret-key')
    city_entry();nav('CinnabarIsland',(18,3),warp=True)
    assert E.read('wCurMap')==mid('CINNABAR_GYM') and S.has_item(ITEMS['SECRET_KEY'])
    print('PASS: the locked gym, real Mansion stairs and fall, alternating switches, Secret Key and keyed entry.',flush=True)
    return E.state()

def quiz(name,index,answer):
    x,y=[(15,7),(10,1),(9,7),(9,13),(1,13),(1,7)][index-1]
    talk('CinnabarGym',(x,y+1),'up')
    E.advance_until(lambda:'YES' in E.text());E.press('down' if answer else 'up',8,45);E.press('a')

def quizzes_fixture(base):
    E.restore(base);quiz('wrong',1,1)
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:M.event('EVENT_BEAT_CINNABAR_GYM_TRAINER_1') and E.read('wCinnabarGymCurScript')==0,'blaine-wrong-quiz');S.close_text()
    assert M.event('EVENT_CINNABAR_GYM_GATE1_UNLOCKED')
    E.restore(base)
    for index,answer in enumerate([0,1,1,1,0,1],1):
        quiz('correct',index,answer)
        E.advance_until(lambda:M.event(f'EVENT_CINNABAR_GYM_GATE{index}_UNLOCKED'));S.close_text()
    nav('CinnabarGym',(3,4));E.photo('blaine-six-quiz-doors')
    print('PASS: a wrong answer starts a trainer battle; all six correct answers open the actual doors.',flush=True)
    return E.state()

def blaine_fixture(base,name,starter):
    E.restore(base)
    slots=['BLASTOISE','DUGTRIO']+([] if starter=='BLASTOISE' else [starter])
    S.train(slots,[48]*len(slots));talk('CinnabarGym',(3,4),'up')
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:bool(E.read('wObtainedBadges')&64),name+'-blaine');S.close_text()
    assert E.read('wObtainedBadges')==0x7f and M.event('EVENT_BEAT_BLAINE') and M.event('EVENT_GOT_TM38')
    assert A.item_count(ITEMS['TM38'])==1
    E.press('up',4,20);E.press('a');E.advance_until(lambda:'This demo ends' in E.text());S.close_text()
    assert all(M.event(f'EVENT_BEAT_CINNABAR_GYM_TRAINER_{i}') for i in range(7))
    E.photo(name+'-blaine-complete')
    print('PASS: '+name+' wins the Volcano Badge and TM38 FLAME POUNCE.',flush=True)
    return E.state()

def fossil_talk():
    for _ in range(30):
        x=E.read('wSprite01StateData2MapX')-4
        talk('CinnabarLabFossilRoom',(x,3),'up',cleared=[(5,2)])
        if 'fossil' in E.text() or 'FOSSIL' in E.text() or 'Where were' in E.text() or 'take a little' in E.text():return
    raise AssertionError(('Fossil scientist',E.text()))

def fossils_fixture(base):
    for item,slot in [('DOME_FOSSIL','KABUTO'),('HELIX_FOSSIL','OMANYTE'),('OLD_AMBER','AERODACTYL')]:
        E.restore(base);room_for_rewards();S.train(['BLASTOISE'],[48])
        for other in ('DOME_FOSSIL','HELIX_FOSSIL','OLD_AMBER'):K.remove_item(ITEMS[other])
        add_item(ITEMS[item]);M.warp(mid('CINNABAR_LAB_FOSSIL_ROOM'),0)
        fossil_talk();E.advance_until(lambda:item.replace('_',' ') in E.text());E.press('a')
        E.advance_until(lambda:'YES' in E.text());E.press('a')
        E.advance_until(lambda:M.event('EVENT_GAVE_FOSSIL_TO_LAB'));S.close_text()
        assert not S.has_item(ITEMS[item]) and M.event('EVENT_LAB_STILL_REVIVING_FOSSIL')
        fossil_talk();E.advance_until(lambda:'walk' in E.text());S.close_text();assert E.read('wPartyCount')==1
        city_entry();M.warp(mid('CINNABAR_LAB_FOSSIL_ROOM'),0)
        fossil_talk();E.advance_until(lambda:'give a nickname' in E.text());E.press('down',8,45);E.press('a')
        E.advance_until(lambda:E.read('wPartyCount')==2);S.close_text()
        assert E.read('wPartyMon2Species')==E.IDS[slot] and E.read('wPartyMon2Level')==30
        assert not M.event('EVENT_GAVE_FOSSIL_TO_LAB') and not M.event('EVENT_LAB_HANDING_OVER_FOSSIL_MON')
        E.photo('blaine-revival-'+slot.lower())
    print('PASS: all three fossils are consumed, wait for a city visit, and revive the correct level-30 dog.',flush=True)

def owned_guardian():
    return bool(E.gb.memory[E.SYMS['wPokedexOwned'][1]+143//8]&1<<(143%8))

def guardian_battle():
    talk('SeafoamIslandsB4F',(6,2),'up')
    E.advance_until(lambda:E.read('wIsInBattle')==1)
    assert E.read('wEnemyMonSpecies')==E.IDS['ARTICUNO'] and E.read('wEnemyMonLevel')==50
    E.advance_until(lambda:'FIGHT' in E.text() and 'RUN' in E.text())

def hall_retry(value,caught):
    E.restore(value);count=E.read('wNumHoFTeams')
    M.warp(mid('HALL_OF_FAME'),0)
    E.advance_until(lambda:E.read('wNumHoFTeams')>count and E.read('wHallOfFameCurScript')==0,limit=1600)
    assert M.event('EVENT_BEAT_ARTICUNO')==caught
    assert hidden_object('SEAFOAMISLANDSB4F_ARTICUNO')==caught and owned_guardian()==caught

def guardian_fixture(base):
    E.restore(base);assert not owned_guardian();guardian_battle();E.photo('blaine-frostmaul-battle')
    assert S.has_item(ITEMS['MASTER_BALL'])
    K.battle_option('ITEM');A.select_item(ITEMS['MASTER_BALL']);E.press('a')
    E.advance_until(lambda:'give a nickname' in E.text());E.press('down',8,45);E.press('a')
    E.advance_until(lambda:M.event('EVENT_BEAT_ARTICUNO'));S.close_text()
    assert owned_guardian() and hidden_object('SEAFOAMISLANDSB4F_ARTICUNO') and not S.has_item(ITEMS['MASTER_BALL'])
    assert E.read('wPartyMon4Species')==E.IDS['ARTICUNO'] and E.read('wPartyMon4Level')==50
    caught=E.state();hall_retry(caught,True)
    E.restore(base);guardian_battle()
    for _ in range(15):
        E.advance_until(lambda:('FIGHT' in E.text() and 'RUN' in E.text()) or M.event('EVENT_BEAT_ARTICUNO'))
        if M.event('EVENT_BEAT_ARTICUNO'):break
        K.battle_option('RUN')
    E.advance_until(lambda:M.event('EVENT_BEAT_ARTICUNO'));S.close_text()
    assert not owned_guardian();hall_retry(E.state(),False)
    E.restore(base);S.train(['RAICHU','BLASTOISE'],[55,55]);guardian_battle()
    M.fight_until(lambda:M.event('EVENT_BEAT_ARTICUNO'),'blaine-frostmaul-defeat');S.close_text()
    assert not owned_guardian();hall_retry(E.state(),False)
    E.restore(caught)
    print('PASS: the level-50 guardian can be caught, fled from or defeated; Hall of Fame restores only an uncaught guardian.',flush=True)
    return caught

def tm35_fixture(base):
    E.restore(base);room_for_rewards();M.warp(mid('CINNABAR_LAB_METRONOME_ROOM'),0)
    talk('CinnabarLabMetronomeRoom',(7,3),'up')
    E.advance_until(lambda:M.event('EVENT_GOT_TM35'));S.close_text()
    assert A.item_count(ITEMS['TM35'])==1
    E.press('up',4,20);E.press('a');E.advance_until(lambda:'WILD TRICK' in E.text());S.close_text()
    assert A.item_count(ITEMS['TM35'])==1
    print('PASS: the lab gives TM35 WILD TRICK once.',flush=True)

def coastal_fixture(base):
    E.restore(base);M.warp(mid('SEAFOAM_ISLANDS_1F'),2,last_map=mid('ROUTE_20'))
    E.walk('up',1)
    nav('SeafoamIslands1F',(26,17),warp=True)
    if E.read('wCurMap')==mid('SEAFOAM_ISLANDS_1F'):E.press('down',8,180)
    assert E.read('wCurMap')==mid('ROUTE_20')
    assert M.event('EVENT_SEAFOAM3_BOULDER1_DOWN_HOLE') and owned_guardian()
    nav('Route20',(58,11));E.press('down',4,20);A.field_move('DOG PADDLE')
    E.advance_until(lambda:E.read('wWalkBikeSurfState')==2);S.close_text()
    beaten('EVENT_BEAT_ROUTE_20_TRAINER_',10)
    nav('Route20',(0,14));E.press('left',8,180)
    assert E.read('wCurMap')==mid('CINNABAR_ISLAND')
    nav('CinnabarIsland',(17,12));assert E.read('wWalkBikeSurfState')==0
    E.photo('blaine-cinnabar-coastal-arrival')
    print('PASS: the Seafoam exit preserves completed dams; DOG PADDLE crosses Route 20 and lands on Cinnabar.',flush=True)
    return E.state()

def main():
    try:
        base=S.load_checkpoint('sabrina-complete')
        if '--seafoam-only' in sys.argv:
            seafoam_fixture(base);S.checkpoint('blaine-seafoam');return
        if '--guardian-only' in sys.argv:
            guardian_fixture(S.load_checkpoint('blaine-seafoam'));return
        seafoam=seafoam_fixture(base);S.checkpoint('blaine-seafoam')
        guardian=guardian_fixture(seafoam);S.checkpoint('blaine-guardian')
        guardian=coastal_fixture(guardian)
        if '--from-mansion' in sys.argv:mansion=S.load_checkpoint('blaine-mansion')
        else:mansion=mansion_fixture(guardian);S.checkpoint('blaine-mansion')
        quiz_state=quizzes_fixture(mansion);S.checkpoint('blaine-quizzes')
        completed={name:blaine_fixture(quiz_state,name,starter) for name,starter in [('groen','VENUSAUR'),('shiba','CHARIZARD'),('newf','BLASTOISE')]}
        E.restore(completed['newf']);S.checkpoint('blaine-complete')
        E.save_reload(completed['newf'],expected_map=mid('CINNABAR_GYM'),expected_badges=0x7f)
        assert owned_guardian() and M.event('EVENT_BEAT_ARTICUNO') and hidden_object('SEAFOAMISLANDSB4F_ARTICUNO')
        fossils_fixture(base)
        tm35_fixture(base)
        (E.QA/'blaine-results.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(E.ROM).hexdigest(),'seafoam_boulder_drops_and_currents':True,'guardian_capture_flee_defeat_and_hall_retry':True,'surf_route20_to_cinnabar':True,'mansion_switches_fall_and_secret_key':True,'six_quiz_doors_and_wrong_answer_battle':True,'fossil_revivals':3,'lab_tm35':True,'blaine':list(completed),'save_load_seven_badges_and_caught_guardian':True,'fixture':'trained parties, inventory room, fossil items, room-entry warps, optional trainers and Repel; Hall of Fame entry warp tests the retry hook rather than League progress'},indent=2)+'\n')
    finally:E.gb.stop();E.tmp.cleanup()

if __name__=='__main__':main()
