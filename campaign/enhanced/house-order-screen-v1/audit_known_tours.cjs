// Replay every saved geometric tour against one preview build. Finite coverage only.
const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const dir=__dirname;
const sources=[];
for(let band=1001;band<=1901;band+=100){
  for(const variant of ['reverse','rotate','swap_first','swap_middle','swap_last'])
    sources.push(`final-${band}-${variant}.json`);
  const prefix=band===1901?'candidate-events-1901-v2':`candidate-events-${band}`;
  for(const direction of ['ENWS','WSEN','NESW','SWNE'])
    sources.push(`${prefix}-${direction}.json`);
}
for(let seed=Number(process.env.LLC_MIN_SCREEN_SEED||1);seed<=Number(process.env.LLC_MAX_SCREEN_SEED||64);seed++)sources.push(`random-1001-2000-seed${seed}.json`);
const rows=[],missing=[];
for(const source of sources){
  const file=path.join(dir,source);
  if(!fs.existsSync(file)){missing.push(source);continue;}
  for(const candidate of JSON.parse(fs.readFileSync(file)).rows){
    const route=candidate.staticCandidateRoute,n=candidate.level;
    if(!route)continue;
    api.choose(n);api.begin();const level=api.getLevel();
    if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
    let blocked=false;
    for(let i=1;i<route.length;i++){
      const state=api.getState();
      if(level.lightBridgeRequiresPower&&state.active&&!state.bridgeBuilt&&!api.useBridge()){blocked=true;break;}
      if(!api.move(route[i])){blocked=true;break;}
    }
    const end=api.getState();
    if(!blocked&&end.done&&!end.failed)rows.push({source,level:n,steps:route.length-1,referenceSteps:candidate.verifiedRouteSteps,finishLight:end.light});
  }
}
const shorter=rows.filter(r=>r.steps<r.referenceSteps);
const report={sources:sources.length,missing,completed:rows.length,shorter:shorter.length,
  uniqueShorterLevels:[...new Set(shorter.map(r=>r.level))].sort((a,b)=>a-b),shorterRoutes:shorter,
  scope:'Saved geometric tours replayed under full preview rules. Finite sample; not a proof of minimum routes or all reachable states.'};
const output=process.env.LLC_KNOWN_TOUR_OUTPUT?path.resolve(process.env.LLC_KNOWN_TOUR_OUTPUT):path.join(dir,'known-tour-replay.json');
fs.writeFileSync(output,JSON.stringify(report,null,2));
console.log(JSON.stringify({sources:report.sources,missing:missing.length,completed:report.completed,shorter:report.shorter,uniqueShorterLevels:report.uniqueShorterLevels}));
