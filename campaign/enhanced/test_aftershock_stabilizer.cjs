// Check the Map Stabilizer interaction against the generated preview rules.
const fs=require('fs');
const path=require('path');
const api=require('./test_integrated_preview.cjs');
const proof=JSON.parse(fs.readFileSync(path.join(__dirname,'quakes-v1/post_event_routes.json'),'utf8')).find(item=>item.level===951);
if(!proof)throw Error('Level 951 route proof missing');
for(const stabilized of [false,true]){
  api.choose(951);
  api.begin();
  if(stabilized&&!api.usePower('map_stabilizer'))throw Error('Map Stabilizer unavailable');
  for(let i=1;i<proof.route.length;i++)if(!api.move(proof.route[i].p))throw Error(`Route blocked at step ${i}`);
  const state=api.getState(),tile=api.getLevel().aftershock.tile;
  if(!state.done||state.failed||api.isOpen(tile)!==stabilized)throw Error(`Aftershock state mismatch: stabilized=${stabilized}`);
}
console.log('PASS: Level 951 completes with both branches; Map Stabilizer keeps the aftershock tile open');
