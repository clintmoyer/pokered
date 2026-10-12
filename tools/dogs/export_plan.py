#!/usr/bin/env python3
"""Export reviewable roster and move tables from the finalized JSON design."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def acquisition_text(value):
    if value['method'] == 'evolution':
        return f"{value['from_slot']} at L{value['level']}"
    if value['method'] == 'stone_evolution':
        return f"{value['from_slot']} + {value['item']} (unlimited Celadon purchase)"
    levels = '-'.join(map(str, value['levels']))
    return f"{value['map']} {value['terrain']}, L{levels}, gate={value['gate']}"


def export():
    roster = json.loads((ROOT / 'data/dogs/roster.json').read_text())
    moves = json.loads((ROOT / 'data/dogs/moves.json').read_text())
    with (ROOT / 'docs/ROSTER.csv').open('w', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['dex', 'original_slot', 'short_name', 'full_breed', 'types', 'hp', 'attack', 'defense', 'speed', 'special', 'evolution', 'obtain', 'signature', 'initial_moves', 'level_up', 'tm_hm_slots'])
        for d in roster:
            evolution = f"L{d['evolution'][0]} -> {d['evolution'][1]}" if d['evolution'] else '; '.join(f"{e['item']} -> {e['target']}" for e in d.get('branch_evolutions', []))
            writer.writerow([d['dex'], d['slot'], d['name'], d['breed'], '/'.join(dict.fromkeys(d['types'])), *d['stats'], evolution, acquisition_text(d['acquisition']), d['signature'], '; '.join(d['base']), '; '.join(f'{level}:{move}' for level, move in d['learnset']), '; '.join(d['tms'])])
    with (ROOT / 'docs/MOVES.csv').open('w', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['id', 'original_slot', 'dog_move', 'type', 'power', 'accuracy', 'pp', 'effect', 'hm_function', 'animation'])
        for m in moves:
            writer.writerow([m['id'], m['slot'], m['name'], m['type'], m['power'], m['accuracy'], m['pp'], m['effect'], m['hm'] or '', m['animation']])
    lines = ['# Full dog roster', '', 'Generated from `data/dogs/roster.json` by `tools/dogs/export_plan.py`.', '', 'These 151 forms span 79 breed families. The design is finalized; implementation coverage is listed separately in `data/dogs/implemented.json`.', '', 'Stats below are HP / Attack / Defense / Speed / Special. See [ROSTER.csv](ROSTER.csv) for learnsets, signatures, and TM/HM compatibility.', '', '| Dex | Slot | Name | Breed | Types | Stats | Obtain |', '|---|---|---|---|---|---|---|']
    for d in roster:
        types = '/'.join(dict.fromkeys(d['types'])).replace('PSYCHIC_TYPE', 'PSYCHIC')
        lines.append(f"| {d['dex']} | {d['slot']} | {d['name']} | {d['breed']} | {types} | {'/'.join(map(str,d['stats']))} | {acquisition_text(d['acquisition'])} |")
    (ROOT / 'docs/ROSTER.md').write_text('\n'.join(lines) + '\n')
    print(f'Exported {len(roster)} forms and {len(moves)} moves.')


if __name__ == '__main__':
    export()
