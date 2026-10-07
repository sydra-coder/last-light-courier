// Replace an Echo-forbidden immediate reversal with a real street loop.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const source=JSON.parse(fs.readFileSync(path.join(__dirname,'early-order-301-310-static.json'))).rows.find(x=>x.level===301);
const initial=source.staticCandidateRoute,blocked=17;
const walls=new Set(api.LEVELS[300].walls),size=api.LEVELS[300].grid;
const start=initial[blocked-1],options=[];
function enumerate(p,target,trail,seen){
  if(trail.length>10)return;
  if(p[0]===target[0]&&p[1]===target[1]){options.push({target,trail});return}
  for(const q of [[p[0]-1,p[1]],[p[0]+1,p[1]],[p[0],p[1]-1],[p[0],p[1]+1]]){
    const key=q.join(',');if(q[0]<0||q[1]<0||q[0]>=size||q[1]>=size||walls.has(key)||seen.has(key))continue;
    if(Math.abs(q[0]-start[0])+Math.abs(q[1]-start[1])>6)continue;
    enumerate(q,target,[...trail,q],new Set([...seen,key]));
  }
}
for(let j=blocked+1;j<=blocked+4;j++)enumerate(start,initial[j],[],new Set([start.join(',')]));
const unique=new Map();for(const option of options){
  const j=initial.findIndex((p,index)=>index>=blocked+1&&p[0]===option.target[0]&&p[1]===option.target[1]);
  const route=[...initial.slice(0,blocked),...option.trail,...initial.slice(j+1)];
  unique.set(JSON.stringify(route),{route,rejoin:j});
}
const candidates=[...unique.values()].sort((a,b)=>a.route.length-b.route.length).slice(0,500);
const results=[];let found=null;
for(const candidate of candidates){
  api.choose(301);api.begin();let fail=null;
  for(let i=1;i<candidate.route.length;i++)if(!api.move(candidate.route[i])){fail=i;break}
  const end=api.getState();
  results.push({rejoin:candidate.rejoin,steps:candidate.route.length-1,blocked:fail,finishLight:end.light,
    route:candidate.route});
  if(fail===null&&end.done&&!end.failed){found=results.at(-1);break}
}
results.sort((a,b)=>(b.blocked||999)-(a.blocked||999)||a.steps-b.steps);
fs.writeFileSync(path.join(__dirname,'early-order-301-splice-search.json'),JSON.stringify({generated:options.length,tested:results.length,found,best:results.slice(0,20)},null,2));
console.log(JSON.stringify({generated:options.length,tested:results.length,found:found&&{steps:found.steps,finishLight:found.finishLight},
  best:results.slice(0,5).map(x=>({rejoin:x.rejoin,steps:x.steps,blocked:x.blocked}))}));
