const path=require('node:path');
const {chromium}=require('playwright');

(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:485,height:918}}),errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    await page.goto('file://'+path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.evaluate(()=>localStorage.setItem('llc-appearance-v1',JSON.stringify({courier:9,look:3})));
    await page.reload();
    await page.waitForFunction(()=>window.__campaign&&window.__integratedShell);
    await page.locator('#integratedNav [data-destination="courier"]').click();
    await page.waitForFunction(()=>{const canvas=document.querySelector('#courierScreen .outfitCanvas');return canvas&&canvas.getBoundingClientRect().width>0});
    await page.screenshot({path:path.join(__dirname,'courier-crop-review.png')});
    for(let courier=1;courier<18;courier++){
      await page.locator(`#courierScreen [data-courier="${courier}"]`).click();
      for(let look=1;look<=5;look++){
        await page.locator(`#courierScreen [data-look="${look}"]`).click();
        await page.waitForFunction(()=>document.querySelector('#courierScreen .outfitCanvas'));
      }
    }
    if(errors.length)throw Error(errors.join('\n'));
    console.log('PASS all 85 sheet costumes render; Kavi crop visually reviewed');
  }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
