// Try relaxed static tours through the actual preview rules; never call them minima.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const source=JSON.parse(fs.readFileSync(process.env.LLC_STATIC_AUDIT_PATH?path.resolve(process.env.LLC_STATIC_AUDIT_PATH):path.join(__dirname,'static-shortcut-audit-901-1000.json'),'utf8'));
const overrides=process.env.LLC_WALL_OVERRIDES_PATH?JSON.parse(fs.readFileSync(path.resolve(process.env.LLC_WALL_OVERRIDES_PATH),'utf8')):{};
const closures=process.env.LLC_QUAKE_CLOSE_OVERRIDES_PATH?JSON.parse(fs.readFileSync(path.resolve(process.env.LLC_QUAKE_CLOSE_OVERRIDES_PATH),'utf8')):{};
const shadowFields=process.env.LLC_SHADOW_FIELDS_PATH?JSON.parse(fs.readFileSync(path.resolve(process.env.LLC_SHADOW_FIELDS_PATH),'utf8')):{};
const rows=[];
for(const candidate of source.rows){
  const n=candidate.level,route=candidate.staticCandidateRoute;
  if(!route){rows.push({level:n,staticSteps:null,verifiedReferenceSteps:candidate.verifiedRouteSteps,
    completed:false,finishLight:null,failure:{step:0,reason:'no geometric tour'}});continue;}
  if(overrides[n])api.LEVELS[n-1].walls=[...api.LEVELS[n-1].walls,...overrides[n]];
  if(closures[n])api.LEVELS[n-1].quakeEvent.close=closures[n];
  if(shadowFields[n])api.LEVELS[n-1].shadowInfluence2x2=shadowFields[n];
  api.choose(n);api.begin();
  const level=api.getLevel();
  if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
  let failure=null;
  for(let i=1;i<route.length;i++){
    const before=api.getState();
    if(level.lightBridgeRequiresPower&&before.active&&!before.bridgeBuilt&&!api.useBridge()){
      failure={step:i,reason:'required bridge unavailable',deliveries:before.mask.toString(2).replace(/0/g,'').length};break;
    }
    if(!api.move(route[i])){
    const s=api.getState();failure={step:i,reason:s.reason||'move rejected',deliveries:s.mask.toString(2).replace(/0/g,'').length};break;
    }
  }
  const end=api.getState();
  rows.push({level:n,staticSteps:candidate.staticTourSteps,verifiedReferenceSteps:candidate.verifiedRouteSteps,
    completed:!failure&&end.done&&!end.failed,finishLight:!failure&&end.done?end.light:null,failure});
}
const completed=rows.filter(r=>r.completed);
const report={attempted:rows.length,completed:completed.length,
  scope:'Exactly one static shortest-tour tie-break per map replayed under full rules. Rejection does not prove there is no shorter legal route.',
  completedRoutes:completed,failed:rows.filter(r=>!r.completed)};
fs.writeFileSync(process.env.LLC_STATIC_DYNAMIC_OUTPUT_PATH?path.resolve(process.env.LLC_STATIC_DYNAMIC_OUTPUT_PATH):path.join(__dirname,'static-shortcut-dynamic-audit-901-1000.json'),JSON.stringify(report,null,2));
console.log(`Static tour replay: ${completed.length}/${rows.length} completed; first failures: `+JSON.stringify(report.failed.slice(0,5)));
