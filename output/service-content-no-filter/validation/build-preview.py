"""Local native-wrapper harness. Data/category selection here is simulated, not WordPress."""
from pathlib import Path
import json,html,shutil
root=Path(__file__).resolve().parents[1]
fixtures=root/'validation/fixtures';fixtures.mkdir(exist_ok=True)
for i in range(1,5):shutil.copyfile(root.parent/f'assets/demo-project-{i}.jpg',fixtures/f'artwork-{i}.jpg')
card=json.loads((root/'SYNCs-Service-Card.json').read_text())['content'][0]

def node_html(n,lang,post=None):
    s=n['settings'];kind=n.get('widgetType');id=n['id'];classes='elementor-element elementor-element-'+id
    if n['elType']=='container':
        return '<div data-id="'+id+'" class="'+classes+' e-con '+s.get('css_classes','')+'">'+''.join(node_html(c,lang,post) for c in n['elements'])+'</div>'
    body=''
    if kind=='heading':body='<'+s.get('header_size','h2')+' class="elementor-heading-title">'+html.escape(s['title'])+'</'+s.get('header_size','h2')+'>'
    elif kind=='html':body=s['html']
    elif kind=='image':body='<a href="'+post['url']+'"><img src="'+post['image']+'" alt="'+('رسم تجريبي للمعاينة' if lang=='AR' else 'Abstract preview fixture')+'"></a>'
    elif kind=='icon-box':body='<div class="elementor-icon-box-wrapper"><div class="elementor-icon-box-content"><h3 class="elementor-icon-box-title"><a href="'+post['url']+'">'+html.escape(post['title'])+'</a></h3></div></div>'
    elif kind=='loop-grid':body='<div class="elementor-loop-container elementor-grid">'+''.join(cards(lang)[str(i)] for i in range(1,5))+'</div>'
    else:raise ValueError(kind)
    return '<div data-id="'+id+'" class="'+classes+' elementor-widget elementor-widget-'+kind+' '+s.get('_css_classes','')+'"><div class="elementor-widget-container">'+body+'</div></div>'

def cards(lang):
    titles=['إبداع يجمع الناس','تفاصيل تصنع الفارق','تجارب استثنائية متكاملة','لحظات تستحق الاحتفال'] if lang=='AR' else ['Ideas that bring people together','Details that make the difference','Extraordinary experiences. Perfectly in sync.','Moments worth celebrating']
    result={}
    for i in range(1,9):
        post={'url':'#mock-content-'+str(i),'image':'validation/fixtures/artwork-'+str((i-1)%4+1)+'.jpg','title':titles[(i-1)%4]}
        result[str(i)]='<article class="elementor e-loop-item e-loop-item-'+str(i)+'" data-mock-post="'+str(i)+'">'+node_html(card,lang,post)+'</article>'
    return result

for kind in ['Projects','Articles']:
 for lang in ['EN','AR']:
    doc=json.loads((root/f'SYNCs-Service-{kind}-{lang}.json').read_text())
    body=''.join(node_html(n,lang) for n in doc['content'])
    note='معاينة محلية ببيانات تجريبية؛ ليست صفحة WordPress' if lang=='AR' else 'Local layout harness with simulated data; not a WordPress render'
    script='<script>const mockCards='+json.dumps(cards(lang))+';window.mockRender=ids=>{document.querySelector(".elementor-loop-container").innerHTML=ids.map(id=>mockCards[id]).join("");};</script>'
    preview='<!doctype html><html lang="'+lang.lower()+'" dir="'+('rtl' if lang=='AR' else 'ltr')+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Service '+kind+' — no filter</title><style>*{box-sizing:border-box}body{margin:0;background:#09131f;font-family:Arial,sans-serif}.e-con{display:flex;flex-direction:column;min-width:0}.elementor-widget{min-width:0;width:100%}.note{text-align:center;margin:0;padding:14px;color:#b4c0cd;font-size:12px}</style></head><body><p class="note">'+note+'</p>'+body+script+'</body></html>'
    (root/f'preview-{kind.lower()}-{lang.lower()}.html').write_text(preview)
print('Built four localized layout harnesses with no category/filter UI')
