#!/usr/bin/env python3
"""Prove single-ROM collection access from compiled wild/guardian/evolution data.

This checks repeatable encounter roots and ordinary level/stone evolutions, not
party gifts or choices, link trading, glitches, Debug gifts or Pokédex fixtures.
It establishes data reachability; natural balance and a legitimate full-collection
playthrough still require human testing. --report writes the reproducible guide.
"""
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from data import DOGS

ROOT=Path(__file__).resolve().parents[2]

def audit(stem='pokered',report=False):
    rom=(ROOT/f'{stem}.gbc').read_bytes()
    symbols={m[3]:(int(m[1],16),int(m[2],16)) for line in (ROOT/f'{stem}.sym').read_text().splitlines()
             if (m:=re.match(r'([\da-fA-F]+):([\da-fA-F]+) (\S+)',line))}
    def offset(label):
        bank,address=symbols[label];return bank*0x4000+address%0x4000 if bank else address
    def pointed(label,address):
        return symbols[label][0]*0x4000+address%0x4000
    ids={name:int(value,16) for name,value in re.findall(r'^\s*const (\w+)\s*; \$?([\dA-F]{2})\b',(ROOT/'constants/pokemon_constants.asm').read_text(),re.M)}
    by_id={ids[d['slot']]:d for d in DOGS}
    assert len(by_id)==151
    map_ids={code:int(value,16) for code,value in re.findall(r'^\s*map_const (\w+),[^;]+; \$([\dA-F]+)',(ROOT/'constants/map_constants.asm').read_text(),re.M)}
    maps={}
    for header in (ROOT/'data/maps/headers').glob('*.asm'):
        name=header.stem;code=re.search(r'map_header \w+, (\w+)',header.read_text())[1]
        map_id=map_ids[code];hp=offset('MapHeaderPointers')+map_id*2
        actual=(rom[offset('MapHeaderBanks')+map_id],int.from_bytes(rom[hp:hp+2],'little'))
        if actual==symbols[name+'_h']:maps[code]=(map_id,name) # exclude unreferenced copy headers
    roots=defaultdict(list);table_count=0;expected_sources={};source_levels=defaultdict(list)
    for code,(map_id,name) in maps.items():
        hp=offset('MapHeaderPointers')+map_id*2
        assert int.from_bytes(rom[hp:hp+2],'little')==symbols[name+'_h'][1],(stem,name,map_id,hex(int.from_bytes(rom[hp:hp+2],'little')),symbols[name+'_h'])
        assert rom[offset('MapHeaderBanks')+map_id]==symbols[name+'_h'][0]
        hpos=offset(name+'_h');tileset=rom[hpos];height,width=rom[hpos+1:hpos+3]
        tp=offset('Tilesets')+tileset*12;bank=rom[tp]
        blockpos=bank*0x4000+int.from_bytes(rom[tp+1:tp+3],'little')%0x4000
        blockdata=rom[blockpos:blockpos+4096];bp=offset(name+'_Blocks') if name+'_Blocks' in symbols else None
        if bp is not None:
            blocks=rom[bp:bp+width*height]
            feet={blockdata[block*16+i] for block in blocks for i in [4,6,12,14]}
            right_feet={blockdata[block*16+i] for block in blocks for i in [5,7,13,15]}
        else:feet=right_feet=set()
        pos=offset('WildDataPointers')+map_id*2
        pos=pointed('WildDataPointers',int.from_bytes(rom[pos:pos+2],'little'))
        for terrain in ('grass','surf'):
            rate=rom[pos];pos+=1
            if not rate:continue
            table_count+=1
            if terrain=='surf':assert 0x14 in feet,(stem,name,'Surf terrain absent')
            elif map_id<0x25 or tileset==3:
                assert rom[tp+10] in right_feet,(stem,name,'grass terrain absent')
            for level,sid in zip(rom[pos:pos+20:2],rom[pos+1:pos+20:2]):
                assert sid in by_id and 1<=level<=100,(stem,name,terrain,level,sid)
                source=f'{name} {terrain}, L{level}'
                if source not in roots[sid]:roots[sid].append(source)
                expected_sources.setdefault((name,terrain),set()).add(sid)
                source_levels[(name,terrain,sid)].append(level)
            pos+=20
    # Super Rod groups are read using the compiled map/group pointers.
    p=offset('SuperRodData');by_map={mid:name for mid,name in maps.values()}
    while rom[p]!=255:
        map_id=rom[p];group=pointed('SuperRodData',int.from_bytes(rom[p+1:p+3],'little'));count=rom[group];p+=3
        assert map_id in by_map,(stem,'fishing map',map_id)
        for i in range(count):
            level,sid=rom[group+1+i*2:group+3+i*2];assert sid in by_id and 1<=level<=100
            source=f'{by_map[map_id]} Super Rod, L{level}'
            if source not in roots[sid]:roots[sid].append(source)
    # All five retryable guardians are normal catchable static wild battles.
    specials=[('SeafoamIslandsB4F','ARTICUNO',50),('PowerPlant','ZAPDOS',50),
              ('VictoryRoad2F','MOLTRES',50),('CeruleanCaveB1F','MEWTWO',60),('CeruleanCave2F','MEW',50)]
    for name,slot,level in specials:
        p=offset(name+'_Object')+1;p+=1+rom[p]*4;p+=1+rom[p]*3;count=rom[p];p+=1
        found=False
        for _ in range(count):
            flags=rom[p+5];size=8 if flags&0x40 else 7 if flags&0x80 else 6
            if flags&0x40 and tuple(rom[p+6:p+8])==(ids[slot],level):found=True
            p+=size
        assert found,(stem,name,slot,level)
        roots[ids[slot]].append(f'{name} guardian, L{level}; uncaught retries after Hall of Fame')
    # Unlimited stones in the compiled Celadon mart; no Moon Stone evolution.
    p=offset('CeladonMart4FClerkText');assert rom[p]==0xfe
    stock=set(rom[p+2:p+2+rom[p+1]])
    item_ids={name:int(value,16) for name,value in re.findall(r'^\s*const (\w+)\s*; \$?([\dA-F]{2})\b',(ROOT/'constants/item_constants.asm').read_text(),re.M)}
    item_names={v:k for k,v in item_ids.items()}
    edges=defaultdict(list)
    for sid,dog in by_id.items():
        p=offset('EvosMovesPointerTable')+(sid-1)*2;p=pointed('EvosMovesPointerTable',int.from_bytes(rom[p:p+2],'little'))
        while rom[p]:
            method=rom[p]
            if method==1:
                _,level,target=rom[p:p+3];assert 1<=level<=100;rule=f'L{level}';p+=3
            elif method==2:
                _,item,minimum,target=rom[p:p+4];assert item in stock and minimum==1;rule=item_names[item]+' (unlimited Celadon purchase)';p+=4
            else:raise AssertionError((stem,dog['name'],'trade/unsupported evolution',method))
            assert target in by_id;edges[sid].append((target,rule))
    reached={sid:sources[0] for sid,sources in roots.items()}
    for _ in range(151):
        changed=False
        for sid,targets in edges.items():
            if sid not in reached:continue
            for target,rule in targets:
                if target not in reached:reached[target]=by_id[sid]['name']+' -> '+rule;changed=True
        if not changed:break
    assert set(reached)==set(by_id), (stem,'unobtainable',[d['name'] for sid,d in by_id.items() if sid not in reached])
    qa=ROOT/'build/qa';qa.mkdir(parents=True,exist_ok=True)
    (qa/(stem+'-collection-sources.json')).write_text(json.dumps({f'{name}/{terrain}/{by_id[sid]["slot"]}':levels for (name,terrain,sid),levels in source_levels.items()},indent=2)+'\n')
    # Each design's promised wild source must actually contain that species.
    for sid,dog in by_id.items():
        a=dog['acquisition']
        if a['method']=='wild':
            assert sid in expected_sources.get((a['map'],a['terrain']),set()),(stem,dog['name'],a)
            assert any(a['levels'][0]<=v<=a['levels'][1] for v in source_levels[(a['map'],a['terrain'],sid)]),(stem,dog['name'],'source levels',a)
    # Regression: existing persistent IDs are fixed, Mudi gets a reserved byte/bit.
    assert symbols['wCeruleanCave2FCurScript'][1] == symbols['wVictoryRoad1FCurScript'][1]+1
    assert symbols['wLancesRoomCurScript'][1] == symbols['wCeruleanCave2FCurScript'][1]+1
    if report:
        lines=['# Collection guide','', 'Generated from compiled Red ROM data by `tools/dogs/validate_collection.py --report`.', '',
               'All 151 forms are reachable in one ROM through repeatable wild encounters, normal level evolutions, unlimited Celadon stones, and five retryable guardians. Gifts and choices are optional collection shortcuts. No trades, version exclusives, glitches or event distribution are required.', '',
               'Both Red and Blue builds pass the same collection audit. A defeated or fled guardian returns after another Hall of Fame entry; a previously caught guardian stays gone even after release. Cerulean Cave unlocks after the Champion and Hall of Fame.', '',
               'This guide proves collection data access. It does not replace a continuous playthrough or a legitimate 151-form save.', '',
               '| Dex | Dog | Breed | One collection path |','|---|---|---|---|']
        for d in DOGS:
            sid=ids[d['slot']];a=d['acquisition']
            # Prefer the design's repeatable source over a later evolved wild shortcut.
            source=next((s for s in roots.get(sid,[]) if s.startswith(a.get('map','?')+' ')),reached[sid])
            if a['method']=='evolution':source=by_id[ids[a['from_slot']]]['name']+f" -> L{a['level']}"
            if a['method']=='stone_evolution':source=by_id[ids[a['from_slot']]]['name']+' + '+a['item']+' (unlimited Celadon purchase)'
            lines.append(f"| {d['dex']} | {d['name']} | {d['breed']} | {source} |")
        (ROOT/'docs/COLLECTION.md').write_text('\n'.join(lines)+'\n')
    print(f'PASS: {stem}: all 151 forms reachable from {len(roots)} encounter roots, {table_count} grass/Surf tables, fishing, five retryable guardians and {sum(map(len,edges.values()))} level/stone evolutions; no trade or version restriction.')
    return {'rom_sha256':hashlib.sha256(rom).hexdigest(),'forms':len(reached),'encounter_roots':len(roots),'tables':table_count}

if __name__=='__main__':
    audit('pokered',report='--report' in sys.argv);audit('pokeblue');audit('pokeblue_debug')
