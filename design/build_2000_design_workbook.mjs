import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';

const root='C:/Sydra/Last Light Courier';
const out=path.join(root,'outputs/01a1112f-b897-7c03-a6b3-f25018e9f557');
const maps=JSON.parse(await fs.readFile(path.join(root,'CAMPAIGN_1000_LEVELS.json'),'utf8'));
const archive=JSON.parse(await fs.readFile(path.join(root,'design/map-solutions-1000.json'),'utf8')).levels;
if(maps.length!==1000||archive.length!==1000) throw Error('Expected 1,000 maps and route records');
const arcs=[
 ['Ember Road','Route, light, shadows'],['Dimming Crossroads','Trap, decoy, switch'],['Veiled Hamlet','Hidden houses and reveals'],['Lantern District','Functional houses'],['Broken Causeways','Fragile and one-way roads'],['Hunting Dark','Hunter, leech, 3×3 influence'],['The Shadowworks','Shadow locks and doors'],['River of Glass','Deposits and light bridges'],['Quake Frontier','Earthquake transformations'],['Faultline City','Triggered quakes and rotation'],['Storm March','Wind, storms, flood'],['The Long Night','Fog and day/night rules'],['Breachlands','Spawner, Echo, merge/split'],['The Lumen Engine','Light networks and overload'],["Keeper's Arsenal",'Advanced tools and stabilisation'],['Convergence','Learned systems interact'],['The Moving Kingdom','Chained map states'],['Last Provinces','Regional route strategy'],['Black Horizon','Multi-phase consequences'],['The Last Light','Bespoke mastery']
];
const powers=['Trap','Decoy','Reveal','Flask','Freeze','Light bridge','Road repair','Rewind','Stabilizer'];
const milestones={111:'Trap',131:'Decoy',211:'Reveal',311:'Flask',411:'Road repair',511:'Freeze',711:'Light bridge',811:'Stabilizer',1411:'Rewind'};
const phase=o=>o<10?'Introduce':o<35?'Practice':o<65?'Combine':o<85?'Pressure':o<99?'Variation':'Finale';
const eventFor=(arc,o)=>{
 if(arc===5&&o>=20&&o%5===0)return 'Leech dims recharge house';
 const e=[null,'Trap/decoy lure','Reveal on delivery','House ability on delivery','Road changes after crossing','Hunter shifts after delivery','Shadow occupies lock','Deposit opens bridge','Quake after delivery','Aftershock after switch','Storm turn window','Day/night turn window','Spawner threshold','Network overload','Tool-controlled map state','Two-system chain','Two-stage transformation','Region transit choice','Phase 2 after objective','Full-language sequence'][arc];
 return e||'Existing fixed hazards';
};
const proposedSupply=(n,arc,o)=>{
 const v=Array(9).fill(0); const give=(name,count=1)=>{v[powers.indexOf(name)]=count};
 if(n<101) return v;
 if(n>=111&&arc===1&&o%5===10%5) give('Trap');
 if(n>=131&&arc===1&&o%7===0) give('Decoy');
 if(n>=211&&arc===2&&o%6===0) give('Reveal');
 if(n>=311&&arc===3&&o%7===0) give('Flask');
 if(n>=411&&arc===4&&o%6===0) give('Road repair');
 if(n>=511&&arc===5&&o%8===0) give('Freeze');
 if(n>=711&&arc===7&&o%6===0) give('Light bridge');
 if(n>=811&&arc===8&&o%10===0) give('Stabilizer');
 if(n>=1411&&arc===14&&o%8===0) give('Rewind');
 if(n>=1501&&o%20===0) give(powers[[0,1,2,3,4,5,6,7,8][Math.floor(o/20)%9]]);
 // Revisit learned tools in later arcs; one supplied charge is a design target, not current inventory.
 if(arc>=2&&o%10===4){
  const unlocked=Object.entries(milestones).filter(([at])=>Number(at)<=n).map(([,name])=>name);
  if(unlocked.length)give(unlocked[(arc+Math.floor(o/10))%unlocked.length]);
 }
 for(const [at,name] of Object.entries(milestones)) if(n===Number(at)) give(name);
 return v;
};
const proposedShadow=(arc,o)=>arc===5?(o<20?'Hunter':o<50?'Leech':o<75?'Sentinel':'Hunter + Leech'):arc===6?'Shadow lock / door':arc===12?(o<50?'Spawner':'Merge / Split'):arc>=15?['Hunter','Leech','Sentinel','Spawner','Merge / Split'][Math.floor(o/20)]:null;
const proposedHazard=(arc,o)=>[null,'2×2 influence / gate timing','Hidden house / route','Recharge / beacon / cursed house','Fragile / one-way road','3×3 influence / recharge drain','Shadow lock / door','Light deposit / powered road','Earthquake','Aftershock / rotating district','Storm wind / flood','Fog / day-night','Spawner / merge-split','Light network / overload','Map control','Two-system combination','Chained transformation','Regional transit','Multi-phase consequence','Mastery combination'][arc]||'Existing route hazards';
const headers=['Level','Region','Status','Grid','Houses','Required','Patrol','Echo','Lantern','Shadow types','Map hazards','Bridge / road','Event / system','Free powers (+)','Min base','Min shortcut','Verified base','Verified shortcut','Route note'];
const rows=[headers];
const counts={exact:0,reference:0,planned:0,missingBase:0};
for(let n=1;n<=2000;n++){
 const arc=Math.floor((n-1)/100), o=(n-1)%100, a=arcs[arc], m=maps[n-1], record=archive[n-1];
 const s0=record?.solutions?.find(s=>!s.repairPurchased&&['solved','verified_reference'].includes(s.status));
 const s1=record?.solutions?.find(s=>s.repairPurchased&&['solved','verified_reference'].includes(s.status));
 const source=n<=200?'Playable baseline':n<=1000?'Archived map / reference':'Planning target';
 if(n<=200) counts.exact++; else if(n<=1000) counts.reference++; else counts.planned++;
 if(n<=1000&&!s0) counts.missingBase++;
 const supplied=proposedSupply(n,arc,o);
 if(m?.reservedFreeRepair) supplied[powers.indexOf('Road repair')]=1;
 const road=m?(m.repairRequired?'Required repair + free charge':m.repair?'Optional road repair':'None'):(arc===4?'Fragile / one-way':arc===7?'Light bridge':arc===8||arc===9||arc===16?'Transforming roads':arc===10?'Flood crossing':arc===17?'Transit link':'None planned');
 const existingHaz=m?['fade','dark','ice','switch','gate'].filter(k=>m[k]!=null).join(' / '):'';
 const mechanic=n<=50?(existingHaz||'Baseline route'):(n<=1000?`${existingHaz||'Baseline'} | proposal: ${eventFor(arc,o)}`:eventFor(arc,o));
 const timing=n<=50?'Existing fixed map':n<=1000?'Existing fixed; proposal trigger TBD':'Fixed authored trigger; turn/tile TBD';
 // Follow the 24×24 archive with a gentle reduction, then vary size for puzzle purpose.
 const grid=m?(m.grid||8):(arc===10?[22,22,20,22,20][Math.floor(o/20)]:[18,20,18,22,20][Math.floor(o/20)]);
 const homes=m?m.homes.length:[4,5,6,7,8][Math.floor(o/20)];
 const patrol=m?(m.patrol?1:0)+(m.patrol2?1:0):arc===12?2+(o>=65?1:0):2;
 const echo=m?Number(!!m.echo):(arc>=12&&o%4!==0?1:arc>=15&&o%5===0?1:0);
 const targetReserve=n<=1000?null:(o<10?6:o<35?5:o<65?4:o<85?3:o<99?2:1);
 // Later light starts cannot be set responsibly until a specific layout and its full state graph exist.
 const powerText=supplied.map((v,i)=>v?`${powers[i]} ${v}`:null).filter(Boolean).join(', ')||'—';
 const shadowBase=[`Patrol ${patrol}`,echo?`Echo ${echo}`:null].filter(Boolean).join(' + ');
 const shadowProposal=n<=50?null:proposedShadow(arc,o);
 const shadowMix=shadowProposal?`${shadowBase}; plan ${shadowProposal}`:shadowBase;
 const mapHazards=[existingHaz||null,n>50?`plan ${proposedHazard(arc,o)}`:null].filter(Boolean).join('; ')||'—';
 const routeNote=n<=50?'Opening preserved':n<=200?'Exact baseline steps; powers proposed':n<=1000?'Reference steps only; proposals untested':`Planned ${phase(o).toLowerCase()}; light reserve ${targetReserve}; solver needed`;
 rows.push([n,a[0],source,grid,homes,m?m.required:homes,patrol,echo,m?m.cap:null,shadowMix,mapHazards,road,mechanic,powerText,n<=200?(s0?.steps??null):null,n<=200?(s1?.steps??null):null,n<=1000?(s0?.steps??null):null,n<=1000?(s1?.steps??null):null,routeNote]);
}

const wb=Workbook.create();
const level=wb.worksheets.add('Level plan');
const rules=wb.worksheets.add('Design rules');
const catalog=wb.worksheets.add('Mechanics index');
for(const sh of [level,rules,catalog]){sh.showGridLines=false;sh.tabColor='#23656B';}
level.getRangeByIndexes(0,0,rows.length,headers.length).values=rows;
level.getUsedRange().format.font={name:'Aptos',size:10,color:'#213642'};
level.getRange('A1:S1').format={fill:'#183949',font:{name:'Aptos',size:10,bold:true,color:'#FFFFFF'},rowHeight:38,wrapText:true,verticalAlignment:'center'};
level.getRange('A1:S2001').format.rowHeight=22;
level.getRange('A1:S1').format.rowHeight=40;
level.getRange('A:A').format.columnWidth=9;
level.getRange('B:B').format.columnWidth=22;
level.getRange('C:C').format.columnWidth=24;
level.getRange('D:I').format.columnWidth=11;
level.getRange('J:J').format.columnWidth=34;
level.getRange('K:K').format.columnWidth=44;
level.getRange('L:L').format.columnWidth=28;
level.getRange('M:M').format.columnWidth=42;
level.getRange('N:N').format.columnWidth=35;
level.getRange('O:R').format.columnWidth=16;
level.getRange('S:S').format.columnWidth=39;
level.getRange('A1:S1').format.borders={bottom:{style:'medium',color:'#4D9A9D'}};
for(let i=100;i<=1900;i+=100){const rr=i+1;level.getRange(`A${rr}:S${rr}`).format.borders={bottom:{style:'medium',color:'#9FBBB9'}};}
level.freezePanes.freezeRows(1);level.freezePanes.freezeColumns(3);
const levelTable=level.tables.add('A1:S2001',true,'LevelDesignPlan');
levelTable.showFilterButton=true;

const ruleRows=[
 ['LAST LIGHT COURIER — 2,000 LEVEL DESIGN RULES',''],
 ['Decision','Fixed authored event timing for the first pass. A seeded variant is allowed only when its seed and full event timeline are locked before the player moves and every variant has a solver proof.'],
 ['Opening 1–50','Preserve the existing level records and feel. Existing patrol/repair/Echo timing is intentionally retained despite the handover differences.'],
 ['Source boundary','1–200 playable baseline; 201–1000 archived map records with replay-verified reference completions; 1001–2000 planning targets without authored maps.'],
 ['Steps meaning','For 1–200, base and shortcut columns hold archived exact shortest results. For 201–1000, route columns hold verified completions only. New-power minimums require an expanded map solver and are not claimed here.'],
 ['Lantern meaning','Lantern is the recorded start for 1–1000. Later starts stay blank until a map-specific route and light-budget proof exist; the reserve in Route note is a design goal, not granted light.'],
 ['Power counts','Free powers (+) lists proposed charges supplied within that level, not total persistent inventory. A dash means none supplied. All additions beyond the current map code need rules and solver integration.'],
 ['Unlock proposal','Trap 111; Decoy 131; Reveal 211; Flask 311; Road repair 411; Freeze 511; Light bridge 711; Stabilizer 811; Rewind 1411. These are design targets and may move after prototypes.'],
 ['Required-power rule','If a level needs a tool, its charge is supplied in that level or already guaranteed from progression. A purchase is never the only winning route.'],
 ['Trap rule proposal','Player lays a carried Anchor Trap on a legal tile. When a shadow enters, it cannot move for the rest of the run in the current sample. Specify stacking and tile occupation before campaign integration.'],
 ['House trigger rule','House delivery should change a visible route that affects a future choice. Never block the only path to the first required house. Preview the affected bridge/door and show the changed state.'],
 ['Event specification','For each authored map record: trigger (turn/house/tile), pre-event warning, exact tile/state delta, duration, repeatability, inventory effects, and reset on retry.'],
 ['Solver gate','Search courier position, deliveries, light, inventory, all shadow positions/phases, gate state, terrain state, event clock and event flags. Solve every forced post-event state and each optional branch.'],
 ['Fairness gate','Prove a no-purchase completion; prove mandatory supplies are available before use; prevent unreachable required houses, stranded courier, exhausted light, unavoidable shadow hit, or event loops.'],
 ['Variation gate','Use small authored event alternatives only after all alternatives pass the same solver/replay checks. Runtime randomness cannot change the board into an untested state.'],
 ['Fun cadence','Within each 100-level arc: 1–10 introduce; 11–35 practice; 36–65 combine; 66–85 pressure; 86–99 variation; 100 finale. After a finale, lower pressure briefly.'],
 ['Complexity cap','Prefer one main new system plus one familiar system. Keep later grids varied rather than expanding without limit; review phone readability and route variety.'],
 ['Grid transition','Level 1000 is 24×24; level 1001 starts at 22×22. Later maps vary mostly 18–22. A smaller map is used for a focused mechanic or breather, not as an abrupt campaign reset.'],
 ['Shadow movement','The current patrols travel around local 2×2 circuits. Keep that readable pattern in early levels. Hunter, Leech, Spawner and later variants may use authored routes or bounded zones; do not confine all shadows to 2×2 for the entire campaign.'],
 ['Shadow influence','Movement and influence are separate. A proposed early 2×2 influence footprint needs a visible boundary and exact effect; larger 3×3 influence belongs later. Existing maps currently record 2×2 patrol movement, not a proven 2×2 influence system.'],
 ['House light-off','Propose the first Leech/recharge interaction at level 521 after functional houses are introduced. A Leech temporarily dims a lit recharge/beacon house until the courier relights it; completed delivery remains credited. Verify the post-drain route and light budget.'],
 ['Release check','A planned row becomes an authored level only after map, exact rules, full-state solver result, independent replay, light margin, alternate-route review, and human playtest.'],
 [],['Start','End','Region','Primary system / design intention']
];
for(let i=0;i<arcs.length;i++)ruleRows.push([i*100+1,(i+1)*100,arcs[i][0],arcs[i][1]]);
rules.getRangeByIndexes(0,0,ruleRows.length,4).values=ruleRows.map(r=>[...r,...Array(4-r.length).fill(null)]);
rules.getUsedRange().format.font={name:'Aptos',size:10,color:'#213642'};
rules.getRange('A1:D1').merge();rules.getRange('A1:D1').format={fill:'#183949',font:{name:'Aptos',size:15,bold:true,color:'#FFFFFF'},rowHeight:34};
rules.getRange('A24:D24').format={fill:'#23656B',font:{name:'Aptos',size:10,bold:true,color:'#FFFFFF'},rowHeight:25};
rules.getRange('A:A').format.columnWidth=22;rules.getRange('B:B').format.columnWidth=24;rules.getRange('C:C').format.columnWidth=24;rules.getRange('D:D').format.columnWidth=52;
rules.getRange('A2:D22').format.rowHeight=58;
for(let rr=2;rr<=22;rr++) rules.getRange(`B${rr}:D${rr}`).merge();
rules.getRange('B2:D22').format.wrapText=true;
rules.getRange('B2:D22').format.verticalAlignment='center';
rules.getRange('A25:D44').format.rowHeight=24;
const mechanics=[
 ['Category','Mechanic / hazard','First planned','Status / test'],
 ...[['Anchor Trap',111],['Decoy Light',131],['Reveal Pulse',211],['Lumen Flask',311],['Road Repair',411],['Freeze Seal',511],['Light Bridge',711],['Map Stabilizer',811],['Rewind',1411]].map(([name,n])=>['Power',name,n,'Playable Power Lab sample; campaign use proposed']),
 ['Shadow','Patrol',1,'Existing 2×2 circuit; playable baseline'],['Shadow','Echo',41,'Existing map field; playable baseline'],
 ['Shadow','Hunter',501,'Planned; new shadow test'],['Shadow','Leech / house drain',521,'Planned; new shadow test'],['Shadow','Sentinel',551,'Planned; new shadow test'],['Shadow','Spawner',1201,'Planned; new shadow test'],['Shadow','Merge / Split',1251,'Planned; new shadow test'],
 ['Map','2×2 influence',111,'Proposed rule; not baseline movement'],['Map','3×3 influence',501,'Mechanic Lab ward is a separate prototype'],
 ['House','Hidden / beacon',211,'Mechanic Lab hidden-house trial'],['House','Recharge / cursed',311,'Proposed; Leech interaction later'],
 ['Road','Fragile / one-way',401,'Mechanic Lab one-use bridge trial'],['Road','Shadow lock / door',601,'Planned'],['Road','Light deposit / powered road',701,'Planned'],
 ['Event','Earthquake',801,'Mechanic Lab trial'],['Event','Aftershock / rotation',901,'Rotation trial; aftershock planned'],['Event','Storm / wind',1001,'Mechanic Lab gust trial'],['Event','Flood',1001,'Mechanic Lab ford trial'],['Event','Fog / day-night',1101,'Mechanic Lab nightfall trial'],
 ['Light','Network / overload',1301,'Planned'],['Map','Chained transformations',1601,'Planned']
];
catalog.getRangeByIndexes(0,0,mechanics.length,4).values=mechanics;
catalog.getUsedRange().format.font={name:'Aptos',size:10,color:'#213642'};
catalog.getRange('A1:D1').format={fill:'#183949',font:{name:'Aptos',size:10,bold:true,color:'#FFFFFF'},rowHeight:28};
catalog.getRange('A:A').format.columnWidth=15;catalog.getRange('B:B').format.columnWidth=29;catalog.getRange('C:C').format.columnWidth=17;catalog.getRange('D:D').format.columnWidth=53;
catalog.getRangeByIndexes(0,0,mechanics.length,4).format.rowHeight=24;
catalog.freezePanes.freezeRows(1);
const mechanicTable=catalog.tables.add(`A1:D${mechanics.length}`,true,'MechanicsIndex');mechanicTable.showFilterButton=true;
wb.recalculate();
await fs.mkdir(out,{recursive:true});
for(const [sheetName,range,file] of [['Level plan','A1:S13','preview-level.png'],['Design rules','A1:D27','preview-rules.png'],['Mechanics index','A1:D17','preview-mechanics.png']]){
 const pic=await wb.render({sheetName,range,scale:1,format:'png'});
 await fs.writeFile(path.join(out,file),new Uint8Array(await pic.arrayBuffer()));
}
const xlsx=await SpreadsheetFile.exportXlsx(wb);
const target=path.join(out,'Last_Light_Courier_2000_Level_Design_Plan.xlsx');
await xlsx.save(target);
console.log(JSON.stringify({target,rows:rows.length-1,counts,example:[rows[1].slice(0,14),rows[1000].slice(0,14),rows[2000].slice(0,14)]}));
