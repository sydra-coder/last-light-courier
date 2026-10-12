const path=require('node:path');
const {chromium}=require('playwright');

(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    for(const file of ['index.html','tester.html']){
      const page=await browser.newPage();
      const errors=[];
      page.on('pageerror',e=>errors.push(e.message));
      await page.goto('file://'+path.join(__dirname,file).replaceAll('\\','/'));
      await page.waitForFunction(()=>!!window.__campaign);
      const result=await page.evaluate(()=>{
        const c=window.__campaign;
        const run=()=>{c.choose(1);const before=c.getSave().wallet;const spine=c.getCurrentLevel().spine;for(const tile of spine.slice(1)){if(!c.move(tile))throw Error('Route blocked at '+tile);if(c.getState().done||c.getState().failed)break}const state=c.getState();if(!state.done||state.failed)throw Error('Level 1 did not complete');return {earned:state.earned,walletDelta:c.getSave().wallet-before,best:c.getSave().best[1]}};
        return {first:run(),replay:run(),cleared:!!c.getSave().cleared[1]};
      });
      if(!result.cleared||result.first.earned<=0||result.first.walletDelta!==result.first.earned||result.replay.earned!==Math.floor(result.first.earned/5)||result.replay.walletDelta!==result.replay.earned||result.replay.best!==result.first.best)throw Error(file+' replay payout wrong: '+JSON.stringify(result));
      if(errors.length)throw Error(file+' page errors: '+errors.join(' | '));
      await page.close();
      console.log('PASS '+file+' first '+result.first.earned+', replay '+result.replay.earned);
    }
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
