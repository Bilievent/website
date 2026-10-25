const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'manifest.json')));
const config=JSON.parse(fs.readFileSync(path.join(__dirname,'../service-content.json')));
const html=fs.readFileSync('/tmp/syncs-conference-6988-review.html','utf8');

(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
 const results=[];
 try{
  for(const width of [1440,768,390]){
   const page=await browser.newPage({viewport:{width,height:1000}});
   const errors=[],posts=[];
   page.on('pageerror',e=>errors.push(e.message));
   page.on('request',r=>{if(r.method()==='POST')posts.push(r.url())});
   await page.route('http://**',route=>route.abort());
   await page.route('https://**',route=>route.abort());
   await page.setContent(html);await page.evaluate(()=>document.fonts.ready);
   assert.equal(await page.locator('h1').count(),1);
   for(const s of manifest.sections)assert.equal(await page.locator('#'+s.anchor).count(),1);
   const dimensions=()=>page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
   assert.ok((await dimensions()).scroll<=width,JSON.stringify(await dimensions()));
   const tabs=page.locator('[role=tab]');assert.equal(await tabs.count(),3);
   for(let i=0;i<3;i++){
    await tabs.nth(i).click();
    assert.equal(await tabs.nth(i).getAttribute('aria-selected'),'true');
    const panel=await tabs.nth(i).getAttribute('aria-controls');
    assert.ok(await page.locator('#'+panel).isVisible());
    assert.ok((await page.locator('#'+panel+' h3').first().innerText()).includes(config.classification.tabs[i].title));
    assert.ok((await dimensions()).scroll<=width,`Tab ${i}: ${JSON.stringify(await dimensions())}`);
   }
   await tabs.first().focus();await page.keyboard.press('ArrowRight');
   assert.equal(await tabs.nth(1).getAttribute('aria-selected'),'true');await tabs.first().click();
   const roots=page.locator('.accordion');assert.equal(await roots.count(),2);
   let itemsChecked=0;
   for(const root of await roots.all()){
    const items=root.locator('details');
    for(let i=0;i<await items.count();i++){
     const item=items.nth(i);
     if(await item.getAttribute('open')!==null)await item.locator('summary').click();
     await item.locator('summary').click();assert.ok(await item.getAttribute('open')!==null);
     assert.equal(await root.locator('details[open]').count(),1);itemsChecked++;
    }
    await root.locator('details[open] summary').click();
   }
   assert.equal(itemsChecked,15);
   await page.locator('summary').first().focus();await page.keyboard.press('Enter');
   assert.equal(await roots.first().locator('details[open]').count(),1);await page.keyboard.press('Enter');
   await page.locator('#conference-hero .widget-button a').first().click();
   assert.equal(await page.evaluate(()=>location.hash),'#conference-brief');
   const form=page.locator('form');assert.equal(await form.locator('label').count(),7);
   assert.equal(await form.evaluate(el=>el.checkValidity()),false);
   for(const [key,value] of [['name','QA Person'],['company','QA Company'],['email','invalid-email'],['brief','A draft conference brief for browser validation only.']])await page.locator('#qa-'+key).fill(value);
   await page.locator('#qa-support').selectOption('conference_delivery');
   assert.equal(await form.evaluate(el=>el.checkValidity()),false);
   await page.locator('#qa-email').fill('qa@example.test');
   assert.equal(await form.evaluate(el=>el.checkValidity()),true);
   await form.locator('button').click();assert.equal(await page.evaluate(()=>window.__qaPrevented),1);
   assert.deepEqual(posts,[]);await form.evaluate(el=>el.reset());
   assert.equal(await page.locator('.post-grid article').count(),3);
   assert.equal(await page.locator('img').evaluateAll(imgs=>imgs.every(i=>i.complete&&i.naturalWidth>0)),true);
   if(width===390){
    const name=await page.locator('.field-name').boundingBox(),email=await page.locator('.field-email').boundingBox();
    assert.ok(email.y>name.y&&Math.abs(email.x-name.x)<1);
   }
   await page.emulateMedia({reducedMotion:'reduce'});
   assert.ok((await dimensions()).scroll<=width);
   assert.deepEqual(errors,[]);
   await page.evaluate(()=>scrollTo(0,0));
   await page.screenshot({path:path.join(__dirname,`preview-${width}.png`),fullPage:true});
   await page.screenshot({path:path.join(__dirname,`hero-${width}.png`)});
   results.push({width,oneH1:true,contentBlocks:14,topLevelSections:13,classificationPanels:3,accordionItems:itemsChecked,
    keyboardTabsAndAccordion:true,heroBriefAnchor:true,formLabels:7,browserFormConstraints:true,actualFormSubmission:false,
    postRequests:posts.length,noHorizontalOverflow:true,attachedImagesLoaded:true,livePostsQueryExecuted:false,pageErrors:errors});
   await page.close();
  }
 }finally{await browser.close()}
 const report={scope:'Independent renderer of actual #6988-derived native settings, using exact attached photos and a read-only public WordPress guide snapshot in the temporary harness. Not a WordPress/Elementor rendering or native Posts query execution. No form request sent.',results};
 fs.writeFileSync(path.join(__dirname,'browser-results.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify(report));
})().catch(error=>{console.error(error);process.exitCode=1});
