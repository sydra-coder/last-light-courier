const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const proof=JSON.parse(fs.readFileSync(path.join(__dirname,'early-winding-v1/shortest_routes.json'),'utf8'))[23];
if(proof.level!==124||proof.steps!==72)throw Error('Unexpected exact proof');
api.choose(124);api.begin();
for(let i=1;i<proof.route.length;i++)if(!api.move(proof.route[i].p))throw Error(`Exact route blocked at ${i}: ${api.getState().reason}`);
const end=api.getState();
if(!end.done||end.failed||end.turns!==72)throw Error('Exact route did not finish');
console.log('PASS: level 124 exact 72-step route still finishes after patrol revision');
