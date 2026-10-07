// Exercise noncanonical legal moves after the first delivery on every map.
const fs=require('fs');
const path=require('path');
const test=require('./test_integrated_preview.cjs');
const root=path.resolve(__dirname,'../..');
const early=JSON.parse(fs.readFileSync(path.join(root,'design/map-solutions-1000.json'),'utf8')).levels;
const quake=JSON.parse(fs.readFileSync(path.join(__dirname,'quakes-v1/post_event_routes.json'),'utf8'));
const later=JSON.parse(fs.readFileSync(path.join(__dirname,'road-events-v1/post_event_routes.json'),'utf8'));
let variedMoves=0,levelsWithMoves=0,deadEnds=0,completed=0,failed=0;
for(let n=1;n<=2000;n++){
  const route=n<=800?early[n-1].solutions[0].route:n<=1000?quake[n-801].route:later[n-1001].route;
  test.choose(n);test.begin();
  const level=test.getLevel();
  if(level.repairRequired&&!test.buyFreeRepair())throw Error(`Level ${n}: free repair unavailable`);
  let trigger=-1;
  for(let i=1;i<route.length;i++){
    if(!test.move(route[i].p))throw Error(`Level ${n}: recorded setup blocked at ${i}`);
    if(test.getState().mask){trigger=i;break;}
  }
  if(trigger<0)throw Error(`Level ${n}: no first delivery`);
  let moves=0,seed=(n*2654435761)>>>0;
  for(let turn=0;turn<50;turn++){
    const before=test.getState();
    if(before.done||before.failed)break;
    if(level.lightBridgeRequiresPower&&!before.bridgeBuilt){
      if(!test.useBridge())throw Error(`Level ${n}: level bridge unavailable`);
    }
    const [x,y]=before.pos;
    const neighbors=[[x+1,y],[x,y+1],[x-1,y],[x,y-1]];
    seed=(Math.imul(seed,1664525)+1013904223)>>>0;
    const start=seed%4;
    let moved=false;
    for(let offset=0;offset<4;offset++){
      const p=neighbors[(start+offset)%4];
      if(test.move(p)){moved=true;break;}
    }
    if(!moved){deadEnds++;break;}
    const after=test.getState();
    if(after.turns!==before.turns+1||after.light<0||after.mask<before.mask)
      throw Error(`Level ${n}: invalid state after varied move ${turn+1}`);
    moves++;variedMoves++;
  }
  if(moves)levelsWithMoves++;
  if(test.getState().done)completed++;
  if(test.getState().failed)failed++;
}
const report={levels:2000,levelsWithMoves,variedMoves,deadEnds,completed,failed};
fs.writeFileSync(path.join(__dirname,'post-delivery-fuzz-report.json'),JSON.stringify(report,null,2));
console.log(`PASS: ${levelsWithMoves}/2000 levels accepted ${variedMoves} varied post-delivery moves; ${deadEnds} dead ends, ${completed} completions, ${failed} expected puzzle failures`);
