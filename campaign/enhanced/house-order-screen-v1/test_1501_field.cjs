// Check the field itself activates on delivery and that the reference remains playable.
const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const n=1501,proof=JSON.parse(fs.readFileSync(path.join(__dirname,'../road-events-v1/post_event_routes.json'))).find(x=>x.level===n);
api.choose(n);api.begin();
const field=api.getLevel().shadowInfluence2x2;
if(!field||field.origin.join(',')!=='11,2'||field.triggerCount!==1)throw Error('Missing intended level-1501 field');
if(field.cells.some(p=>api.shadowBlocked(p)))throw Error('Field blocked before delivery');
let active=false;
for(let i=1;i<proof.route.length;i++){
  if(!api.move(proof.route[i].p))throw Error(`Reference move ${i} blocked`);
  if(api.getState().mask&&!active){
    active=true;
    if(!field.cells.every(p=>api.shadowBlocked(p)))throw Error('Field failed to block four cells after delivery');
  }
}
const s=api.getState();
if(!active||!s.done||s.failed)throw Error('Level-1501 reference failed');
console.log('PASS: level 1501 field appears after first delivery, blocks all four tiles, and the recorded route finishes');
