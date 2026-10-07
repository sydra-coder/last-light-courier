// Normalize signal-branch routes against current live state for safe paid hints.
const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const {hintStateHash}=require('./signature.js');
const root=path.resolve(__dirname,'..');
const baseline=JSON.parse(fs.readFileSync(path.join(root,'candidates-v3/ROUTES_1001_2000_BASELINE.json'),'utf8'));
const exact=JSON.parse(fs.readFileSync(path.join(root,'phase-choices-v1/exact_signal_minima.json'),'utf8')).certified;
const overrides={};
const crossBranchFast=[1807,1828,1980,1994];
const defaultHints=JSON.parse(fs.readFileSync(process.env.LLC_HINTS_PATH||path.join(root,'reference-hints-v1/normalized_routes.json'),'utf8'));
for(const n of crossBranchFast)overrides[n]=defaultHints[n-201].map(s=>s.slice(0,2));
overrides[1873]=JSON.parse(fs.readFileSync(path.join(root,'phase-choices-v1/signal_1873_detour.json'),'utf8')).route;
for(const proof of exact){
  const start=(Math.floor((proof.level-1)/100)*100)+1;
  const report=JSON.parse(fs.readFileSync(path.join(root,`event-aware-${start}-${start+99}-signal-replay.json`),'utf8'));
  overrides[proof.level]=report.completedRoutes.find(x=>x.level===proof.level).route;
}
if(process.env.LLC_SIGNAL_EXTRA_OVERRIDES){
  const extra=JSON.parse(fs.readFileSync(path.resolve(process.env.LLC_SIGNAL_EXTRA_OVERRIDES),'utf8'));
  for(const [number,route] of Object.entries(extra))overrides[number]=route;
}
const checkpointsByLevel={},failed=[];
let tested=0;
for(const record of baseline){
  const n=record.level;
  if(n<1801||!api.LEVELS[n-1].phaseChoice)continue;
  const route=overrides[n]||record.solutions[0].route.map(s=>s.p);
  api.choose(n);api.begin();
  const level=api.getLevel();
  if(level.repairRequired&&!api.buyFreeRepair())throw Error(`Signal repair unavailable ${n}`);
  if(!api.signal())throw Error(`Signal action unavailable ${n}`);
  const checkpoints=[];
  for(let i=0;i<route.length;i++){
    if(i&&!api.move(route[i])){failed.push({level:n,step:i});break}
    const state=api.getState();
    checkpoints.push([state.pos[0],state.pos[1],state.mask,hintStateHash(state)]);
  }
  if(!failed.some(x=>x.level===n)){
    const end=api.getState();
    if(!end.done||end.failed)failed.push({level:n,reason:'route did not finish'});
    else checkpointsByLevel[n]=checkpoints;
  }
  tested++;
}
const output=process.env.LLC_SIGNAL_HINT_OUTPUT_DIR?path.resolve(process.env.LLC_SIGNAL_HINT_OUTPUT_DIR):__dirname;
fs.mkdirSync(output,{recursive:true});
fs.writeFileSync(path.join(output,'signal-hint-audit.json'),JSON.stringify({tested,failed},null,2));
if(!failed.length){
  fs.writeFileSync(path.join(output,'normalized_signal_routes.json'),JSON.stringify(checkpointsByLevel));
  fs.writeFileSync(path.join(output,'signal_route_overrides.json'),JSON.stringify(overrides));
}
console.log(JSON.stringify({tested,normalized:Object.keys(checkpointsByLevel).length,failed:failed.length,examples:failed.slice(0,3)}));
if(failed.length)process.exitCode=1;
