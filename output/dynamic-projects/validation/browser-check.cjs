const { chromium } = require('playwright');
const fs=require('fs');
const path=require('path');
(async()=>{
  const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{}),args:['--no-sandbox']});
  const page=await browser.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const checks=[];
  const status=()=>page.locator('.sx-live-controls [role=status]').textContent();
  const count=()=>page.locator('.sx-is-active').count();
  const wait=()=>page.waitForTimeout(600);
  for(const width of [1440,768,390]){
    await page.setViewportSize({width,height:1000});
    await page.goto(process.env.PREVIEW_URL||'http://127.0.0.1:8765/dynamic-projects/preview.html');await wait();
    const initial=await status();
    if(await count()!==1)throw Error('Initial selection missing');
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
    if(overflow)throw Error('Page overflow at '+width);
    await page.screenshot({path:path.join(__dirname,`preview-${width}.png`),fullPage:true});
    await page.locator('.sx-live-next').click();await wait();
    if(await status()===initial)throw Error('Next failed');
    await page.locator('.sx-live-prev').click();await wait();
    if(await status()!==initial)throw Error('Previous failed');
    await page.locator('.elementor-loop-container').focus();await page.keyboard.press('ArrowRight');await wait();
    if(await status()===initial)throw Error('Keyboard failed');
    await page.locator('[data-filter=events]').click();await wait();
    if(await page.locator('.e-loop-item').count()!==2||await count()!==1||!(await status()).endsWith('/ 2'))throw Error('AJAX replacement failed');
    const ids=await page.locator('.e-loop-item').evaluateAll(items=>items.map(i=>i.dataset.mockPost));
    if(ids.join(',')!=='1,3')throw Error('Filter data not preserved');
    const link=await page.locator('.e-loop-item').first().locator('h3 a').getAttribute('href');
    if(link!=='#mock-project-1')throw Error('Native project link changed');
    await page.locator('[data-filter=empty]').click();await wait();
    if(await page.locator('.sx-live-controls').isVisible()||await count()!==0)throw Error('Empty category failed');
    await page.locator('[data-filter=exhibitions]').click();await wait();
    if(await count()!==1||!(await status()).endsWith('/ 3'))throw Error('Recover from empty failed');
    // One item: controls disabled; no NaN widths or active selection loss.
    await page.evaluate(()=>mockRender([5],true));await wait();
    if(await status()!=='1 / 1'||!(await page.locator('.sx-live-next').isDisabled()))throw Error('Single item failed');
    // Newly added posts become selectable without rebuilding hardcoded slides.
    await page.evaluate(()=>mockRender([1,2,3,4,5,6,7,8],true));await wait();
    if(await page.locator('.e-loop-item').count()!==8||!(await status()).endsWith('/ 8'))throw Error('New projects failed');
    for(let i=0;i<5;i++){await page.locator('.sx-live-next').click();await wait();}
    if(await count()!==1)throw Error('Multiple pages of cards failed');
    if(width===390){
      await page.locator('.elementor-loop-container').evaluate(e=>e.scrollTo({left:0,behavior:'instant'}));await wait();
      if(await status()!=='1 / 8')throw Error('Touch-scroll state failed');
    }
    checks.push({width,pageOverflow:false,buttons:'passed',keyboard:'passed',simulatedFilterReplace:'passed',emptyCategory:'passed',singleProject:'passed',newProjects:'passed',projectLinksPreserved:true});
  }
  await page.emulateMedia({reducedMotion:'reduce'});
  if(await page.locator('.e-loop-item').first().evaluate(e=>getComputedStyle(e).transitionDuration)!=='0s')throw Error('Reduced motion failed');
  // Repeated script execution must not install duplicate controllers.
  await page.addScriptTag({path:path.resolve(__dirname,'../assets/loop-grid.js')});
  await page.setViewportSize({width:1440,height:1000});await wait();
  await page.evaluate(()=>{window.mockScrollCalls=0;const track=document.querySelector('.elementor-loop-container');const original=track.scrollBy.bind(track);track.scrollBy=(...args)=>{window.mockScrollCalls++;original(...args)};});
  const before=await status();await page.locator('.sx-live-next').click();await wait();
  if(await page.evaluate(()=>window.mockScrollCalls)!==1)throw Error('Duplicate native scroll handlers');
  const after=await status();
  const [oldIndex,total]=before.split('/').map(Number),newIndex=Number(after.split('/')[0]);
  if(newIndex!==oldIndex%total+1)throw Error('Duplicate initialization listeners');
  if(errors.length)throw Error(errors.join('\n'));
  fs.writeFileSync(path.join(__dirname,'browser-results.json'),JSON.stringify({renderer:'Local native-wrapper harness; WordPress/Elementor runtime not available',checks,reducedMotion:'passed',duplicateInitialization:'passed',pageErrors:errors},null,2));
  await browser.close();console.log('PASS',JSON.stringify(checks));
})().catch(e=>{console.error(e);process.exit(1)});
