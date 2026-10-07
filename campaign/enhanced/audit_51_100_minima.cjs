// Exact BFS under the opening rule set, followed by a live-rule replay.
const fs=require('fs'),path=require('path');
const solver=require('../../campaign/route-solver.js');
const api=require('./test_integrated_preview.cjs');
const archive=JSON.parse(fs.readFileSync(path.join(__dirname,'../../design/map-solutions-1000.json'),'utf8')).levels;
const rows=[];
for(let n=51;n<=100;n++){
  const level=api.LEVELS[n-1];
  for(const extra of ['shadowInfluence2x2','hunterDen','sentinelCenter','shadowDoor','lightBridge','oneWayTile','collapseTile','hiddenRoad'])
    if(level[extra])throw Error(`Level ${n} has unsupported ${extra}`);
  const solved=solver.solve(level);
  if(solved.status!=='solved')throw Error(`Level ${n}: ${solved.status}`);
  api.choose(n);api.begin();
  let failure=null;
  for(let i=1;i<solved.route.length;i++)if(!api.move(solved.route[i].p)){
    failure={step:i,reason:api.getState().reason};break;
  }
  const state=api.getState();
  if(failure||!state.done||state.failed||state.turns!==solved.steps)
    throw Error(`Level ${n}: shortest route failed live replay ${JSON.stringify({failure,steps:state.turns,expected:solved.steps})}`);
  const archived=Math.min(...archive[n-1].solutions.filter(s=>!s.repairPurchased).map(s=>s.steps));
  rows.push({level:n,shortestSteps:solved.steps,archivedSteps:archived,finishLight:state.light,explored:solved.explored,match:solved.steps===archived});
  if(n%10===0)console.log(n,'checked');
}
const report={scope:'Opening mechanics only: BFS with phase, lights, timers, Echo and houses, each returned route replayed through live preview rules.',rows};
fs.writeFileSync(path.join(__dirname,'opening-v1/minima_51_100_audit.json'),JSON.stringify(report,null,2));
console.log('51-100 exact minima',rows.length,'archive matches',rows.filter(r=>r.match).length,'mismatches',rows.filter(r=>!r.match));
