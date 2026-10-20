const { chromium } = require('playwright');
const path = require('node:path');
const fs = require('node:fs');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', headless: true, args: ['--no-sandbox'] });
  const results = [];
  try {
    for (const width of [1440, 768, 390]) {
      const page = await browser.newPage({viewport: {width, height: 1000}});
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.setContent(fs.readFileSync(path.join(__dirname, 'color-review.html'), 'utf8'));
      const before = await page.locator('.cta').first().evaluate(el => {
        const c = getComputedStyle(el); return {background: c.backgroundColor, color: c.color};
      });
      assert.deepEqual(before, {background: 'rgb(143, 123, 184)', color: 'rgb(29, 22, 42)'});
      await page.locator('.cta').first().hover();
      const hover = await page.locator('.cta').first().evaluate(el => getComputedStyle(el).backgroundColor);
      assert.equal(hover, 'rgb(201, 188, 227)');
      await page.locator('.cta').first().focus();
      const focus = await page.locator('.cta').first().evaluate(el => getComputedStyle(el).backgroundColor);
      assert.equal(focus, hover);
      const tab = page.locator('.tab').first();
      await tab.hover();
      const tabHover = await tab.evaluate(el => ({background: getComputedStyle(el).backgroundColor, color: getComputedStyle(el).color}));
      assert.deepEqual(tabHover, {background: 'rgb(201, 188, 227)', color: 'rgb(29, 22, 42)'});
      const layout = await page.evaluate(() => ({sections: document.querySelectorAll('section').length, width: innerWidth, scroll: document.documentElement.scrollWidth, images: document.images.length}));
      assert.equal(layout.sections, 4); assert.equal(layout.images, 0); assert.ok(layout.scroll <= width);
      assert.deepEqual(errors, []);
      await page.locator('.notice').click();
      await page.screenshot({path: path.join(__dirname, `color-review-${width}.png`), fullPage: true});
      results.push({width, passed: true, buttonNormal: before, buttonHoverBackground: hover, tabHover, ...layout});
      await page.close();
    }
  } finally { await browser.close(); }
  const report = {scope: 'Independent palette harness only; not an actual Elementor or WordPress render', results};
  fs.writeFileSync(path.join(__dirname, 'browser-results.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
})().catch(error => { console.error(error); process.exitCode = 1; });
