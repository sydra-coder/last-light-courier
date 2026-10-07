// Replay every late reference route to expose lantern slack and progression outliers.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const root=__dirname;
const defaults=JSON.parse(fs.readFileSync(process.env.LLC_HINTS_PATH||path.join(root,'reference-hints-v1/normalized_routes.json'),'utf8'));
const signals=JSON.parse(fs.readFileSync(process.env.LLC_SIGNAL_HINTS_PATH||path.join(root,'reference-hints-v1/normalized_signal_routes.json'),'utf8'));
const rows=[];
function replay(n,branch,checkpoints){
  api.choose(n);api.begin();
  const level=api.getLevel();
  if(level.repairRequired)api.buyFreeRepair();
  if(branch==='signal'&&!api.signal())throw Error(`Level ${n}: signal unavailable`);
  for(let i=1;i<checkpoints.length;i++){
    const point=checkpoints[i];
    if(!api.move([point[0],point[1]]))throw Error(`Level ${n} ${branch}: route blocked at ${i}`);
  }
  const end=api.getState();
  if(!end.done||end.failed||end.turns!==checkpoints.length-1)
    throw Error(`Level ${n} ${branch}: route did not finish`);
  return {level:n,branch,grid:level.grid,houses:level.homes.length,cap:level.cap,
    steps:end.turns,finishLight:end.light,lightFraction:+(end.light/level.cap).toFixed(3),
    requiredFreeRepair:!!level.repairRequired,ratedMinimum:api.minimum(),
    family:level.enhancedPlan?.eventFamily||level.masteryArchetype||'other'};
}
for(let n=1001;n<=2000;n++)rows.push(replay(n,'default',defaults[n-201]));
for(const [number,checkpoints] of Object.entries(signals))rows.push(replay(Number(number),'signal',checkpoints));
const summarize=items=>{
  const sorted=items.map(x=>x.finishLight).sort((a,b)=>a-b);
  return {routes:items.length,min:sorted[0],median:sorted[Math.floor(sorted.length/2)],max:sorted.at(-1),
    tight02:items.filter(x=>x.finishLight<=2).length,highQuarter:items.filter(x=>x.lightFraction>=.25).length,
    veryHighHalf:items.filter(x=>x.lightFraction>=.5).length,
    above24Light:items.filter(x=>x.finishLight>24).length,
    exactRated:items.filter(x=>x.ratedMinimum!==null).length};
};
const byDistrict={};
for(let start=1001;start<=1901;start+=100)byDistrict[`${start}-${start+99}`]=summarize(rows.filter(x=>x.branch==='default'&&x.level>=start&&x.level<start+100));
const paired=[];
for(const signal of rows.filter(x=>x.branch==='signal')){
  const base=rows.find(x=>x.level===signal.level&&x.branch==='default');
  paired.push({level:signal.level,defaultSteps:base.steps,signalSteps:signal.steps,
    stepGap:Math.abs(base.steps-signal.steps),defaultFinishLight:base.finishLight,
    signalFinishLight:signal.finishLight,lightGap:Math.abs(base.finishLight-signal.finishLight)});
}
const report={scope:'Fully replayed canonical late default and signal routes. Finish light measures only these routes, not player route difficulty or global minimum except where a certificate exists.',
  default:summarize(rows.filter(x=>x.branch==='default')),signal:summarize(rows.filter(x=>x.branch==='signal')),
  byDistrict,phasePairs:paired,rows};
fs.writeFileSync(process.env.LLC_LANTERN_AUDIT_OUTPUT?path.resolve(process.env.LLC_LANTERN_AUDIT_OUTPUT):path.join(root,'lantern-balance-audit.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({default:report.default,signal:report.signal,byDistrict}));
