const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const folder = path.dirname(__dirname);
const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, 'manifest.json')));
const pageData = JSON.parse(fs.readFileSync(path.join(folder, manifest.page)));
const nodes = [];
function walk(es){for(const e of es){nodes.push(e);walk(e.elements||[])}}
walk(pageData.content);
const selector = title => `[data-id="${nodes.find(e=>e.settings._title===title).id}"]`;

(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
 const results=[];
 try{
  for(const width of [1440,768,390]){
   const context=await browser.newContext({viewport:{width,height:1000}});
   await context.route('https://syncs.com.sa/**',route=>route.abort());
   const page=await context.newPage();const errors=[];const posts=[];
   page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(r.method()==='POST')posts.push(r.url())});
   await page.setContent(fs.readFileSync('/tmp/syncs-scega-native-review.html','utf8'));
   await page.evaluate(()=>document.fonts.ready);
   assert.equal(await page.locator('h1').count(),1);
   for(const section of manifest.sections){assert.equal(await page.locator('#'+section.anchor).count(),1)}
   const overflow=()=>page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth}));
   let dimensions=await overflow();assert.ok(dimensions.scroll<=width,JSON.stringify(dimensions));
   if(width===1440){
    const strip=await Promise.all([0,1,2,3,4].map(i=>page.locator(selector('Trust strip item '+i)).boundingBox()));
    assert.ok(strip.every(b=>Math.abs(b.y-strip[0].y)<1),'All five event-strip items must stay on one desktop row');
   }
   const tabChecks=[];
   const titles=['Conference Permit Support','Exhibition Permit Support','Workshop Permit Support','Training Event Support','Business Meeting Support'];
   for(let i=0;i<5;i++){
    const tab=page.locator('[role=tab]').nth(i);await tab.click();
    assert.equal(await tab.getAttribute('aria-selected'),'true');
    assert.equal(await page.locator('[role=tab][aria-selected=true]').count(),1);
    const id=await tab.getAttribute('aria-controls');
    assert.ok(await page.locator('#'+id).isVisible());
    assert.ok((await page.locator('#'+id+' h3').first().innerText()).includes(titles[i]));
    dimensions=await overflow();assert.ok(dimensions.scroll<=width,`tab ${i}: ${JSON.stringify(dimensions)}`);
    tabChecks.push(titles[i]);
   }
   await page.locator('[role=tab]').first().focus();await page.keyboard.press('ArrowDown');
   assert.equal(await page.locator('[role=tab]').nth(1).getAttribute('aria-selected'),'true');
   await page.locator('[role=tab]').first().click();
   const accordionRoots=page.locator('.e-n-accordion');assert.equal(await accordionRoots.count(),3);
   assert.equal(await page.locator('details[open]').count(),0);
   let accordionChecks=0;
   for(let i=0;i<3;i++){
    const root=accordionRoots.nth(i);const items=root.locator('details');const count=await items.count();
    for(let j=0;j<count;j++){
     await items.nth(j).locator('summary').click();
     assert.ok(await items.nth(j).getAttribute('open')!==null);
     assert.equal(await root.locator('details[open]').count(),1);
     await items.nth(j).locator('summary').click();
     assert.equal(await root.locator('details[open]').count(),0);accordionChecks++;
    }
   }
   await page.locator('summary').first().focus();await page.keyboard.press('Enter');
   assert.equal(await page.locator('details[open]').count(),1);
   await page.keyboard.press('Enter');assert.equal(await page.locator('details[open]').count(),0);
   await page.locator(selector('Hero discuss event')+' a').click();
   assert.equal(await page.evaluate(()=>location.hash),'#sx-event-brief');
   const form=page.locator('form');assert.equal(await form.locator('label').count(),4);
   assert.equal(await form.evaluate(el=>el.checkValidity()),false);
   await page.locator('#qa-name').fill('QA Person');await page.locator('#qa-email').fill('invalid-email');
   await page.locator('#qa-event_type').selectOption('conference');
   assert.equal(await form.evaluate(el=>el.checkValidity()),false);
   await page.locator('#qa-email').fill('qa@example.test');
   assert.equal(await form.evaluate(el=>el.checkValidity()),true);
   await form.locator('button[type=submit]').click();
   assert.equal(await page.evaluate(()=>window.__qaSubmitPrevented),1);assert.deepEqual(posts,[]);
   if(width===390){
    const name=await page.locator('.field-name').boundingBox(),email=await page.locator('.field-email').boundingBox();
    assert.ok(email.y>name.y && Math.abs(name.x-email.x)<1);
   }
   await form.evaluate(el=>el.reset());
   await page.emulateMedia({reducedMotion:'reduce'});dimensions=await overflow();assert.ok(dimensions.scroll<=width);
   assert.deepEqual(errors,[]);
   await page.evaluate(()=>scrollTo(0,0));
   await page.screenshot({path:path.join(__dirname,`layout-review-${width}.png`),fullPage:true});
   await page.screenshot({path:path.join(__dirname,`hero-review-${width}.png`)});
   results.push({width,passed:true,sections:14,tabPanels:tabChecks,accordionItems:accordionChecks,keyboardTabsAndAccordion:true,heroAnchorToBrief:true,browserFormConstraints:true,realFormSubmission:false,postRequests:posts.length,noHorizontalOverflow:true,reducedMotionLayout:true});
   await context.close();
  }
 }finally{await browser.close()}
 const report={scope:'Independent DOM harness from native controls. Tabs use a test-only controller; Form submit is prevented. Not an Elementor/WordPress render or backend submission test. Photo requests are blocked and show the configured native solid fallbacks.',results};
 fs.writeFileSync(path.join(__dirname,'browser-results.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify(report));
})().catch(e=>{console.error(e);process.exitCode=1});
