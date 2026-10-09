const path = require('node:path');
const { chromium } = require('playwright');

const levels = [1,8,6,9,11,31,51,61,101,151,201,301,401,402,501,601,701,801,901,902,951,952,1001,1002,1003,1101,1201,1204,1301,1401,1402,1601,1701,1805];

(async () => {
  const browser = await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try {
    const page = await browser.newPage({viewport:{width:390,height:844}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('file://' + path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.waitForFunction(() => !!window.__campaign && !!window.__integratedShell);
    for (const n of levels) {
      const result = await page.evaluate(n => {
        __campaign.choose(n);
        return {number:__campaign.levels[n-1].n,cells:document.querySelectorAll('#board .cell').length,title:document.querySelector('#levelTitle').textContent,powers:document.querySelectorAll('#candidatePower .powerIcon').length};
      },n);
      if (result.number !== n || result.cells < 64 || !result.title.includes(String(n)) || result.powers !== 9) throw Error('Level failed: '+JSON.stringify(result));
    }
    await page.evaluate(() => __campaign.choose(3));
    await page.screenshot({path:path.join(__dirname,'depot-review.png')});
    const bridgeIcon = await page.locator('[data-power="light_bridge"]').boundingBox();
    await page.mouse.click(bridgeIcon.x+bridgeIcon.width/2,bridgeIcon.y+bridgeIcon.height/2);
    await page.screenshot({path:path.join(__dirname,'power-info-review.png')});
    const beforeMove = await page.evaluate(() => ({stock:[...document.querySelectorAll('#candidatePower .powerIcon')].map(button=>Number(button.querySelector('i').textContent)),flask:document.querySelector('[data-power="lumen_flask"]').classList.contains('ready')}));
    if(beforeMove.stock.length!==9||beforeMove.stock.some(stock=>stock<9)||beforeMove.flask)throw Error('Tester starting inventory or power readiness failed: '+JSON.stringify(beforeMove));
    const afterMove = await page.evaluate(() => {__campaign.move(__campaign.levels[2].spine[1]);return document.querySelector('[data-power="lumen_flask"]').classList.contains('ready')});
    if(!afterMove)throw Error('Lumen Flask did not become ready after spending light');
    const reveal = await page.evaluate(() => {__campaign.choose(201);return document.querySelector('[data-power="reveal_pulse"]').classList.contains('ready')});
    if(!reveal)throw Error('Reveal Pulse is not ready on its sample level');
    if (errors.length) throw Error(errors.join(' | '));
    console.log(`PASS ${levels.length} review levels, nine tester powers, no page errors`);
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error);process.exitCode=1});
