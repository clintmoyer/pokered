#!/usr/bin/env python3
"""Generate shared Cerulean Cave encounters, guardian levels and palettes."""
import json
import re
from pathlib import Path
from data import DOGS

ROOT = Path(__file__).resolve().parents[2]
plan = json.loads((ROOT / 'data/dogs/postgame.json').read_text())
names = {d['name'] for d in DOGS}
for name, encounters in plan['wild'].items():
    assert len(encounters) == 10 and all(dog in names for _, dog in encounters)
    lines = [name + 'WildMons:', f"\tdef_grass_wildmons {plan['rates'][name]}"]
    lines += [f'\tdb {level:2d}, {dog}' for level, dog in encounters]
    lines += ['\tend_grass_wildmons', '', '\tdef_water_wildmons 0', '\tend_water_wildmons', '']
    (ROOT / f'data/wild/maps/{name}.asm').write_text('\n'.join(lines))
path = ROOT / 'data/pokemon/palettes.asm'
source = path.read_text()
for slot, palette in plan['palettes'].items():
    source, count = re.subn(rf'^\tdb PAL_\w+\s+; {slot}(?: / [A-Z]+)?$',
                           f'\tdb {palette:<13} ; {slot}', source, flags=re.M)
    assert count == 1, slot
path.write_text(source)
path = ROOT / 'data/maps/objects/CeruleanCaveB1F.asm'
source, count = re.subn(r'(TEXT_CERULEANCAVEB1F_MEWTWO, )\w+, \d+', r'\g<1>PSIGUARD, 60', path.read_text())
assert count == 1
path.write_text(source)
print('Generated three shared Cave encounter tables, two guardian palettes and PSIGUARD at level 60.')
