// Exercise Map Stabilizer on earned-tool earthquake maps in the preview.
const fs=require('fs');
const path=require('path');
const api=require('./test_integrated_preview.cjs');
const proofs=JSON.parse(fs.readFileSync(path.join(__dirname,'quakes-v1/post_event_routes.json'),'utf8')).filter(item=>item.level>=901&&item.level<=950);
if(proofs.length!==50)throw Error('Expected 50 earthquake proofs');
api.grantPower('map_stabilizer',proofs.length);
for(const proof of proofs){
  api.choose(proof.level);api.begin();
  const level=api.getLevel();
  if(!api.usePower('map_stabilizer'))throw Error(`Level ${proof.level}: tool unavailable`);
  if(level.repairRequired&&!api.buyFreeRepair())throw Error(`Level ${proof.level}: free repair unavailable`);
  for(let i=1;i<proof.route.length;i++)if(!api.move(proof.route[i].p))throw Error(`Level ${proof.level}: blocked at step ${i}`);
  const state=api.getState();
  if(!state.done||state.failed||!api.isOpen(level.quakeEvent.close)||level.quakeEvent.open.some(tile=>!api.isOpen(tile)))throw Error(`Level ${proof.level}: earthquake branch failed`);
}
console.log('PASS: 50 earthquake maps complete with closure stabilized and new roads open');
