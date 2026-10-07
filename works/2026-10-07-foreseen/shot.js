// node shot.js -> seen/face-1100.png, seen/face-390.png, seen/face-390-tapped.png; reports page errors and horizontal overflow
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const errs = [];
 for (const w of [1100, 390]) { const p = await b.newPage({ viewport: { width: w, height: 900 } }); p.on('pageerror', e => errs.push(w + ': ' + e.message));
  await p.goto('file://' + path.join(__dirname, 'index.html')); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(__dirname, 'seen', `face-${w}.png`) });
  const box = await p.locator('#line').boundingBox(); await p.mouse.click(box.x + box.width * 0.13, box.y + box.height * 0.4);
  await p.locator('#mx td.c').nth(26).click();
  await p.screenshot({ path: path.join(__dirname, 'seen', `face-${w}-tapped.png`), fullPage: true });
  console.log(w, 'overflow', await p.evaluate(() => document.documentElement.scrollWidth > innerWidth), await p.locator('#say').innerText()); }
 console.log('errors', errs); await b.close(); })();
