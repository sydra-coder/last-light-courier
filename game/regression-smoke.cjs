const path=require('node:path');
const {chromium}=require('playwright');
(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const scenarios=['all','roads','weather','shadows','circuit'],results=[];
    for(const build of [{file:'regression.html',level:1,mask:7,saveKey:'last-light-courier-regression-v1'},{file:'level-500-test.html',level:500,mask:15,saveKey:'last-light-courier-level-500-test-v1'}])for(const scenario of scenarios){
      const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
      page.on('pageerror',e=>errors.push(e.message));
      await page.goto('file://'+path.join(__dirname,build.file).replaceAll('\\','/')+'?scenario='+scenario);
      await page.waitForFunction(()=>!!window.__campaign&&!!window.LLCRegression&&!!document.getElementById('regressionBar'));
      await page.waitForTimeout(250);
      const initial=await page.evaluate(()=>({level:__campaign.getCurrentLevel().n,grid:__campaign.getCurrentLevel().grid,scenario:LLCRegression.scenario,powers:document.querySelectorAll('#candidatePower .powerIcon').length,stock:Object.values(__campaign.getSave().powerStock),wallet:__campaign.getSave().wallet,home:document.querySelector('#playScreen').classList.contains('homeMode'),frame:document.querySelector('.boardframe').getBoundingClientRect().width}));
      if(initial.level!==build.level||initial.grid!==12||initial.scenario!==scenario||initial.powers!==9||initial.stock.length!==9||initial.stock.some(n=>n<10)||initial.wallet<10000||initial.home||initial.frame<360)throw Error('Regression setup failed: '+JSON.stringify(initial));
      if(build.level===500&&scenario==='all'){
        const layout=await page.evaluate(()=>({trayBottom:document.getElementById('candidatePower').getBoundingClientRect().bottom,phaseBottom:document.getElementById('phaseChoiceControl').getBoundingClientRect().bottom,labels:[...document.querySelectorAll('.powerIcon')].map(button=>button.dataset.label),statusHidden:document.getElementById('boardMessage').hidden}));
        if(layout.trayBottom>844||layout.phaseBottom>844||layout.labels.some(label=>!label)||!layout.statusHidden)throw Error('Compact layout failed: '+JSON.stringify(layout));
        await page.locator('#regressionMessageToggle').click();
        if(!await page.locator('#boardMessage').isVisible())throw Error('Map message did not open');
        await page.locator('#regressionMessageToggle').click();
        if(await page.locator('#boardMessage').isVisible())throw Error('Map message did not close');
      }
      if(scenario==='all'){
        if(build.level===500){await page.evaluate(()=>__campaign.move(__campaign.getCurrentLevel().spine[1]));await page.waitForTimeout(450);await page.screenshot({path:path.join(__dirname,'level-500-test-review.png')});await page.evaluate(()=>__campaign.reset())}
        else await page.screenshot({path:path.join(__dirname,'regression-all-hazards-review.png')});
      }
      if(scenario==='roads'){
        const before=await page.evaluate(()=>__campaign.getSave().powerStock.reveal_pulse);
        await page.locator('.powerIcon[data-power="reveal_pulse"]').click();
        const power=await page.evaluate(()=>({used:!!__campaign.getState().usedPowers.reveal_pulse,stock:__campaign.getSave().powerStock.reveal_pulse,revealed:__campaign.getState().beaconRevealed}));
        if(!power.used||power.stock!==before-1||!power.revealed)throw Error('Reveal power failed: '+JSON.stringify({before,...power}));
        await page.locator('#regressionReplay').click();
        await page.waitForFunction(()=>!!window.__campaign&&!!window.LLCRegression&&__campaign.getState().turns===0);
        const reset=await page.evaluate(()=>({stock:__campaign.getSave().powerStock.reveal_pulse,revealed:__campaign.getState().beaconRevealed,scenario:LLCRegression.scenario}));
        if(reset.stock!==10||reset.revealed||reset.scenario!=='roads')throw Error('Replay reset failed: '+JSON.stringify(reset));
      }
      const route=await page.evaluate(()=>{const spine=__campaign.getCurrentLevel().spine;let blockedAt=null;for(let i=1;i<spine.length;i++){if(!__campaign.move(spine[i])){blockedAt=i;break}if(__campaign.getState().done||__campaign.getState().failed)break}const s=__campaign.getState();return {blockedAt,done:s.done,failed:s.failed,turns:s.turns,mask:s.mask,reason:s.reason}});
      if(route.blockedAt!==null||!route.done||route.failed||route.mask!==build.mask)throw Error(build.file+' '+scenario+' route failed: '+JSON.stringify(route));
      if(errors.length)throw Error(scenario+' browser errors: '+errors.join(' | '));
      results.push({build:build.file,scenario,...route});
      await page.close();
    }
    console.log(JSON.stringify(results));
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
