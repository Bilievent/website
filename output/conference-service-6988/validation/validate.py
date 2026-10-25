"""Audit the actual parent-derived export, explicit colors, and first-party media gate."""
import collections
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from build import ROOT, PARENT, CONTENT, SOURCE, C, walk

manifest=json.loads((ROOT/'validation/manifest.json').read_text())
page=json.loads((ROOT/manifest['page']).read_text())
nodes=list(walk(page['content']))
source_types={e.get('widgetType') for e in walk(PARENT['content'])}
types=collections.Counter(e.get('widgetType','container') for e in nodes)
assert set(types)-{'container'}<=source_types|{'form'}
assert page['version']==PARENT['version']=='0.4' and page['type']=='page'
assert len(page['content'])==13 and len(nodes)==manifest['elements']==240
assert not set(types)&{'html','shortcode','metform','taxonomy-filter'}
ids=[e['id'] for e in nodes]
assert len(ids)==len(set(ids)) and all(re.fullmatch('[0-9a-f]{8}',v) for v in ids)
h1s=[e for e in nodes if (e.get('widgetType')=='heading' and e['settings'].get('header_size')=='h1') or (e.get('widgetType')=='animated-headline' and e['settings'].get('tag')=='h1')]
assert len(h1s)==1
anchors=[e['settings']['_element_id'] for e in nodes if e['settings'].get('_element_id')]
assert len(anchors)==len(set(anchors))==14


def leaves(value):
    if isinstance(value,dict):
        for k,v in value.items():yield k,v;yield from leaves(v)
    elif isinstance(value,list):
        for v in value:yield from leaves(v)


urls=[];images=[]
for key,value in leaves(page):
    assert key not in {'html','custom_css','custom_js'}
    if isinstance(value,str):
        assert '[uc_local]' not in value and 'data:image' not in value
        assert not re.search(r'<(?:script|style|iframe|table|div)\b',value,re.I)
        if key=='url' and value:
            urls.append(value)
            if value.startswith('#'):assert value[1:] in anchors,value
            elif value.startswith('tel:'):assert value=='tel:+966565006560',value
            else:assert urlparse(value).hostname in {'syncs.com.sa','www.syncs.com.sa','wa.me','eportal.scega.gov.sa'},value
            if '/wp-content/uploads/' in value:
                images.append(value);assert urlparse(value).hostname in {'syncs.com.sa','www.syncs.com.sa'}
assert not manifest['missing_original_media_urls'] and manifest['ready_for_media_import']
assert CONTENT['project']['url'] in urls
assert len([u for u in urls if u==CONTENT['project']['url']])>=2
for record,e in zip(manifest['sections'],page['content']):
    part=json.loads((ROOT/record['file']).read_text())
    assert part['content']==[e] and part['type']=='container'
    section_ids=[n['id'] for n in walk(part['content'])];assert len(section_ids)==len(set(section_ids))

tabs=next(e for e in nodes if e.get('widgetType')=='nested-tabs')
assert len(tabs['settings']['tabs'])==len(tabs['elements'])==3
assert [t['tab_title'] for t in tabs['settings']['tabs']]==[t['label'] for t in CONTENT['classification']['tabs']]
scope=next(e for e in nodes if e.get('widgetType')=='nested-accordion')
assert len(scope['settings']['items'])==len(scope['elements'])==5
faq=next(e for e in nodes if e.get('widgetType')=='elementskit-accordion')
assert len(faq['settings']['ekit_accordion_items'])==10
assert [v['acc_title'] for v in faq['settings']['ekit_accordion_items']]==[v['question'] for v in CONTENT['faqs']]
assert len([e for e in nodes if e['settings'].get('_title','').startswith('Preparation ') and e['elType']=='container'])==6
form=next(e['settings'] for e in nodes if e.get('widgetType')=='form')
assert len(form['form_fields'])==7 and len({f['custom_id'] for f in form['form_fields']})==7
assert form['submit_actions']==['save-to-database'] and 'email_to' not in form
assert all(f['width_mobile']=='100' for f in form['form_fields'])
assert all(f['field_options'].splitlines()[0].endswith('|') for f in form['form_fields'] if f['field_type']=='select')
posts=next(e['settings'] for e in nodes if e.get('widgetType')=='posts')
assert posts['cards_posts_per_page']==3 and posts['cards_columns']=='3' and posts['cards_columns_tablet']=='2' and posts['cards_columns_mobile']=='1'
assert posts['posts_select_date']=='anytime' and not any(posts.get(k) for k in ('posts_date_after','posts_date_before','posts_query_id'))
assert posts['posts_include_term_ids']==[] and posts['posts_posts_ids']==[str(v) for v in CONTENT['guide_post_ids']]
assert posts['posts_post_type']=='by_id' and posts['pagination_type']==''
assert next(e['settings'] for e in nodes if e.get('widgetType')=='image-carousel')['autoplay']=='no'

# Added core/Pro names are corroborated against public sources, never installed as runtime code.
for kind,path,group_prefix in [('animated-headline','/tmp/syncs-service-animated.php',None),('form','/tmp/syncs-conference-form.php',None)]:
    text=Path(path).read_text();controls=set(re.findall(r"add_(?:responsive_)?control\(\s*['\"]([^'\"]+)",text))
    groups=set(re.findall(r"['\"]name['\"]\s*=>\s*['\"]([^'\"]+)",text))
    baseline_keys=set().union(*(set(e['settings']) for e in SOURCE.values() if e.get('widgetType')==kind)) if any(e.get('widgetType')==kind for e in SOURCE.values()) else set()
    for e in [e for e in nodes if e.get('widgetType')==kind]:
        for key in set(e['settings'])-baseline_keys-{'_title','_animation'}:
            normalized=re.sub(r'_(tablet|mobile)$','',key)
            assert normalized in controls or any(normalized.startswith(g+'_') for g in groups),(kind,key)


def rgb(color):return [int(color[i:i+2],16)/255 for i in (1,3,5)]
def composite(color,bg):
    if len(color)==7:return color
    alpha=int(color[7:9],16)/255
    mixed=[round((a*alpha+b*(1-alpha))*255) for a,b in zip(rgb(color),rgb(bg))]
    return '#'+''.join(f'{v:02X}' for v in mixed)
def luminance(color):
    linear=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb(color)]
    return sum(v*w for v,w in zip(linear,(.2126,.7152,.0722)))
checks=[];photo_checks=[]
def check(label,state,fg,bg,minimum=4.5,photo=False):
    a,b=sorted((luminance(fg),luminance(bg)));value=(b+.05)/(a+.05)
    item=dict(element=label,state=state,foreground=fg,background=bg,ratio=round(value,2),minimum=minimum)
    if photo:photo_checks.append(item);return
    checks.append(item);assert value>=minimum,item
def color_walk(es,bg,photo=False):
    for e in es:
        s=e['settings'];kind=e.get('widgetType');label=s.get('_title',e['id'])
        surface=composite(s.get('background_color',bg),bg) if e['elType']=='container' else bg
        ph=photo
        if e['elType']=='container':
            if s.get('background_color') and len(s['background_color'])==7:ph=False
            if s.get('background_image',{}).get('url'):ph=True
        if kind=='heading':
            n=s.get('typography_font_size',{}).get('size',16);minimum=3 if n>=24 else 4.5
            check(label,'heading',s.get('title_color',C['bg']),surface,minimum,ph)
        elif kind=='animated-headline':
            check(label,'headline',s['title_color'],surface,3,ph);check(label,'highlighted',s['words_color'],surface,3,ph)
        elif kind=='text-editor':check(label,'body',s.get('text_color',C['graphite']),surface,photo=ph)
        elif kind=='icon-box':
            check(label,'title',s.get('title_color',C['bg']),surface,photo=ph)
            if s.get('description_text'):check(label,'description',s.get('description_color',C['graphite']),surface,photo=ph)
        elif kind=='icon-list':check(label,'list',s.get('text_color',C['graphite']),surface,photo=ph)
        elif kind=='counter':check(label,'number',s['number_color'],surface,3,ph)
        elif kind=='button':
            button_bg=composite(s['background_color'],surface)
            check(label,'button',s['button_text_color'],button_bg,photo=ph and s['background_color'].endswith('00'))
            check(label,'button hover',s['hover_color'],s['button_background_hover_color'])
        elif kind=='form':
            check(label,'label',s['label_color'],surface)
            check(label,'field',s['field_text_color'],s['field_background_color'])
            check(label,'field border',s['field_border_color'],s['field_background_color'],3)
            check(label,'submit',s['button_text_color'],s['button_background_color'])
        elif kind=='nested-accordion':
            for state in ('normal','hover','active'):check(label,state,s[state+'_title_color'],s['accordion_background_'+state+'_color'])
        elif kind=='elementskit-accordion':
            check(label,'FAQ closed',s['ekit_accordion_title_color_close'],s['ekit_accordion_background_close_color'])
            check(label,'FAQ answer',s['ekit_accordion_content_color'],s['ekit_accordion_background_color'])
        color_walk(e['elements'],surface,ph)
color_walk(page['content'],C['soft'])

report=dict(structure_passed=True,original_site_media_resolved=True,source_template='6988',top_level_sections=13,content_blocks=14,elements=len(nodes),
    native_and_existing_types=dict(types),new_type_previously_approved='Elementor Pro Form replacing unresolved external MetForm reference',
    zero_html_css_js=True,unique_anchors=len(anchors),faq_items=10,scope_items=5,classification_panels=3,preparation_cards=6,
    form_fields=7,form_backend_tested=False,live_media_hosts=sorted({urlparse(u).hostname for u in images}),media_placements=len(images),
    unique_media_urls=len(set(images)),solid_contrast_checks=len(checks),photo_dependent_checks=len(photo_checks),
    actual_wordpress_import_edit_reexport='not run: WordPress runtime and installed Elementor/Pro/add-on versions unavailable')
(ROOT/'validation/results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(ROOT/'validation/contrast.json').write_text(json.dumps(dict(passed=True,solid=checks,photo_dependent_not_certified=photo_checks),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
