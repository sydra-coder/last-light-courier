import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const root = 'C:/Sydra/Last Light Courier';
const out = path.join(root, 'outputs/01a11116-d047-76b1-be23-e386d7dced2f');
await fs.mkdir(out, { recursive: true });
const existing = JSON.parse(await fs.readFile(path.join(root, 'CAMPAIGN_1000_LEVELS.json'), 'utf8'));
if (existing.length !== 1000 || existing.some((v, i) => v.n !== i + 1)) throw new Error('Unexpected source level numbering');

const bands = [
  [1,100,'Courier basics','Existing archive','Core / early repair','Learn deliveries, banking, light and first hazards'],
  [101,200,'Classic expansion','Existing archive','Second patrol / echo','Scale routes and shadow timing'],
  [201,300,'Branching streets I','Existing archive','Repair choices','Validate route variety and economy'],
  [301,400,'Branching streets II','Existing archive','Repair choices','Shorter light reserves'],
  [401,500,'Wider districts I','Existing archive','Patrol + gates','Keep route options readable'],
  [501,600,'Wider districts II','Existing archive','Patrol + gates','Tighter route planning'],
  [601,700,'Large districts I','Existing archive','Hazard mix','Audit turn burden on phones'],
  [701,800,'Large districts II','Existing archive','Hazard mix','Improve route variety'],
  [801,900,'Large districts III','Existing archive','Hazard mix','Review tight light and visibility'],
  [901,1000,'Large districts IV','Existing archive','Hazard mix','Review straight routes before shipping'],
  [1001,1100,'Second journey reset','Proposed design','Route mastery','Reintroduce readable branching routes; no new hazard'],
  [1101,1200,'Shadow trap','Proposed / rule TBD','Shadow trap candidate','Teach one trap, then combine with patrols'],
  [1201,1300,'Influence zone','Proposed / rule TBD','3×3 influence candidate','Teach area effect and safe timing'],
  [1301,1400,'Revealed houses','Proposed / rule TBD','Hidden/reveal + house unlock candidate','House order becomes a route decision'],
  [1401,1500,'Shifting ground','Proposed / rule TBD','Earthquake candidate','Preview deterministic map change before commitment'],
  [1501,1600,'Storm front','Proposed / rule TBD','Storm candidate','Weather changes route cost or visibility'],
  [1601,1700,'Floodplain','Proposed / rule TBD','Flood candidate','Temporary crossings and detours'],
  [1701,1800,'Long night','Proposed / rule TBD','Night candidate','Light management under a readable clock'],
  [1801,1900,'Turning city','Proposed / rule TBD','Rotation candidate','Board changes with safe preview and undo'],
  [1901,2000,'Combined finale','Proposed / rule TBD','Approved mechanics only','One primary event plus one familiar supporting hazard'],
];

const wb = Workbook.create();
const overview = wb.worksheets.add('Progression');
const levels = wb.worksheets.add('Level plan');
const mechanics = wb.worksheets.add('Mechanics & sources');
for (const s of [overview,levels,mechanics]) { s.showGridLines=false; s.tabColor='#21475C'; }

const ovRows = [
  ['LAST LIGHT COURIER · 2,000-LEVEL PROGRESSION'],
  ['Planning status','1–1,000 = recorded map data; 1,001–2,000 = design targets, not authored maps.'],
  ['Design principle','Difficulty rises through meaningful choices and timing, not map size alone. Keep large maps legible on a phone.'],
  ['Extension beyond 2,000','Add one approved rule per 100-level arc; teach, practice, combine, then rest. Revalidate solver and economy.'],
  ['Release gate','No candidate mechanic ships until its exact deterministic rule, preview, failure behavior, and no-purchase solution are verified.'],
  [],
  ['Start','End','Arc','Status','Primary focus','Review target'],
  ...bands,
  [],
  ['DESIGN CADENCE (proposed for each new 100-level arc)'],
  ['Levels 1–10','Teach rule with safe margin; first example isolates the new rule.'],
  ['Levels 11–40','Practice several route layouts; at least two meaningful route choices.'],
  ['Levels 41–70','Combine with one familiar mechanic; never stack two new rules.'],
  ['Levels 71–90','Increase timing and resource pressure, with validated alternate route.'],
  ['Levels 91–100','Mastery and finale, followed by a breather at the next arc.'],
  ['Light targets','Plan 6→2 spare light by subphase; 1-light finales only after solver and playtest. This is a design target, not source data.'],
  ['Route targets','At least 3 meaningful junctions on medium/large maps; avoid long mandatory straight corridors, especially 901–1,000.'],
  ['Power fairness','Any stage-earned or shop-replenished power is optional unless the level grants it free within the run. No paid lock.'],
];
overview.getRangeByIndexes(0,0,ovRows.length,6).values=ovRows.map(r=>[...r,...Array(6-r.length).fill(null)]);
for(const r of [2,3,4,5,30,31,32,33,34,35,36,37,38]) overview.getRange(`B${r}:F${r}`).merge();

const headers=['Level','Chapter','Record status','Arc','Phase','Grid target / actual','Houses target / actual','Required houses actual','Light cap actual','Reference margin actual','Target spare light','Patrol count actual','Echo actual','Core hazard actual','New mechanic candidate','Power milestone candidate','Repair required actual','Route design target','Validation / decision'];
const rows=[headers];
const arcFor=n=>bands[Math.floor((n-1)/100)];
for (const v of existing) {
  const haz=['fade','dark','switch','gate','ice','repair'].filter(k=>v[k]!=null).join(', ');
  const b=arcFor(v.n);
  rows.push([v.n,v.chapter,'Existing JSON',b[2],null,v.grid ?? 8,v.homes.length,v.required,v.cap,v.referenceMargin ?? null,null,v.patrol2?2:1,!!v.echo,haz,null,null,!!v.repairRequired,null,v.n>=901?'Review route shape; source map is unchanged':'Source map; not reauthored']);
}
const phaseFor=offset=>offset<10?'Teach':offset<40?'Practice':offset<70?'Combine':offset<90?'Pressure':'Mastery';
const spareFor=offset=>offset<10?6:offset<40?5:offset<70?4:offset<90?3:2;
const powerMilestones={1101:'Shadow-sense candidate',1201:'Ward candidate',1301:'Reveal pulse candidate',1401:'Stabilizer candidate',1501:'Storm shelter candidate',1601:'Crossing kit candidate',1701:'Light reserve candidate',1801:'Anchor candidate'};
for(let n=1001;n<=2000;n++){
  const b=arcFor(n), offset=(n-1)%100, phase=phaseFor(offset);
  const candidate=b[4]==='Route mastery'?null:b[4].replace(' candidate','');
  const grid=offset<10?18:offset<40?20:offset<70?22:24;
  const houses=offset<10?7:offset<40?8:offset<70?9:10;
  const route=phase==='Teach'?'One clear rule; visible safe branch':phase==='Practice'?'At least 3 junctions; two viable routes':phase==='Combine'?'One new rule + one familiar hazard; branch':phase==='Pressure'?'Two viable strategies; no blind timing':'Finale with validated detour and recovery';
  rows.push([n,Math.ceil(n/10),'Proposed only',b[2],phase,grid,houses,null,null,null,spareFor(offset),null,null,null,candidate,powerMilestones[n]??null,null,route,'Define rule, author map, solver replay, phone playtest']);
}
levels.getRangeByIndexes(0,0,rows.length,headers.length).values=rows;

const mechRows=[
  ['Mechanic / system','Handover status','What is recorded','Planning treatment / open decision','Source'],
  ['Shadow trap','Not named exactly','Generic traps and shadow-house interactions are mentioned.','Candidate for 1101–1200. Define trigger, warning, duration, escape, and solver state before building.','CODEX_MASTER_PROMPT.md § mechanics'],
  ['Earthquake','Named concept','Deterministic earthquake is explicitly listed; no timing or tile rules.','Candidate for 1401–1500. Define forecast, affected tiles, trigger, repeatability, and safe fallback.','CODEX_MASTER_PROMPT.md; BRANCH_COMPARISON.md'],
  ['Storm','Named concept','Listed with deterministic world events; no detailed rule.','Candidate for 1501–1600; define visibility, movement/light cost, and preview.','CODEX_MASTER_PROMPT.md; BRANCH_COMPARISON.md'],
  ['Flood','Named concept','Listed with deterministic world events; no detailed rule.','Candidate for 1601–1700; define rising/falling schedule and crossings.','CODEX_MASTER_PROMPT.md; BRANCH_COMPARISON.md'],
  ['Night','Named concept','Listed with deterministic world events; no detailed rule.','Candidate for 1701–1800; define clock and light pressure.','CODEX_MASTER_PROMPT.md; BRANCH_COMPARISON.md'],
  ['Rotation','Named concept','Listed with deterministic world events; no detailed rule.','Candidate for 1801–1900; define affected area and positional safety.','CODEX_MASTER_PROMPT.md; BRANCH_COMPARISON.md'],
  ['3×3 influence','Named concept','3×3 influence is listed without effect definition.','Candidate for 1201–1300; define radius, duration, stacking, and UI.','CODEX_MASTER_PROMPT.md'],
  ['Hidden houses / house unlocks','Named concept','Hidden houses and house-triggered unlocks are listed.','Candidate for 1301–1400; define reveal order and fair route preview.','CODEX_MASTER_PROMPT.md'],
  ['Special powers','High-level intent','Powers earned at stage milestones and replenished in shop; no complete catalog, costs or cooldowns.','Power names in Level plan are suggestions only. Approve catalog and no-purchase solutions first.','BRANCH_COMPARISON.md; CODEX_MASTER_PROMPT.md'],
  ['Hints / repair / tunnel','Separate design proposal','Shop plan proposes hint, repair voucher and tunnel token with preliminary gem values. Not fully integrated.','Keep separate from canonical existing levels; balance after mechanic prototypes.','design/shop-hints-plan.md'],
  ['Existing hazards','Recorded data','Patrol, echo, fade, dark, switch, gate, ice and repair appear in 1,000-map JSON.','Use actual fields in Level plan. Existing route archive is verified reference, not global shortest proof.','CAMPAIGN_1000_LEVELS.json; design/campaign-1000-handoff.md'],
  ['Existing 1–1,000 status','Recorded data','1,000 records / 100 chapters; 201–1,000 route validation; 32 repair-required maps every 25 levels from 225.','No source map changed. Prior 901–1,000 straight-route feedback remains a review item.','design/campaign-1000-handoff.md'],
  ['2,000-level target','Handover vision','Enhanced branch targets 2,000, but no authored 1,001–2,000 map set was found.','This workbook proposes progression only; map authoring comes after rule approval.','BRANCH_COMPARISON.md; START_HERE.md'],
];
mechanics.getRangeByIndexes(0,0,mechRows.length,5).values=mechRows;

const navy='#163044', teal='#1C6670', white='#FFFFFF', ink='#203747', pale='#E9F3F1';
for (const s of [overview,levels,mechanics]) s.getUsedRange().format.font={name:'Aptos',size:10,color:ink};
overview.getRange('A1:F1').merge(); overview.getRange('A1').format={fill:navy,font:{name:'Aptos Display',size:18,bold:true,color:white}};
overview.getRange('A7:F7').format={fill:teal,font:{name:'Aptos',size:10,bold:true,color:white}};
overview.getRange('A29:F29').merge(); overview.getRange('A29').format={fill:navy,font:{name:'Aptos',size:12,bold:true,color:white}};
overview.getRange('A1:F36').format.rowHeight=27;
overview.getRange('A:A').format.columnWidth=20;
overview.getRange('B:B').format.columnWidth=17;
overview.getRange('C:C').format.columnWidth=29;
overview.getRange('D:D').format.columnWidth=24;
overview.getRange('E:E').format.columnWidth=34;
overview.getRange('F:F').format.columnWidth=70;
overview.getRange('B2:F5').format.wrapText=true;
overview.getRange('B30:F36').format.wrapText=true;
overview.getRange('A2:F5').format.rowHeight=42;
overview.getRange('A30:F38').format.rowHeight=34;
overview.getRange('A8:F27').format.rowHeight=38;
overview.getRange('C8:F27').format.wrapText=true;
overview.freezePanes.freezeRows(7);

levels.getRange('A1:S1').format={fill:navy,font:{name:'Aptos',size:10,bold:true,color:white}};
levels.getRange('A1:S1').format.rowHeight=32;
levels.getRange('A:A').format.columnWidth=9;
levels.getRange('B:B').format.columnWidth=9;
levels.getRange('C:C').format.columnWidth=18;
levels.getRange('D:D').format.columnWidth=25;
levels.getRange('E:E').format.columnWidth=13;
levels.getRange('F:M').format.columnWidth=16;
levels.getRange('N:N').format.columnWidth=32;
levels.getRange('O:O').format.columnWidth=27;
levels.getRange('P:P').format.columnWidth=28;
levels.getRange('Q:Q').format.columnWidth=18;
levels.getRange('R:R').format.columnWidth=46;
levels.getRange('S:S').format.columnWidth=53;
levels.getRange('A1:S1').format.wrapText=true;
levels.getRange('C2:C1001').format.fill=pale;
levels.getRange('C1002:C2001').format.fill='#FFF2DA';
levels.freezePanes.freezeRows(1);
levels.tables.add('A1:S2001',true,'LevelPlanTable');

mechanics.getRange('A1:E1').format={fill:navy,font:{name:'Aptos',size:10,bold:true,color:white}};
mechanics.getRange('A:A').format.columnWidth=28;
mechanics.getRange('B:B').format.columnWidth=23;
mechanics.getRange('C:C').format.columnWidth=65;
mechanics.getRange('D:D').format.columnWidth=83;
mechanics.getRange('E:E').format.columnWidth=56;
mechanics.getRange(`A2:E${mechRows.length}`).format.rowHeight=54;
mechanics.getRange(`A1:E${mechRows.length}`).format.wrapText=true;
mechanics.getRange(`A1:E${mechRows.length}`).format.verticalAlignment='center';
mechanics.freezePanes.freezeRows(1);
mechanics.tables.add(`A1:E${mechRows.length}`,true,'MechanicsSourcesTable');

wb.recalculate();
const info=await wb.inspect({kind:'workbook,sheet,table',maxChars:4000,tableMaxRows:3,tableMaxCols:6});
console.log(JSON.stringify(info).slice(0,4000));
for(const [sheetName,range,file] of [['Progression','A1:F37','progression-preview.png'],['Level plan','A1:S12','level-plan-preview.png'],['Mechanics & sources','A1:E8','mechanics-preview.png']]){
  const p=await wb.render({sheetName,range,scale:1,format:'png'});
  await fs.writeFile(path.join(out,file),new Uint8Array(await p.arrayBuffer()));
}
const xlsx=await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(path.join(out,'Last_Light_Courier_2000_Level_Progression.xlsx'));
console.log(`Saved ${path.join(out,'Last_Light_Courier_2000_Level_Progression.xlsx')}`);
