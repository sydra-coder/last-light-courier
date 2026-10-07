// Explore short safe street detours at a blocked move in the 801 event-aware tour.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const n=Number(process.env.LLC_REPAIR_LEVEL||801);
const input=process.env.LLC_REPAIR_INPUT||path.join(__dirname,'event-aware-801-sample.json');
const source=JSON.parse(fs.readFileSync(input)).rows.find(x=>x.level===n);
if(!source?.staticCandidateRoute)throw Error('candidate route missing');
let route=source.staticCandidateRoute.map(p=>[...p]);
const same=(a,b)=>a&&b&&a[0]===b[0]&&a[1]===b[1];
function replay(points){
  api.choose(n);api.begin();const level=api.getLevel();
  if(level.repairRequired&&!api.buyFreeRepair())return {failedAt:0,reason:'repair unavailable'};
  for(let i=1;i<points.length;i++)if(!api.move(points[i]))return {failedAt:i,state:api.getState(),open:api.isOpen(points[i]),shadow:api.shadowBlocked(points[i])};
  const end=api.getState();return {done:end.done&&!end.failed,steps:end.turns,light:end.light,failedAt:end.done?null:points.length};
}
function detours(current,target,prev,maxLength=7){
  const size=api.getLevel().grid,found=[];
  const queue=[{p:current,path:[],seen:new Set([current.join(',')])}];
  for(let head=0;head<queue.length;head++){
    const item=queue[head];if(item.path.length>=maxLength)continue;
    const [x,y]=item.p;
    for(const p of [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]){
      if(p[0]<0||p[1]<0||p[0]>=size||p[1]>=size||item.seen.has(p.join(','))||!api.isOpen(p))continue;
      if(item.path.length===0&&same(p,prev))continue;
      const path=[...item.path,p];
      if(same(p,target)){found.push(path);continue;}
      if(path.length<maxLength&&queue.length<5000)queue.push({p,path,seen:new Set([...item.seen,p.join(',')])});
    }
  }
  return found.sort((a,b)=>a.length-b.length);
}
const changes=[],log=[];
for(let iteration=0;iteration<20;iteration++){
  const first=replay(route);
  if(first.done){
    const output={level:n,completed:true,steps:first.steps,light:first.light,route,changes,log};
    fs.writeFileSync(path.join(__dirname,`event-aware-${n}-repaired.json`),JSON.stringify(output,null,2));
    console.log(JSON.stringify({level:n,completed:true,steps:first.steps,light:first.light,detours:changes.length}));process.exit(0);
  }
  const i=first.failedAt;
  if(!i||i>=route.length){log.push({iteration,stopped:first});break;}
  const current=route[i-1],prev=i>=2?route[i-2]:null,target=route[i];
  const paths=detours(current,target,prev);let accepted=null,examined=0;
  for(const path of paths){
    examined++;
    const candidate=[...route.slice(0,i),...path,...route.slice(i+1)];
    const result=replay(candidate);
    if(result.done||result.failedAt>i+path.length){accepted={route:candidate,path,result};break;}
  }
  log.push({iteration,blockedStep:i,current,target,shadow:first.shadow,open:first.open,candidates:paths.length,examined,accepted:!!accepted});
  if(!accepted)break;
  changes.push({step:i,replacement:accepted.path});route=accepted.route;
}
const finish=replay(route),output={level:n,completed:!!finish.done,steps:finish.steps||null,light:finish.light||null,route,changes,log,finish};
fs.writeFileSync(path.join(__dirname,`event-aware-${n}-repaired.json`),JSON.stringify(output,null,2));
console.log(JSON.stringify({level:n,completed:output.completed,detours:changes.length,finish,log:log.slice(-3)}));
