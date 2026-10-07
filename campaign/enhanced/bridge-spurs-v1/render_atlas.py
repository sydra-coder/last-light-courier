"""Render all final Light Bridge source maps as four review contact sheets."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).parent
line=next(line for line in (ROOT/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
routes=json.loads((HERE/'routes.json').read_text(encoding='utf-8'))
out=HERE/'atlas';out.mkdir(exist_ok=True)
font=ImageFont.load_default();tile=8;panel=216
for page in range(4):
    image=Image.new('RGB',(panel*5,panel*5),'#161d2b');draw=ImageDraw.Draw(image)
    for index in range(25):
        number=701+page*25+index;level=levels[number-1];route=routes[str(number)]
        x0=(index%5)*panel+18;y0=(index//5)*panel+30;walls=set(level['walls'])
        for y in range(level['grid']):
            for x in range(level['grid']):
                draw.rectangle((x0+x*tile,y0+y*tile,x0+x*tile+tile-1,y0+y*tile+tile-1),
                               fill='#121a28' if f'{x},{y}' in walls else '#40506a')
        for x,y in level.get('shadowInfluence2x2',{}).get('cells',[]):
            draw.rectangle((x0+x*tile,y0+y*tile,x0+x*tile+tile-1,y0+y*tile+tile-1),fill='#a64f82')
        for a,b in zip(route,route[1:]):
            draw.line((x0+a[0]*tile+tile//2,y0+a[1]*tile+tile//2,
                       x0+b[0]*tile+tile//2,y0+b[1]*tile+tile//2),fill='#79d5cb',width=2)
        for house in level['homes']:
            x,y=house['p'];draw.ellipse((x0+x*tile+1,y0+y*tile+1,x0+x*tile+tile-2,y0+y*tile+tile-2),fill='#ffc276')
        for point,color in ((level['lightBridge'],'#fc72cf'),(level['oneWayTile'],'#63a9ff'),(level['depot'],'#fff5d2')):
            x,y=point;draw.ellipse((x0+x*tile,y0+y*tile,x0+x*tile+tile-1,y0+y*tile+tile-1),fill=color)
        draw.text(((index%5)*panel+10,(index//5)*panel+9),f'{number}  {len(route)-1} steps  {level["cap"]} light',font=font,fill='#f6e5c7')
    target=out/f'bridge_maps_{page+1}.png';image.save(target)
    print(target)
