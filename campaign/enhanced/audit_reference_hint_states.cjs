// Check whether canonical route records can safely identify current play state.
const fs=require('fs');
const path=require('path');
const test=require('./test_integrated_preview.cjs');
const {hintStateHash}=require('./reference-hints-v1/signature.js');
const root=path.resolve(__dirname,'../..');
const early=JSON.parse(fs.readFileSync(path.join(root,'design/map-solutions-1000.json'),'utf8')).levels;
const quake=JSON.parse(fs.readFileSync(path.join(__dirname,'quakes-v1/post_event_routes.json'),'utf8'));
const later=JSON.parse(fs.readFileSync(path.join(__dirname,'road-events-v1/post_event_routes.json'),'utf8'));
const overridePath=process.env.LLC_HINT_ROUTE_OVERRIDES||path.join(__dirname,'reference-hints-v1/route_overrides.json');
const routeOverrides=fs.existsSync(overridePath)?JSON.parse(fs.readFileSync(overridePath,'utf8')):{};
const spurPath=process.env.LLC_BRIDGE_SPUR_ROUTES_PATH||path.join(__dirname,'bridge-spurs-v1/routes.json');
const spurs=fs.existsSync(spurPath)?JSON.parse(fs.readFileSync(spurPath,'utf8')):{};
const summary={tested:0,fullMatch:0,mismatches:[],failed:[]};
const normalized=Array(1800).fill(null);
for(let n=201;n<=2000;n++){
  const proof=routeOverrides[n]?routeOverrides[n].map(p=>({p})):spurs[n]?spurs[n].map(p=>({p})):n<=800?early[n-1].solutions[0].route:n<=1000?quake[n-801].route:later[n-1001].route;
  test.choose(n);test.begin();
  const level=test.getLevel();
  if(level.repairRequired&&!test.buyFreeRepair())throw Error(`Level ${n}: missing free repair`);
  summary.tested++;
  let mismatch=null,failed=null;
  const checkpoints=[];
  for(let i=0;i<proof.length;i++){
    if(i){
      const before=test.getState();
      if(level.lightBridgeRequiresPower&&before.active&&!before.bridgeBuilt){
        if(!test.useBridge()){failed={level:n,step:i,reason:'bridge unavailable'};break;}
        checkpoints[i-1][4]=hintStateHash(test.getState());
      }
      if(!test.move(proof[i].p)){failed={level:n,step:i};break;}
    }
    const state=test.getState(),p=proof[i];
    checkpoints.push([state.pos[0],state.pos[1],state.mask,hintStateHash(state)]);
    if(!mismatch&&(state.pos[0]!==p.p[0]||state.pos[1]!==p.p[1]||(p.mask!==undefined&&(state.mask!==p.mask||state.light!==p.light))))
      mismatch={level:n,step:i,actual:[state.pos,state.mask,state.light],recorded:[p.p,p.mask,p.light]};
  }
  if(failed)summary.failed.push(failed);
  else if(mismatch)summary.mismatches.push(mismatch);
  else summary.fullMatch++;
  if(!failed)normalized[n-201]=checkpoints;
}
const stageDir=process.env.LLC_HINT_OUTPUT_DIR?path.resolve(process.env.LLC_HINT_OUTPUT_DIR):null;
if(stageDir)fs.mkdirSync(stageDir,{recursive:true});
fs.writeFileSync(stageDir?path.join(stageDir,'reference-hint-state-audit.json'):path.join(__dirname,'reference-hint-state-audit.json'),JSON.stringify(summary,null,2));
if(!summary.failed.length)fs.writeFileSync(stageDir?path.join(stageDir,'normalized_routes.json'):path.join(__dirname,'reference-hints-v1','normalized_routes.json'),JSON.stringify(normalized));
console.log(JSON.stringify({tested:summary.tested,fullMatch:summary.fullMatch,
  mismatches:summary.mismatches.length,failed:summary.failed.length,
  firstMismatch:summary.mismatches[0]||null}));
if(summary.failed.length)process.exitCode=1;
