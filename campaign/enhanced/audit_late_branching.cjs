// Measure actual local route choices before and just after the first delivery.
// A branch is only a potential route; this does not prove its continuation wins.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const proofs=JSON.parse(fs.readFileSync(path.join(__dirname,'road-events-v1/post_event_routes.json')));
const key=p=>p.join(',');
function options(){
  const s=api.getState(),[x,y]=s.pos;
  const candidates=[[x+1,y],[x-1,y],[x,y+1],[x,y-1]];
  const transit=api.getLevel().transitLink;
  if(transit&&s.active){const [a,b]=transit.stops;if(key(s.pos)===key(a))candidates.push(b);else if(key(s.pos)===key(b))candidates.push(a)}
  return candidates.filter(api.legal);
}
const rows=[];
for(const proof of proofs){
  const n=proof.level,route=proof.route;
  api.choose(n);api.begin();
  const level=api.getLevel();
  if(level.repairRequired&&level.repair?.cost===0&&!api.buyFreeRepair())throw Error(`Free repair failed ${n}`);
  const initial=options(),seen=new Set([key(route[0].p)]);
  let first=null,preEventBranchTurns=0,postEventBranchTurns=0;
  for(let i=1;i<route.length;i++){
    const before=api.getState(),available=options();
    const previous=i>1?key(route[i-2].p):null;
    const forward=available.filter(p=>key(p)!==previous);
    if(forward.length>=2){if(before.mask)postEventBranchTurns++;else preEventBranchTurns++}
    if(!api.move(route[i].p))throw Error(`Recorded route failed ${n} at ${i}`);
    seen.add(key(route[i].p));
    const after=api.getState();
    if(!first&&after.mask){
      const post=options(),next=route[i+1]?.p,prior=route[i-1].p;
      first={step:i,legal:post.length,forward:post.filter(p=>key(p)!==key(prior)).length,
        alternate:post.filter(p=>key(p)!==key(prior)&&key(p)!==key(next)).length,
        newCells:post.filter(p=>!seen.has(key(p))).length,eventTriggered:after.eventTriggered};
    }
  }
  const end=api.getState();
  if(!end.done||end.failed||!first)throw Error(`Reference failed ${n}`);
  rows.push({level:n,grid:level.grid,houses:level.homes.length,steps:end.turns,initial:initial.length,
    firstDelivery:first,preEventBranchTurns,postEventBranchTurns});
}
const bands=[];
for(let a=1001;a<=1901;a+=100){const subset=rows.filter(r=>a<=r.level&&r.level<a+100);bands.push({from:a,to:a+99,
  initialOne:subset.filter(r=>r.initial<=1).length,postFirstForced:subset.filter(r=>r.firstDelivery.forward<=1).length,
  postFirstAlternate:subset.filter(r=>r.firstDelivery.alternate>0).length,
  preEventNoBranches:subset.filter(r=>r.preEventBranchTurns===0).length,
  postEventNoBranches:subset.filter(r=>r.postEventBranchTurns===0).length});}
const report={scope:'Legal local choices along one recorded route. Does not prove alternate completion, optimality, or player preference.',
  levels:rows.length,bands,rows};
fs.writeFileSync(process.env.LLC_BRANCHING_OUTPUT?path.resolve(process.env.LLC_BRANCHING_OUTPUT):path.join(__dirname,'late-branching-audit.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({levels:rows.length,bands}));
