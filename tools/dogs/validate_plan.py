#!/usr/bin/env python3
"""Validate design coverage, evolution reachability, and preserved HM contracts.

This checks the planned collection graph, not whether every future encounter has
already been implemented in the ROM. validate_rom.py checks the implemented slice.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TYPES = {'NORMAL', 'FIGHTING', 'FLYING', 'POISON', 'GROUND', 'ROCK', 'BUG', 'GHOST', 'FIRE', 'WATER', 'GRASS', 'ELECTRIC', 'PSYCHIC_TYPE', 'ICE', 'DRAGON'}
HMS = {'CUT': 'BRAMBLE BITE', 'FLY': 'SKYBOUND', 'SURF': 'DOG PADDLE', 'STRENGTH': 'HAUL', 'FLASH': 'BEACON BARK'}


def validate():
    dogs = json.loads((ROOT / 'data/dogs/roster.json').read_text())
    moves = json.loads((ROOT / 'data/dogs/moves.json').read_text())
    implemented = json.loads((ROOT / 'data/dogs/implemented.json').read_text())
    species = re.findall(r'^\s*const DEX_(\w+)\s*;', (ROOT / 'constants/pokedex_constants.asm').read_text(), re.M)
    attack_constants = (ROOT / 'constants/move_constants.asm').read_text().split('DEF NUM_ATTACKS')[0]
    attacks = re.findall(r'^\s*const (\w+)\s*;', attack_constants, re.M)[1:]
    assert [d['slot'] for d in dogs] == species and len(dogs) == 151
    assert [m['slot'] for m in moves] == attacks and len(moves) == 165
    assert [d['dex'] for d in dogs] == list(range(1, 152))
    assert [m['id'] for m in moves] == list(range(1, 166))
    assert len({d['name'] for d in dogs}) == 151
    assert len({m['name'] for m in moves}) == 165
    assert len({m['alias'] for m in moves}) == 165
    assert len({d['breed'] for d in dogs}) == 79
    assert {t for d in dogs for t in d['types']} == TYPES
    assert len(set(implemented)) == len(implemented) and set(implemented) <= set(species)
    by_slot = {d['slot']: d for d in dogs}
    aliases = {m['alias'] for m in moves}
    move_slots = {m['slot']: m for m in moves}
    tm_slots = set(re.findall(r'^\s*add_(?:tm|hm) (\w+)', (ROOT / 'constants/item_constants.asm').read_text(), re.M))
    assert tm_slots <= {m for d in dogs for m in d['tms']}, 'Every TM/HM needs an obtainable carrier'
    reachable = set()
    for d in dogs:
        assert re.fullmatch(r'[A-Z]+', d['name']) and len(d['name']) <= 10, d['name']
        assert len(d['stats']) == 5 and all(1 <= s <= 255 for s in d['stats'])
        assert len(d['types']) == 2 and set(d['types']) <= TYPES
        assert all(m in aliases for m in d['base']) and len(d['base']) <= 4
        assert all(m in aliases and 1 <= level <= 100 for level, m in d['learnset'])
        assert d['learnset'] == sorted(d['learnset'], key=lambda pair: pair[0]), d['name']
        assert set(d['tms']) <= tm_slots and d['signature'] in aliases
        a = d['acquisition']
        if a['method'] in ('wild', 'special'):
            assert (ROOT / f"data/maps/objects/{a['map']}.asm").exists(), a
            assert 1 <= a['levels'][0] <= a['levels'][1] <= 100
            if a['method'] == 'wild':
                assert a['repeatable'] and a['terrain'] in ('grass', 'surf')
            else:
                assert a['retry'], d['name']
            reachable.add(d['slot'])
        elif a['method'] == 'evolution':
            assert by_slot[a['from_slot']]['evolution'] == [a['level'], d['slot']], d['name']
        elif a['method'] == 'stone_evolution':
            edges = by_slot[a['from_slot']]['branch_evolutions']
            assert {'method': 'stone', 'item': a['item'], 'target': d['slot']} in edges
            assert a['item_source'] == 'CeladonMart4F; unlimited purchase'
        else:
            raise AssertionError(a)
    for _ in range(151):
        previous = set(reachable)
        for d in dogs:
            a = d['acquisition']
            if a.get('from_slot') in reachable:
                reachable.add(d['slot'])
        if previous == reachable:
            break
    assert reachable == set(species), set(species) - reachable
    for m in moves:
        assert re.fullmatch(r'[A-Z ]+', m['name']) and 1 <= len(m['name']) <= 12
        assert m['type'] in TYPES and 0 <= m['power'] <= 255
        assert 1 <= m['accuracy'] <= 100 and 1 <= m['pp'] <= 40
    assert {m['slot']: m['name'] for m in moves if m['hm']} == HMS
    # All five field functions have a carrier from the opening slice or Route 25.
    early = {d['slot'] for d in dogs if d['acquisition'].get('gate') in ('none', 'boulder')}
    for _ in range(3):
        early |= {d['slot'] for d in dogs if d['acquisition'].get('from_slot') in early and d['acquisition']['method'] == 'evolution'}
    for hm in HMS:
        assert any(hm in by_slot[s]['tms'] for s in early), hm
    print('PASS: 151 forms / 79 breeds, all 15 types, 165 moves, all forms reachable in the planned single-ROM graph, five preserved HMs with early carriers.')


if __name__ == '__main__':
    validate()
