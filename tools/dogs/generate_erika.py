#!/usr/bin/env python3
"""Generate the Rock Tunnel/Celadon chapter and version-independent dog prizes."""
import json
import re
from pathlib import Path
from data import DOGS

ROOT = Path(__file__).resolve().parents[2]
plan = json.loads((ROOT / 'data/dogs/erika.json').read_text())
names = {d['name'] for d in DOGS}

for route, encounters in plan['wild'].items():
    assert len(encounters) == 10 and all(name in names for _, name in encounters)
    lines = [f'{route}WildMons:', f"\tdef_grass_wildmons {plan['rates'][route]}"]
    lines += [f'\tdb {level:2d}, {name}' for level, name in encounters]
    lines += ['\tend_grass_wildmons', '', '\tdef_water_wildmons 0', '\tend_water_wildmons']
    (ROOT / f'data/wild/maps/{route}.asm').write_text('\n'.join(lines) + '\n')

teams = {label: {int(index): members for index, members in parties.items()}
         for label, parties in plan['trainers'].items()}
teams['ErikaData'] = {1: plan['erika']}
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

path = ROOT / 'data/pokemon/palettes.asm'
source = path.read_text()
for slot, palette in plan['palettes'].items():
    source, count = re.subn(rf'^\tdb PAL_\w+\s+; {slot}(?: / [A-Z]+)?$',
                           f'\tdb {palette:<13} ; {slot}', source, flags=re.M)
    assert count == 1, slot
path.write_text(source)

path = ROOT / 'data/events/prizes.asm'
source = path.read_text()
for group, members in enumerate([plan['prizes'][:3], plan['prizes'][3:]], 1):
    for suffix, lines in [
        ('Entries', [f'\tdb {name}' for _, name, _ in members]),
        ('Cost', [f'\tbcd2 {price}' for _, _, price in members])]:
        label = f'PrizeMenuMon{group}{suffix}'
        replacement = label + ':\n' + '\n'.join(lines) + '\n\tdb "@"\n\n'
        source, count = re.subn(rf'^{label}:\n[\s\S]*?(?=^\w+:)', replacement, source, flags=re.M)
        assert count == 1, label
path.write_text(source)
source = 'PrizeMonLevelDictionary:\n' + ''.join(f'\tdb {name}, {level}\n' for level, name, _ in plan['prizes'])
(ROOT / 'data/events/prize_mon_levels.asm').write_text(source)
print(f'Generated seven Rock Tunnel/Celadon wild tables, {len(updated)} trainer parties, six dog prizes, and breed palettes.')
