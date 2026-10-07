// Try a single new wall on an exact straight segment, then solve the altered map.
const fs=require('fs');
const path=require('path');
const solve=require('../../route-solver.js').solve;
const root=path.resolve(__dirname,'../../..');
const n=Number(process.argv[2]||102);
const level=JSON.parse(fs.readFileSync(path.join(root,'CAMPAIGN_1000_LEVELS.json'),'utf8'))[n-1];
const proof=JSON.parse(fs.readFileSync(path.join(__dirname,'shortest_routes.json'),'utf8'))[n-101];
if(!level||proof.level!==n)throw Error(`Missing level ${n}`);
const firstWall=process.argv[3];
let baseRoute=proof.route;
if(firstWall){
  level.walls=[...level.walls,firstWall];
  const first=solve(level,null,{repaired:!!level.repairRequired});
  if(first.status!=='solved')throw Error(`First wall ${firstWall} has no completion route`);
  baseRoute=first.route;
}
const points=baseRoute.map(step=>step.p);
const runs=[];let start=0;
const dirs=points.slice(1).map((p,i)=>[p[0]-points[i][0],p[1]-points[i][1]]);
for(let i=1;i<=dirs.length;i++){
  if(i<dirs.length&&dirs[i][0]===dirs[start][0]&&dirs[i][1]===dirs[start][1])continue;
  if(i-start>12)runs.push({start,end:i,length:i-start});
  start=i;
}
const special=new Set([level.depot,...level.homes.map(h=>h.p),...level.patrol,...(level.patrol2||[]),
  ...['fade','ice','dark','switch','gate'].flatMap(k=>level[k]?[level[k]]:[]),
  ...(level.repair?[level.repair.tile]:[])].map(p=>p.join(',')));
function longest(route){
  const p=route.map(s=>s.p);let best=0,run=0,previous='';
  for(let i=1;i<p.length;i++){
    const d=`${p[i][0]-p[i-1][0]},${p[i][1]-p[i-1][1]}`;
    run=d===previous?run+1:1;best=Math.max(best,run);previous=d;
  }
  return best;
}
const candidates=[...new Set(runs.flatMap(r=>points.slice(r.start+2,r.end-1).map(p=>p.join(','))))]
  .filter(k=>!special.has(k)&&!level.walls.includes(k));
const results=[];
for(const tile of candidates){
  const map={...level,walls:[...level.walls,tile]};
  const t=Date.now();
  const result=solve(map,null,{repaired:!!map.repairRequired});
  results.push({tile,status:result.status,steps:result.steps,longestStraight:result.route?longest(result.route):null,
    elapsedMs:Date.now()-t,route:result.route||null});
  console.log(`${tile}: ${result.status} ${result.steps||''} moves, straight ${result.route?longest(result.route):'-'}`);
}
const out=path.join(__dirname,`closure_search_${n}${firstWall?'_after_'+firstWall.replace(',','_'):''}.json`);
fs.writeFileSync(out,JSON.stringify({level:n,originalSteps:proof.steps,candidates:results}));
console.log(`Saved ${results.length} candidates to ${out}`);
