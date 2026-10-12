#!/usr/bin/env python3
"""Generate the Vermilion chapter without changing later trainer parties."""
import json
import re
from pathlib import Path
from data import DOGS

ROOT = Path(__file__).resolve().parents[2]
plan = json.loads((ROOT / 'data/dogs/surge.json').read_text())
names = {d['name'] for d in DOGS}

for route, encounters in plan['wild'].items():
    assert len(encounters) == 10 and all(name in names for _, name in encounters)
    lines = [f'{route}WildMons:', f"\tdef_grass_wildmons {plan['rates'][route]}"]
    lines += [f'\tdb {level:2d}, {name}' for level, name in encounters]
    lines += ['\tend_grass_wildmons', '', '\tdef_water_wildmons 0', '\tend_water_wildmons']
    (ROOT / f'data/wild/maps/{route}.asm').write_text('\n'.join(lines) + '\n')

teams = {label: {int(index): members for index, members in parties.items()}
         for label, parties in plan['trainers'].items()}
teams['Rival2Data'] = {i + 1: members for i, members in enumerate(plan['rival'])}
teams['LtSurgeData'] = {1: plan['lt_surge']}
path = ROOT / 'data/trainers/parties.asm'
lines = path.read_text().splitlines(keepends=True)
label = None
index = 0
updated = set()
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

# These optional trades use repeatably catchable chapter dogs on both sides.
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

path = ROOT / 'data/pokemon/palettes.asm'
source = path.read_text()
for slot, palette in plan['palettes'].items():
    source, count = re.subn(rf'^\tdb PAL_\w+\s+; {slot}(?: / [A-Z]+)?$',
                           f'\tdb {palette:<13} ; {slot}', source, flags=re.M)
    assert count == 1, slot
path.write_text(source)
print(f'Generated four Vermilion wild tables, {len(updated)} trainer parties, five dog trades, and breed palettes.')
