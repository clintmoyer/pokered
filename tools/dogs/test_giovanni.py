#!/usr/bin/env python3
"""Replay the Power Plant, seven-badge gate, gym spinners and Route 22.

Requires matching-ROM Sabrina and Blaine checkpoints. Trained parties, entry
warps, inventory space, capture balls, optional trainers and Repel are fixtures.
Surf, encounters, capture, badge/TM rewards, rival triggers and saving use inputs.
Hall of Fame entry warps isolate both retry hooks; they do not test the League.
"""
import hashlib
import json
import sys
import test_blaine as B
from test_blaine import E, M, S, A, K, ITEMS, mid, beaten

ARROWS=[(19,11),(19,1),(18,2),(11,2),(16,10),(4,6),(5,13),(4,14),(0,15),(1,15),(13,16),(13,17)]

def nav(name,position,cleared=(),warp=False):
    cleared=list(cleared)
    blocked=[]
    if name=='ViridianGym':
        blocked=[p for p in ARROWS if p!=position]
        if not M.event('EVENT_BEAT_VIRIDIAN_GYM_TRAINER_4'):blocked += [(14,5),(15,5)]
        if not M.event('EVENT_BEAT_VIRIDIAN_GYM_TRAINER_5'):blocked += [(10,2),(10,3)]
        import re
        source=(E.ROOT/'data/maps/objects/ViridianGym.asm').read_text()
        objects=re.findall(r'object_event\s+(\d+),\s*(\d+)',source)
        for index,(x,y) in enumerate(objects,1):
            current=(E.read(f'wSprite{index:02d}StateData2MapX')-4,E.read(f'wSprite{index:02d}StateData2MapY')-4)
            original=(int(x),int(y))
            if current!=original:
                cleared.append(original);blocked.append(current)
    A.navigate(name,position,cleared=cleared,stop_on_warp=warp,live_blocks=True,
               allowed_tiles=(0x14,) if E.read('wWalkBikeSurfState')==2 else (),blocked_tiles=blocked)

def talk(name,position,direction,cleared=()):
    nav(name,position,cleared);E.press(direction,4,20);E.press('a')

def owned(dex):
    return bool(E.gb.memory[E.SYMS['wPokedexOwned'][1]+(dex-1)//8]&1<<((dex-1)%8))

def exit_center(code,name,last_map):
    M.warp(mid(code),0,last_map=mid(last_map));E.walk('up',1)
    nav(name,(3,7),warp=True)
    if E.read('wCurMap')==mid(code):E.press('down',8,180)
    assert E.read('wCurMap')==mid(last_map)

def capture(slot,dex):
    K.battle_option('ITEM');A.select_item(ITEMS['MASTER_BALL']);E.press('a')
    E.advance_until(lambda:'give a nickname' in E.text());E.press('down',8,45);E.press('a')
    E.advance_until(lambda:E.read('wIsInBattle')==0);S.close_text()
    assert owned(dex) and E.read(f'wPartyMon{E.read("wPartyCount")}Species')==E.IDS[slot]

def run_encounter():
    for _ in range(20):
        if E.read('wIsInBattle')==0:break
        E.advance_until(lambda:('FIGHT' in E.text() and 'RUN' in E.text()) or E.read('wIsInBattle')==0)
        if E.read('wIsInBattle')==0:break
        K.battle_option('RUN')
    E.advance_until(lambda:E.read('wIsInBattle')==0);S.close_text()

def power_plant_fixture(base):
    E.restore(base);B.room_for_rewards();S.train(['DUGTRIO','BLASTOISE'],[55,52])
    A.teach_hm(ITEMS['HM03'],'SURF',1)
    beaten('EVENT_BEAT_ROUTE_10_TRAINER_',6)
    exit_center('ROCK_TUNNEL_POKECENTER','RockTunnelPokecenter','ROUTE_10')
    nav('Route10',(14,4));E.press('up',4,20);A.field_move('DOG PADDLE',1)
    E.advance_until(lambda:E.read('wWalkBikeSurfState')==2);S.close_text()
    nav('Route10',(17,3));nav('Route10',(17,46));nav('Route10',(15,46))
    # Cross the western shore, then walk to the original plant entrance.
    nav('Route10',(15,44));assert E.read('wWalkBikeSurfState')==0
    nav('Route10',(6,39),warp=True);assert E.read('wCurMap')==mid('POWER_PLANT')
    E.photo('giovanni-power-plant-surf-entry')
    print('PASS: actual Surf follows Route 10 to the Power Plant and lands at its entrance.',flush=True)
    B.add_item(ITEMS['MASTER_BALL']);nav('PowerPlant',(4,33))
    for attempt in range(400):
        E.write('wRepelRemainingSteps',0);E.press('right' if attempt%2==0 else 'left',8,90)
        if E.read('wIsInBattle')!=1:continue
        E.advance_until(lambda:'FIGHT' in E.text() and 'RUN' in E.text())
        if E.read('wEnemyMonSpecies')==E.IDS['ELECTABUZZ']:
            assert 28<=E.read('wEnemyMonLevel')<=36
            E.photo('giovanni-dalmspark-wild');capture('ELECTABUZZ',125);break
        run_encounter()
    else:raise AssertionError('No natural Dalmatian encounter')
    print('PASS: a natural Power Plant encounter gives a catchable Dalmatian.',flush=True)
    cleared=[]
    for index,(x,y,slot,level) in enumerate([(9,20,'VOLTORB',40),(32,18,'VOLTORB',40),(21,25,'VOLTORB',40),(25,18,'ELECTRODE',43),(23,34,'VOLTORB',40),(26,28,'VOLTORB',40),(21,14,'ELECTRODE',43),(37,32,'VOLTORB',40)]):
        stance,direction=[((9,21),'up'),((33,18),'left'),((21,26),'up'),((25,17),'down'),((22,34),'right'),((26,29),'up'),((20,14),'right'),((38,32),'left')][index]
        talk('PowerPlant',stance,direction,cleared)
        E.advance_until(lambda:E.read('wIsInBattle')==1)
        assert E.read('wEnemyMonSpecies')==E.IDS[slot] and E.read('wEnemyMonLevel')==level
        run_encounter();assert M.event(f'EVENT_BEAT_POWER_PLANT_VOLTORB_{index}')
        cleared.append((x,y))
    for x,y,item in [(26,32,'TM25'),(20,32,'TM33')]:
        talk('PowerPlant',(26,31) if item=='TM25' else (20,33),'down' if item=='TM25' else 'up',cleared)
        E.advance_until(lambda:S.has_item(ITEMS[item]));S.close_text();cleared.append((x,y))
    nav('PowerPlant',(4,10),cleared)
    S.checkpoint('giovanni-plant')
    print('PASS: all eight item-disguised dog encounters and the TM25/TM33 pickups.',flush=True)
    return E.state()

def guardian_battle():
    E.press('up',4,20);E.press('a')
    E.advance_until(lambda:E.read('wIsInBattle')==1)
    assert E.read('wEnemyMonSpecies')==E.IDS['ZAPDOS'] and E.read('wEnemyMonLevel')==50
    E.advance_until(lambda:'FIGHT' in E.text() and 'RUN' in E.text())

def hall_retry(value,caught):
    E.restore(value);count=E.read('wNumHoFTeams');M.warp(mid('HALL_OF_FAME'),0)
    E.advance_until(lambda:E.read('wNumHoFTeams')>count and E.read('wHallOfFameCurScript')==0,limit=1600)
    assert M.event('EVENT_BEAT_ZAPDOS')==caught and B.hidden_object('POWERPLANT_ZAPDOS')==caught and owned(145)==caught
    assert M.event('EVENT_BEAT_ARTICUNO') and B.hidden_object('SEAFOAMISLANDSB4F_ARTICUNO') and owned(144)

def guardian_fixture(base):
    E.restore(base);assert not owned(145);B.add_item(ITEMS['MASTER_BALL']);guardian_battle()
    E.photo('giovanni-stormlaek-battle');capture('ZAPDOS',145)
    assert M.event('EVENT_BEAT_ZAPDOS') and B.hidden_object('POWERPLANT_ZAPDOS')
    caught=E.state();hall_retry(caught,True)
    E.restore(base);guardian_battle();run_encounter();assert not owned(145)
    hall_retry(E.state(),False)
    E.restore(base);S.train(['DUGTRIO','RAICHU','BLASTOISE'],[55]*3);guardian_battle()
    M.fight_until(lambda:M.event('EVENT_BEAT_ZAPDOS'),'giovanni-stormlaek-defeat');S.close_text()
    assert not owned(145);hall_retry(E.state(),False)
    E.restore(caught);S.checkpoint('giovanni-guardian')
    print('PASS: STORMLAEK capture, flee and defeat; only an uncaught guardian returns, while caught FROSTMAUL stays gone.',flush=True)
    return caught

def parcel_story():
    if M.event('EVENT_GOT_POKEDEX'):return
    K.remove_item(ITEMS['POKE_BALL']) # earlier chapter capture fixtures obtained balls before the parcel
    M.warp(mid('VIRIDIAN_MART'),0,last_map=mid('VIRIDIAN_CITY'))
    E.advance_until(lambda:M.event('EVENT_GOT_OAKS_PARCEL'));S.close_text()
    M.warp(mid('OAKS_LAB'),0,last_map=mid('PALLET_TOWN'))
    x=E.read('wSprite05StateData2MapX')-4;y=E.read('wSprite05StateData2MapY')-4
    talk('OaksLab',(x,y+1),'up',cleared=[(5,10),(4,3)])
    E.advance_until(lambda:M.event('EVENT_GOT_POKEDEX') and M.event('EVENT_ROUTE22_RIVAL_WANTS_BATTLE'));S.close_text()
    print('PASS: parcel delivery and the real Pokédex reward open northern Viridian.',flush=True)

def gym_exterior():
    # A room-entry warp places the fixture on the north side of Viridian's
    # ledge, without depending on the opening parcel quest in chapter saves.
    M.warp(mid('VIRIDIAN_GYM'),0,last_map=mid('VIRIDIAN_CITY'));E.walk('up',1)
    nav('ViridianGym',(16,17),warp=True)
    if E.read('wCurMap')==mid('VIRIDIAN_GYM'):E.press('down',8,180)
    assert E.read('wCurMap')==mid('VIRIDIAN_CITY')

def gate_fixture(six,seven):
    E.restore(six);assert E.read('wObtainedBadges')==0x3f
    gym_exterior();E.advance_until(lambda:'locked' in E.text());S.close_text()
    assert not M.event('EVENT_VIRIDIAN_GYM_OPEN') and E.read('wYCoord')==10,(E.read('wXCoord'),E.read('wYCoord'))
    E.restore(seven);assert E.read('wObtainedBadges')==0x7f
    B.room_for_rewards();S.train(['BLASTOISE','DUGTRIO'],[52,52]);gym_exterior()
    assert M.event('EVENT_VIRIDIAN_GYM_OPEN')
    E.press('up',8,180);assert E.read('wCurMap')==mid('VIRIDIAN_GYM')
    print('PASS: six earned badges leave Viridian Gym locked; seven earned badges open the door.',flush=True)
    # Leave the two corridor trainers active: their real approach movement
    # opens the route. Mark the other five optional trainers beaten.
    for i in [1,2,3,6,7]:M.event(f'EVENT_BEAT_VIRIDIAN_GYM_TRAINER_{i}',True)
    nav('ViridianGym',(12,8));E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:M.event('EVENT_BEAT_VIRIDIAN_GYM_TRAINER_0'),'giovanni-gym-trainer');S.close_text()
    for position,index in [((16,6),4),((10,4),5)]:
        nav('ViridianGym',position)
        if index==4:E.press('up',8,180)
        E.advance_until(lambda:E.read('wIsInBattle')==2)
        M.fight_until(lambda:M.event(f'EVENT_BEAT_VIRIDIAN_GYM_TRAINER_{index}'),f'giovanni-corridor-{index}');S.close_text()
    nav('ViridianGym',(14,17));E.press('left',8,960)
    assert (E.read('wXCoord'),E.read('wYCoord'))==(1,17) and E.read('wViridianGymCurScript')==0,(E.read('wXCoord'),E.read('wYCoord'),E.read('wViridianGymCurScript'),E.read('wJoyIgnore'))
    nav('ViridianGym',(0,16));E.press('up',8,960)
    assert (E.read('wXCoord'),E.read('wYCoord'))==(0,7) and E.read('wViridianGymCurScript')==0,(E.read('wXCoord'),E.read('wYCoord'),E.read('wViridianGymCurScript'),E.read('wJoyIgnore'))
    for stance,direction,stop in [((3,6),'right',(4,13)),((4,13),'right',(13,13)),((19,12),'up',(19,2)),((19,2),'up',(11,1))]:
        nav('ViridianGym',stance);E.press(direction,8,960)
        assert (E.read('wXCoord'),E.read('wYCoord'))==stop and E.read('wViridianGymCurScript')==0,stop
    nav('ViridianGym',(2,2));E.photo('giovanni-gym-spinners')
    S.checkpoint('giovanni-gym')
    print('PASS: three gym trainer battles and six real spinner rides reach Giovanni.',flush=True)
    return E.state()

def giovanni_fixture(base,name,starter,rival):
    E.restore(base);slots=[starter,'BLASTOISE','DUGTRIO'] if starter!='BLASTOISE' else ['BLASTOISE','VENUSAUR','DUGTRIO']
    S.train(slots,[52]*len(slots))
    E.write('wPlayerStarter',E.IDS[{'VENUSAUR':'BULBASAUR','CHARIZARD':'CHARMANDER','BLASTOISE':'SQUIRTLE'}[starter]])
    E.write('wRivalStarter',E.IDS[rival]);E.press('up',4,20);E.press('a')
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:E.read('wObtainedBadges')==0xff,name+'-giovanni');S.close_text()
    assert M.event('EVENT_BEAT_VIRIDIAN_GYM_GIOVANNI') and M.event('EVENT_GOT_TM27') and A.item_count(ITEMS['TM27'])==1
    assert M.event('EVENT_2ND_ROUTE22_RIVAL_BATTLE') and M.event('EVENT_ROUTE22_RIVAL_WANTS_BATTLE') and not B.hidden_object('ROUTE22_RIVAL2')
    E.photo(name+'-earth-badge');E.press('up',4,20);E.press('a')
    E.advance_until(lambda:B.hidden_object('VIRIDIANGYM_GIOVANNI'));S.close_text()
    nav('ViridianGym',(10,2),cleared=[(2,1)]);E.press('right',8,960)
    assert (E.read('wXCoord'),E.read('wYCoord'))==(17,2)
    E.press('right',8,960);assert (E.read('wXCoord'),E.read('wYCoord'))==(18,11)
    talk('ViridianGym',(16,14),'down',cleared=[(2,1)])
    E.advance_until(lambda:'This demo ends' in E.text());S.close_text()
    assert A.item_count(ITEMS['TM27'])==1
    print('PASS: '+name+' wins Earth Badge/TM27, triggers the late rival, and sees Giovanni depart.',flush=True)
    return E.state()

def rival_fixture(base,name,starter):
    E.restore(base);S.train(['RAICHU','BLASTOISE','DUGTRIO','VENUSAUR','CHARIZARD','HYPNO'],[56]*6)
    nav('ViridianGym',(16,17),cleared=[(2,1)],warp=True)
    if E.read('wCurMap')==mid('VIRIDIAN_GYM'):E.press('down',8,180)
    E.press('down',8,180) # jump down from the gym-front ledge
    nav('ViridianCity',(0,17));E.press('left',8,180)
    assert E.read('wCurMap')==mid('ROUTE_22')
    nav('Route22',(29,4));E.advance_until(lambda:E.read('wIsInBattle')==2)
    expected={'groen':12,'shiba':10,'newf':11}[name];assert E.read('wTrainerNo')==expected
    M.fight_until(lambda:M.event('EVENT_BEAT_ROUTE22_RIVAL_2ND_BATTLE') and E.read('wRoute22CurScript')==7,name+'-route22',limit=420);S.close_text()
    assert B.hidden_object('ROUTE22_RIVAL2') and not M.event('EVENT_ROUTE22_RIVAL_WANTS_BATTLE')
    assert not M.event('EVENT_2ND_ROUTE22_RIVAL_BATTLE') and E.read('wObtainedBadges')==0xff
    E.photo(name+'-route22-complete')
    print('PASS: '+name+' late Route 22 rival, earned trigger and departure.',flush=True)
    return E.state()

def early_fixture():
    base=E.bootstrap()
    for name,x,slot,rival,breed in [('groen',8,'BULBASAUR','CHARMANDER','GROENENDAEL'),('shiba',6,'CHARMANDER','SQUIRTLE','SHIBA INU'),('newf',7,'SQUIRTLE','BULBASAUR','NEWFOUNDLAND')]:
        E.restore(base);E.choose_starter(x,{'groen':'GROENPUP','shiba':'SHIBAPUP','newf':'NEWFPUP'}[name],breed,(slot,rival))
        parcel_story()
        S.train([slot,'MANKEY'],[12,12])
        exit_center('VIRIDIAN_POKECENTER','ViridianPokecenter','VIRIDIAN_CITY')
        nav('ViridianCity',(0,17));E.press('left',8,180)
        assert E.read('wCurMap')==mid('ROUTE_22')
        nav('Route22',(29,4));E.advance_until(lambda:E.read('wIsInBattle')==2)
        M.fight_until(lambda:M.event('EVENT_BEAT_ROUTE22_RIVAL_1ST_BATTLE') and E.read('wRoute22CurScript')==0,name+'-route22-early');S.close_text()
        assert not M.event('EVENT_1ST_ROUTE22_RIVAL_BATTLE') and not M.event('EVENT_ROUTE22_RIVAL_WANTS_BATTLE')
        print('PASS: '+name+' early Route 22 rival team and departure.',flush=True)
    (E.QA/'giovanni-early-results.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(E.ROM).hexdigest(),'new_game_starters_and_tutorial':3,'parcel_delivery_and_pokedex':3,'early_rival_teams_and_departures':3,'fixture':'level-12 trained parties and building-entry warps; quest rewards, rival triggers and battles use inputs'},indent=2)+'\n')

def main():
    try:
        if '--early' in sys.argv:early_fixture();return
        if '--from-plant' in sys.argv:plant=S.load_checkpoint('giovanni-plant')
        else:plant=power_plant_fixture(S.load_checkpoint('blaine-complete'))
        if '--plant-only' in sys.argv:return
        guardian=S.load_checkpoint('giovanni-guardian') if '--from-guardian' in sys.argv else guardian_fixture(plant)
        gym=gate_fixture(S.load_checkpoint('sabrina-complete'),guardian)
        done={}
        for name,starter,rival in [('groen','VENUSAUR','CHARMANDER'),('shiba','CHARIZARD','SQUIRTLE'),('newf','BLASTOISE','BULBASAUR')]:
            won=giovanni_fixture(gym,name,starter,rival);done[name]=rival_fixture(won,name,starter)
        E.restore(done['newf']);S.checkpoint('giovanni-complete')
        E.save_reload(E.state(),expected_map=mid('ROUTE_22'),expected_badges=0xff)
        assert E.read('wObtainedBadges')==0xff and owned(125) and owned(144) and owned(145)
        assert M.event('EVENT_BEAT_ROUTE22_RIVAL_2ND_BATTLE') and M.event('EVENT_GOT_TM27')
        assert A.item_count(ITEMS['TM27'])==1 and E.read('wBeatGymFlags')==0xff
        assert B.hidden_object('POWERPLANT_ZAPDOS') and B.hidden_object('SEAFOAMISLANDSB4F_ARTICUNO')
        assert all(S.has_item(ITEMS[f'HM{i:02d}']) for i in range(1,6))
        (E.QA/'giovanni-results.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(E.ROM).hexdigest(),'route10_surf_entry':True,'natural_dalmatian_capture':True,'static_dogs':8,'plant_tms':[25,33],'storm_guardian_capture_flee_defeat_and_retry':True,'caught_frostmaul_preserved':True,'earned_six_seven_badge_gate':True,'three_gym_trainers_and_six_spinners':True,'giovanni_and_late_rivals':list(done),'eight_badge_save_load':True,'fixture':__doc__},indent=2)+'\n')
        print('PASS: eight-badge save/load preserves both caught guardians, Dalmatian, late rival victory, TM27 and all five HMs.',flush=True)
    finally:E.gb.stop();E.tmp.cleanup()

if __name__=='__main__':main()
