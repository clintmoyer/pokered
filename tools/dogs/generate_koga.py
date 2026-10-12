#!/usr/bin/env python3
"""Generate the Rocket/Tower/Fuchsia chapter from its explicit dog plan."""
import json
import re
from pathlib import Path
from data import DOGS

ROOT = Path(__file__).resolve().parents[2]
plan = json.loads((ROOT / 'data/dogs/koga.json').read_text())
names = {d['name'] for d in DOGS}

for route in plan['wild'].keys() | plan['water'].keys():
    lines = [f'{route}WildMons:']
    for terrain, key, rates in [('grass', 'wild', 'rates'), ('water', 'water', 'water_rates')]:
        encounters = plan[key].get(route, [])
        assert not encounters or len(encounters) == 10
        assert all(name in names for _, name in encounters)
        lines.append(f"\tdef_{terrain}_wildmons {plan[rates].get(route, 0)}")
        lines += [f'\tdb {level:2d}, {name}' for level, name in encounters]
        lines += [f'\tend_{terrain}_wildmons', '']
    (ROOT / f'data/wild/maps/{route}.asm').write_text('\n'.join(lines).rstrip() + '\n')

teams = {label: {int(i): team for i, team in parties.items()}
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
            team = teams[label][index]
            assert all(name in names for _, name in team)
            lines[i] = '\tdb $FF, ' + ', '.join(str(v) for pair in team for v in pair) + ', 0\n'
            updated.add((label, index))
assert updated == {(label, i) for label, parties in teams.items() for i in parties}
path.write_text(''.join(lines))

path = ROOT / 'data/pokemon/palettes.asm'
source = path.read_text()
for slot, palette in plan['palettes'].items():
    source, count = re.subn(rf'^\tdb PAL_\w+\s+; {slot}(?: / [A-Z]+)?$',
                           f'\tdb {palette:<13} ; {slot}', source, flags=re.M)
    assert count == 1, slot
path.write_text(source)

lines = ['; repeatable dog encounters with the Good Rod', 'GoodRodMons:']
lines += [f'\tdb {level}, {name}' for level, name in plan['good_rod']]
(ROOT / 'data/wild/good_rod.asm').write_text('\n'.join(lines) + '\n')
path = ROOT / 'data/wild/super_rod.asm'
source = path.read_text()
for group, encounters in plan['super_rod'].items():
    assert all(name in names for _, name in encounters)
    replacement = f'.Group{group}:\n\tdb {len(encounters)}\n'
    replacement += ''.join(f'\tdb {level}, {name}\n' for level, name in encounters)
    source, count = re.subn(rf'\.Group{group}:\n[\s\S]*?(?=\n\.Group|\Z)', replacement, source)
    assert count == 1, group
path.write_text(source)
print(f'Generated {len(plan["wild"])} grass tables, {len(plan["water"])} water table, {len(updated)} trainer parties, both rod tables, and breed palettes.')
