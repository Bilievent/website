// Independent native-control layout review, not an Elementor runtime.
const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.dirname(__dirname);
const document = JSON.parse(fs.readFileSync(path.join(root, 'SYNCs-SCEGA-Complete-Page-Brand-Colors.json')));
const source = fs.readFileSync('/tmp/syncs-scega-brand-color-review.html', 'utf8');

(async () => {
  const browser = await chromium.launch({executablePath:'/usr/bin/chromium', args:['--no-sandbox']});
  const results = [];
  try {
    for (const width of [1440, 768, 390]) {
      const page = await browser.newPage({viewport:{width, height:1000}});
      // Unavailable network imagery uses the native solid fallback; no substituted photos.
      await page.route('https://syncs.com.sa/**', route => route.abort());
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.setContent(source);
      await page.evaluate(() => document.fonts.ready);
      assert.equal(await page.locator('h1').count(), 1);
      assert.equal(await page.locator('section').count(), 12);
      const dimensions = await page.evaluate(() => ({width:innerWidth, scroll:document.documentElement.scrollWidth}));
      assert.ok(dimensions.scroll <= width, JSON.stringify(dimensions));
      const sections = [];
      for (const element of document.content[0].elements) {
        const locator = page.locator(`[data-id="${element.id}"]`);
        const color = await locator.evaluate(el => getComputedStyle(el).backgroundColor);
        const rgb = element.settings.background_color.match(/\w\w/g).map(v => parseInt(v, 16));
        assert.equal(color, `rgb(${rgb.join(', ')})`);
        sections.push({section:element.settings._title, background:color});
      }
      await page.screenshot({path:path.join(__dirname, `color-review-${width}.png`), fullPage:true});
      if (width === 1440) await page.screenshot({path:path.join(__dirname, 'hero-color-review.png')});
      assert.deepEqual(errors, []);
      results.push({width, noHorizontalOverflow:true, sectionColorsMatchExport:true, sections, pageErrors:errors});
      await page.close();
    }
  } finally { await browser.close(); }
  const report = {
    scope:'Independent DOM harness from the unchanged native layout controls; not a WordPress/Elementor rendering. Remote photo requests blocked, showing declared fallback colors. No form submission performed.',
    results,
  };
  fs.writeFileSync(path.join(__dirname, 'browser-results.json'), JSON.stringify(report, null, 2)+'\n');
  console.log(JSON.stringify({passed:true, widths:results.map(r => r.width), sectionColorsMatchExport:true, noHorizontalOverflow:true}));
})().catch(error => {console.error(error); process.exitCode=1;});
