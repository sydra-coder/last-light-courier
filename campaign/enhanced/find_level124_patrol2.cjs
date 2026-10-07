// Temporary search for a patrol loop that makes the assigned trap useful.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const n=124,level=api.LEVELS[n-1];
const route=JSON.parse(fs.readFileSync(path.join(__dirname,'../../design/map-solutions-1000.json'),'utf8')).levels[n-1].solutions[0].route;
const used=new Set(route.map(s=>s.p.join(','))),walls=new Set(level.walls),g=level.grid;
const original=level.patrol2,found=[];
function run(loop,trapAt=null,tile=null){
  level.patrol2=loop;api.choose(n);api.begin();
  let captured=false,held=false;
  for(let i=1;i<route.length;i++){
    if(!api.move(route[i].p))return false;
    if(i===trapAt){
      if(!api.usePower('anchor_trap')||!api.canTrapAt(tile))return false;
      api.placeTrap(tile);
    }
    const s=api.getState();
    if(s.trappedPatrol)captured=true;
    if(i>trapAt&&captured&&s.trappedPatrol===2&&i>trapAt+1)held=true;
  }
  const s=api.getState();return s.done&&!s.failed&&(trapAt===null||captured&&held);
}
const loops=[];
for(let y=0;y<g-1;y++)for(let x=0;x<g-1;x++){
  const loop=[[x,y],[x+1,y],[x+1,y+1],[x,y+1]];
  if(loop.some(p=>walls.has(p.join(','))||used.has(p.join(','))))continue;
  loops.push(loop);
}
for(let at=1;at<route.length-5&&!found.length;at++){
  if(!route[at].mask)continue;
  for(const loop of loops){
    const tiles=loop.filter(tile=>Math.abs(tile[0]-route[at].p[0])+Math.abs(tile[1]-route[at].p[1])<=2);
    if(!tiles.length||!run(loop))continue;
    for(const tile of tiles)if(run(loop,at,tile)){
      found.push({loop,useAfterStep:at,tile});break;
    }
    if(found.length)break;
  }
}
level.patrol2=original;
console.log(JSON.stringify(found));
if(!found.length)process.exitCode=1;
