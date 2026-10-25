const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const folder = path.dirname(__dirname);
const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, 'manifest.json')));
const data = JSON.parse(fs.readFileSync(path.join(folder, manifest.page)));
const source = fs.readFileSync('/tmp/syncs-conference-review.html', 'utf8');
const assets = '/tmp/syncs-conference-assets/images';
const nodes = [];
function walk(es){for(const e of es){nodes.push(e);walk(e.elements||[])}}
walk(data.content);
const id = title => nodes.find(e => e.settings._title === title).id;

(async () => {
  const browser = await chromium.launch({executablePath:'/usr/bin/chromium', args:['--no-sandbox']});
  const results = [];
  try {
    for (const width of [1440, 768, 390]) {
      const page = await browser.newPage({viewport:{width, height:1000}});
      const errors = [], requests = [], knownPhotos = new Set();
      page.on('pageerror', e => errors.push(e.message));
      page.on('request', r => {if(r.method() === 'POST')requests.push(r.url())});
      await page.route('https://syncs.com.sa/**', async route => {
        const name = path.basename(new URL(route.request().url()).pathname);
        const local = path.join(assets, name);
        if (fs.existsSync(local)) { knownPhotos.add(name); await route.fulfill({path:local}); }
        else await route.abort();
      });
      await page.setContent(source);
      await page.evaluate(() => document.fonts.ready);
      assert.equal(await page.locator('h1').count(), 1);
      for (const s of manifest.sections) assert.equal(await page.locator('#'+s.anchor).count(), 1);
      const dimensions = await page.evaluate(() => ({width:innerWidth, scroll:document.documentElement.scrollWidth}));
      assert.ok(dimensions.scroll <= width, JSON.stringify(dimensions));
      const roots = page.locator('.e-n-accordion');
      assert.equal(await roots.count(), 2);
      assert.equal(await page.locator('details[open]').count(), 2);
      let checked = 0;
      for (let i=0; i<2; i++) {
        const root = roots.nth(i), items = root.locator('details');
        for (let j=0; j<await items.count(); j++) {
          const item = items.nth(j);
          if (await item.getAttribute('open') !== null) await item.locator('summary').click();
          await item.locator('summary').click();
          assert.ok(await item.getAttribute('open') !== null);
          assert.equal(await root.locator('details[open]').count(), 1);
          checked++;
        }
        await root.locator('details[open] summary').click();
      }
      assert.equal(checked, 11);
      await page.locator('summary').first().focus();
      await page.keyboard.press('Enter');
      assert.equal(await roots.first().locator('details[open]').count(), 1);
      await page.locator(`[data-id="${id('Discuss requirements')}"] a`).click();
      assert.equal(await page.evaluate(() => location.hash), '#cf-conference-brief');
      const form = page.locator('form');
      assert.equal(await form.locator('label').count(), 7);
      assert.equal(await form.evaluate(el => el.checkValidity()), false);
      await page.locator('#qa-name').fill('QA Person');
      await page.locator('#qa-company').fill('QA Company');
      await page.locator('#qa-email').fill('bad-email');
      await page.locator('#qa-support').selectOption('permit_only');
      await page.locator('#qa-brief').fill('QA conference brief, not submitted to a server.');
      assert.equal(await form.evaluate(el => el.checkValidity()), false);
      await page.locator('#qa-email').fill('qa@example.test');
      assert.equal(await form.evaluate(el => el.checkValidity()), true);
      await form.locator('button[type=submit]').click();
      assert.equal(await page.evaluate(() => window.__prevented), 1);
      assert.deepEqual(requests, []);
      if (width === 390) {
        const name = await page.locator('.field-name').boundingBox(), email = await page.locator('.field-email').boundingBox();
        assert.ok(email.y > name.y && Math.abs(name.x-email.x)<1);
      }
      await form.evaluate(el => el.reset());
      assert.equal(await page.locator('.native-posts article').count(), 4);
      for (const root of await roots.all()) {
        await root.locator('details').first().evaluate(el => {el.open=true});
      }
      await page.emulateMedia({reducedMotion:'reduce'});
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
      assert.deepEqual(errors, []);
      await page.evaluate(() => scrollTo(0, 0));
      await page.screenshot({path:path.join(__dirname, `layout-${width}.png`), fullPage:true});
      await page.screenshot({path:path.join(__dirname, `hero-${width}.png`)});
      results.push({width, sections:15, accordionItemsChecked:checked, keyboardAccordion:true, heroBriefAnchor:true,
        browserFormConstraints:true, actualFormSubmission:false, postRequests:requests.length, noHorizontalOverflow:true,
        dynamicQueryExecuted:false, availableLocalSourcePhotos:[...knownPhotos], pageErrors:errors});
      await page.close();
    }
  } finally {await browser.close()}
  const report = {scope:'Independent DOM review from native controls; not WordPress or Elementor frontend. Sample Posts content is QA-only. Only exact-name source photos available in the user ZIP are served locally; other media use solid fallbacks. No form request is sent.',results};
  fs.writeFileSync(path.join(__dirname, 'browser-results.json'), JSON.stringify(report, null, 2)+'\n');
  console.log(JSON.stringify(report));
})().catch(e => {console.error(e); process.exitCode=1;});
