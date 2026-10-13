#!/usr/bin/env python3
"""Generate the Seafoam/Cinnabar chapter from its explicit dog plan."""
import json
import re
from pathlib import Path
from data import DOGS

ROOT = Path(__file__).resolve().parents[2]
plan = json.loads((ROOT / 'data/dogs/blaine.json').read_text())
names = {d['name'] for d in DOGS}

for route in plan['wild'].keys() | plan['water'].keys():
    lines = [f'{route}WildMons:']
    for terrain, key, rates in [('grass', 'wild', 'rates'), ('water', 'water', 'water_rates')]:
        encounters = plan[key].get(route, [])
        assert not encounters or len(encounters) == 10
        assert all(name in names for _, name in encounters)
        lines.append(f"\tdef_{terrain}_wildmons {plan[rates].get(route, 0)}")
        lines += [f'\tdb {level:2d}, {name}' for level, name in encounters]
        lines += ['\tend_' + terrain + '_wildmons', '']
    (ROOT / f'data/wild/maps/{route}.asm').write_text('\n'.join(lines).rstrip() + '\n')

teams = {label: {int(index): members for index, members in parties.items()}
         for label, parties in plan['trainers'].items()}
path = ROOT / 'data/trainers/parties.asm'
lines = path.read_text().splitlines(keepends=True)
label, index, updated = None, 0, set()
for i, line in enumerate(lines):
    match = re.match(r'^(\w+Data):', line)
    if match:
        label, index = match[1], 0
    elif line.startswith('\tdb '):
        index += 1
        if index in teams.get(label, {}):
            members = teams[label][index]
            assert all(name in names for _, name in members)
            lines[i] = '\tdb $FF, ' + ', '.join(str(v) for pair in members for v in pair) + ', 0\n'
            updated.add((label, index))
assert updated == {(label, index) for label, parties in teams.items() for index in parties}
path.write_text(''.join(lines))

path = ROOT / 'data/pokemon/palettes.asm'
source = path.read_text()
for slot, palette in plan['palettes'].items():
    source, count = re.subn(rf'^\tdb PAL_\w+\s+; {slot}(?: / [A-Z]+)?$',
                           f'\tdb {palette:<13} ; {slot}', source, flags=re.M)
    assert count == 1, slot
path.write_text(source)

trade_ids = ['TRADE_FOR_TERRY', 'TRADE_FOR_MARCEL', 'UNUSED', 'TRADE_FOR_SAILOR',
             'TRADE_FOR_DUX', 'TRADE_FOR_MARC', 'TRADE_FOR_LOLA', 'TRADE_FOR_DORIS',
             'TRADE_FOR_CRINKLES', 'TRADE_FOR_SPOT']
path = ROOT / 'data/events/trades.asm'
lines = path.read_text().splitlines(keepends=True)
index = 0
for i, line in enumerate(lines):
    if line.startswith('\tnpctrade '):
        trade = plan['trades'].get(trade_ids[index])
        if trade:
            give, receive, nickname = trade
            assert give in names and receive in names
            comment = line.split(';', 1)[1].strip()
            lines[i] = f'\tnpctrade {give}, {receive}, TRADE_DIALOGSET_CASUAL, "{nickname}" ; {comment}\n'
        index += 1
assert index == len(trade_ids)
path.write_text(''.join(lines))
print(f'Generated {len(plan["wild"])} Seafoam/Mansion/coastal tables, {len(updated)} trainer parties, four palettes, and three dog trades.')
