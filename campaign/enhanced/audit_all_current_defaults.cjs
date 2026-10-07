// Replay one current default route on every selectable campaign level.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const root=path.resolve(__dirname,'../..');
const opening=JSON.parse(fs.readFileSync(path.join(__dirname,'opening-v1/shortest_routes.json')));
const archive=JSON.parse(fs.readFileSync(path.join(root,'design/map-solutions-1000.json'))).levels;
const early=JSON.parse(fs.readFileSync(path.join(__dirname,'early-winding-v1/shortest_routes.json')));
const normalized=JSON.parse(fs.readFileSync(process.env.LLC_HINTS_PATH||path.join(__dirname,'reference-hints-v1/normalized_routes.json')));
const bands={opening:{tested:0,passed:0},legacy:{tested:0,passed:0},early:{tested:0,passed:0},later:{tested:0,passed:0}};
const failures=[];
for(let n=1;n<=2000;n++){
  const band=n<=50?'opening':n<=100?'legacy':n<=200?'early':'later';
  bands[band].tested++;
  const record=n<=50?opening[n-1].route:n<=100?archive[n-1].solutions[0].route:
    n<=200?early[n-101].route:normalized[n-201];
  const route=record.map(step=>Array.isArray(step)?step.slice(0,2):step.p);
  api.choose(n);api.begin();
  const level=api.getLevel();
  let problem=null;
  if(level.repairRequired&&!api.buyFreeRepair())problem='free repair unavailable';
  for(let i=1;i<route.length&&!problem;i++){
    const state=api.getState();
    if(level.lightBridgeRequiresPower&&state.active&&!state.bridgeBuilt&&!api.useBridge()){
      problem=`bridge unavailable at ${i}`;break;
    }
    if(!api.move(route[i]))problem=`move ${i} blocked: ${api.getState().reason||'rejected'}`;
  }
  const end=api.getState();
  // The game accepts a successful delivery with exactly zero light left.
  if(!problem&&(!end.done||end.failed||end.light<0))problem=`incomplete: ${JSON.stringify({done:end.done,failed:end.failed,light:end.light})}`;
  if(problem)failures.push({level:n,band,problem,routeSteps:route.length-1,playedSteps:end.turns});
  else bands[band].passed++;
}
const report={scope:'One recorded default route per current selectable level; full generated-preview rules, required free repair and bridge use. Not a proof of other reachable states, powered minima or player quality.',
  tested:2000,passed:2000-failures.length,bands,failures};
fs.writeFileSync(path.join(__dirname,'all-current-defaults-audit.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({tested:report.tested,passed:report.passed,bands,failures:failures.slice(0,20)}));
if(failures.length)process.exitCode=1;
