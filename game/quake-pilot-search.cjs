const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');

const root=path.resolve(__dirname,'..');
const source=fs.readFileSync(path.join(__dirname,'index.html'),'utf8');
const expose='window.__quakeSolve=(candidate,opts)=>ROUTE_SOLVER.solve({...level,quakeEvent:candidate},structuredClone(state),opts);window.__campaign={levels:LEVELS,choose,move,reset,';
const marker='window.__campaign={levels:LEVELS,choose,move,reset,';
const oldWall='if(eq(p,level.quakeEvent.close))return true;';
if(!source.includes(marker)||!source.includes(oldWall)&&!source.includes('level.quakeEvent.closeExtra?.some'))throw Error('Quake solver probe markers changed');
const probe=path.join(__dirname,'quake-pilot-probe.html');
const routes=JSON.parse(fs.readFileSync(path.join(root,'campaign/enhanced/reference-hints-v1/normalized_routes.json'),'utf8'));
const targetLevels=(process.env.LLC_QUAKE_SEARCH_LEVELS||'801,802,808').split(',').map(Number);

(async()=>{
  fs.writeFileSync(probe,source.replace(marker,expose).replace(oldWall,'if(eq(p,level.quakeEvent.close)||level.quakeEvent.closeExtra?.some(tile=>eq(p,tile)))return true;'));
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage();
    await page.goto('file://'+probe.replaceAll('\\','/'));
    await page.waitForFunction(()=>window.__quakeSolve&&window.__campaign?.levels?.length===2000);
    const plans=[];
    for(const n of targetLevels){
      const route=routes[n-201].map(step=>step.slice(0,2));
      const result=await page.evaluate(({n,route})=>{
        const key=p=>p.join(','),eq=(a,b)=>a[0]===b[0]&&a[1]===b[1],dirs=[[1,0],[-1,0],[0,1],[0,-1]];
        let seed=n*78323;const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296};
        __campaign.choose(n);let first=0;
        for(const tile of route.slice(1)){first++;if(!__campaign.move(tile))throw Error(`Level ${n} recorded route failed at ${first}`);if(__campaign.getState().mask)break}
        const level=__campaign.getCurrentLevel(),state=__campaign.getState(),base=level.quakeEvent,walls=new Set(level.walls),fixed=new Set([key(level.depot),...level.homes.map(h=>key(h.p)),key(state.pos),key(base.close),...base.open.map(key)]);
        const closePool=route.slice(first+5,-7).filter(p=>!walls.has(key(p))&&!fixed.has(key(p)));
        const nearWall=p=>dirs.map(([dx,dy])=>[p[0]+dx,p[1]+dy]).filter(q=>q[0]>=0&&q[1]>=0&&q[0]<level.grid&&q[1]<level.grid&&walls.has(key(q))&&!fixed.has(key(q)));
        const accepted=[],seen=new Set();
        const original=__quakeSolve(base,{eventAware:true,search:'astar',maxExplored:12000});
        for(let attempt=0;attempt<300&&accepted.length<5;attempt++){
          const a=closePool[Math.floor(random()*closePool.length)],b=closePool[Math.floor(random()*closePool.length)];
          if(!a||!b||eq(a,b)||Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1])<6)continue;
          const aa=nearWall(a),bb=nearWall(b);if(!aa.length||!bb.length)continue;
          const oa=aa[Math.floor(random()*aa.length)],ob=bb[Math.floor(random()*bb.length)];if(eq(oa,ob))continue;
          const candidate={trigger:'first_delivery',close:base.close,closeExtra:[a,b],open:[...base.open,oa,ob]};
          const signature=JSON.stringify(candidate.closeExtra)+'|'+JSON.stringify(candidate.open.slice(1));if(seen.has(signature))continue;seen.add(signature);
          const t=performance.now(),solved=__quakeSolve(candidate,{eventAware:true,search:'astar',maxExplored:12000});
          if(solved.status!=='solved'||solved.route.at(-1).light<4)continue;
          accepted.push({id:`${n}-${accepted.length+1}`,quakeEvent:candidate,proof:{firstHouseMove:first,firstHouse:state.pos,remainingLight:state.light,completionMoves:solved.steps,finishingLight:solved.route.at(-1).light,explored:solved.explored,solveMs:Math.round(performance.now()-t),originalMoves:original.steps}});
        }
        return {level:n,grid:level.grid,required:level.required,firstHouseMask:state.mask,variants:accepted};
      },{n,route});
      plans.push(result);
      console.log(`Level ${n}: ${result.variants.length} verified variants`);
    }
    const output=path.join(__dirname,'quake-pilot-layouts.json'),prior=process.env.LLC_QUAKE_SEARCH_LEVELS&&fs.existsSync(output)?JSON.parse(fs.readFileSync(output,'utf8')).plans.filter(plan=>!targetLevels.includes(plan.level)):[];
    const merged=[...prior,...plans].filter(plan=>plan.variants.length).sort((a,b)=>a.level-b.level);
    fs.writeFileSync(output,JSON.stringify({scope:'Tester build only; levels '+merged.map(plan=>plan.level).join(', '),method:'Three roads close and three open after the first delivery; runtime solver must verify the actual state before accepting a random variant.',plans:merged},null,2)+'\n');
  }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1}).finally(()=>{if(fs.existsSync(probe))fs.unlinkSync(probe)});
