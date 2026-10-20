const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

const folder = path.dirname(__dirname);
const template = JSON.parse(fs.readFileSync(path.join(folder, 'SYNCs-Why-Us-Native-5-Services.json')));
const services = JSON.parse(fs.readFileSync(path.join(folder, 'services.json')));
const elements = [];
function walk(items) { for (const e of items) { elements.push(e); walk(e.elements || []); } }
walk(template.content);
const node = title => elements.find(e => e.settings._title === title);
const select = title => `[data-id="${node(title).id}"]`;

(async () => {
  const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', headless: true, args: ['--no-sandbox']});
  const results = [];
  try {
    for (const width of [1440, 768, 390]) {
      const context = await browser.newContext({viewport: {width, height: 900}, javaScriptEnabled: false});
      // Known network denial: internal review uses the native background fallback, never substitute photos.
      await context.route('https://syncs.com.sa/**', route => route.abort());
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      await page.setContent(fs.readFileSync('/tmp/syncs-whyus-native-review.html', 'utf8'));
      assert.equal(await page.locator('article').count(), 5);
      assert.equal(await page.locator('nav a').count(), 5);
      const geometry = await page.evaluate(() => ({width: innerWidth, scrollWidth: document.documentElement.scrollWidth}));
      assert.ok(geometry.scrollWidth <= width, JSON.stringify(geometry));
      const navBox = await page.locator('nav').boundingBox();
      const cardBox = await page.locator('article').first().boundingBox();
      if (width > 1024) assert.ok(cardBox.x >= navBox.x + navBox.width + 30);
      else assert.ok(cardBox.y >= navBox.y + navBox.height + 15);
      const notes = await page.locator(select('event-management details')).boundingBox();
      const photo = await page.locator(select('event-management photo')).boundingBox();
      if (width > 767) assert.ok(photo.x > notes.x + notes.width);
      else assert.ok(photo.y >= notes.y + notes.height + 15);
      const targets = [];
      for (const service of services) {
        const target = '#sx-whyus-' + service.slug;
        const link = page.locator(`nav a[href="${target}"]`);
        const linkBox = await link.boundingBox();
        assert.ok(linkBox.height >= 44, `Navigation target ${linkBox.height}px`);
        await link.click();
        const status = await page.locator(target).evaluate(el => ({hash: location.hash, top: el.getBoundingClientRect().top, titleTop: el.querySelector('h3').getBoundingClientRect().top, display: getComputedStyle(el).display}));
        assert.equal(status.hash, target);
        assert.ok(status.titleTop >= 0 && status.titleTop < 900, JSON.stringify(status));
        assert.notEqual(status.display, 'none');
        targets.push({target, nativeAnchor: true, targetHeight: linkBox.height});
      }
      const firstLink = page.locator('nav a').first();
      await firstLink.focus();
      await page.keyboard.press('Enter');
      assert.equal(await page.evaluate(() => location.hash), '#sx-whyus-event-management');
      const button = page.locator('.elementor-button').first();
      assert.equal(await button.getAttribute('href'), 'https://syncs.com.sa/contact-us/');
      const buttonBox = await button.boundingBox();
      assert.ok(buttonBox.height >= 44);
      await button.hover();
      assert.equal(await button.evaluate(el => getComputedStyle(el).backgroundColor), 'rgb(201, 188, 227)');
      assert.deepEqual(errors, []);
      await page.locator('body').click({position: {x: 2, y: 2}});
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.screenshot({path: path.join(__dirname, `native-layout-review-${width}.png`)});
      if (width === 1440) await page.screenshot({path: path.join(__dirname, 'native-layout-review-full.png'), fullPage: true});
      results.push({width, passed: true, noHorizontalOverflow: true, nav: navBox, firstCard: cardBox, nativeAnchorChecks: targets, keyboardEnter: true, customJavaScriptDisabled: true});
      await context.close();
    }
  } finally { await browser.close(); }
  const report = {scope: 'Independent DOM harness generated from native JSON controls; not WordPress/Elementor runtime. Photos unavailable and replaced by the specified native solid fallback only in QA.', results};
  fs.writeFileSync(path.join(__dirname, 'browser-results.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
})().catch(e => {console.error(e); process.exitCode = 1;});
