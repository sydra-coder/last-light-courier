const path=require('node:path');
const {chromium}=require('playwright');

(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    await page.goto('file://'+path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.waitForFunction(()=>window.__campaign&&window.__integratedShell);
    const prices=await page.evaluate(()=>({optional:LLCGemShop.repairPriceFor(__campaign.levels[1201]),required:LLCGemShop.repairPriceFor(__campaign.levels[124]),gems:__campaign.getSave().gems}));
    if(prices.optional!==20||prices.required!==0||prices.gems<20)throw Error('Wrong optional or required repair pricing: '+JSON.stringify(prices));
    await page.evaluate(()=>{__campaign.choose(1202);__integratedShell.enterBoard();const r=__campaign.getCurrentLevel().repair,cell=document.querySelector(`#board .cell[data-x="${r.tile[0]}"][data-y="${r.tile[1]}"]`);__integratedShell.showRepairTile(cell)});
    if(!await page.locator('#repairPopover [data-repair-apply="gems"][aria-label="Spend 20 gems"]').isVisible())throw Error('Optional shortcut does not show 20 gems');
    if(await page.locator('#repairPopover .freeRepair').count())throw Error('Optional shortcut is still free');
    await page.screenshot({path:path.join(__dirname,'repair-pricing-review.png')});
    if(errors.length)throw Error(errors.join('\n'));
    console.log('PASS optional repair costs 20 gems; required repair stays free');
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
