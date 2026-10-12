const path=require('node:path');
const {chromium}=require('playwright');

(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    await page.goto('file://'+path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.waitForFunction(()=>window.__campaign&&window.__integratedShell);
    await page.evaluate(()=>{__campaign.choose(1202);__integratedShell.enterBoard();const r=__campaign.getCurrentLevel().repair,__cell=document.querySelector(`#board .cell[data-x="${r.tile[0]}"][data-y="${r.tile[1]}"]`);__integratedShell.showRepairTile(__cell)});
    const save=await page.evaluate(()=>__campaign.getSave());
    if(save.gems<1)throw Error('Tester gem balance was not seeded');
    if(!await page.locator('#repairPopover .freeRepair').isVisible())throw Error('Zero-cost repair does not show Free');
    if(await page.locator('#repairPopover .gemAmount').count())throw Error('Zero-cost repair still shows a gem price');
    if(await page.locator('#repairPopover [data-repair-apply="inventory"]').count())throw Error('Free repair offers to consume inventory');
    await page.screenshot({path:path.join(__dirname,'free-repair-review.png')});
    if(errors.length)throw Error(errors.join('\n'));
    console.log('PASS level 1202 free repair shows no gem or charge cost');
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
