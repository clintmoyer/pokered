#!/usr/bin/env python3
"""Replay the earned Champion gate, Cerulean Cave and final guardian collection.

Requires matching-ROM League checkpoints. Trained parties, room-entry positioning,
capture balls, optional bridge trainer flags and Repel are fixtures. Nugget reward,
Surf, all Cave stairs, wild battles, captures, full five-battle League rematches,
guardian retries and real Save/Continue use game inputs. Diploma threshold tests
use explicit 150/151-owned-bit fixtures, not a legitimate full-collection save.
"""
import hashlib
import json
import re
import sys
import test_league as L
from test_league import G,E,M,S,A,K,B,ITEMS,mid,beaten

GUARDS=[('MEW',151,'EVENT_BEAT_MUDIMYTH','CERULEANCAVE2F_MUDIMYTH',50),
        ('MEWTWO',150,'EVENT_BEAT_MEWTWO','CERULEANCAVEB1F_MEWTWO',60)]

def nav(name,target,warp=False):
    cleared=[original for _,original,_,label in L.objects(name) if B.hidden_object(label)]
    A.navigate(name,target,cleared=cleared,stop_on_warp=warp,live_blocks=True,
               allowed_tiles=(0x14,) if E.read('wWalkBikeSurfState')==2 else (),
               blocked_tiles=[(10,15)] if name=='Route24' and target!=(10,15) and not M.event('EVENT_GOT_NUGGET') else ())

def surf(name,stance,direction,index=None):
    if index is None:
        index=next(i for i in range(E.read('wPartyCount')) if E.MIDS['SURF'] in E.gb.memory[E.SYMS[f'wPartyMon{i+1}Moves'][1]:E.SYMS[f'wPartyMon{i+1}Moves'][1]+4])
    nav(name,stance);E.press(direction,4,20)
    assert E.read('wTileInFrontOfPlayer')==0x14,(name,stance,direction,E.read('wTileInFrontOfPlayer'))
    A.field_move('DOG PADDLE',index);S.close_text()
    assert E.read('wWalkBikeSurfState')==2,(name,E.text())

def cave_approach(base,champion):
    E.restore(base);assert E.read('wNumHoFTeams')==int(champion)
    B.room_for_rewards();S.train(['BLASTOISE','FEAROW','SCYTHER','RAICHU'],[75]*4)
    A.teach_hm(ITEMS['HM03'],'SURF',0);A.teach_hm(ITEMS['HM02'],'FLY',1)
    # Use an interior anchor and exit onto Cerulean's normal town floor.
    G.exit_center('CERULEAN_POKECENTER','CeruleanPokecenter','CERULEAN_CITY')
    if not M.event('EVENT_BEAT_CERULEAN_RIVAL'):
        nav('CeruleanCity',(20,7));E.press('up',8,90)
        E.advance_until(lambda:E.read('wIsInBattle')==2)
        M.fight_until(lambda:M.event('EVENT_BEAT_CERULEAN_RIVAL'),'postgame-cerulean-rival');S.close_text()
        E.advance_until(lambda:E.read('wJoyIgnore')==0)
    nav('CeruleanCity',(20,0));E.press('up',8,240)
    assert E.read('wCurMap')==mid('ROUTE_24')
    beaten('EVENT_BEAT_ROUTE_24_TRAINER_',6)
    if not M.event('EVENT_GOT_NUGGET'):
        nav('Route24',(10,16));E.press('up',8,90)
        for _ in range(180):
            if E.read('wIsInBattle')==2:break
            E.press('b' if 'YES' in E.text() and 'NO' in E.text() else 'a')
        else:raise AssertionError(('Nugget Bridge',E.text()))
        M.fight_until(lambda:M.event('EVENT_BEAT_ROUTE24_ROCKET'),'postgame-nugget');S.close_text()
        assert M.event('EVENT_GOT_NUGGET')
    surf('Route24',(7,15),'down')
    nav('Route24',(7,35));E.press('down',8,240);assert E.read('wCurMap')==mid('CERULEAN_CITY')
    nav('CeruleanCity',(4,13));assert E.read('wWalkBikeSurfState')==0
    assert B.hidden_object('CERULEANCITY_SUPER_NERD3')==champion
    if not champion:
        E.press('up',4,20);E.press('a');E.advance_until(lambda:'allowed in!' in E.text())
        E.photo('postgame-before-champion-gate');S.close_text();E.press('up',8,90)
        assert E.read('wCurMap')==mid('CERULEAN_CITY') and (E.read('wXCoord'),E.read('wYCoord'))==(4,13)
        print('PASS: eight earned badges alone do not admit the player to Cerulean Cave.',flush=True)
        return
    nav('CeruleanCity',(4,11),warp=True)
    if E.read('wCurMap')==mid('CERULEAN_CITY'):E.press('up',8,240)
    assert E.read('wCurMap')==mid('CERULEAN_CAVE_1F') and E.read('wLastMap')==mid('CERULEAN_CITY')
    nav('CeruleanCave1F',(23,7),warp=True);assert E.read('wCurMap')==mid('CERULEAN_CAVE_2F')
    nav('CeruleanCave2F',(26,7));E.photo('postgame-mudimyth-overworld');S.checkpoint('postgame-mudimyth-base')
    print('PASS: the earned Hall of Fame unlocks the cave; real Surf, landing and stairs reach MUDIMYTH.',flush=True)
    return E.state()

def guardian(index,case):
    slot,dex,event,label,level=GUARDS[index]
    if case=='capture' and not S.has_item(ITEMS['MASTER_BALL']):B.add_item(ITEMS['MASTER_BALL'])
    L.lead('SCYTHER') if case=='defeat' else None
    E.press('right' if index==0 else 'up',4,20);E.press('a')
    E.advance_until(lambda:E.read('wIsInBattle')==1)
    assert E.read('wEnemyMonSpecies')==E.IDS[slot] and E.read('wEnemyMonLevel')==level
    dog=next(d for d in E.DOGS if d['slot']==slot)
    assert (E.read('wEnemyMonType1'),E.read('wEnemyMonType2'))==tuple(M.TYPES[k] for k in dog['types'])
    address=E.SYMS['wEnemyMonDVs'][1];v,w=E.gb.memory[address:address+2]
    dvs=[v>>4,v&15,w>>4,w&15];hp=sum((dv&1)<<shift for dv,shift in zip(dvs,[3,2,1,0]))
    expected=[(dog['stats'][0]+hp)*2*level//100+level+10]+[(base+dv)*2*level//100+5 for base,dv in zip(dog['stats'][1:],dvs)]
    actual=[M.word('wEnemyMon'+stat) for stat in ['MaxHP','Attack','Defense','Speed','Special']]
    assert actual==expected,(slot,actual,expected)
    E.advance_until(lambda:'FIGHT' in E.text() and 'RUN' in E.text());E.photo('postgame-'+case+'-'+dog['name'].lower())
    if case=='capture':
        if not S.has_item(ITEMS['MASTER_BALL']):B.add_item(ITEMS['MASTER_BALL'])
        G.capture(slot,dex)
    elif case=='flee':G.run_encounter()
    else:M.fight_until(lambda:M.event(event),'postgame-defeat-'+dog['name'].lower());S.close_text()
    assert M.event(event) and B.hidden_object(label) and G.owned(dex)==(case=='capture')
    S.checkpoint('postgame-'+dog['name'].lower()+'-'+case)
    print('PASS: '+dog['name']+' '+case+' at L'+str(level)+', with the planned typing and persistent encounter flag.',flush=True)

def psiguard_route():
    nav('CeruleanCave2F',(29,1),warp=True);assert E.read('wCurMap')==mid('CERULEAN_CAVE_1F')
    surf('CeruleanCave1F',(23,3),'down');nav('CeruleanCave1F',(15,3));assert E.read('wWalkBikeSurfState')==0
    nav('CeruleanCave1F',(7,1),warp=True);assert E.read('wCurMap')==mid('CERULEAN_CAVE_2F')
    before=A.item_count(ITEMS['FULL_RESTORE']);nav('CeruleanCave2F',(13,5));E.press('down',4,20);E.press('a')
    E.advance_until(lambda:B.hidden_object('CERULEANCAVE2F_FULL_RESTORE'));S.close_text()
    assert A.item_count(ITEMS['FULL_RESTORE'])==before+1
    nav('CeruleanCave2F',(19,7),warp=True);assert E.read('wCurMap')==mid('CERULEAN_CAVE_1F')
    nav('CeruleanCave1F',(3,11),warp=True);assert E.read('wCurMap')==mid('CERULEAN_CAVE_2F')
    nav('CeruleanCave2F',(1,3),warp=True);assert E.read('wCurMap')==mid('CERULEAN_CAVE_1F')
    E.press('right',8,90) # leave the stair onto its floor, avoiding the southern cliff tile
    nav('CeruleanCave1F',(0,6),warp=True)
    if E.read('wCurMap')==mid('CERULEAN_CAVE_1F'):E.press('left',8,240)
    assert E.read('wCurMap')==mid('CERULEAN_CAVE_B1F')
    surf('CeruleanCaveB1F',(13,13),'down');nav('CeruleanCaveB1F',(27,7))
    assert E.read('wWalkBikeSurfState')==0
    surf('CeruleanCaveB1F',(27,7),'down')
    _,land=L.map_grid('CeruleanCaveB1F')
    A.navigate('CeruleanCaveB1F',(26,16),live_blocks=True,allowed_tiles=(0x14,),blocked_tiles=list(land))
    E.press('up',8,90);assert E.read('wWalkBikeSurfState')==0
    nav('CeruleanCaveB1F',(27,14))
    E.photo('postgame-psiguard-overworld');S.checkpoint('postgame-psiguard-base')
    print('PASS: real travel crosses all six 2F stairs, the three Cave floors and basement Surf to PSIGUARD.',flush=True)

def verify_guards(expected):
    for (_,dex,event,label,_),caught in zip(GUARDS,expected):
        assert G.owned(dex)==caught and M.event(event)==caught and B.hidden_object(label)==caught,(dex,caught)
    assert B.hidden_object('CERULEANCAVE2F_FULL_RESTORE') # guardian retry never resets item flags
    assert all(G.owned(dex) for dex in [144,145])
    assert B.hidden_object('SEAFOAMISLANDSB4F_ARTICUNO') and B.hidden_object('POWERPLANT_ZAPDOS')
    assert not G.owned(146) and not B.hidden_object('VICTORYROAD2F_MOLTRES')
    assert all(A.item_count(ITEMS[f'HM{i:02d}'])==1 for i in range(1,6))

def rematch(base,expected,label):
    state=L.league_fixture(base,'newf','BLASTOISE','BULBASAUR',False)
    verify_guards(expected);S.checkpoint('postgame-rematch-'+label)
    E.photo('postgame-rematch-'+label);print('PASS: earned five-battle League rematch and fresh Continue restore only uncaught guardians: '+label+'.',flush=True)
    return state

def collected_save(base):
    E.restore(base);owned_before=bytes(E.gb.memory[E.SYMS['wPokedexOwned'][1]:E.SYMS['wPokedexOwnedEnd'][1]])
    party=[E.read(f'wPartyMon{i}Species') for i in range(1,E.read('wPartyCount')+1)]
    E.save_reload(E.state(),expected_map=mid('CERULEAN_CAVE_B1F'),expected_badges=255)
    E.advance_until(lambda:'CONTINUE' not in E.text() and E.read('wCurMap')==mid('CERULEAN_CAVE_B1F'))
    assert [E.read(f'wPartyMon{i}Species') for i in range(1,E.read('wPartyCount')+1)]==party
    assert bytes(E.gb.memory[E.SYMS['wPokedexOwned'][1]:E.SYMS['wPokedexOwnedEnd'][1]])==owned_before
    for _,dex,event,label,_ in GUARDS:assert G.owned(dex) and M.event(event) and B.hidden_object(label)
    assert E.IDS['MEW'] in party and E.IDS['MEWTWO'] in party
    assert all(A.item_count(ITEMS[f'HM{i:02d}'])==1 for i in range(1,6))
    S.checkpoint('postgame-collected');print('PASS: a real Cave save and fresh Continue keep both captured dogs, their Pokédex entries, flags and all five HMs.',flush=True)
    return E.state()

def diploma_fixture(base):
    E.restore(base);M.warp(mid('CELADON_MANSION_3F'),0,last_map=mid('CELADON_CITY'));nav('CeladonMansion3F',(2,4))
    for count in [150,151]:
        E.write('wPokedexOwned',[255]*18+[63 if count==150 else 127]);E.press('up',4,20);E.press('a')
        if count==150:
            E.advance_until(lambda:'151 dogs is tough' in E.text());E.photo('postgame-diploma-150-rejected');S.close_text()
        else:
            E.advance_until(lambda:'All 151 dogs!' in E.text());E.advance_until(lambda:'Diploma' in E.text())
            E.photo('postgame-diploma-151');E.press('a');S.close_text()
    print('PASS: explicit 150/151-owned fixtures verify the diploma threshold and display.',flush=True)

def main():
    try:
        if '--from-base' in sys.argv:base=S.load_checkpoint('postgame-mudimyth-base')
        else:
            cave_approach(S.load_checkpoint('league-lobby'),False)
            base=cave_approach(S.load_checkpoint('league-complete'),True)
        if '--route' in sys.argv:
            E.restore(base);guardian(0,'capture');psiguard_route();guardian(1,'capture');collected_save(E.state());return
        results={}
        for label,cases in [('both-caught',('capture','capture')),('mudi-caught',('capture','defeat')),('psi-caught',('flee','capture')),('neither-caught',('defeat','flee'))]:
            E.restore(base);guardian(0,cases[0]);psiguard_route();guardian(1,cases[1]);state=E.state()
            if label=='both-caught':state=collected_save(state);collected=state
            results[label]=rematch(state,tuple(c=='capture' for c in cases),label)
        # Actually revisit the reset object after the uncaught rematch; compare
        # map-local object 4 and its appended global index after loading 2F.
        E.restore(results['neither-caught']);B.room_for_rewards()
        S.train(['BLASTOISE','FEAROW','SCYTHER','RAICHU'],[75]*4);A.teach_hm(ITEMS['HM03'],'SURF',0)
        M.warp(mid('CERULEAN_CAVE_2F'),1,last_map=mid('CERULEAN_CITY'));nav('CeruleanCave2F',(26,7))
        guardian(0,'capture');M.warp(mid('CERULEAN_CAVE_B1F'),0,last_map=mid('CERULEAN_CITY'))
        surf('CeruleanCaveB1F',(13,13),'down');nav('CeruleanCaveB1F',(27,7))
        surf('CeruleanCaveB1F',(27,7),'down')
        _,land=L.map_grid('CeruleanCaveB1F')
        A.navigate('CeruleanCaveB1F',(26,16),live_blocks=True,allowed_tiles=(0x14,),blocked_tiles=list(land))
        E.press('up',8,90);nav('CeruleanCaveB1F',(27,14));guardian(1,'capture')
        assert G.owned(150) and G.owned(151)
        diploma_fixture(collected);E.restore(collected);S.checkpoint('postgame-complete')
        (E.QA/'postgame-results.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(E.ROM).hexdigest(),'earned_champion_gate':True,'surf_and_all_six_cave_stairs':True,'both_guardians_capture_flee_defeat':True,'four_earned_league_rematches':list(results),'caught_stay_gone_uncaught_return':True,'actual_recapture_after_retry':True,'both_caught_save_continue':True,'five_hms_preserved':True,'diploma_150_151_bit_fixtures':True,'fixture':__doc__},indent=2)+'\n')
    except Exception:
        E.photo('postgame-failure');S.checkpoint('postgame-failure');raise
    finally:E.gb.stop();E.tmp.cleanup()

if __name__=='__main__':main()
