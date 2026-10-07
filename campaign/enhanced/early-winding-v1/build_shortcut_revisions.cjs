// Stage wall and exact-route revisions for long early shortest-path straights.
const fs=require('fs');
const path=require('path');
const solve=require('../../route-solver.js').solve;
const root=path.resolve(__dirname,'../../..');
const levels=JSON.parse(fs.readFileSync(path.join(root,'CAMPAIGN_1000_LEVELS.json'),'utf8'));
const exact=JSON.parse(fs.readFileSync(path.join(__dirname,'shortest_routes.json'),'utf8'));
const output=path.join(__dirname,'shortcut_revisions_candidate.json');
const limit=Number(process.argv[2]||100);
let results=fs.existsSync(output)?JSON.parse(fs.readFileSync(output,'utf8')):[];
function runs(route){
  const p=route.map(s=>s.p),dirs=p.slice(1).map((q,i)=>[q[0]-p[i][0],q[1]-p[i][1]]),out=[];
  let start=0;
  for(let i=1;i<=dirs.length;i++){
    if(i<dirs.length&&dirs[i][0]===dirs[start][0]&&dirs[i][1]===dirs[start][1])continue;
    out.push({start,end:i,length:i-start,points:p.slice(start+1,i)});
    start=i;
  }
  return out;
}
function score(route){
  const lengths=runs(route).map(r=>r.length);
  return {excess:lengths.reduce((sum,x)=>sum+Math.max(0,x-12),0),longest:Math.max(...lengths),steps:route.length-1};
}
function better(a,b){return a.excess<b.excess||a.excess===b.excess&&(a.longest<b.longest||a.longest===b.longest&&a.steps<b.steps)}
for(let n=101;n<=200&&results.length<limit;n++){
  if(results.some(r=>r.level===n))continue;
  const original=exact[n-101],initial=score(original.route);
  if(initial.excess===0){results.push({level:n,changed:false,score:initial});continue;}
  const game=structuredClone(levels[n-1]);
  const special=new Set([game.depot,...game.homes.map(h=>h.p),...game.patrol,...(game.patrol2||[]),
    ...['fade','ice','dark','switch','gate'].flatMap(k=>game[k]?[game[k]]:[]),
    ...(game.repair?[game.repair.tile]:[])].map(p=>p.join(',')));
  let route=original.route,current=initial;const added=[];
  for(let round=0;round<5&&current.excess>0;round++){
    const walls=new Set(game.walls);
    const candidates=[...new Set(runs(route).filter(r=>r.length>12)
      .flatMap(r=>r.points.slice(1,-1).map(p=>p.join(','))))]
      .filter(tile=>!special.has(tile)&&!walls.has(tile));
    let best=null;
    for(const tile of candidates){
      const trial={...game,walls:[...game.walls,tile]};
      const result=solve(trial,null,{repaired:!!trial.repairRequired});
      if(result.status!=='solved')continue;
      const candidateScore=score(result.route);
      if(better(candidateScore,current)&&(!best||better(candidateScore,best.score)))
        best={tile,route:result.route,score:candidateScore,explored:result.explored};
    }
    if(!best)break;
    game.walls.push(best.tile);
    added.push(best.tile);
    route=best.route;current=best.score;
  }
  const item={level:n,changed:added.length>0,success:current.excess===0,addedWalls:added,
    before:initial,after:current,route:added.length?route:null};
  results.push(item);
  fs.writeFileSync(output,JSON.stringify(results));
  console.log(`${n}: ${initial.longest}->${current.longest} straight; ${added.length} wall(s); ${item.success?'ready':'needs work'}`);
}
fs.writeFileSync(output,JSON.stringify(results));
console.log(`Staged ${results.length} levels, ${results.filter(r=>r.changed).length} changed, ${results.filter(r=>r.changed&&!r.success).length} incomplete`);
