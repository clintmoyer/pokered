"""Load the finalized design and select the forms implemented in this ROM slice."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROSTER = json.loads((ROOT / 'data/dogs/roster.json').read_text())
MOVE_PLAN = json.loads((ROOT / 'data/dogs/moves.json').read_text())
IMPLEMENTED = set(json.loads((ROOT / 'data/dogs/implemented.json').read_text()))

def species_label(slot):
    return ''.join(part.capitalize() for part in slot.split('_'))

def sprite_filename(slot):
    return 'mr.mime' if slot == 'MR_MIME' else slot.lower().replace('_', '')

DOGS = []
for record in ROSTER:
    if record['slot'] in IMPLEMENTED:
        dog = dict(record)
        for field in ('stats', 'types', 'base', 'tms', 'height'):
            dog[field] = tuple(dog[field])
        DOGS.append(dog)

# alias: stable original move slot, display name, effect, power, type, accuracy, PP
MOVES = {
    m['alias']: (m['slot'], m['name'], m['effect'], m['power'], m['type'], m['accuracy'], m['pp'])
    for m in MOVE_PLAN
}
