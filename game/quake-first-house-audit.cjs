const path=require('node:path');
const {chromium}=require('playwright');

(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  const results=[];
  try{
    const page=await browser.newPage();
    await page.goto('file://'+path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.waitForFunction(()=>window.__campaign&&window.LLCQuakePilot);
    const only=process.env.LLC_QUAKE_AUDIT_HOUSE||'';
    const levels=(process.env.LLC_QUAKE_AUDIT_LEVELS||'801,802,808').split(',').map(Number);
    for(const n of levels.filter(n=>!only||only.startsWith(n+':'))){
      const candidates=await page.evaluate(n=>{
        const l=__campaign.levels[n-1],key=p=>p.join(','),walls=new Set(l.walls),dirs=[[1,0],[-1,0],[0,1],[0,-1]],out=[];
        for(let h=0;h<l.homes.length;h++){
          const target=l.homes[h].p,queue=[l.depot],previous=new Map([[key(l.depot),null]]);
          for(let head=0;head<queue.length&&!previous.has(key(target));head++)for(const [dx,dy] of dirs){const p=[queue[head][0]+dx,queue[head][1]+dy],k=key(p);if(p[0]<0||p[1]<0||p[0]>=l.grid||p[1]>=l.grid||walls.has(k)||previous.has(k)||l.homes.some((house,i)=>i!==h&&key(house.p)===k))continue;previous.set(k,queue[head]);queue.push(p)}
          if(!previous.has(key(target)))continue;
          const route=[];let p=target;while(p){route.push(p);p=previous.get(key(p))}route.reverse();out.push({house:h+1,route});
        }
        return out;
      },n);
      for(const choice of candidates.filter(choice=>!only||only===`${n}:${choice.house}`)){
        const result=await page.evaluate(({n,choice})=>{
          __campaign.choose(n);__integratedShell.enterBoard();
          for(const tile of choice.route.slice(1))if(!__campaign.move(tile))return {level:n,house:choice.house,status:'first_route_rejected',tile};
          const s=__campaign.getState(),pilot=s.quakePilot,verified=LLCQuakePilot.lastVerifiedRoute();
          if(!pilot||!verified)return {level:n,house:choice.house,status:'no_verified_route',variant:pilot?.variant,checked:pilot?.checked,light:s.light,pos:s.pos,mask:s.mask};
          for(const tile of verified.slice(1))if(!__campaign.move(tile))return {level:n,house:choice.house,status:'completion_rejected',variant:pilot.variant,tile};
          const end=__campaign.getState();return {level:n,house:choice.house,status:end.done?'complete':'incomplete',variant:pilot.variant,needed:pilot.neededLight,available:pilot.availableLight,topUp:pilot.topUp,checkMs:pilot.checked.reduce((sum,row)=>sum+row.ms,0)};
        },{n,choice});
        results.push(result);
      }
      console.log('Level '+n+': '+results.filter(row=>row.level===n&&row.status==='complete').length+' / '+candidates.length+' reachable first houses completed');
    }
    const failures=results.filter(row=>row.status!=='complete');
    console.log(JSON.stringify({tested:results.length,complete:results.length-failures.length,failures,variants:[...new Set(results.map(row=>row.variant))],slowestCheckMs:Math.max(...results.map(row=>row.checkMs||0))}));
    if(failures.length)process.exitCode=1;
  }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
