// Replay each exact base-rule shortest route in the generated preview.
const fs=require('fs');
const path=require('path');
const test=require('./test_integrated_preview.cjs');
const records=JSON.parse(fs.readFileSync(path.join(__dirname,'early-winding-v1','shortest_routes.json'),'utf8'));
if(records.length!==100)throw Error(`Expected 100 shortest routes, got ${records.length}`);
for(let i=0;i<records.length;i++){
  const proof=records[i];
  if(proof.level!==i+101||proof.steps!==proof.route.length-1)throw Error(`Bad record ${i}`);
  test.choose(proof.level);
  test.begin();
  if(proof.freeRepairRequired&&!test.buyFreeRepair())throw Error(`Level ${proof.level}: free repair unavailable`);
  for(let step=1;step<proof.route.length;step++){
    if(!test.move(proof.route[step].p))throw Error(`Level ${proof.level}: blocked at step ${step}`);
  }
  const state=test.getState();
  if(!state.done||state.failed||state.turns!==proof.steps||state.light!==proof.finishLight||state.powerUsed)
    throw Error(`Level ${proof.level}: completion mismatch`);
}
console.log('PASS: 100 exact no-tool shortest routes replay in the generated preview');
