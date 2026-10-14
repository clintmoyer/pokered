#!/usr/bin/env python3
"""Replay badge checkpoints, Victory Road, the League and Hall of Fame.

Requires matching-ROM Blaine/Giovanni checkpoints. Parties, money, capture balls,
PP supplies, entry warps, optional trainer flags and Repel are fixtures. Badge
gates, Surf, boulder pushes, falls, battles, purchases, healing, Hall of Fame and
Continue use game inputs; no puzzle, capture or League victory flags are injected.
"""
from collections import deque
import hashlib
import json
import re
import sys
from pyboy import PyBoy
import test_giovanni as G
from test_giovanni import E,M,S,A,K,B,ITEMS,mid,beaten

PLAN=json.loads((E.ROOT/'data/dogs/league.json').read_text())
BY_NAME={d['name']:d for d in E.DOGS}
DIRECTIONS=[('up',(0,-1)),('down',(0,1)),('left',(-1,0)),('right',(1,0))]

def objects(name):
    source=(E.ROOT/f'data/maps/objects/{name}.asm').read_text()
    names=re.findall(r'const_export (\w+)',source)
    return [(index,(int(x),int(y)),sprite,names[index-1])
            for index,(x,y,sprite) in enumerate(re.findall(r'object_event\s+(\d+),\s*(\d+),\s*(\w+)',source),1)]

def xy(index):
    return E.read(f'wSprite{index:02d}StateData2MapX')-4,E.read(f'wSprite{index:02d}StateData2MapY')-4

def nav(name,target,warp=False,cleared=()):
    blocked=[(23,15)] if name=='VictoryRoad3F' and target!=(23,15) else []
    if name=='Route23' and E.read('wWalkBikeSurfState')==2:blocked += [(8,90),(9,90),(8,91),(9,91)]
    cleared=list(cleared)
    for index,original,sprite,label in objects(name):
        if sprite=='SPRITE_BOULDER':
            cleared.append(original)
            if not B.hidden_object(label):blocked.append(xy(index))
    if name=='VictoryRoad1F' and target in [(8,17),(9,17)] and not warp:
        nav(name,(7,17))
        for _ in range(target[0]-7):E.press('right',8,60)
        assert (E.read('wXCoord'),E.read('wYCoord'))==target
        return
    A.navigate(name,target,cleared=cleared,stop_on_warp=warp,live_blocks=True,
               allowed_tiles=(0x14,) if E.read('wWalkBikeSurfState')==2 else (),blocked_tiles=blocked)

def talk(name,target,direction,cleared=()):
    nav(name,target,cleared=cleared);E.press(direction,4,20);E.press('a')

def map_grid(name):
    code,tileset=re.search(r'map_header \w+, (\w+), (\w+)',(E.ROOT/f'data/maps/headers/{name}.asm').read_text()).groups()
    _,width,height=A.MAPS[code];stride=width//2+6
    address=E.SYMS['wOverworldMap'][1]+3*stride+3
    blocks=bytes(E.gb.memory[address+y*stride+x] for y in range(height//2) for x in range(width//2))
    label=''.join(p.capitalize() for p in tileset.split('_'));pos=E.rom_offset(label+'_Block');tiles=E.ROM[pos:pos+4096]
    pos=E.rom_offset(label+'_Coll');allowed=set(E.ROM[pos:E.ROM.index(255,pos)])
    foot={(x,y):tiles[blocks[(y//2)*(width//2)+x//2]*16+y%2*8+x%2*2+4] for y in range(height) for x in range(width)}
    return foot,{p for p,t in foot.items() if t in allowed}

def push_to(name,index,goal):
    # Find a route through the loaded cave, then execute every walk and push.
    # This is navigation planning only: the game must move each boulder and
    # set its switch/hole event itself.
    foot,walkable=map_grid(name)
    blocked={xy(i) for i,_,sprite,label in objects(name) if i!=index and not B.hidden_object(label)}
    source=(E.ROOT/f'data/maps/objects/{name}.asm').read_text()
    blocked|={(int(x),int(y)) for x,y in re.findall(r'warp_event\s+(\d+),\s*(\d+)',source) if not (name=='VictoryRoad1F' and int(y)==17)}
    hole={(23,15)} if name=='VictoryRoad3F' else set()
    forbidden={frozenset((a,b)) for a,b in [(0x20,0x05),(0x41,0x05),(0x2a,0x05),(0x05,0x21)]}
    def connected(a,b):return a in foot and b in foot and frozenset((foot[a],foot[b])) not in forbidden
    def region(player,box):
        seen={player};queue=deque([player])
        while queue:
            x,y=queue.popleft()
            for _,(dx,dy) in DIRECTIONS:
                p=(x+dx,y+dy)
                if p in walkable and p not in blocked|hole|{box} and p not in seen and connected((x,y),p):seen.add(p);queue.append(p)
        return seen
    player=(E.read('wXCoord'),E.read('wYCoord'));box=xy(index)
    queue=deque([(box,player,[])]);seen=set();solution=None
    while queue:
        box,player,path=queue.popleft()
        if box==goal:solution=path;break
        reachable=region(player,box);key=(box,min(reachable))
        if key in seen:continue
        seen.add(key)
        for direction,(dx,dy) in DIRECTIONS:
            stance=(box[0]-dx,box[1]-dy);destination=(box[0]+dx,box[1]+dy)
            if stance in reachable and destination in walkable and destination not in blocked and foot[destination]!=0x15 and connected(stance,destination):
                queue.append((destination,box,path+[(stance,direction,destination)]))
    assert solution is not None,('No push route',name,index,xy(index),goal)
    for stance,direction,destination in solution:
        nav(name,stance);B.push(direction)
        assert xy(index)==destination,(name,index,xy(index),destination)
    print(f'PASS: {name} boulder {index} reaches {goal} in {len(solution)} real pushes.',flush=True)

def boulder_gate_fixture():
    base=E.bootstrap();E.restore(base);E.choose_starter(7,'NEWFPUP','NEWFOUNDLAND',('SQUIRTLE','BULBASAUR'))
    M.warp(mid('ROUTE_22_GATE'),0,last_map=mid('ROUTE_22'))
    nav('Route22Gate',(4,3));E.press('up',8,90)
    E.advance_until(lambda:'BOULDERBADGE' in E.text());S.close_text()
    assert E.read('wObtainedBadges')==0 and E.read('wYCoord')==3 and E.read('wRoute22GateCurScript')==0
    print('PASS: the original Boulder Badge gate rejects a new game.',flush=True)

def route23_fixture(base,earth):
    E.restore(base);B.room_for_rewards();S.train(['BLASTOISE','RATICATE','RAICHU'],[52]*3)
    A.teach_hm(ITEMS['HM03'],'SURF',0);A.teach_hm(ITEMS['HM04'],'STRENGTH',1)
    M.warp(mid('ROUTE_22_GATE'),0,last_map=mid('ROUTE_22'))
    nav('Route22Gate',(4,3));E.press('up',8,90)
    E.advance_until(lambda:E.read('wRoute22GateCurScript')==2);S.close_text()
    nav('Route22Gate',(4,0),warp=True)
    if E.read('wCurMap')==mid('ROUTE_22_GATE'):E.press('up',8,180)
    assert E.read('wCurMap')==mid('ROUTE_23')
    for x,y,badge in [(7,136,'CASCADE'),(9,119,'THUNDER'),(10,105,'RAINBOW'),(10,96,'SOUL'),(10,85,'MARSH'),(9,56,'VOLCANO'),(6,35,'EARTH')]:
        if badge=='SOUL':
            nav('Route23',(10,104));E.press('up',4,20);A.field_move('DOG PADDLE',0)
            E.advance_until(lambda:E.read('wWalkBikeSurfState')==2);S.close_text()
        if badge=='VOLCANO':
            nav('Route23',(10,68));assert E.read('wWalkBikeSurfState')==0
        nav('Route23',(x,y+1));E.press('up',8,90)
        event=f'EVENT_PASSED_{badge}BADGE_CHECK'
        if badge=='EARTH' and not earth:
            E.advance_until(lambda:'yet' in E.text());S.close_text()
            assert not M.event(event) and E.read('wYCoord')==36
            print('PASS: seven earned badges pass the earlier guards but fail the Earth Badge checkpoint.',flush=True)
            return
        E.advance_until(lambda:M.event(event));S.close_text()
    nav('Route23',(4,31),warp=True);assert E.read('wCurMap')==mid('VICTORY_ROAD_1F')
    E.photo('league-route23-eight-badges')
    print('PASS: all eight badge checkpoints, real Route 23 Surf and landing, and Victory Road entry.',flush=True)
    return E.state()

def victory_road_fixture(base):
    E.restore(base)
    for floor,count in [(1,2),(2,5),(3,4)]:beaten(f'EVENT_BEAT_VICTORY_ROAD_{floor}_TRAINER_',count)
    M.event('EVENT_BEAT_VICTORY_ROAD_1_TRAINER_0',False) # optional battle under test
    B.haul();assert not M.event('EVENT_VICTORY_ROAD_1_BOULDER_ON_SWITCH')
    push_to('VictoryRoad1F',5,(17,13));assert M.event('EVENT_VICTORY_ROAD_1_BOULDER_ON_SWITCH')
    talk('VictoryRoad1F',(7,6),'up');E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:M.event('EVENT_BEAT_VICTORY_ROAD_1_TRAINER_0'),'league-road-trainer');S.close_text()
    nav('VictoryRoad1F',(1,1),warp=True);assert E.read('wCurMap')==mid('VICTORY_ROAD_2F');B.haul()
    push_to('VictoryRoad2F',11,(1,16));assert M.event('EVENT_VICTORY_ROAD_2_BOULDER_ON_SWITCH1')
    nav('VictoryRoad2F',(23,7),warp=True);assert E.read('wCurMap')==mid('VICTORY_ROAD_3F');B.haul()
    push_to('VictoryRoad3F',7,(3,5));assert M.event('EVENT_VICTORY_ROAD_3_BOULDER_ON_SWITCH1')
    nav('VictoryRoad3F',(2,0),warp=True);assert E.read('wCurMap')==mid('VICTORY_ROAD_2F')
    nav('VictoryRoad2F',(11,6));E.photo('league-sunmast-island');S.checkpoint('league-guardian-base')
    return E.state()

def guardian_battle():
    E.press('up',4,20);E.press('a');E.advance_until(lambda:E.read('wIsInBattle')==1)
    assert E.read('wEnemyMonSpecies')==E.IDS['MOLTRES'] and E.read('wEnemyMonLevel')==50
    E.advance_until(lambda:'FIGHT' in E.text() and 'RUN' in E.text())

def guardian_cases(base):
    E.restore(base);B.add_item(ITEMS['MASTER_BALL']);guardian_battle();E.photo('league-sunmast-battle');G.capture('MOLTRES',146)
    caught=E.state();assert M.event('EVENT_BEAT_MOLTRES') and B.hidden_object('VICTORYROAD2F_MOLTRES')
    E.restore(base);guardian_battle();G.run_encounter();assert M.event('EVENT_BEAT_MOLTRES') and not G.owned(146);fled=E.state()
    E.restore(base);S.train(['BLASTOISE','RAICHU','RATICATE'],[55]*3);guardian_battle()
    M.fight_until(lambda:M.event('EVENT_BEAT_MOLTRES'),'league-sunmast-defeat');S.close_text();assert not G.owned(146);defeated=E.state()
    for label,value in [('caught',caught),('fled',fled),('defeated',defeated)]:E.restore(value);S.checkpoint('league-sunmast-'+label)
    print('PASS: the level-50 SUNMAST encounter supports capture, flee and defeat.',flush=True)
    return caught,fled,defeated

def road_exit_fixture(base):
    E.restore(base);nav('VictoryRoad2F',(1,1),warp=True);assert E.read('wCurMap')==mid('VICTORY_ROAD_3F');B.haul()
    push_to('VictoryRoad3F',10,(23,15))
    assert M.event('EVENT_VICTORY_ROAD_3_BOULDER_ON_SWITCH2') and B.hidden_object('VICTORYROAD3F_BOULDER4')
    nav('VictoryRoad3F',(23,15),warp=True);E.gb.tick(360)
    assert E.read('wCurMap')==mid('VICTORY_ROAD_2F');B.haul()
    push_to('VictoryRoad2F',13,(9,16));assert M.event('EVENT_VICTORY_ROAD_2_BOULDER_ON_SWITCH2')
    nav('VictoryRoad2F',(25,14),warp=True);assert E.read('wCurMap')==mid('VICTORY_ROAD_3F')
    nav('VictoryRoad3F',(26,8),warp=True);assert E.read('wCurMap')==mid('VICTORY_ROAD_2F')
    nav('VictoryRoad2F',(29,7),warp=True)
    if E.read('wCurMap')==mid('VICTORY_ROAD_2F'):E.press('right',8,180)
    assert E.read('wCurMap')==mid('ROUTE_23')
    nav('Route23',(9,0));E.press('up',8,180);assert E.read('wCurMap')==mid('INDIGO_PLATEAU')
    nav('IndigoPlateau',(9,5),warp=True);assert E.read('wCurMap')==mid('INDIGO_PLATEAU_LOBBY')
    E.photo('league-indigo-arrival');S.checkpoint('league-lobby')
    print('PASS: the 3F boulder fall, actual dungeon fall, final 2F switch, cave exit and Indigo Plateau arrival.',flush=True)
    return E.state()

def buy(item,index,quantity):
    before=A.item_count(ITEMS[item]);talk('IndigoPlateauLobby',(2,5),'left')
    E.advance_until(lambda:'BUY' in E.text());E.press('a')
    for _ in range(30):
        current=E.read('wCurrentMenuItem')+E.read('wListScrollOffset')
        if current==index:break
        E.press('down' if current<index else 'up',8,45)
    else:raise AssertionError(('Mart selection',item))
    E.press('a')
    for _ in range(quantity-1):E.press('up',8,45)
    E.press('a');E.advance_until(lambda:'YES' in E.text());E.press('a')
    E.advance_until(lambda:A.item_count(ITEMS[item])==before+quantity);S.close_text()

def nurse():
    talk('IndigoPlateauLobby',(7,7),'up');E.advance_until(lambda:'HEAL' in E.text() and 'CANCEL' in E.text());E.press('a')
    E.advance_until(lambda:all(M.word(f'wPartyMon{i}HP')==M.word(f'wPartyMon{i}MaxHP') and E.read(f'wPartyMon{i}Status')==0 for i in range(1,E.read('wPartyCount')+1)));S.close_text()
    print('PASS: Indigo Plateau nurse heals the party through the normal recovery script.',flush=True)

def prepare_party(starter):
    slots=[starter,'RAICHU','HYPNO','JYNX','DUGTRIO','BLASTOISE' if starter!='BLASTOISE' else 'CHARIZARD']
    S.train(slots,[64]*6);B.room_for_rewards();E.write('wPlayerMoney',[0x15,0,0])
    for item in ['FULL_RESTORE','REVIVE','MAX_ELIXER']:K.remove_item(ITEMS[item])
    buy('FULL_RESTORE',2,20);buy('REVIVE',5,10)
    B.add_item(ITEMS['MAX_ELIXER']);address=E.SYMS['wBagItems'][1]
    # PP restorers represent supplies collected earlier; they are not sold here.
    E.gb.memory[address+S.bag()[::2].index(ITEMS['MAX_ELIXER'])*2+1]=12
    assert A.item_count(ITEMS['FULL_RESTORE'])==20 and A.item_count(ITEMS['REVIVE'])==10
    print('PASS: the lobby mart sells actual League healing and revival supplies.',flush=True)

def use_on_party(item,index,done):
    before=A.item_count(ITEMS[item]);E.start_option('ITEM');A.select_item(ITEMS[item]);E.press('a');E.press('a')
    S.choose_party(index);E.advance_until(done);S.close_text()
    assert A.item_count(ITEMS[item])==before-1,(item,index)

def heal_party():
    for i in range(1,E.read('wPartyCount')+1):
        if M.word(f'wPartyMon{i}HP')==0:use_on_party('REVIVE',i-1,lambda i=i:M.word(f'wPartyMon{i}HP')>0)
        if M.word(f'wPartyMon{i}HP')<M.word(f'wPartyMon{i}MaxHP') or E.read(f'wPartyMon{i}Status'):
            use_on_party('FULL_RESTORE',i-1,lambda i=i:M.word(f'wPartyMon{i}HP')==M.word(f'wPartyMon{i}MaxHP') and E.read(f'wPartyMon{i}Status')==0)
        moves=E.SYMS[f'wPartyMon{i}Moves'][1];pp=E.SYMS[f'wPartyMon{i}PP'][1]
        if any(E.gb.memory[moves+j] and E.gb.memory[pp+j]&63<5 for j in range(4)):
            use_on_party('MAX_ELIXER',i-1,lambda i=i,pp=pp:all(not E.gb.memory[moves+j] or E.gb.memory[pp+j]&63>=5 for j in range(4)))

def lead(slot):
    if E.read('wPartyMon1Species')==E.IDS[slot]:return
    index=next(i for i in range(E.read('wPartyCount')) if E.read(f'wPartyMon{i+1}Species')==E.IDS[slot])
    E.start_option('POKéMON');S.choose_party(index);E.advance_until(lambda:'SWITCH' in E.text());M.select_row('SWITCH');E.press('a');S.choose_party(0);S.close_text()
    assert E.read('wPartyMon1Species')==E.IDS[slot]

def enemy_team(label,index):
    members=PLAN['trainers'][label][str(index)]
    assert E.read('wEnemyPartyCount')==len(members)
    for n,(level,name) in enumerate(members,1):
        dog=BY_NAME[name]
        assert E.read(f'wEnemyMon{n}Species')==E.IDS[dog['slot']] and E.read(f'wEnemyMon{n}Level')==level
        legal={E.MIDS[E.MOVES[m][0]] for m in list(dog['base'])+[m for l,m in dog['learnset'] if l<=level]}
        legal|={E.MIDS[m] for m in dog['tms']}
        address=E.SYMS[f'wEnemyMon{n}Moves'][1]
        assert set(E.gb.memory[address:address+4])<=(legal|{0}),(name,list(E.gb.memory[address:address+4]))
    if label=='Rival3Data':
        for n,key in [(1,'lead'),(6,{1:'water',2:'grass',3:'fire'}[index])]:
            assert E.gb.memory[E.SYMS[f'wEnemyMon{n}Moves'][1]+3]==E.MIDS[E.MOVES[PLAN['champion_moves'][key]][0]]
    else:
        trainer={'LoreleiData':'LORELEI','BrunoData':'BRUNO','AgathaData':'AGATHA','LanceData':'LANCE'}[label]
        assert E.gb.memory[E.SYMS['wEnemyMon5Moves'][1]+3]==E.MIDS[E.MOVES[PLAN['boss_moves'][trainer]][0]]

def enter_lorelei():
    nav('IndigoPlateauLobby',(8,0),warp=True)
    assert E.read('wCurMap')==mid('LORELEIS_ROOM')
    E.advance_until(lambda:E.read('wJoyIgnore')==0 and M.event('EVENT_AUTOWALKED_INTO_LORELEIS_ROOM'))
    assert not M.event('EVENT_BEAT_LORELEIS_ROOM_TRAINER_0')

def league_battle(room,label,event,name):
    if room=='LancesRoom':
        nav(room,(6,3));E.press('up',8,180)
    else:talk(room,(5,3),'up')
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    E.advance_until(lambda:'FIGHT' in E.text() and 'RUN' in E.text());enemy_team(label,1)
    M.fight_until(lambda:M.event(event),name+'-'+room.lower(),limit=420);S.close_text()
    E.photo(name+'-'+room.lower()+'-won')
    print('PASS: '+name+' defeats '+label.removesuffix('Data')+' with the planned dog team and legal ace move.',flush=True)

def hall_continue(name,caught):
    previous=E.read('wNumHoFTeams')
    E.advance_until(lambda:E.read('wNumHoFTeams')>previous and E.read('wHallOfFameCurScript')==0,limit=1600)
    # Wait until the reset/retry/save routine has actually finished.
    E.gb.tick(1200)
    assert E.read('wSaveFileStatus')==2 and E.read('wNumHoFTeams')==previous+1
    expected=[(E.read(f'wPartyMon{i}Species'),E.read(f'wPartyMon{i}Level')) for i in range(1,7)]
    S.checkpoint('league-before-continue')
    E.gb.stop();E.gb=PyBoy(str(E.rom_path),window='null',sound_emulated=False);E.gb.set_emulation_speed(0)
    E.gb.tick(2000);E.press('start',wait=330);assert 'CONTINUE' in E.text();E.press('a',wait=600)
    E.advance_until(lambda:E.read('wCurMap')==mid('PALLET_TOWN') and 'CONTINUE' not in E.text())
    assert E.read('wCurMap')==mid('PALLET_TOWN') and E.read('wNumHoFTeams')==previous+1 and E.read('wObtainedBadges')==0xff,(E.read('wCurMap'),E.read('wNumHoFTeams'),previous,E.read('wObtainedBadges'),E.text())
    assert E.read('wElite4Flags')&1 and not M.event('EVENT_BEAT_CHAMPION_RIVAL')
    assert all(not M.event(f'EVENT_BEAT_{room}_ROOM_TRAINER_0') for room in ['LORELEIS','BRUNOS','AGATHAS','LANCES'])
    assert all(E.read(f'w{room}CurScript')==0 for room in ['LoreleisRoom','BrunosRoom','AgathasRoom','LancesRoom'])
    assert G.owned(146)==caught and M.event('EVENT_BEAT_MOLTRES')==caught and B.hidden_object('VICTORYROAD2F_MOLTRES')==caught
    assert all(G.owned(dex) for dex in [144,145]) and B.hidden_object('POWERPLANT_ZAPDOS') and B.hidden_object('SEAFOAMISLANDSB4F_ARTICUNO')
    assert all(A.item_count(ITEMS[f'HM{i:02d}'])==1 for i in range(1,6))
    # Read the current saved Hall of Fame team without modifying SRAM content.
    bank,address=E.SYMS['sHallOfFame'];E.gb.memory[0x0000]=0x0a;E.gb.memory[0x4000]=bank
    address+=min(previous,49)*96 # current Hall entry, including postgame rematches
    record=list(E.gb.memory[address:address+96]);E.gb.memory[0x0000]=0
    assert [(record[i*16],record[i*16+1]) for i in range(6)]==expected
    for i,(species,_) in enumerate(expected):
        dog=next(d for d in E.DOGS if E.IDS[d['slot']]==species)
        nickname=''.join(E.CHARS.get(v,'?') for v in record[i*16+2:i*16+13] if v!=0x50)
        assert nickname==dog['name'],(dog['name'],nickname)
    E.photo(name+'-champion-continue');S.checkpoint('league-complete-'+name)
    print('PASS: '+name+' Champion, six dog Hall of Fame entries, automatic save, Pallet Continue and guardian retry state.',flush=True)
    return E.state()

def league_fixture(base,name,starter,rival,caught,warp=True):
    E.restore(base)
    if warp:M.warp(mid('INDIGO_PLATEAU_LOBBY'),0,last_map=mid('INDIGO_PLATEAU'))
    nurse();prepare_party(starter)
    E.write('wPlayerStarter',E.IDS[{'VENUSAUR':'BULBASAUR','CHARIZARD':'CHARMANDER','BLASTOISE':'SQUIRTLE'}[starter]])
    E.write('wRivalStarter',E.IDS[rival]);lead('RAICHU');enter_lorelei()
    for room,label,event,counter,next_room in [
        ('LoreleisRoom','LoreleiData','EVENT_BEAT_LORELEIS_ROOM_TRAINER_0','RAICHU','BRUNOS_ROOM'),
        ('BrunosRoom','BrunoData','EVENT_BEAT_BRUNOS_ROOM_TRAINER_0','HYPNO','AGATHAS_ROOM'),
        ('AgathasRoom','AgathaData','EVENT_BEAT_AGATHAS_ROOM_TRAINER_0','HYPNO','LANCES_ROOM'),
        ('LancesRoom','LanceData','EVENT_BEAT_LANCE','JYNX','CHAMPIONS_ROOM')]:
        heal_party();lead(counter);league_battle(room,label,event,name)
        if name=='groen' and room=='LoreleisRoom':S.checkpoint('league-after-lorelei')
        heal_party()
        if room=='LancesRoom':lead('RAICHU');target=(5,0)
        else:target=(4,0)
        nav(room,target,warp=True)
        code=re.search(r'map_header \w+, (\w+)',(E.ROOT/f'data/maps/headers/{room}.asm').read_text())[1]
        if E.read('wCurMap')==mid(code):E.press('up',8,240)
        assert E.read('wCurMap')==mid(next_room)
        if next_room!='CHAMPIONS_ROOM':E.advance_until(lambda:E.read('wJoyIgnore')==0)
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    E.advance_until(lambda:'FIGHT' in E.text() and 'RUN' in E.text())
    index={'groen':3,'shiba':1,'newf':2}[name];assert E.read('wTrainerNo')==index;enemy_team('Rival3Data',index)
    M.fight_until(lambda:M.event('EVENT_BEAT_CHAMPION_RIVAL'),name+'-champion',limit=540)
    assert E.read('wObtainedBadges')==0xff
    return hall_continue(name,caught)

def loss_fixture():
    E.restore(S.load_checkpoint('league-after-lorelei'));S.train(['MAGIKARP'],[5])
    nav('LoreleisRoom',(4,0),warp=True)
    if E.read('wCurMap')==mid('LORELEIS_ROOM'):E.press('up',8,240)
    E.advance_until(lambda:E.read('wJoyIgnore')==0)
    talk('BrunosRoom',(5,3),'up');E.advance_until(lambda:E.read('wIsInBattle')==2)
    for _ in range(400):
        if E.read('wIsInBattle')==0 and E.read('wCurMap') in [mid('INDIGO_PLATEAU'),mid('INDIGO_PLATEAU_LOBBY')]:break
        E.press('a',wait=240)
    else:raise AssertionError(('League blackout',E.read('wCurMap'),E.text()))
    if E.read('wCurMap')==mid('INDIGO_PLATEAU'):nav('IndigoPlateau',(9,5),warp=True)
    assert E.read('wCurMap')==mid('INDIGO_PLATEAU_LOBBY')
    assert not M.event('EVENT_BEAT_LORELEIS_ROOM_TRAINER_0') and not M.event('EVENT_BEAT_BRUNOS_ROOM_TRAINER_0')
    assert not E.read('wElite4Flags')&2 and E.read('wNumHoFTeams')==0
    enter_lorelei();assert M.event('EVENT_AUTOWALKED_INTO_LORELEIS_ROOM')
    print('PASS: an actual Bruno loss returns to the lobby, resets the won Lorelei round, and restarts the challenge.',flush=True)

def main():
    try:
        if '--league-only' in sys.argv:
            lobby=S.load_checkpoint('league-lobby');fled=S.load_checkpoint('league-sunmast-fled');defeated=S.load_checkpoint('league-sunmast-defeated')
        else:
            if '--from-road' in sys.argv:road=S.load_checkpoint('league-road')
            else:
                boulder_gate_fixture();route23_fixture(S.load_checkpoint('blaine-complete'),False)
                road=route23_fixture(S.load_checkpoint('giovanni-complete'),True);S.checkpoint('league-road')
            if '--gates' in sys.argv:return
            guardian=S.load_checkpoint('league-guardian-base') if '--from-guardian' in sys.argv else victory_road_fixture(road)
            if '--road' in sys.argv:return
            caught,fled,defeated=guardian_cases(guardian);lobby=road_exit_fixture(caught)
            if '--exit' in sys.argv:return
        completed={}
        for name,starter,rival,value,caught in [
            ('groen','VENUSAUR','CHARMANDER',lobby,True),
            ('shiba','CHARIZARD','SQUIRTLE',fled,False),
            ('newf','BLASTOISE','BULBASAUR',defeated,False)]:
            completed[name]=league_fixture(value,name,starter,rival,caught,warp=name!='groen')
        loss_fixture();E.restore(completed['newf']);S.checkpoint('league-complete')
        (E.QA/'league-results.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(E.ROM).hexdigest(),'boulder_gate_rejection':True,'seven_badge_earth_rejection':True,'all_eight_badge_checks_and_surf':True,'victory_road_real_switches_and_fall':True,'sunmast_capture_flee_defeat_and_earned_hall_retry':True,'lobby_nurse_and_mart':True,'five_battle_league_runs':list(completed),'all_champion_variants':True,'six_dog_hall_records_and_pallet_continue':True,'loss_resets_challenge':True,'fixture':__doc__},indent=2)+'\n')
    finally:E.gb.stop();E.tmp.cleanup()

if __name__=='__main__':main()
