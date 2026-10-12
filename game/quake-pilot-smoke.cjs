const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');

(async()=>{
  const root=path.resolve(__dirname,'..');
  const plans=JSON.parse(fs.readFileSync(path.join(__dirname,'quake-pilot-layouts.json'),'utf8')).plans;
  const routes=JSON.parse(fs.readFileSync(path.join(root,'campaign/enhanced/reference-hints-v1/normalized_routes.json'),'utf8'));
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  const summary=[];
  try{
    const page=await browser.newPage({viewport:{width:390,height:844}});
    for(const plan of plans)for(const variant of plan.variants){
      const url='file://'+path.join(__dirname,'tester.html').replaceAll('\\','/')+'?quakeVariant='+variant.id;
      await page.goto(url);
      await page.waitForFunction(()=>window.__campaign&&window.LLCQuakePilot);
      const firstRoute=routes[plan.level-201].map(step=>step.slice(0,2));
      const result=await page.evaluate(({level,firstRoute})=>{
        __campaign.choose(level);__integratedShell.enterBoard();
        for(const tile of firstRoute.slice(1)){
          if(!__campaign.move(tile))throw Error('First-house route was rejected');
          if(__campaign.getState().mask)break;
        }
        const afterQuake=__campaign.getState(),pilot=afterQuake.quakePilot;
        if(!pilot||!pilot.variant.startsWith(level+'-'))throw Error('Expected a verified random quake pattern: '+JSON.stringify(pilot));
        if(pilot.neededLight>pilot.availableLight)throw Error('Selected quake exceeds available light');
        const route=LLCQuakePilot.lastVerifiedRoute();
        if(!route?.length)throw Error('Verified completion route missing');
        for(const tile of route.slice(1))if(!__campaign.move(tile))throw Error('Verified route failed at '+tile.join(','));
        const end=__campaign.getState(),expected=(1<<__campaign.getCurrentLevel().homes.length)-1;
        if(!end.done||end.mask!==expected)throw Error('Completion failed: '+JSON.stringify({done:end.done,mask:end.mask,expected}));
        __campaign.choose(level);
        if(__campaign.getCurrentLevel().quakeEvent.closeExtra?.length)throw Error('Quake pattern survived replay reset');
        return {variant:pilot.variant,needed:pilot.neededLight,available:pilot.availableLight,finishLight:end.light,moves:pilot.completionMoves};
      },{level:plan.level,firstRoute});
      if(result.variant!==variant.id)throw Error('Forced variant '+variant.id+' was not selected: '+result.variant);
      summary.push(result);
    }
    console.log('PASS '+summary.length+' tester quake variants across '+plans.length+' maps; each verified route completed and replay reset restored the map');
    console.log(JSON.stringify(summary.map(({variant,needed,available,finishLight})=>({variant,needed,available,finishLight}))));
  }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
