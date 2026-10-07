// Screen saved geometric tours under the player-selected phase road.
const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const dir=__dirname;
const baseline=JSON.parse(fs.readFileSync(path.join(__dirname,'../candidates-v3/ROUTES_1001_2000_BASELINE.json')));
const signalSteps=new Map(baseline.filter(x=>api.LEVELS[x.level-1].phaseChoice)
  .map(x=>[x.level,x.solutions[0].route.length-1]));
const sources=[];
for(const band of [1801,1901]){
  for(const variant of ['reverse','rotate','swap_first','swap_middle','swap_last'])sources.push(`final-${band}-${variant}.json`);
  const prefix=band===1901?'candidate-events-1901-v2':`candidate-events-${band}`;
  for(const direction of ['ENWS','WSEN','NESW','SWNE'])sources.push(`${prefix}-${direction}.json`);
}
for(let seed=Number(process.env.LLC_MIN_SCREEN_SEED||1);seed<=Number(process.env.LLC_MAX_SCREEN_SEED||64);seed++)sources.push(`random-1001-2000-seed${seed}.json`);
const shorter=[],completed=[];let attempted=0;
for(const source of sources){
  const file=path.join(dir,source);if(!fs.existsSync(file))throw Error(`Missing ${file}`);
  for(const candidate of JSON.parse(fs.readFileSync(file)).rows){
    const n=candidate.level,reference=signalSteps.get(n),route=candidate.staticCandidateRoute;
    if(reference===undefined||!route||route.length-1>=reference)continue;
    attempted++;api.choose(n);api.begin();const level=api.getLevel();
    if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
    if(!api.signal())throw Error(`Signal unavailable ${n}`);
    let blocked=false;
    for(let i=1;i<route.length;i++)if(!api.move(route[i])){blocked=true;break}
    const end=api.getState();
    if(!blocked&&end.done&&!end.failed){
      const result={source,level:n,steps:route.length-1,signalReferenceSteps:reference,
        finishLight:end.light,route};
      completed.push(result);if(result.steps<reference)shorter.push(result);
    }
  }
}
const report={sources:sources.length,phaseLevels:signalSteps.size,attempted,completed:completed.length,
  shorter:shorter.length,uniqueShorterLevels:[...new Set(shorter.map(x=>x.level))].sort((a,b)=>a-b),
  shorterRoutes:shorter,scope:'Finite geometric-tour screen under the chosen signal. A completed shorter route disproves the recorded signal minimum; zero does not prove optimality.'};
fs.writeFileSync(path.join(dir,'signal-tour-screen.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({sources:report.sources,phaseLevels:report.phaseLevels,attempted,
  completed:report.completed,shorter:report.shorter,uniqueShorterLevels:report.uniqueShorterLevels}));
