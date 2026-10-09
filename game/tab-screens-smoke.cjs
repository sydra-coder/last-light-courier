const path=require('node:path');
const {chromium}=require('playwright');

(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    await page.goto('file://'+path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.waitForFunction(()=>window.__campaign&&window.__integratedShell);
    for(const [tab,screen] of [['courier','#courierScreen'],['trophies','#trophiesScreen'],['map','#levelJourney']]){
      await page.locator(`#integratedNav [data-destination="${tab}"]`).click();
      if(tab!=='map'&&!await page.locator(screen).isVisible())throw Error(`${tab} is not a separate visible screen`);
      if(!await page.locator('#integratedOverlay').isHidden())throw Error(`${tab} opened an overlay`);
      if(!await page.locator('#resourceStrip').isVisible())throw Error(`${tab} hides shared balances`);
      if(!await page.locator('#integratedNav').isVisible())throw Error(`${tab} hides bottom navigation`);
      if(tab==='courier')await page.screenshot({path:path.join(__dirname,'courier-screen-review.png')});
      if(tab==='trophies')await page.screenshot({path:path.join(__dirname,'trophies-screen-review.png')});
    }
    await page.evaluate(()=>{const key='last-light-courier-tester-v1',save=JSON.parse(localStorage.getItem(key));save.cleared[1]=true;localStorage.setItem(key,JSON.stringify(save))});
    await page.reload();
    await page.waitForFunction(()=>window.__campaign&&window.__integratedShell);
    await page.locator('#integratedNav [data-destination="trophies"]').click();
    const before=await page.evaluate(()=>__campaign.getSave().wallet);
    await page.locator('[data-claim-trophy="first-delivery"]').click();
    const after=await page.evaluate(()=>__campaign.getSave().wallet);
    if(after-before!==100||await page.evaluate(()=>__campaign.claimTrophy('first-delivery')))throw Error('Trophy reward was not paid exactly once');
    await page.reload();
    await page.waitForFunction(()=>window.__campaign&&window.__integratedShell);
    if(!await page.evaluate(expected=>__campaign.getSave().trophyClaims?.['first-delivery']&&__campaign.getSave().wallet===expected,after))throw Error('Trophy claim did not persist');
    await page.locator('#integratedNav [data-destination="play"]').click();
    if(await page.locator('#resourceStrip').isVisible())throw Error('Shared balances consume board space');
    if(errors.length)throw Error(errors.join('\n'));
    console.log('PASS separate screens, shared balances, one-time persistent trophy rewards');
  }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
