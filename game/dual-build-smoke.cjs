const path=require('node:path');
const {chromium}=require('playwright');

(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    const open=async file=>{
      await page.goto('file://'+path.join(__dirname,file).replaceAll('\\','/'));
      await page.waitForFunction(()=>!!window.__campaign&&!!window.__integratedShell);
      await page.evaluate(()=>__campaign.choose(17));
    };
    await open('index.html');
    const player=await page.evaluate(()=>({saveKey:localStorage.getItem('last-light-courier-2000-candidate-v1')!==null,tester:document.body.classList.contains('testerBuild'),icons:document.querySelectorAll('#candidatePower .powerIcon').length,board:document.querySelector('.boardframe').getBoundingClientRect().height,screen:document.querySelector('#playScreen').getBoundingClientRect().height}));
    if(!player.saveKey||player.tester||player.icons>=9||player.board<370)throw Error('Player layout or inventory regression: '+JSON.stringify(player));
    await page.screenshot({path:path.join(__dirname,'player-board-review.png')});
    await page.evaluate(()=>{__campaign.choose(1);for(const tile of __campaign.levels[0].spine.slice(1,4))__campaign.move(tile)});
    await page.waitForTimeout(500);
    if(!(await page.evaluate(()=>__campaign.getState().mask)))throw Error('House was not lit for visual review');
    await page.screenshot({path:path.join(__dirname,'lit-house-review.png')});
    await page.evaluate(()=>{const s=__campaign.getSave();s.cleared={2:true,3:true,4:true,5:true};s.hints=1;s.hintRewardMilestone=0;s.pendingHintRewards=0;localStorage.setItem('last-light-courier-2000-candidate-v1',JSON.stringify(s))});
    await page.reload();await page.waitForFunction(()=>!!window.__campaign);
    await page.evaluate(()=>{__campaign.choose(1);for(const tile of __campaign.levels[0].spine.slice(1)){__campaign.move(tile);if(__campaign.getState().done||__campaign.getState().failed)break}});
    const hints=await page.evaluate(()=>({done:__campaign.getState().done,hints:__campaign.getSave().hints,milestone:__campaign.getSave().hintRewardMilestone}));
    if(!hints.done||hints.hints!==2||hints.milestone!==1)throw Error('Five-clear hint award failed: '+JSON.stringify(hints));
    await open('tester.html');
    const tester=await page.evaluate(()=>({flag:document.body.classList.contains('testerBuild'),icons:document.querySelectorAll('#candidatePower .powerIcon').length,stock:Object.values(__campaign.getSave().powerStock||{}),wallet:__campaign.getSave().wallet,hints:__campaign.getSave().hints,playerSave:JSON.parse(localStorage.getItem('last-light-courier-2000-candidate-v1')).hints,testerRecords:!!localStorage.getItem('llc-tester-data-v1'),playerRecords:!!localStorage.getItem('llc-player-data-v1')}));
    if(!tester.flag||tester.icons!==9||tester.stock.length!==9||tester.stock.some(n=>n<10)||tester.wallet<10000||tester.hints!==5||tester.playerSave!==2||!tester.testerRecords||!tester.playerRecords)throw Error('Tester seeding or save isolation failed: '+JSON.stringify(tester));
    await page.screenshot({path:path.join(__dirname,'tester-board-review.png')});
    if(errors.length)throw Error('Browser errors: '+errors.join(' | '));
    console.log('PASS player/tester isolation, 9 tester powers, 5-clear automatic hint, board size',Math.round(player.board));
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
