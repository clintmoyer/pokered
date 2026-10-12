#!/usr/bin/env python3
"""Generate version-independent Misty encounters and the affected trainer slice."""
import json
import re
from pathlib import Path
from data import DOGS

ROOT = Path(__file__).resolve().parents[2]
plan = json.loads((ROOT / 'data/dogs/misty.json').read_text())
names = {d['name'] for d in DOGS}
for route, encounters in plan['wild'].items():
    assert len(encounters) == 10 and all(name in names for _, name in encounters)
    rate = 25 if route == 'Route24' else 15 if route == 'Route25' else 10 if route.startswith('MtMoon') else 20
    lines = [f'{route}WildMons:', f'\tdef_grass_wildmons {rate}']
    lines += [f'\tdb {level:2d}, {name}' for level, name in encounters]
    lines += ['\tend_grass_wildmons', '', '\tdef_water_wildmons 0', '\tend_water_wildmons']
    (ROOT / f'data/wild/maps/{route}.asm').write_text('\n'.join(lines) + '\n')

path = ROOT / 'data/trainers/parties.asm'
lines = path.read_text().splitlines(keepends=True)
active = False
for i, line in enumerate(lines):
    if re.match(r'^\w+Data:', line):
        active = False
    elif line.startswith('; '):
        active = any(line[2:].startswith(area) for area in plan['scope'])
    elif active and line.startswith('\tdb '):
        for old, name in plan['trainer_replacements'].items():
            line = re.sub(rf'\b{old}\b', name, line)
        if line.startswith('\tdb 31, '):
            line = '\tdb $FF, 12, LAGOPUP, 14, LAGOPUP, 16, LAGOTTO, 0\n'
        lines[i] = line
source = ''.join(lines)
source = re.sub(r'(MistyData:\n)\tdb [^\n]+', r'\g<1>\tdb $FF, 18, OTTERPUP, 21, OTTERMIND, 0', source)
for old, new in [('SQUIRTLE','NEWFIE'),('BULBASAUR','GROEN'),('CHARMANDER','SHIBA')]:
    source = source.replace(f'\tdb $FF, 18, PIDGEOTTO, 15, ABRA, 15, RATTATA, 17, {old}, 0', f'\tdb $FF, 18, WHIPPET, 15, POODPUP, 15, BEAGPUP, 17, {new}, 0')
path.write_text(source)
print('Generated seven wild tables, dog-only chapter trainers, Cerulean rival teams, and Misty.')
