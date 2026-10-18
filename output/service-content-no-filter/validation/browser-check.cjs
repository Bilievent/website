const {chromium}=require('playwright');
const fs=require('fs'),path=require('path');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});
 const page=await browser.newPage();const errors=[];page.on('pageerror',error=>errors.push(error.message));
 const base=process.env.PREVIEW_BASE||'http://127.0.0.1:8772/';
 const wait=()=>page.waitForTimeout(500);
 const count=()=>page.locator('.sx-service-active').count();
 const status=()=>page.locator('.sx-service-controls [role=status]').textContent();
 const checks=[];
 for(const kind of ['projects','articles'])for(const lang of ['en','ar'])for(const width of [1440,768,390]){
  await page.setViewportSize({width,height:1000});await page.goto(`${base}preview-${kind}-${lang}.html`);await page.waitForTimeout(600);
  if(await page.locator('.elementor-widget-taxonomy-filter,.e-filter,[data-filter]').count())throw Error('Filter UI present');
  if(await page.locator('h1').count())throw Error('Service section must not add a second page H1');
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Horizontal document overflow');
  if(await page.locator('.e-loop-item').count()!==4||await count()!==1)throw Error('Invalid initial cards');
  const cards=await page.locator('.e-loop-item').evaluateAll(items=>items.map(i=>({active:i.classList.contains('sx-service-active'),width:i.getBoundingClientRect().width,height:i.getBoundingClientRect().height})));
  if(width>600){const active=cards.find(c=>c.active),small=cards.find(c=>!c.active);if(active.width<small.width*2.3||active.height<=small.height)throw Error('Expanding card design lost: '+JSON.stringify({kind,lang,width,cards}));}
  const label=await page.locator('.sx-service-next').getAttribute('aria-label');
  if(label!==(lang==='ar'?'العنصر التالي':'Next item'))throw Error('Wrong controller language');
  await page.screenshot({path:path.join(__dirname,`preview-${kind}-${lang}-${width}.png`),fullPage:true});
  const initial=await status();await page.locator('.sx-service-next').click();await wait();if(await status()===initial)throw Error('Next failed');
  await page.locator('.sx-service-prev').click();await wait();if(await status()!==initial)throw Error('Previous failed');
  const href=await page.locator('.e-loop-item h3 a').first().getAttribute('href');if(href!=='#mock-content-1')throw Error('Dynamic link overwritten');
  checks.push({kind,lang,width,taxonomyFilterWidgets:0,documentOverflow:false,expandingCards:'passed',controls:'passed',localizedLabels:'passed'});
 }
 // New native query output, zero and one result, and append without hardcoded slides.
 await page.evaluate(()=>mockRender([]));await page.waitForTimeout(100);if(await page.locator('.sx-service-controls').isVisible())throw Error('Empty state failed');
 await page.evaluate(()=>mockRender([5]));await page.waitForTimeout(100);if(!await page.locator('.sx-service-next').isDisabled()||await count()!==1)throw Error('Single result failed');
 await page.evaluate(()=>mockRender([5,6,7,8]));await page.waitForTimeout(100);if(await page.locator('.e-loop-item').count()!==4||await count()!==1)throw Error('New native results not discovered');
 await page.locator('.elementor-loop-container').focus();const prior=await status();await page.keyboard.press('ArrowLeft');await wait();if(await status()===prior)throw Error('RTL keyboard failed');
 await page.emulateMedia({reducedMotion:'reduce'});if(await page.locator('.e-loop-item').first().evaluate(e=>getComputedStyle(e).transitionDuration)!=='0s')throw Error('Reduced motion failed');
 if(errors.length)throw Error(errors.join('\n'));
 fs.writeFileSync(path.join(__dirname,'browser-results.json'),JSON.stringify({renderer:'Local native-wrapper harness, simulated query records; not Elementor/WordPress',checks,emptyAndSingleResult:'passed',newNativeResults:'passed',rtlKeyboard:'passed',reducedMotion:'passed',pageErrors:errors,serviceCategoryQueryAndNativeImport:'not executed; requires native setup and staging'},null,2));
 await browser.close();console.log('PASS 12 responsive/language/content cases plus dynamic-result, RTL and motion checks');
})().catch(error=>{console.error(error);process.exit(1)});
