#!/usr/bin/env python3
"""Replay Flash, Rock Tunnel traversal, Fly, Celadon collection, and Erika.

Trained parties, money, capture-count variants and map warps are fixtures. Cave
and optional gym trainers are marked beaten during navigation. All HM rewards,
teaching, field effects, purchases, evolutions, battles and saving use game inputs.
"""
from collections import deque
import hashlib
import json
import re
import sys
import test_surge as S
from test_surge import E, M

ITEMS=E.constants('constants/item_constants.asm')
for kind in ('hm','tm'):
    source=(E.ROOT/'constants/item_constants.asm').read_text()
    for index,hex_id in enumerate(re.findall(rf'^\s*add_{kind} \w+\s*; \$([\dA-F]+)',source,re.M),1):
        ITEMS[f'{kind.upper()}{index:02d}']=int(hex_id,16)
MAPS={}
for code,width,height,hex_id in re.findall(r'^\s*map_const (\w+),\s*(\d+),\s*(\d+)\s*; \$([\dA-F]+)',(E.ROOT/'constants/map_constants.asm').read_text(),re.M):
    MAPS[code]=(int(hex_id,16),int(width)*2,int(height)*2)

def item_count(item):
    return next((qty for key,qty in zip(S.bag()[::2],S.bag()[1::2]) if key==item),0)

def select_item(item):
    target=S.bag()[::2].index(item)
    for _ in range(30):
        current=E.read('wCurrentMenuItem')+E.read('wListScrollOffset')
        if current==target:return
        E.press('down' if current<target else 'up',8,45)
    raise AssertionError(('Item selection',item,E.text()))

def teach_hm(item,move,index=0):
    E.start_option('ITEM');select_item(item);E.press('a');E.press('a')
    E.advance_until(lambda:'YES' in E.text() and 'NO' in E.text());E.press('a')
    E.advance_until(lambda:'ABLE' in E.text());S.choose_party(index)
    for _ in range(100):
        address=E.SYMS[f'wPartyMon{index+1}Moves'][1]
        if E.MIDS[move] in E.gb.memory[address:address+4]:break
        E.press('b' if 'Abandon learning' in E.text() else 'a')
    else:raise AssertionError(('HM teaching',move,E.text()))
    S.close_text();assert item_count(item)==1
    print('PASS: '+move+' is taught through its reusable HM.',flush=True)

def field_move(name,index=0):
    E.start_option('POKéMON');S.choose_party(index)
    E.advance_until(lambda:name in E.text());M.select_row(name);E.press('a')

def navigate(filename,target,cleared=(),stop_on_warp=False,live_blocks=False,allowed_tiles=(),blocked_tiles=()):
    header=(E.ROOT/f'data/maps/headers/{filename}.asm').read_text()
    code,tileset=re.search(r'map_header \w+, (\w+), (\w+)',header).groups()
    map_id,width,height=MAPS[code]
    assert E.read('wCurMap')==map_id,(filename,E.read('wCurMap'))
    blocks=(E.ROOT/f'maps/{filename}.blk').read_bytes()
    if live_blocks:
        # Switches replace blocks in the loaded map, inside a three-block border.
        stride=width//2+6;address=E.SYMS['wOverworldMap'][1]+3*stride+3
        blocks=bytes(E.gb.memory[address+y*stride+x] for y in range(height//2) for x in range(width//2))
    # Read compiled tables: Dojo and Gym share a blockset, and several other
    # tilesets also have aliases rather than a matching .bst filename.
    label=''.join(part.capitalize() for part in tileset.split('_'))
    pos=E.rom_offset(label+'_Block');tiles=E.ROM[pos:pos+4096]
    pos=E.rom_offset(label+'_Coll');allowed=set(E.ROM[pos:E.ROM.index(255,pos)])
    allowed.update(allowed_tiles)
    walkable={(x,y) for y in range(height) for x in range(width)
              if tiles[blocks[(y//2)*(width//2)+x//2]*16+(y%2)*8+(x%2)*2+4] in allowed}
    source=(E.ROOT/f'data/maps/objects/{filename}.asm').read_text()
    blocked={(int(x),int(y)) for x,y in re.findall(r'object_event\s+(\d+),\s*(\d+)',source)}
    blocked|={(int(x),int(y)) for x,y in re.findall(r'warp_event\s+(\d+),\s*(\d+)',source) if (int(x),int(y))!=target}
    blocked-=set(cleared) # removed objects and changed floor blocks after real scripts
    blocked|=set(blocked_tiles)
    walkable|=set(cleared)|{target}
    directions=[('up',(0,-1)),('down',(0,1)),('left',(-1,0)),('right',(1,0))]
    blocked_edges=set()
    for _ in range(1600):
        current=(E.read('wXCoord'),E.read('wYCoord'))
        if current==target:return
        queue=deque([current]);paths={current:[]}
        while queue and target not in paths:
            x,y=queue.popleft()
            for button,(dx,dy) in directions:
                step=(x+dx,y+dy)
                if step in walkable and step not in blocked and step not in paths and ((x,y),step) not in blocked_edges:
                    paths[step]=paths[(x,y)]+[(button,step)];queue.append(step)
        assert target in paths,('No map path',filename,current,target)
        button,step=paths[target][0]
        E.write('wRepelRemainingSteps',250) # isolate traversal from random wild fights
        E.press(button,8,45)
        if stop_on_warp and step==target:
            E.gb.tick(240);return # also handle warp pads whose destination is the same map
        if E.read('wCurMap')!=map_id:
            E.gb.tick(180);return
        after=(E.read('wXCoord'),E.read('wYCoord'))
        if after==current:
            if live_blocks:blocked_edges.add((current,step)) # cave cliffs depend on the tile pair, not just the destination
            else:blocked.add(step)
    raise AssertionError(('Map navigation',filename,target))

def flash_fixture(base):
    E.restore(base);S.train(['PIKACHU'],[24]);M.warp(0x31,0,last_map=0x0d)
    navigate('Route2Gate',(2,4));E.press('left',4,20)
    E.write('wPokedexOwned',[255,1]+[0]*17) # nine owned forms for the rejection case
    E.press('a');E.advance_until(lambda:'YES' in E.text());E.press('a')
    E.advance_until(lambda:E.read('hOaksAideResult')==0x80);S.close_text()
    assert not M.event('EVENT_GOT_HM05')
    E.write('wPokedexOwned',[255,3]+[0]*17) # ten valid implemented forms
    E.press('a');E.advance_until(lambda:'YES' in E.text());E.press('a')
    E.advance_until(lambda:M.event('EVENT_GOT_HM05'));S.close_text()
    assert S.has_item(ITEMS['HM05'])
    print('PASS: Oak\'s aide enforces ten registered forms and gives HM05.',flush=True)
    teach_hm(ITEMS['HM05'],'FLASH')
    M.warp(MAPS['ROUTE_10'][0],0)
    for floor,count in [(1,7),(2,8)]:
        for index in range(count):M.event(f'EVENT_BEAT_ROCK_TUNNEL_{floor}_TRAINER_{index}',True)
    M.warp(0x52,0,last_map=MAPS['ROUTE_10'][0])
    assert E.read('wMapPalOffset')==6
    E.photo('erika-rock-tunnel-dark');dark=E.state()
    E.write('wObtainedBadges',E.read('wObtainedBadges')&~1)
    field_move('BEACON BARK');E.advance_until(lambda:'BADGE' in E.text());S.close_text()
    assert E.read('wMapPalOffset')==6
    E.restore(dark);field_move('BEACON BARK')
    E.advance_until(lambda:'lights the area!' in E.text());S.close_text()
    assert E.read('wMapPalOffset')==0
    E.photo('erika-rock-tunnel-lit')
    print('PASS: BEACON BARK lights Rock Tunnel and requires the Boulder Badge.',flush=True)
    for filename,target,next_map in [('RockTunnel1F',(37,3),0xe8),('RockTunnelB1F',(27,3),0x52),('RockTunnel1F',(17,11),0xe8),('RockTunnelB1F',(3,3),0x52),('RockTunnel1F',(15,33),MAPS['ROUTE_10'][0])]:
        navigate(filename,target)
        assert E.read('wCurMap')==next_map,(filename,E.read('wCurMap'),E.text())
        assert E.read('wMapPalOffset')==0
    E.photo('erika-rock-tunnel-south-exit')
    print('PASS: actual walking traverses both lit Rock Tunnel floors to the south exit.',flush=True)
    return E.state()

def fly_fixture(base):
    E.restore(base);S.train(['FEAROW','RATICATE'],[28,26]);teach_hm(ITEMS['HM01'],'CUT',1)
    M.warp(0x7d,0,last_map=6);M.warp(6,0,last_map=6)
    navigate('CeladonCity',(0,18));E.walk('left',1)
    assert E.read('wCurMap')==0x1b
    navigate('Route16',(34,10));E.press('up',4,20)
    assert E.read('wTileInFrontOfPlayer')==0x3d
    field_move('BRAMBLE BITE',1);E.advance_until(lambda:'BRAMBLE BITE!' in E.text());S.close_text()
    E.walk('up',1);assert E.read('wYCoord')==9
    navigate('Route16',(24,4),cleared=[(34,9)])
    if E.read('wCurMap')==0x1b:E.press('left',8,180)
    navigate('Route16Gate1F',(0,2))
    if E.read('wCurMap')==MAPS['ROUTE_16_GATE_1F'][0]:E.press('left',8,180)
    navigate('Route16',(7,5))
    assert E.read('wCurMap')==0xbc
    navigate('Route16FlyHouse',(2,4));E.press('up',4,20);E.press('a')
    E.advance_until(lambda:M.event('EVENT_GOT_HM02'));S.close_text()
    assert S.has_item(ITEMS['HM02'])
    print('PASS: BRAMBLE BITE opens the northern Route 16 path to the HM02 giver.',flush=True)
    teach_hm(ITEMS['HM02'],'FLY')
    navigate('Route16FlyHouse',(2,7))
    if E.read('wCurMap')==0xbc:E.press('down',8,180)
    assert E.read('wCurMap')==0x1b
    ready=E.state();E.write('wObtainedBadges',E.read('wObtainedBadges')&~4)
    field_move('SKYBOUND');E.advance_until(lambda:'BADGE' in E.text());S.close_text()
    assert E.read('wCurMap')==0x1b
    E.restore(ready);field_move('SKYBOUND')
    E.advance_until(lambda:'To' in E.text())
    for _ in range(20):
        if 'VERMILION' in E.text():break
        E.press('up',8,90)
    else:raise AssertionError(('Fly destination',E.text()))
    E.photo('erika-fly-destination');E.press('a',wait=600)
    E.advance_until(lambda:E.read('wCurMap')==5 and E.read('wJoyIgnore')==0)
    assert S.has_item(ITEMS['HM02']);E.photo('erika-fly-vermilion')
    print('PASS: SKYBOUND requires the Thunder Badge and flies to visited Vermilion.',flush=True)
    return E.state()

def gift_fixture(base):
    E.restore(base);S.train(['FEAROW'],[28]);M.warp(0x84,0)
    navigate('CeladonMansionRoofHouse',(5,3));E.press('left',4,20);E.press('a')
    E.advance_until(lambda:E.read('wPartyCount')==2)
    E.advance_until(lambda:'give a nickname' in E.text());E.press('down',8,45);E.press('a');S.close_text()
    assert E.read('wPartyMon2Species')==E.IDS['EEVEE']
    E.photo('erika-tervpup-gift')
    print('PASS: the mansion gift gives level-25 TERVPUP through the real adoption script.',flush=True)
    return E.state()

def buy_stone(item,index):
    before=item_count(item)
    E.press('down',4,20);E.press('a');E.advance_until(lambda:'BUY' in E.text());E.press('a')
    for _ in range(30):
        current=E.read('wCurrentMenuItem')+E.read('wListScrollOffset')
        if current==index:break
        E.press('down' if current<index else 'up',8,45)
    E.press('a');E.press('a');E.advance_until(lambda:'YES' in E.text());E.press('a')
    E.advance_until(lambda:item_count(item)==before+1);S.close_text()

def stones_fixture(base):
    E.restore(base);E.write('wPlayerMoney',[5,0,0]);M.warp(0x7d,0)
    navigate('CeladonMart4F',(5,5))
    for slot,index in [('WATER_STONE',3),('THUNDER_STONE',2),('FIRE_STONE',1),('WATER_STONE',3)]:buy_stone(ITEMS[slot],index)
    assert item_count(ITEMS['WATER_STONE'])==2
    print('PASS: Celadon sells all three Tervuren stones and allows repeat purchases.',flush=True)
    purchased=E.state()
    for stone,target in [('WATER_STONE','VAPOREON'),('THUNDER_STONE','JOLTEON'),('FIRE_STONE','FLAREON')]:
        E.restore(purchased);before=item_count(ITEMS[stone])
        E.start_option('ITEM');select_item(ITEMS[stone]);E.press('a');E.press('a');S.choose_party(1)
        E.advance_until(lambda:E.read('wPartyMon2Species')==E.IDS[target]);S.close_text()
        assert item_count(ITEMS[stone])==before-1
        expected=next(d for d in S.M.DOGS if d['slot']==target)
        assert E.read('wPartyMon2Type1')==M.TYPES[expected['types'][0]]
        E.photo('erika-'+target.lower()+'-stone')
        print('PASS: '+stone+' evolves TERVPUP into '+expected['name']+' with the new typing.',flush=True)

def prize_fixture(base):
    E.restore(base);S.train(['FEAROW'],[28]);M.warp(0x8a,0,last_map=6)
    navigate('CeladonDiner',(1,1));E.press('left',4,20);E.press('a')
    E.advance_until(lambda:S.has_item(ITEMS['COIN_CASE']));S.close_text()
    E.write('wPlayerCoins',[0x05,0x00]);M.warp(0x89,0,last_map=6)
    navigate('GameCornerPrizeRoom',(2,3));E.press('up',4,20);E.press('a')
    E.advance_until(lambda:'YES' in E.text());E.press('a')
    E.advance_until(lambda:'POODPUP' in E.text());E.press('a')
    E.advance_until(lambda:'YES' in E.text());E.press('a')
    E.advance_until(lambda:E.read('wPartyCount')==2)
    E.advance_until(lambda:'give a nickname' in E.text());E.press('down',8,45);E.press('a');S.close_text()
    assert E.read('wPartyMon2Species')==E.IDS['ABRA']
    E.photo('erika-game-corner-poodpup')
    print('PASS: the diner gives a Coin Case and the prize exchange gives POODPUP.',flush=True)

def erika_fixture(base,name,slots,levels,carrier):
    E.restore(base);S.train(slots,levels);teach_hm(ITEMS['HM01'],'CUT',carrier)
    for index in range(7):M.event(f'EVENT_BEAT_CELADON_GYM_TRAINER_{index}',True)
    M.warp(0x86,0,last_map=6)
    navigate('CeladonGym',(5,8));E.press('up',4,20)
    assert E.read('wTileInFrontOfPlayer')==0x50
    field_move('BRAMBLE BITE',carrier);E.advance_until(lambda:'BRAMBLE BITE!' in E.text());S.close_text()
    navigate('CeladonGym',(4,4),cleared=[(4,6),(5,6),(4,7),(5,7)]);E.press('up',4,20);E.press('a')
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:bool(E.read('wObtainedBadges')&8),name+'-erika')
    S.close_text()
    assert E.read('wObtainedBadges')&0x0f==0x0f
    assert M.event('EVENT_BEAT_ERIKA') and M.event('EVENT_GOT_TM21') and S.has_item(ITEMS['TM21'])
    E.press('a');E.advance_until(lambda:'Check the poster' in E.text());E.photo(name+'-erika-complete');S.close_text()
    print('PASS: '+name+' clears the gym tree, beats Erika, and earns the Rainbow Badge and TM21 BRIAR FANG.',flush=True)
    return E.state()

def main():
    try:
        if '--from-base' in sys.argv:base=S.load_checkpoint('erika-surge-base')
        else:
            lab=E.bootstrap();E.restore(lab)
            start=E.choose_starter(7,'NEWFPUP','NEWFOUNDLAND',('SQUIRTLE','BULBASAUR'))
            brock=E.brock_fixture(start,'erika-base',['WARTORTLE'],[16],1)
            misty=M.misty_fixture(brock,'erika-base',['PIKACHU','GLOOM','WARTORTLE'],[20,20,20])
            M.bill_fixture(misty);S.close_text();boarded=S.boarding_fixture(E.state())
            captain=S.ship_fixture(boarded,'erika-base',['WARTORTLE','FEAROW'],[22,22],'SQUIRTLE','BULBASAUR')
            gym=S.cut_fixture(captain,'erika-base',['WARTORTLE','RATTATA'],[22,18],1)
            base=S.surge_fixture(gym,'erika-base',['DUGTRIO','WARTORTLE'],[24,24]);S.checkpoint('erika-surge-base')
        lit=flash_fixture(base);S.checkpoint('erika-lit-tunnel')
        flown=fly_fixture(lit);S.checkpoint('erika-flown')
        gift=gift_fixture(flown);stones_fixture(gift);prize_fixture(flown)
        completed={}
        for name,slots,levels,carrier in [('groen',['FEAROW','IVYSAUR','BEEDRILL'],[28,28,28],1),('shiba',['CHARMELEON','FEAROW','BEEDRILL'],[28,28,28],0),('newf',['FEAROW','WARTORTLE','RATICATE'],[28,28,26],2)]:
            completed[name]=erika_fixture(flown,name,slots,levels,carrier)
        E.restore(completed['newf']);S.checkpoint('erika-complete')
        E.save_reload(completed['newf'],expected_map=0x86,expected_badges=0x0f)
        for slot,level,target in [('NIDORAN_F',15,'NIDORINA'),('NIDORINA',31,'NIDOQUEEN'),('NIDORAN_M',15,'NIDORINO'),('NIDORINO',31,'NIDOKING'),('CLEFAIRY',23,'CLEFABLE'),('VULPIX',23,'NINETALES'),('GROWLITHE',23,'ARCANINE'),('POLIWAG',15,'POLIWHIRL'),('POLIWHIRL',31,'POLIWRATH'),('BELLSPROUT',15,'WEEPINBELL'),('WEEPINBELL',31,'VICTREEBEL'),('CUBONE',23,'MAROWAK'),('OMANYTE',23,'OMASTAR'),('KABUTO',23,'KABUTOPS')]:E.evolution_check(completed['newf'],slot,level,target)
        (E.QA/'erika-results.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(E.ROM).hexdigest(),'flash_reward_and_boulder_gate':True,'rock_tunnel_full_traversal':True,'cut_to_fly_house':True,'fly_reward_and_thunder_gate':True,'fly_visited_town':True,'tervpup_gift':True,'repeat_stone_purchases':True,'stone_branches':3,'coin_case_and_prize':True,'erika':['groen','shiba','newf'],'save_load_four_badges':True,'level_evolutions':14,'fixture':'trained parties and map warps; capture-count and money fixtures; cave/gym trainers marked beaten; repeated Repel during traversal'},indent=2)+'\n')
    finally:E.gb.stop();E.tmp.cleanup()

if __name__=='__main__':main()
