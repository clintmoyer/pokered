#!/usr/bin/env python3
"""Replay ticket boarding, ship rivals, HM teaching, Cut, gym locks, and Surge.

Parties are trained fixtures and maps may be warped between checks. Optional gym
trainers are marked beaten to isolate the puzzle and leader. Battles, HM teaching,
tree removal, rewards and saving use ordinary game inputs and actual scripts.
"""
from collections import deque
import hashlib
import json
import sys
import test_misty as M
from test_misty import E

HASH=hashlib.sha256(E.ROM).hexdigest()

def checkpoint(name):
    (E.QA/(name+'.state')).write_bytes(E.state())
    (E.QA/(name+'.sha256')).write_text(HASH)

def load_checkpoint(name):
    assert (E.QA/(name+'.sha256')).read_text()==HASH,'Checkpoint belongs to a different ROM'
    return (E.QA/(name+'.state')).read_bytes()

def bag():
    address=E.SYMS['wBagItems'][1]
    return list(E.gb.memory[address:address+E.read('wNumBagItems')*2])

def has_item(item):return item in bag()[::2]

def train(slots,levels):
    items=bag()
    E.trained_party(slots,levels)
    E.write('wNumBagItems',len(items)//2);E.write('wBagItems',items+[255])

def close_text():
    for _ in range(10):E.press('b',wait=60)

def choose_party(index):
    for _ in range(12):
        if E.read('wCurrentMenuItem')==index:
            E.press('a');return
        E.press('down',8,45)
    raise AssertionError(('Party selection',index,E.text()))

def boarding_fixture(base):
    E.restore(base)
    assert has_item(0x3f) # S.S. Ticket earned from Bill
    M.warp(5,5,last_map=5)
    M.walk_axis('wYCoord',29,'up')
    dock_approach=E.state()
    # Remove only the ticket for the rejection variant, then restore it.
    items=[v for pair in zip(bag()[::2],bag()[1::2]) if pair[0]!=0x3f for v in pair]
    E.write('wNumBagItems',len(items)//2);E.write('wBagItems',items+[255])
    E.walk('down',1)
    E.advance_until(lambda:'Sorry!' in E.text())
    close_text();E.gb.tick(180)
    assert E.read('wCurMap')==5 and E.read('wYCoord')==29,E.text()
    print('PASS: the dock guard rejects boarding without the S.S. Ticket.',flush=True)
    E.restore(dock_approach);E.walk('down',1)
    E.advance_until(lambda:'flashed' in E.text())
    E.photo('surge-ticket-boarding');close_text()
    E.walk('down',1)
    assert E.read('wCurMap')==0x5e,(E.read('wCurMap'),E.text())
    E.walk('down',2)
    assert E.read('wCurMap')==0x5f,(E.read('wCurMap'),E.text())
    E.photo('surge-ship-entry')
    print('PASS: Bill\'s ticket admits the player through the dock onto the S.S. Anne.',flush=True)
    return E.state()

def ship_fixture(base,name,slots,levels,starter,rival):
    E.restore(base);train(slots,levels)
    E.write('wPlayerStarter',E.IDS[starter]);E.write('wRivalStarter',E.IDS[rival])
    M.warp(0x60,8)
    E.walk('down',4)
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:E.read('wSSAnne2FCurScript')==4 and E.read('wJoyIgnore')==0,name+'-ship-rival')
    close_text()
    print('PASS: '+name+' S.S. Anne rival battle and captain-stair unlock.',flush=True)
    E.walk('up',4)
    assert E.read('wCurMap')==0x65,(E.read('wCurMap'),E.text())
    E.walk('up',2);E.walk('right',4);E.walk('up',2);E.press('up',4,20);E.press('a')
    E.advance_until(lambda:M.event('EVENT_GOT_HM01'))
    assert has_item(0xc4),bag() # stable HM01 item ID
    E.photo(name+'-captain-hm01');close_text()
    print('PASS: '+name+' captain conversation awards HM01 BRAMBLE BITE.',flush=True)
    return E.state()

def teach_cut(name,party_index):
    E.start_option('ITEM')
    target=bag()[::2].index(0xc4)
    for _ in range(30):
        current=E.read('wCurrentMenuItem')+E.read('wListScrollOffset')
        if current==target:break
        E.press('down' if current<target else 'up',8,45)
    else:raise AssertionError(('HM item selection',E.text()))
    E.press('a');E.press('a')
    E.advance_until(lambda:'YES' in E.text() and 'NO' in E.text());E.press('a')
    E.advance_until(lambda:'ABLE' in E.text())
    choose_party(party_index)
    for _ in range(100):
        moves=E.SYMS[f'wPartyMon{party_index+1}Moves'][1]
        if E.MIDS['CUT'] in E.gb.memory[moves:moves+4]:break
        screen=E.text()
        if 'Abandon learning' in screen:E.press('b')
        elif 'YES' in screen and 'NO' in screen:E.press('a')
        else:E.press('a')
    else:raise AssertionError(('HM teaching failed',name,E.text()))
    close_text()
    assert has_item(0xc4),'Teaching an HM must not consume it'
    print('PASS: '+name+' learns BRAMBLE BITE through HM01; the HM remains reusable.',flush=True)

def field_cut(party_index):
    E.start_option('POKéMON')
    choose_party(party_index)
    E.advance_until(lambda:'BRAMBLE BITE' in E.text())
    M.select_row('BRAMBLE BITE');E.press('a')

def cut_fixture(base,name,slots,levels,carrier,check_badge=False):
    E.restore(base);train(slots,levels);teach_cut(name,carrier)
    M.warp(5,4,last_map=5)
    M.walk_axis('wXCoord',20,'left');M.walk_axis('wYCoord',17,'up')
    M.walk_axis('wXCoord',15,'left');E.press('down',4,20)
    E.photo(name+'-gym-tree')
    assert E.read('wTileInFrontOfPlayer')==0x3d,(E.read('wXCoord'),E.read('wYCoord'),E.read('wTileInFrontOfPlayer'))
    ready=E.state()
    if check_badge:
        E.write('wObtainedBadges',E.read('wObtainedBadges')&~2)
        field_cut(carrier)
        E.advance_until(lambda:'BADGE' in E.text())
        E.photo('surge-cut-badge-required');close_text()
        assert E.read('wTileInFrontOfPlayer')==0x3d
        E.restore(ready)
        print('PASS: BRAMBLE BITE cannot clear the gym tree without the Cascade Badge.',flush=True)
    field_cut(carrier)
    E.advance_until(lambda:'BRAMBLE BITE!' in E.text());E.photo(name+'-using-bramble-bite');close_text()
    E.walk('down',1)
    assert E.read('wYCoord')==18,(E.read('wXCoord'),E.read('wYCoord'),E.text())
    E.photo(name+'-cleared-gym-tree')
    assert has_item(0xc4)
    E.walk('down',2);E.walk('left',3);E.walk('up',1)
    assert E.read('wCurMap')==0x5c,(E.read('wCurMap'),E.read('wXCoord'),E.read('wYCoord'),E.text())
    print('PASS: '+name+' uses BRAMBLE BITE, traverses the cleared tree, and enters Vermilion Gym.',flush=True)
    return E.state()

def navigate_gym(target):
    # Plan on the small grid, learning walls from actual failed movement inputs.
    blocked={(1+2*c,7+2*r) for c in range(5) for r in range(3)}
    blocked|={(9,6),(3,8),(0,10),(4,14),(5,1)}
    directions=[('up',(0,-1)),('down',(0,1)),('left',(-1,0)),('right',(1,0))]
    for _ in range(240):
        current=(E.read('wXCoord'),E.read('wYCoord'))
        if current==target:return
        queue=deque([current]);paths={current:[]}
        while queue and target not in paths:
            x,y=queue.popleft()
            for button,(dx,dy) in directions:
                step=(x+dx,y+dy)
                if 0<=step[0]<10 and 0<=step[1]<17 and step not in blocked and step not in paths:
                    paths[step]=paths[(x,y)]+[(button,step)];queue.append(step)
        assert target in paths,('No gym path',current,target,blocked)
        button,step=paths[target][0];E.press(button,8,60)
        after=(E.read('wXCoord'),E.read('wYCoord'))
        if after==current:blocked.add(step)
        assert E.read('wCurMap')==0x5c
    raise AssertionError(('Gym navigation',target,E.text()))

def inspect_can(index):
    x,y=1+2*(index//3),7+2*(index%3)
    above=index==3
    navigate_gym((x,y-1 if above else y+1))
    E.press('down' if above else 'up',4,20);E.press('a')
    close_text()

def surge_fixture(base,name,slots,levels):
    E.restore(base);train(slots,levels)
    for index in range(3):M.event(f'EVENT_BEAT_VERMILION_GYM_TRAINER_{index}',True)
    inspect_can(E.read('wFirstLockTrashCanIndex'))
    assert M.event('EVENT_1ST_LOCK_OPENED'),E.text()
    inspect_can(E.read('wSecondLockTrashCanIndex'))
    assert M.event('EVENT_2ND_LOCK_OPENED'),E.text()
    E.photo(name+'-surge-locks-open')
    print('PASS: '+name+' opens both gym locks through the actual trash-can scripts.',flush=True)
    navigate_gym((5,2));E.press('up',4,20);E.press('a')
    E.advance_until(lambda:E.read('wIsInBattle')==2)
    M.fight_until(lambda:bool(E.read('wObtainedBadges')&4),name+'-surge')
    close_text()
    assert E.read('wObtainedBadges')&7==7
    assert M.event('EVENT_BEAT_LT_SURGE') and M.event('EVENT_GOT_TM24') and has_item(0xe0),bag()
    E.press('a');E.advance_until(lambda:'Head east' in E.text());E.photo(name+'-surge-complete');close_text()
    print('PASS: '+name+' defeats Surge, earns the Thunder Badge and TM24 VOLT BARK.',flush=True)
    return E.state()

def departure_fixture(base):
    E.restore(base);M.warp(0x5e,1,last_map=5)
    E.advance_until(lambda:M.event('EVENT_SS_ANNE_LEFT') and E.read('wJoyIgnore')==0)
    E.walk('up',2)
    E.advance_until(lambda:E.read('wCurMap')==5 and E.read('wJoyIgnore')==0)
    assert M.event('EVENT_SS_ANNE_LEFT') and has_item(0xc4)
    E.photo('surge-ship-departed')
    print('PASS: the S.S. Anne departure sequence completes after HM01 and keeps the HM.',flush=True)

def main():
    try:
        if '--from-captains' in sys.argv:base=None
        elif '--from-base' in sys.argv:base=load_checkpoint('surge-bill-base')
        else:
            lab=E.bootstrap();E.restore(lab)
            start=E.choose_starter(7,'NEWFPUP','NEWFOUNDLAND',('SQUIRTLE','BULBASAUR'))
            brock=E.brock_fixture(start,'surge-base',['WARTORTLE'],[16],1)
            misty=M.misty_fixture(brock,'surge-base',['PIKACHU','GLOOM','WARTORTLE'],[20,20,20])
            M.bill_fixture(misty);close_text();base=E.state();checkpoint('surge-bill-base')
        if base is not None:
            boarded=boarding_fixture(base);checkpoint('surge-boarded')
        ships={};cut={};completed={}
        routes=[('groen',['IVYSAUR','GYARADOS'],[22,22],'BULBASAUR','CHARMANDER'),
                ('shiba',['GLOOM','CHARMELEON','PIKACHU'],[22,22,22],'CHARMANDER','SQUIRTLE'),
                ('newf',['WARTORTLE','FEAROW'],[22,22],'SQUIRTLE','BULBASAUR')]
        for name,slots,levels,starter,rival in routes:
            if '--from-captains' in sys.argv:ships[name]=load_checkpoint(name+'-surge-captain')
            else:
                ships[name]=ship_fixture(boarded,name,slots,levels,starter,rival)
                checkpoint(name+'-surge-captain')
        departure_fixture(ships['newf'])
        for name,slots,levels,carrier in [('groen',['IVYSAUR'],[22],0),('shiba',['CHARMELEON'],[22],0),('newf',['WARTORTLE','RATTATA'],[22,18],1)]:
            cut[name]=cut_fixture(ships[name],name,slots,levels,carrier,check_badge=name=='groen')
        for name,starter in [('groen','IVYSAUR'),('shiba','CHARMELEON'),('newf','WARTORTLE')]:
            completed[name]=surge_fixture(cut[name],name,['DIGLETT',starter],[24,24])
        E.save_reload(completed['newf'],expected_map=0x5c,expected_badges=7)
        for slot,level,target in [('DIGLETT',23,'DUGTRIO'),('MEOWTH',23,'PERSIAN'),('MACHOP',15,'MACHOKE'),('MACHOKE',31,'MACHAMP'),('MAGNEMITE',23,'MAGNETON'),('DROWZEE',23,'HYPNO'),('VOLTORB',23,'ELECTRODE')]:
            E.evolution_check(completed['newf'],slot,level,target)
        (E.QA/'surge-results.json').write_text(json.dumps({'rom_sha256':HASH,'ship_rivals':['groen','shiba','newf'],'cut_routes':['groen','shiba','newf with Beagle'],'surge':['groen','shiba','newf with Border Terrier'],'fixture':'trained parties, map warps; optional gym trainers marked beaten; RNG lock locations read without modification','ticket_gate':True,'captain_hm01':True,'hm_reusable':True,'cascade_gate':True,'tree_traversal':True,'gym_lock_scripts':True,'ship_departure':True,'save_load_three_badges':True,'new_evolutions':7},indent=2)+'\n')
    finally:E.gb.stop();E.tmp.cleanup()

if __name__=='__main__':main()
