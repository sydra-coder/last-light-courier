// Replay route-preserving Light Bridge relocations with a two-cell one-way spur.
const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const here=__dirname;
const archive=JSON.parse(fs.readFileSync(path.join(here,'../../../design/map-solutions-1000.json'),'utf8')).levels;
const geometry=JSON.parse(fs.readFileSync(path.join(here,'relocated_dogleg_screen.json'),'utf8')).rows;
const initial=JSON.parse(fs.readFileSync(path.join(here,'bridge_spur_search.json'),'utf8')).rows;
const key=p=>p.join(',');
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const near=p=>[[p[0]+1,p[1]],[p[0]-1,p[1]],[p[0],p[1]+1],[p[0],p[1]-1]];
function bridgeFreeReach(level,goal){
  const blocked=new Set(level.walls);blocked.add(key(level.lightBridge));
  if(level.repair?.effect==='open')blocked.delete(key(level.repair.tile));
  const seen=new Set([key(level.depot)]),queue=[level.depot];
  for(let i=0;i<queue.length;i++)for(const p of near(queue[i])){
    if(p[0]<0||p[1]<0||p[0]>=level.grid||p[1]>=level.grid||blocked.has(key(p))||seen.has(key(p))||eq(p,level.oneWayTile)&&!eq(queue[i],level.oneWayFrom))continue;
    seen.add(key(p));queue.push(p);
  }
  return seen.has(key(goal));
}
function replay(n,route){
  api.choose(n);api.begin();const level=api.getLevel();
  if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
  for(let i=1;i<route.length;i++){
    const state=api.getState();
    if(state.active&&!state.bridgeBuilt&&!api.useBridge())return null;
    if(!api.move(route[i]))return null;
  }
  const end=api.getState();return end.done&&!end.failed?{steps:end.turns,light:end.light}:null;
}
const rows=[];
for(let n=701;n<=800;n++){
  const original=api.LEVELS[n-1],proof=archive[n-1].solutions[0].route,points=proof.map(s=>s.p);
  const originalEntry=points.findIndex(p=>eq(p,original.lightBridge));
  const options=[...geometry[n-701].options].sort((a,b)=>Math.abs(a.step-originalEntry)-Math.abs(b.step-originalEntry));
  let winner=initial[n-701].best||null,attempted=0;
  if(!winner){
    for(let capBoost=0;capBoost<=3&&!winner;capBoost++){
      for(const option of options.slice(0,12)){
        const firstLater=proof.findIndex((s,i)=>i>option.step&&s.mask!==proof[option.step].mask);
        if(firstLater<0)continue;
        const houseIndex=Math.log2(proof[firstLater].mask^proof[firstLater-1].mask);
        if(!Number.isInteger(houseIndex))continue;
        const level=structuredClone(original),u=option.houseSpur,w=option.oneWayExit;
        level.lightBridge=option.bridge;level.homes[houseIndex].p=u;
        level.walls=[...new Set([...level.walls,...option.seal.map(key)])].filter(t=>t!==key(u)&&t!==key(w));
        level.oneWayTile=w;level.oneWayFrom=u;level.cap+=capBoost;
        if(bridgeFreeReach(level,u))continue;
        const route=[...points.slice(0,option.step+1),u,w,...points.slice(option.step+1)];
        for(let phase=0;phase<4&&!winner;phase++)for(let phase2=0;phase2<4&&!winner;phase2++){
          level.phase=phase;level.phase2=phase2;api.LEVELS[n-1]=level;attempted++;
          const finish=replay(n,route);
          if(finish)winner={level:n,bridgeFrom:original.lightBridge,bridgeTo:option.bridge,
            houseIndex,houseFrom:original.homes[houseIndex].p,houseTo:u,oneWayTile:w,oneWayFrom:u,
            addedWalls:option.seal.map(key),openedCells:[u,w].filter(p=>original.walls.includes(key(p))).map(key),
            capBoost,phase,phase2,finishSteps:finish.steps,finishLight:finish.light,route};
        }
        if(winner)break;
      }
    }
  }
  api.LEVELS[n-1]=original;
  rows.push({level:n,found:!!winner,attempted,best:winner});
  if(n%10===0)console.log(n,rows.filter(r=>r.found).length,'found');
}
fs.writeFileSync(path.join(here,'relocated_spur_search.json'),JSON.stringify({scope:'Staged rule replay and directed no-bridge reachability; candidate only.','rows':rows},null,2));
console.log('Total powered, bridge-dependent candidates:',rows.filter(r=>r.found).length,'/100');
