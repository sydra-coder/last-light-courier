// Replay Road Repair after three distinct kinds of road damage.
const fs=require('fs');
const path=require('path');
const api=require('./test_integrated_preview.cjs');
const root=path.resolve(__dirname,'../..');
const archived=JSON.parse(fs.readFileSync(path.join(root,'design/map-solutions-1000.json'),'utf8')).levels;
const quakes=JSON.parse(fs.readFileSync(path.join(__dirname,'quakes-v1/post_event_routes.json'),'utf8'));
const cases=[
  ...Array.from({length:50},(_,i)=>({level:402+2*i,kind:'causeway'})),
  ...Array.from({length:50},(_,i)=>({level:901+i,kind:'quake'})),
  ...Array.from({length:50},(_,i)=>({level:951+i,kind:'aftershock'}))
];
api.grantPower('road_repair',cases.length);
for(const {level:n,kind} of cases){
  const route=kind==='causeway'?archived[n-1].solutions[0].route:quakes[n-801].route;
  api.choose(n);api.begin();
  const level=api.getLevel();
  if(level.repairRequired&&!api.buyFreeRepair())throw Error(`Level ${n}: required free repair unavailable`);
  let used=false;
  for(let i=1;i<route.length;i++){
    if(!api.move(route[i].p))throw Error(`Level ${n}: blocked at step ${i}`);
    const state=api.getState();
    const damaged=kind==='causeway'?state.collapseClosed:kind==='quake'?state.quakeTriggered:
      state.aftershockStart!==null&&state.turns-state.aftershockStart>=level.aftershock.closeAfter;
    if(!damaged||used)continue;
    if(!api.usePower('road_repair'))throw Error(`Level ${n}: Road Repair unavailable`);
    used=true;
    const tile=kind==='causeway'?level.collapseTile:kind==='quake'?level.quakeEvent.close:level.aftershock.tile;
    if(!api.isOpen(tile))throw Error(`Level ${n}: repaired tile remains closed`);
  }
  const finish=api.getState();
  if(!used||!finish.done||finish.failed)throw Error(`Level ${n}: repaired route did not finish`);
}
console.log('PASS: 150 Road Repair routes; 50 collapsed causeways, 50 quake roads, 50 aftershock roads');
