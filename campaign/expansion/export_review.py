"""Map review and complete numbered route archive, with paginated move tables."""
from pathlib import Path
import json, math
from statistics import mean
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape,A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(r'C:\Users\rahul\Documents\Codex\2026-09-25\last-light-courier\outputs')
data=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))
pdfmetrics.registerFont(TTFont('Body',r'C:\Windows\Fonts\arial.ttf'));pdfmetrics.registerFont(TTFont('Bold',r'C:\Windows\Fonts\arialbd.ttf'))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
W,H=landscape(A4);style=ParagraphStyle('p',fontName='Body',fontSize=11,leading=16,textColor=HexColor('#24334a'))
def paragraph(c,t,x,y,w):
    p=Paragraph(t,style);_,h=p.wrap(w,900);p.drawOn(c,x,y-h);return y-h-13
def header(c,title,sub,page):
    c.setFillColor(HexColor('#f3f6fb'));c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(HexColor('#20334c'));c.setFont('Bold',22);c.drawString(30,H-42,title)
    c.setFont('Body',9);c.setFillColor(HexColor('#59687c'));c.drawString(30,H-64,sub)
    c.setStrokeColor(HexColor('#c8d2df'));c.line(30,H-76,W-30,H-76)
    c.setFont('Body',8);c.drawString(30,18,'Last Light Courier | 26 September 2026 | Rules preserved; new maps require playtesting');c.drawRightString(W-30,18,str(page))
def board(c,l,route=None,side=400,x0=42,y0=61):
    size=l.get('grid',8);tile=side/size;homes={tuple(h['p']):i+1 for i,h in enumerate(l['homes'])};pat=set(map(tuple,l['patrol']+(l['patrol2'] or [])));walls=set(l['walls'])
    features={tuple(l[f]):f for f in ['switch','gate','fade','ice','dark'] if l[f]};rep=tuple(l['repair']['tile']) if l['repair'] else None
    colors=dict(switch='#bce1c4',gate='#d9c7ea',fade='#e7c6a3',ice='#bae1ed',dark='#96a4bb')
    def center(p):return x0+(p[0]+.5)*tile,y0+(size-p[1]-.5)*tile
    for y in range(size):
        for x in range(size):
            p=(x,y);color='#d5dbe4' if f'{x},{y}' in walls else '#ffffff'
            if p in homes:color='#ffe0a1'
            if p==tuple(l['depot']):color='#b1d9f0'
            if p in features:color=colors[features[p]]
            c.setFillColor(HexColor(color));c.setStrokeColor(HexColor('#c3ccda'));c.setLineWidth(.35);c.rect(x0+x*tile,y0+(size-y-1)*tile,tile,tile,fill=1,stroke=1)
            if p in pat:c.setStrokeColor(HexColor('#aa85c4'));c.setLineWidth(1.1);c.rect(x0+x*tile+1.4,y0+(size-y-1)*tile+1.4,tile-2.8,tile-2.8,fill=0,stroke=1)
            if p==rep:c.setStrokeColor(HexColor('#d4514e' if l.get('repairRequired') else '#369b74'));c.setLineWidth(2);c.rect(x0+x*tile+1,y0+(size-y-1)*tile+1,tile-2,tile-2,fill=0,stroke=1)
            label=str(homes[p]) if p in homes else 'D' if p==tuple(l['depot']) else {'switch':'S','gate':'G','fade':'F','ice':'I','dark':'L'}.get(features.get(p),'')
            if label:c.setFillColor(HexColor('#293951'));c.setFont('Bold',min(11,tile*.5));cx,cy=center(p);c.drawCentredString(cx,cy-tile*.16,label)
    if route:
        c.setStrokeColor(HexColor('#237d7888'));c.setLineWidth(.8)
        for a,b in zip(route,route[1:]):
            ax,ay=center(a['p']);bx,by=center(b['p']);c.line(ax,ay,bx,by)
            mx=ax+(bx-ax)*.7;my=ay+(by-ay)*.7;ang=math.atan2(by-ay,bx-ax);d=min(3,tile*.16);c.line(mx,my,mx-d*math.cos(ang-.6),my-d*math.sin(ang-.6));c.line(mx,my,mx-d*math.cos(ang+.6),my-d*math.sin(ang+.6))
    c.setFillColor(HexColor('#59687c'));c.setFont('Body',6.5)
    for j in range(size):c.drawCentredString(x0+(j+.5)*tile,y0+side+6,str(j+1));c.drawRightString(x0-4,y0+(size-j-.5)*tile-2,str(j+1))
def intro(c,title,route=False):
    header(c,title,'1,000 maps total | 800 new maps | original 001-200 preserved',1)
    y=H-99
    texts=[
        '<b>Scope:</b> Levels 201-1000 are deterministic, varied map layouts built from street-loop and divided-district families. Existing patrol movement, two-step Echo trail, light costs, delivery refill, timed gates, ice and fading crossings are unchanged.',
        '<b>Difficulty direction:</b> the new campaign expands from 18 x 18 to 24 x 24 boards and 8 to 11 mandatory houses. Blockage generally falls from about 35% toward 21%, creating more junctions and loops. Reference-route light margin tightens from 10 toward 1. Complexity rises in bands; individual maps deliberately vary. Structural metrics and valid routes do not prove player difficulty or balanced shortest-route fuel.',
        '<b>Repair-required maps:</b> 32 new maps, every 25th level, split required houses across disconnected districts. They cannot be completed before the marked connection is repaired. A reserved level-bound free repair is specified for each, so gem spending is unnecessary. The gem shop and voucher collection UI remain a separate implementation task; these maps must not ship as paid progression locks.',
        '<b>Verification:</b> all archived routes were replayed under production movement rules. The original 200 retain their archived shortest routes. New maps store a verified completion route, with exact light, house mask, patrol phase, Echo and timer state at every move; global shortest routes for the 800 new maps are not claimed.',
        '<b>Read the map:</b> D = depot; numbered gold tiles = houses; violet outlines = patrol loops; S = switch; G = timed gate; F = fading crossing; I = ice; L = dark street. Gray tiles are blocked. Green outline = optional repair; red outline = mandatory connection. Teal arrows show a reference route, not the only solution. Coordinates in the PDF start at 1.',
        '<b>Review next:</b> inspect route choices, house orders, patrol interaction, temporary-crossing bypasses and repair value. Many extra streets permit shorter alternatives. Phone readability, hint-search performance, global optimum and economy balance need dedicated playtesting before release.'
    ]
    if route:texts.append('<b>Route tables:</b> each entry is move / column,row / light remaining. Move 0 is the start. Yellow means a house was newly lit; green is the finish. Long routes continue onto additional pages. Multiple visits are listed separately. JSON also records all shadow and timer states.')
    for text in texts:y=paragraph(c,text,30,y,W-60)
    c.showPage()
def export_review():
    path=OUT/'Last-Light-Courier-1000-Level-Review.pdf';c=canvas.Canvas(str(path),pagesize=(W,H));c.setTitle('Last Light Courier - 1000 level review');intro(c,'Campaign review: 1,000 levels')
    header(c,'Expansion progression','Measured structure, not a claim of human playtest difficulty',2)
    headings=['Levels','Grid','Houses','Avg block %','Avg junctions','Avg loops','Finish light','Free repairs']
    xs=[30,151,239,309,414,521,620,729]
    for x,h in zip(xs,headings):c.setFont('Bold',10);c.drawString(x,H-113,h)
    for b in range(8):
        es=data['levels'][200+b*100:300+b*100];ls=[e['map'] for e in es];y=H-150-b*37
        vals=[f'{201+b*100}-{300+b*100}',str(ls[0]['grid']),str(ls[0]['required']),f'{mean(l["metrics"]["blockedPercent"] for l in ls):.1f}',f'{mean(l["metrics"]["junctions"] for l in ls):.0f}',f'{mean(l["metrics"]["loops"] for l in ls):.0f}',f'{min(e["solutions"][0]["route"][-1]["light"] for e in es)}-{max(e["solutions"][0]["route"][-1]["light"] for e in es)}',str(sum(l['repairRequired'] for l in ls))]
        c.setFont('Body',11)
        for x,v in zip(xs,vals):c.drawString(x,y,v)
    paragraph(c,'A reserved free repair is specified for each required map. Optional repair gem prices are proposed metadata, not a shop implementation. The original 200-map game and APK are unchanged by this expansion package.',30,130,W-60);c.showPage()
    for e in data['levels']:
        l=e['map'];v=e['solutions'][0];n=l['n'];m=l.get('metrics')
        if not m:
            from build_1000 import metrics
            m=metrics(l)
        header(c,f'Level {n:04d} - '+('Repair required' if l.get('repairRequired') else 'Standard'),f'{l.get("grid",8)} x {l.get("grid",8)} | Light {l["required"]} of {len(l["homes"])} houses | Two patrols + Echo' if n>60 else f'{l.get("grid",8)} x {l.get("grid",8)} | Light {l["required"]} of {len(l["homes"])} houses | Original rules',n+2)
        c.bookmarkPage(f'level{n}');c.addOutlineEntry(f'Level {n}',f'level{n}',0,False)
        board(c,l,v['route']);x=466;y=H-105
        for text in [f'<b>Layout:</b> {m["blockedPercent"]}% blocked; {m["junctions"]} junctions; {m["loops"]} independent street loops.',f'<b>Verified route:</b> {v["steps"]} moves. Start light {v["route"][0]["light"]}; finish light {v["route"][-1]["light"]}. '+('Archived shortest route.' if n<=200 else 'Reference completion, not a global minimum.'),'<b>Objective:</b> '+l['brief'],('<b>Before repair:</b> not possible. Required houses lie in disconnected districts.<br/><b>Free item:</b> one reserved repair for this marked connection. Validate using the repaired layout.' if l.get('repairRequired') else '<b>Before repair:</b> a verified no-purchase completion exists. Optional upgrades may offer alternate routes.'),('<b>Proposed repair:</b> '+str(l.get('repairGemPrice'))+' gems; points are score only in the planned economy.' if n>200 else '<b>Legacy economy:</b> original repair data retained.'),'<b>Review focus:</b> house-order choices, lantern planning, shadow timing and detours. Gray density alone is not difficulty.']:
            y=paragraph(c,text,x,y,W-x-30)
        c.showPage()
    c.save();assert len(PdfReader(str(path)).pages)==1002;print('Created review PDF: 1002 pages',flush=True)
def export_routes():
    path=OUT/'Last-Light-Courier-1000-Map-Route-Archive.pdf';c=canvas.Canvas(str(path),pagesize=(W,H));c.setTitle('Last Light Courier - 1000 maps verified route archive');intro(c,'Verified routes: 1,000 maps',True);page=1
    for e in data['levels']:
        l=e['map']
        for v in e['solutions']:
            route=v['route'];chunks=[route[i:i+140] for i in range(0,len(route),140)]
            for chunkIndex,chunk in enumerate(chunks):
                page+=1;mode='Reserved free repair applied' if l.get('repairRequired') else 'Repair applied' if v['repairPurchased'] else 'No repair'
                header(c,f'Level {l["n"]:04d} - {mode}',f'{v["steps"]} moves | '+('Shortest archived route' if l['n']<=200 else 'Verified reference route; not a global minimum')+f' | Table part {chunkIndex+1} of {len(chunks)}',page)
                board(c,l,route,side=330,x0=43,y0=124)
                paragraph(c,'Columns and rows start at 1. Every visit is listed. '+('Repair is required before following this route.' if l.get('repairRequired') else 'Teal arrows show the full route.'),43,98,330)
                tx=408;top=479;col=98;rows=math.ceil(len(chunk)/4);rowh=11.5
                c.setFont('Bold',10);c.setFillColor(HexColor('#20334c'));c.drawString(tx,499,'Move / column,row / remaining light')
                for j,s in enumerate(chunk):
                    i=chunkIndex*140+j;cx=tx+(j//rows)*col;cy=top-(j%rows)*rowh
                    fresh=i>0 and s['mask']!=route[i-1]['mask'];finish=i==len(route)-1
                    if fresh or finish:c.setFillColor(HexColor('#d3e9dc' if finish else '#ffebbe'));c.rect(cx,cy-9,col-3,rowh-1,fill=1,stroke=0)
                    c.setFont('Body',8);c.setFillColor(HexColor('#20334c'));c.drawString(cx+2,cy-7,f'{i:03d} / {s["p"][0]+1:02d},{s["p"][1]+1:02d} / {s["light"]}')
                c.showPage()
    c.save();assert len(PdfReader(str(path)).pages)==page;print('Created route archive:',page,'pages',flush=True)
if __name__=='__main__':export_review();export_routes()
