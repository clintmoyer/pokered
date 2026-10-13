#!/usr/bin/env python3
"""Generate Saffron's dog teams, palettes, and the Silph rescue gift."""
import json
import re
from pathlib import Path
from data import DOGS

ROOT = Path(__file__).resolve().parents[2]
plan = json.loads((ROOT / 'data/dogs/sabrina.json').read_text())
names = {d['name'] for d in DOGS}
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
level, name = plan['gifts']['silph']
assert name in names
path = ROOT / 'scripts/SilphCo7F.asm'
source, count = re.subn(r'\tlb bc, (?:LAPRAS|LEONTIDE), \d+', f'\tlb bc, {name}, {level}', path.read_text())
assert count == 1
path.write_text(source)
print(f'Generated {len(updated)} Saffron/Silph/Dojo parties, three palettes, and the level-{level} Silph dog gift.')
