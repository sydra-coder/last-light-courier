// Replay every currently unresolved event-aware shortcut in the live preview.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const root=__dirname;
const reports=[
  ['event-aware-1301-1400-partial-replay.json',false],
  ['event-aware-1401-1500-live-replay.json',false],
  ...[1501,1601,1701,1801,1901].map(n=>[`event-aware-${n}-${n+99}-replay.json`,false]),
  ['event-aware-1801-1900-signal-replay.json',true],
  ['event-aware-1901-2000-signal-replay.json',true],
];
const verified=[];
const circuitBlocked=[];
for(const [name,signal] of reports){
  const report=JSON.parse(fs.readFileSync(path.join(root,name),'utf8'));
  for(const candidate of report.completedRoutes){
    api.choose(candidate.level);api.begin();
    const level=api.getLevel();
    if(level.repairRequired&&!api.buyFreeRepair())throw Error(`Repair unavailable: ${candidate.level}`);
    if(signal&&!api.signal())throw Error(`Signal unavailable: ${candidate.level}`);
    let blockedStep=null;
    for(let i=1;i<candidate.route.length;i++)
      if(!api.move(candidate.route[i])){blockedStep=i;break}
    if(blockedStep!==null){
      const state=api.getState();
      if(level.networkCircuitRequired&&blockedStep===candidate.route.length-1&&
         state.mask===(1<<level.homes.length)-1&&!state.done&&
         !(state.networkCharged&&state.overloadCrossed&&state.transferCollected)){
        circuitBlocked.push(candidate.level);continue;
      }
      throw Error(`${name}: ${candidate.level} move ${blockedStep} failed unexpectedly`);
    }
    const finish=api.getState();
    if(!finish.done||finish.failed||candidate.steps>=candidate.referenceSteps)
      throw Error(`${name}: ${candidate.level} no longer proves a shorter completion`);
    verified.push({level:candidate.level,signal,steps:candidate.steps,
      referenceSteps:candidate.referenceSteps,saved:candidate.referenceSteps-candidate.steps,
      repairRequired:!!level.repairRequired,finishLight:finish.light,source:name});
  }
}
const byLevel=new Map();
for(const row of verified){
  const result=byLevel.get(row.level)||{level:row.level,defaultSteps:null,signalSteps:null,
    recordedDefaultSteps:null,recordedSignalSteps:null,repairRequired:row.repairRequired};
  if(row.signal){result.signalSteps=Math.min(result.signalSteps??Infinity,row.steps);result.recordedSignalSteps=row.referenceSteps}
  else{result.defaultSteps=Math.min(result.defaultSteps??Infinity,row.steps);result.recordedDefaultSteps=row.referenceSteps}
  byLevel.set(row.level,result);
}
const rows=[...byLevel.values()].sort((a,b)=>a.level-b.level);
const exact=new Map(JSON.parse(fs.readFileSync(path.join(root,'event-aware-exact-minima-late.json'),'utf8')).certified.map(x=>[x.level,x]));
const express=JSON.parse(fs.readFileSync(path.join(root,'transit-v1/express_routes.json'),'utf8'));
const transitExact=new Map(JSON.parse(fs.readFileSync(path.join(root,'transit-v1/exact_transit_minima.json'),'utf8')).certified.map(x=>[x.level,x]));
const signalExact=new Map(JSON.parse(fs.readFileSync(path.join(root,'phase-choices-v1/exact_signal_minima.json'),'utf8')).certified.map(x=>[x.level,x]));
for(const proof of express){
  api.choose(proof.level);api.begin();
  const level=api.getLevel();
  if(level.repairRequired)api.buyFreeRepair();
  for(let i=1;i<proof.route.length;i++)if(!api.move(proof.route[i]))throw Error(`Express route blocked ${proof.level}:${i}`);
  const finish=api.getState();
  if(!finish.done||finish.failed||finish.turns!==proof.transitSteps||finish.light!==proof.transitFinishLight)
    throw Error(`Express proof stale ${proof.level}`);
  const row=byLevel.get(proof.level);
  if(!row||proof.transitSteps>=row.defaultSteps)throw Error(`Express shortcut not better ${proof.level}`);
  row.expressTransitSteps=proof.transitSteps;
  if(transitExact.has(proof.level)){
    if(transitExact.get(proof.level).exactSteps!==proof.transitSteps)throw Error(`Express certificate mismatch ${proof.level}`);
    row.exactTransitSteps=proof.transitSteps;
  }
}
for(const row of rows)if(exact.has(row.level))row.exactNoPowerSteps=exact.get(row.level).exactNoPowerSteps;
for(const row of rows)if(signalExact.has(row.level)){
  const proof=signalExact.get(row.level);
  if(row.signalSteps!==proof.exactSignalSteps)throw Error(`Signal certificate mismatch ${row.level}`);
  row.exactSignalSteps=proof.exactSignalSteps;
}
const result={scope:'Every listed shortcut beats an older route archive and replays under current full preview rules. No-power, transit-inclusive and signaled certificates establish exact steps for their stated repair conditions. Network bypasses rejected at the depot are excluded. All listed maps require quality review.',
  routes:verified.length,levels:rows.length,exactCertified:rows.filter(x=>x.exactNoPowerSteps).length,
  exactTransitCertified:rows.filter(x=>x.exactTransitSteps).length,
  exactSignalCertified:rows.filter(x=>x.exactSignalSteps).length,
  redesignPending:rows.filter(x=>!x.exactNoPowerSteps&&!x.exactTransitSteps&&!x.exactSignalSteps).length,
  circuitBlocked:[...new Set(circuitBlocked)].sort((a,b)=>a-b),rows};
fs.writeFileSync(path.join(root,'event-aware-unresolved-shortcuts.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify({routes:result.routes,levels:result.levels,
  byBand:Object.fromEntries([...new Set(rows.map(x=>Math.floor((x.level-1)/100)*100+1))].map(start=>[start,rows.filter(x=>x.level>=start&&x.level<start+100).length]))}));
