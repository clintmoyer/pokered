#!/usr/bin/env python3
"""Keep each dog's front/back pair in the same bank; grow beyond one sprite bank."""
from pathlib import Path
import re
from data import DOGS, species_label, sprite_filename

ROOT = Path(__file__).resolve().parents[2]
CHUNK = 8
path = ROOT / 'gfx/pics.asm'
source = re.sub(r'^SECTION "Dog Pics[^"\n]*", ROMX\n', '', path.read_text(), flags=re.M)
for dog in DOGS:
    label = species_label(dog['slot'])
    for view in ('Front', 'Back'):
        source, count = re.subn(rf'^{label}Pic{view}::[^\n]*\n', '', source, flags=re.M)
        if dog['slot'] == 'MEW' and count == 0:
            # Mew's original pictures live beside its separate base stats.
            mew_path = ROOT / 'data/pokemon/mew.asm'
            value, count = re.subn(rf'^{label}Pic{view}::[^\n]*\n', '', mew_path.read_text(), flags=re.M)
            mew_path.write_text(value)
        assert count == 1, (label, view, count)
source = source.rstrip() + '\n\n'
sections = []
for offset in range(0, len(DOGS), CHUNK):
    number = offset // CHUNK + 1
    section = f'Dog Pics {number}'
    sections.append(f'ROMX ${0x2d + number - 1:X}\n\t"{section}"\n')
    source += f'SECTION "{section}", ROMX\n\n'
    for dog in DOGS[offset:offset + CHUNK]:
        label, filename = species_label(dog['slot']), sprite_filename(dog['slot'])
        source += f'{label}PicFront:: INCBIN "gfx/pokemon/front/{filename}.pic"\n'
        source += f'{label}PicBack:: INCBIN "gfx/pokemon/back/{filename}b.pic"\n'
    source += '\n'
path.write_text(source.rstrip()+'\n')
path = ROOT / 'layout.link'
source = re.sub(r'ROMX \$[0-9A-F]+\n\t"Dog Pics[^"\n]*"\n', '', path.read_text())
source = source.replace('WRAM0\n', ''.join(sections) + 'WRAM0\n')
path.write_text(source)
path = ROOT / 'home/pics.asm'
source = path.read_text()
table = 'DogSpriteSpecies:\n'
for dog in DOGS:
    table += f"\tdb {dog['slot']}, BANK({species_label(dog['slot'])}PicFront)\n"
table += '\tdb -1\n'
source, count = re.subn(r'DogSpriteSpecies:\n(?:\tdb [^\n]+\n)+', table, source)
assert count == 1
path.write_text(source)
print(f'Assigned {len(DOGS)} dog pairs to {len(sections)} sprite banks.')
