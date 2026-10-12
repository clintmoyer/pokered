#!/usr/bin/env python3
"""Crop generated atlases and encode crisp four-shade Game Boy PNGs."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
STARTERS = [('bulbasaur','ivysaur','venusaur'), ('charmander','charmeleon','charizard'), ('squirtle','wartortle','blastoise')]
COMPANIONS = [('rattata','raticate','caterpie'), ('metapod','butterfree','mankey'), ('primeape','geodude','graveler'), ('golem','onix',None)]
MISTY_A = [('weedle','kakuna','beedrill'), ('pidgey','pidgeotto','pidgeot'), ('spearow','fearow','ekans'), ('arbok','pikachu','raichu')]
MISTY_B = [('sandshrew','sandslash','jigglypuff'), ('wigglytuff','zubat','golbat'), ('oddish','gloom','vileplume'), ('abra','kadabra','alakazam')]
MISTY_C = [('magikarp','gyarados','staryu'), ('starmie',None,None), (None,None,None), (None,None,None)]

def encode(image, size, content):
    image = image.convert('RGBA')
    mask = image.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError('Empty sprite cell')
    image = image.crop(bbox)
    image.thumbnail((content, content), Image.Resampling.NEAREST)
    canvas = Image.new('RGBA', (size,size), (255,255,255,255))
    # Force hard transparency before palette conversion.
    image.putalpha(image.getchannel('A').point(lambda a: 255 if a >= 128 else 0))
    canvas.alpha_composite(image, ((size-image.width)//2, size-image.height-2))
    grayscale = canvas.convert('L').point(lambda v: min((0,85,170,255), key=lambda p: abs(p-v)))
    return grayscale

def atlas(path, roster, row_bounds=None):
    source = Image.open(path)
    if row_bounds is None:
        row_bounds = [round(source.height*i/len(roster)) for i in range(len(roster)+1)]
    for row, species_list in enumerate(roster):
        for pair, species in enumerate(species_list):
            if species is None:
                continue
            for view in range(2):
                col = pair*2 + view
                crop = source.crop((round(source.width*col/6), row_bounds[row], round(source.width*(col+1)/6), row_bounds[row+1]))
                size = 32 if view else 56
                content = 28 if view else (42,48,52)[pair] if roster == STARTERS else 50
                result = encode(crop, size, content)
                destination = ROOT / ('gfx/pokemon/back' if view else 'gfx/pokemon/front') / (species+('b' if view else '')+'.png')
                result.save(destination)

atlas(ROOT/'assets/dogs/starters-source.png', STARTERS, [0,380,674,1024])
companion_source = ROOT/'assets/dogs/companions-source.png'
if companion_source.exists():
    atlas(companion_source, COMPANIONS, [0,280,510,750,1024])
for name, roster in [('a',MISTY_A),('b',MISTY_B),('c',MISTY_C)]:
    source = ROOT/f'assets/dogs/misty-{name}-source.png'
    if source.exists():
        bounds = {'a':[0,257,506,758,1024], 'b':[0,256,511,750,1024], 'c':[0,281,600,800,1024]}
        atlas(source, roster, bounds[name])

# The quadruped menu icon stores two 8x16 halves in an 8x32 strip.
icon = Image.open(ROOT/'gfx/pokemon/front/bulbasaur.png').crop((10,6,46,42)).resize((16,16), Image.Resampling.NEAREST)
strip = Image.new('L',(8,32),255)
strip.paste(icon.crop((0,0,8,16)),(0,0))
strip.paste(icon.crop((8,0,16,16)),(0,16))
strip.save(ROOT/'gfx/icons/quadruped.png')

# Generic overworld monsters (Bill, the Cerulean companion, and other NPCs).
# Sprite layout is standing down/up/left, then walking down/up/left.
source = ROOT/'assets/dogs/overworld-source.png'
if source.exists():
    sheet = Image.open(source)
    strip = Image.new('L',(16,96),255)
    for frame in range(6):
        row,col=divmod(frame,3)
        crop=sheet.crop((sheet.width*col//3,sheet.height*row//2,sheet.width*(col+1)//3,sheet.height*(row+1)//2))
        strip.paste(encode(crop,16,14),(0,frame*16))
    strip.save(ROOT/'gfx/sprites/monster.png')

from data import DOGS
preview = Image.new('RGB',(600, len(DOGS)*84),'#f5f1e8')
draw = ImageDraw.Draw(preview)
for index, dog in enumerate(DOGS):
    species = dog['slot'].lower()
    y = index*84
    draw.text((8,y+12), dog['name']+' / '+dog['breed'], fill='black')
    for view, x in [('front',350),('back',480)]:
        filename = species+('b' if view == 'back' else '')+'.png'
        im = Image.open(ROOT/f'gfx/pokemon/{view}'/filename).convert('RGB')
        im.thumbnail((64,64),Image.Resampling.NEAREST)
        preview.paste(im,(x,y+6))
(ROOT/'build/qa').mkdir(parents=True,exist_ok=True)
preview.save(ROOT/'build/qa/sprite-preview.png')
grid = Image.new('RGB',(960, ((len(DOGS)+5)//6)*104),'#f5f1e8')
draw = ImageDraw.Draw(grid)
for index, dog in enumerate(DOGS):
    x,y=(index%6)*160,(index//6)*104
    draw.text((x+4,y+3),dog['name'],fill='black')
    for view,dx in [('front',4),('back',84)]:
        filename=dog['slot'].lower()+('b' if view=='back' else '')+'.png'
        im=Image.open(ROOT/f'gfx/pokemon/{view}'/filename).convert('RGB')
        grid.paste(im,(x+dx,y+20))
grid.save(ROOT/'build/qa/sprite-grid.png')
print('Converted starter sprites'+(' and companion sprites.' if companion_source.exists() else '.'))
