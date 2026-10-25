"""Adapt the user's actual #6988 parent export; never execute attached content."""
import copy
import hashlib
import html
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = Path('/workspace/attachments/54785e20-8349-4ffc-972d-4fee2a3a233a/scega_elementor_template.zip')
CONTENT = json.loads((ROOT/'service-content.json').read_text())
MEDIA = json.loads((ROOT/'media-urls.json').read_text())
with zipfile.ZipFile(ARCHIVE) as archive:
    PARENT = json.loads(archive.read('elementor-6988-2026-10-25.json'))


def walk(es):
    for e in es:
        yield e
        yield from walk(e.get('elements', []))


SOURCE = {e['id']:e for e in walk(PARENT['content'])}
C = dict(bg='#1D162A', purple='#8F7BB8', panel='#2B203D', charcoal='#3A3447', lavender='#C9BCE3',
         gray='#F5F5F7', soft='#FAFAFC', silver='#D8D8E0', white='#FFFFFF', graphite='#4A4557', slate='#4D4E63')
BRIEF = '#conference-brief'


def size(n, unit='px'): return dict(unit=unit, size=n, sizes=[])
def dims(t, r=None, b=None, l=None):
    r=t if r is None else r; b=t if b is None else b; l=r if l is None else l
    return dict(unit='px', top=str(t), right=str(r), bottom=str(b), left=str(l), isLinked=t==r==b==l)
def gap(n): return dict(unit='px', column=str(n), row=str(n), size=n, isLinked=True)
def widths(n, tablet=100, mobile=100): return dict(width=size(n,'%'),width_tablet=size(tablet,'%'),width_mobile=size(mobile,'%'))
def font(prefix='typography', n=16, weight='400', line=1.6):
    return {prefix+'_typography':'custom', prefix+'_font_family':'Poppins', prefix+'_font_size':size(n),
            prefix+'_font_weight':weight, prefix+'_line_height':size(line,'em')}


def clone(id_, label=None, children=None, **settings):
    e=copy.deepcopy(SOURCE[id_])
    if label: e['settings']['_title']=label
    if children is not None: e['elements']=children
    e['settings'].update(settings)
    return e


def find(root, id_): return next(e for e in walk([root]) if e['id']==id_)
def text(label, copy_, color=None, n=15):
    return clone('27575089',label,editor='<p>'+html.escape(copy_)+'</p>',text_color=color or C['graphite'],**font(n=n))
def heading(label, title, n=30, tag='h2', color=None):
    return clone('58b8ae02',label,title=title,header_size=tag,title_color=color or C['bg'],
                 _element_width='inherit',**font(n=n,weight='600',line=1.22),typography_font_size_mobile=size(min(n,25)))
def animated(id_,label,before,word,after,n=40,tag='h2',dark=False):
    return clone(id_,label,before_text=before,highlighted_text=word,after_text=after,tag=tag,loop='',headline_style='highlight',rotating_text=word,
        title_color=C['white'] if dark else C['bg'],words_color=C['lavender'] if dark else C['purple'],
        marker_color=C['purple'],**font('title_typography',n,'600',1.18),
        title_typography_font_size_tablet=size(min(n,36)),title_typography_font_size_mobile=size(min(n,30)))
def button(label,title,url=BRIEF,secondary=False,dark=False):
    return clone('7507376c' if secondary else '3a7bc335',label,text=title,
        link=dict(url=url,is_external='',nofollow='',custom_attributes=''),
        background_background='classic',background_color=C['bg']+'00' if secondary else C['slate'],
        button_text_color=(C['lavender'] if dark else C['bg']) if secondary else C['white'],
        button_background_hover_background='classic',button_background_hover_color=C['lavender'],hover_color=C['bg'],
        border_border='solid',border_width=dims(1),border_color=C['purple'] if secondary else C['slate'],
        border_radius=dims(6),text_padding=dims(13,20),**font(n=13,weight='500',line=1.4))
def bullets(label,items,dark=False,links=None):
    e=clone('454ec936',label,text_color=C['silver'] if dark else C['graphite'],
        text_color_hover=C['lavender'] if dark else C['bg'],icon_color=C['lavender'] if dark else C['purple'],
        **font('icon_typography',14))
    template=e['settings']['icon_list'][0]
    e['settings']['icon_list']=[]
    for i,item in enumerate(items):
        row=copy.deepcopy(template);row['text']=item
        if links:row['link']=dict(url=links[i],is_external='',nofollow='',custom_attributes='')
        else:row.pop('link',None)
        e['settings']['icon_list'].append(row)
    return e
def section(label,anchor,children,bg=None):
    return clone('21fed003',label,children,content_width='boxed',boxed_width=size(1280),html_tag='section',
        _element_id=anchor,background_color=bg or C['gray'],padding=dims(48,24),padding_tablet=dims(38,24),
        padding_mobile=dims(30,20),flex_gap=gap(26))
def row(label,children):
    return clone('51b1c461',label,children,flex_direction='row',flex_direction_tablet='row',flex_direction_mobile='column',
        flex_wrap='wrap',flex_gap=gap(18),flex_align_items='stretch',flex_justify_content='space-between')
def card(label,title,copy_,icon,percent=32):
    content=clone('6201177b',label+' content',title_text=title,description_text=copy_,
        selected_icon=dict(value='fas fa-'+icon,library='fa-solid'),title_size='h3',
        **font('title_typography',17,'600',1.35),**font('description_typography',14,'400',1.55))
    return clone('bc673a9',label,[content],**widths(percent,48,100))
def photo_ref(filename,alt=''):return dict(url='[uc_local]'+filename,id='',size='',alt=alt,source='library')


def hero():
    h=clone('221ccbe','Conference hero',_element_id='conference-hero',html_tag='section',
        padding_tablet=dims(40,24),padding_mobile=dims(30,20),background_video_fallback=dict(url='',id=''))
    frame=find(h,'692d33e');frame['settings'].update(flex_direction_tablet='column',flex_direction_mobile='column',flex_gap=gap(32))
    find(h,'64afb0d3')['settings'].update(**widths(48),flex_gap=gap(16))
    find(h,'465ad046')['settings'].update(**widths(48),padding=dims(0),flex_gap=gap(14))
    eyebrow=find(h,'3f6c8a0f')['settings'];eyebrow['icon_list'][0]['text']=CONTENT['hero']['eyebrow']
    eyebrow.update(text_color=C['graphite'],**font('icon_typography',12,'500',1.5))
    find(h,'48e735ea')['settings'].update(title='Conference application support',header_size='p',_margin=dims(0),**font(n=16,weight='500'))
    new=animated('70013b0a','Conference H1',CONTENT['hero']['before'],CONTENT['hero']['highlighted'],CONTENT['hero']['after'],44,'h1')
    find(h,'70013b0a')['settings']=new['settings']
    find(h,'73d1f181')['settings'].update(editor='<p><strong>'+html.escape(CONTENT['hero']['supporting_line'])+'</strong></p><p>'+html.escape(CONTENT['hero']['description'])+'</p>',
        text_color=C['graphite'],**font(n=15))
    for id_,label,title,secondary in [('3a7bc335','Discuss conference requirements',CONTENT['hero']['primary_cta'],False),('7507376c','Send conference brief',CONTENT['hero']['secondary_cta'],True)]:
        find(h,id_)['settings']=button(label,title,secondary=secondary)['settings']
    find(h,'7a54daa5')['settings'].update(flex_wrap='wrap',flex_direction_tablet='row',flex_gap=gap(14))
    image=find(h,'6148df6a')['settings'];image.update(image=photo_ref(CONTENT['project']['photo'],CONTENT['project']['alt']),image_size='full',
        width=size(100,'%'),height=size(355),height_mobile=size(245),image_border_radius=dims(18),**{'object-fit':'cover'})
    helper=find(h,'16d20e40');helper.clear();helper.update(bullets('Conference service points',CONTENT['hero']['points']))
    authority=find(h,'27e60217');authority['elements']=[find(h,'7e501868')]
    for key in list(authority['settings']):
        if key=='container_type' or key.startswith('grid_'):authority['settings'].pop(key)
    authority['settings'].update(flex_direction='row',flex_justify_content='center',width_mobile=size(100,'%'))
    find(h,'7e501868')['settings'].update(width=size(130),image_size='full')
    return h


def clients():
    c=clone('1cfd467c','Approved business clients',_element_id='conference-clients',html_tag='section',padding=dims(26,24))
    inner=find(c,'684c3239');inner['settings'].update(content_width='full',padding=dims(0),flex_gap=gap(16))
    inner['elements'].insert(0,heading('Business clients heading',CONTENT['clients_heading'],18,'h2',C['bg']))
    find(c,'66f03b09')['settings'].update(autoplay='no',speed=500)
    return c


def classification():
    data=CONTENT['classification']
    tabs=clone('3862e690','Conference classification review',children=[],tabs_direction_mobile='block-start',
        tabs_width=size(28,'%'),tabs_width_tablet=size(31,'%'),title_text_color=C['graphite'],title_text_color_hover=C['bg'],title_text_color_active=C['bg'],
        title_typography_font_size_mobile=size(13))
    old_item=tabs['settings']['tabs'][0];tabs['settings']['tabs']=[]
    for i,item in enumerate(data['tabs']):
        entry=copy.deepcopy(old_item);entry['tab_title']=item['label'];tabs['settings']['tabs'].append(entry)
        child=clone('54437e','Conference classification panel '+str(i))
        find(child,'268dd126')['settings'].update(title=item['title'])
        find(child,'188c7bda')['settings'].update(title=item['code'],header_size='p',title_color=C['graphite'])
        find(child,'3b77dcc7')['settings'].update(editor='<p>'+html.escape(item['description'])+'</p>',text_color=C['graphite'],**font(n=15))
        for id_,value in zip(('5f84ea8b','70f8ddd4','71a4f5ce','238c827d'),item['tags']):
            find(child,id_)['settings']['icon_list'][0]['text']=value
            find(child,id_)['settings'].update(text_color=C['graphite'])
        find(child,'1fe458ae')['settings'].update(title=item['caption'],title_color=C['graphite'])
        find(child,'454ec936')['settings']=bullets('Classification checklist '+str(i),item['points'])['settings']
        find(child,'2fdd5ad4')['settings'].update(background_image=photo_ref(item['photo'],item['alt']),min_height=size(220),width_mobile=size(100,'%'))
        find(child,'744a2b65')['settings'].update(flex_direction_mobile='column',flex_gap=gap(20))
        find(child,'542afc0f')['settings']=button('Classification contact '+str(i),'Discuss Your Conference Brief',secondary=True)['settings']
        tabs['elements'].append(child)
    return section('Conference support needs','conference-classification',[
        heading('Classification eyebrow',data['eyebrow'],13,'p',C['graphite']),
        animated('71a71a84','Classification H2',data['before'],data['highlighted'],data['after'],38),
        text('Classification introduction',data['intro']),tabs])


def preparation():
    return section('Conference application preparation','conference-prepare',[
        heading('Preparation heading',CONTENT['prepare_heading']),text('Preparation introduction',CONTENT['prepare_intro']),
        row('Six application preparation cards',[card('Preparation '+str(i),d['title'],d['description'],d['icon']) for i,d in enumerate(CONTENT['prepare'])])])


def scope():
    scope=clone('4b2d78e','Conference service scope panel')
    intro=find(scope,'311f1306');intro['elements']=[heading('Scope heading',CONTENT['scope_heading'],29,color=C['white']),text('Scope introduction',CONTENT['scope_intro'],C['silver'])]
    intro['settings'].update(**widths(30),flex_gap=gap(18))
    find(scope,'714e28bc')['settings'].update(**widths(27),min_height=size(300),min_height_mobile=size(220))
    find(scope,'d5cfe00')['settings'].update(**widths(38))
    find(scope,'2d368439')['settings'].update(flex_direction_tablet='column',flex_gap=gap(24),flex_justify_content='space-between')
    acc=find(scope,'7026dcae')
    for i,(entry,child,content) in enumerate(zip(acc['settings']['items'],acc['elements'],CONTENT['scope']),1):
        entry['item_title']=f"{i:02d}  "+content['title']
        child['elements'][0]['settings'].update(editor='<p>'+html.escape(content['answer'])+'</p>',text_color=C['silver'])
    return section('Conference permit service scope','conference-scope',[scope])


def fees():
    cards=[card('Conference fee '+str(i),d['title'],d['description'],d['icon']) for i,d in enumerate(CONTENT['fees'])]
    return section('Conference permit fees and timelines','conference-fees',[
        heading('Conference fee heading',CONTENT['fees_heading']),row('Conference fee comparison',cards),
        text('Conference fee distinction',CONTENT['fees_note'],n=14),
        button('Official government fee source','Check Official SCEGA Fees',CONTENT['fees_source_url'],secondary=True)],C['soft'])


def cases():
    return section('International and multi activity conferences','conference-special-cases',[
        heading('Special cases heading',CONTENT['cases_heading']),
        row('Four conference considerations',[card('Conference consideration '+str(i),d['title'],d['description'],d['icon'],23.5) for i,d in enumerate(CONTENT['cases'])])])


def why():
    about=clone('39fddc8a','Why SYNC for conferences',_element_id='conference-why-sync',html_tag='section')
    find(about,'3914c15d')['settings'].update(background_position='center right',background_size='cover')
    find(about,'636a0013')['settings'].update(title=CONTENT['why']['eyebrow'],header_size='p',**font(n=13,weight='500'))
    find(about,'1afddeeb')['settings']=animated('1afddeeb','Why SYNC H2',CONTENT['why']['before'],CONTENT['why']['highlighted'],CONTENT['why']['after'],36)['settings']
    find(about,'2fe4a827')['settings'].update(editor='<p>'+html.escape(CONTENT['why']['description'])+'</p>',text_color=C['graphite'],**font(n=15))
    find(about,'2b783e98')['settings'].update(ending_number=15,suffix='',number_color=C['white'],_margin=dims(0),
        **font('number_typography',56,'600',1.1),number_typography_font_size_mobile=size(44))
    find(about,'245b311f')['settings'].update(title='+',header_size='span',title_color=C['lavender'])
    find(about,'4c67d1c8')['settings'].update(title_text=CONTENT['why']['experience_title'],description_text=CONTENT['why']['experience_description'],
        title_color=C['white'],description_color=C['silver'])
    find(about,'2046e656')['settings'].update(title_color=C['bg'],description_color=C['graphite'],primary_color=C['purple'])
    find(about,'51f0bbaa')['settings'].update(editor='<p>'+html.escape(CONTENT['why']['options_intro'])+'</p>',text_color=C['graphite'],**font(n=15))
    find(about,'3dc91a3b')['settings']=bullets('Conference support scope options',CONTENT['why']['options'],links=[BRIEF]*4)['settings']
    return about


def services():
    section_=clone('21fed003','Conference services beyond the permit',_element_id='conference-services')
    find(section_,'6872b99b')['settings']=heading('Conference complementary services heading',CONTENT['services_heading'])['settings']
    find(section_,'71bf8346')['settings']=text('Conference complementary services intro',CONTENT['services_intro'])['settings']
    cards=find(section_,'6a8400a3')['elements']
    for i,(e,d) in enumerate(zip(cards,CONTENT['services'])):
        e['settings'].update(_title=d['title'],**widths(32 if i<3 else 49,48,100))
        image,copy_=e['elements'];image['settings'].update(background_image=photo_ref(d['photo'],d['alt']),min_height=size(205),min_height_mobile=size(210))
        title,description,cta=copy_['elements']
        title['settings'].update(title=d['title'],header_size='h3')
        description['settings'].update(editor='<p>'+html.escape(d['description'])+'</p>')
        cta['settings']=button('Service '+str(i)+' action',d['cta'],d['url'],secondary=True,dark=False)['settings']
        # Retain the parent's dark cards and their readable copy.
        for n in (title,description):
            n['settings']['title_color' if n.get('widgetType')=='heading' else 'text_color']=C['white'] if n.get('widgetType')=='heading' else C['silver']
        cta['settings']['button_text_color']=C['lavender']
    find(section_,'6a8400a3')['settings'].update(flex_wrap='wrap',flex_gap=gap(20),flex_direction_mobile='column')
    return section_


def project():
    p=clone('762cbd4','Relevant conference experience',_element_id='conference-experience',html_tag='section')
    item=find(p,'79630469');item['settings'].update(background_image=photo_ref(CONTENT['project']['photo'],CONTENT['project']['alt']),
        link=dict(url=CONTENT['project']['url'],is_external='',nofollow='',custom_attributes=''),min_height=size(450),min_height_mobile=size(340))
    find(p,'6ed37e1d')['elements']=[item]
    find(p,'4aac13f0')['settings']['link']=dict(url=CONTENT['project']['url'],is_external='',nofollow='',custom_attributes='')
    find(p,'7eca45f1')['settings'].update(title_text=CONTENT['project']['title'],description_text='Conference permit coordination, registration, operations and guest support.',
        title_color=C['white'],description_color=C['white'])
    find(p,'5b07635a')['settings'].update(title=CONTENT['project']['eyebrow'],header_size='p',title_color=C['lavender'],**font(n=13,weight='500'))
    find(p,'5055e63c')['settings']=animated('5055e63c','Conference experience H2',CONTENT['project']['before'],CONTENT['project']['highlighted'],CONTENT['project']['after'],36,dark=True)['settings']
    find(p,'d88fcf3')['settings'].update(editor='<p>'+html.escape(CONTENT['project']['description'])+'</p>',text_color=C['silver'],**font(n=15))
    find(p,'1a96ae40')['settings']=bullets('Conference project scope',CONTENT['project']['points'],dark=True)['settings']
    find(p,'7819fd9a')['settings']=button('Conference project details',CONTENT['project']['cta'],CONTENT['project']['url'],secondary=True,dark=True)['settings']
    find(p,'1b27f6ad')['settings'].update(**widths(48))
    find(p,'7d4c51be')['settings'].update(**widths(48),padding=dims(0))
    p['settings'].update(flex_gap=gap(36),padding=dims(55,24),flex_direction_tablet='column',flex_direction_mobile='column')
    return p


def questions_and_brief():
    q=clone('3fae2627','Conference questions and brief',_element_id='conference-questions',html_tag='section')
    find(q,'27f36713')['settings']=heading('Conference FAQ heading',CONTENT['faq_heading'],30,color=C['white'])['settings']
    faq=find(q,'7038ec8a');base=faq['settings']['ekit_accordion_items'][0]
    faq['settings']['ekit_accordion_items']=[]
    for i,d in enumerate(CONTENT['faqs']):
        entry=copy.deepcopy(base);entry.update(acc_title=d['question'],acc_content='<p>'+html.escape(d['answer'])+'</p>',ekit_acc_is_active='yes' if i==0 else '')
        faq['settings']['ekit_accordion_items'].append(entry)
    faq['settings'].update(ekit_accordion_title_color_close=C['lavender'],ekit_accordion_title_margin_bottom=size(0))
    faqcol=find(q,'3164a9f0');faqcol['settings'].update(**widths(57),padding=dims(0))
    formcol=find(q,'59dc9ed7');formcol['settings'].update(**widths(39),_element_id='conference-brief',flex_align_items='stretch',flex_gap=gap(18))
    find(q,'3563fb4c')['settings'].update(title_text=CONTENT['brief_heading'],title_size='h2',description_text=CONTENT['brief_intro'],
        title_color=C['white'],description_color=C['silver'],**font('title_typography',28,'600',1.25))
    existing=json.loads((ROOT.parent/'scega-conference-native/SYNCs-SCEGA-Conference-Native-Page.json').read_text())
    form=copy.deepcopy(next(e for e in walk(existing['content']) if e.get('widgetType')=='form'))
    form['settings'].update(_title='Self contained conference brief',form_name='SYNC Conference Service 6988 Brief',field_border_color=C['purple'])
    support=next(f for f in form['settings']['form_fields'] if f['custom_id']=='support')
    support['field_options']='Select support|\n'+'\n'.join(title+'|'+value for title,value in zip(CONTENT['why']['options'],['permit_only','conference_delivery','sponsor_booths','registration_guests']))
    formcol['elements']=[find(q,'3563fb4c'),form]
    find(q,'5edbf30e')['settings'].update(flex_gap=gap(34),flex_justify_content='space-between')
    return q


def guides():
    g=clone('75f7edd7','Conference permit planning guides',_element_id='conference-guides',html_tag='section',
        content_width='boxed',boxed_width=size(1280),padding=dims(48,24),padding_mobile=dims(30,20),background_background='classic',background_color=C['gray'],flex_gap=gap(24))
    find(g,'4658ec82')['settings']=heading('Conference guides heading',CONTENT['guides_heading'])['settings']
    g['elements'].insert(1,text('Conference guides introduction',CONTENT['guides_intro']))
    posts=find(g,'2c1b8ce8')['settings']
    posts.update(posts_post_type='by_id',posts_posts_ids=[str(v) for v in CONTENT['guide_post_ids']],posts_include=[],posts_include_term_ids=[],
        posts_select_date='anytime',cards_posts_per_page=3,cards_columns='3',cards_columns_tablet='2',cards_columns_mobile='1',
        posts_orderby='post_date',posts_order='desc',cards_masonry='',pagination_type='',cards_title_color=C['bg'],cards_read_more_color=C['graphite'],
        **font('cards_title_typography',18,'600',1.4))
    for key in ('posts_date_before','posts_date_after'):posts.pop(key,None)
    return g


def final_cta():
    c=clone('2767adb5','Conference final CTA',_element_id='conference-final-cta',html_tag='section')
    h=find(c,'7b68c740')['settings'];h.update(ekit_heading_title=CONTENT['cta_heading'],ekit_heading_use_title_text_fill='',ekit_heading_title_color=C['bg'])
    h.update(ekit_heading_sub_title='',shadow_text_content='',ha_advanced_tooltip_content='')
    h['ekit_heading_seperator_image']=dict(url='',id='')
    inner=find(c,'791f2d26');inner['elements']=[find(c,'7b68c740'),text('Final conference CTA introduction',CONTENT['cta_description']),
        row('Final conference actions',[button('Final conference brief','Send Your Conference Brief'),button('Conference WhatsApp','Discuss on WhatsApp',CONTENT['whatsapp_url'],secondary=True)])]
    return c


def assign_ids(elements,path=''):
    for i,e in enumerate(elements):
        address=path+'/'+str(i)+'/'+e['id'];e['id']=hashlib.sha256(('conference-6988'+address).encode()).hexdigest()[:8]
        s=e['settings']
        for key in list(s):
            if key.startswith(('motion_fx_', '_transform_')) or key in {'sticky','sticky_parent','sticky_on','sticky_offset'}:s.pop(key)
        s['_animation']='none'
        for key in ('tabs','items','icon_list','ekit_accordion_items','form_fields'):
            for j,entry in enumerate(s.get(key,[])):entry['_id']=hashlib.sha256((address+key+str(j)).encode()).hexdigest()[:8]
        assign_ids(e.get('elements',[]),address)


def resolve_media(value,missing):
    if isinstance(value,dict):
        for key,v in value.items():
            if key=='url' and isinstance(v,str) and v.startswith('[uc_local]'):
                name=v[len('[uc_local]'):]
                if name in MEDIA:value[key]=MEDIA[name]
                else:missing.add(name)
            else:resolve_media(v,missing)
    elif isinstance(value,list):
        for v in value:resolve_media(v,missing)


def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    sections=[hero(),clients(),classification(),preparation(),scope(),fees(),cases(),why(),services(),project(),questions_and_brief(),guides(),final_cta()]
    assign_ids(sections)
    page=dict(version='0.4',title='SYNC — Conference Permit Service — Based on Template 6988',type='page',page_settings=[],content=sections)
    missing=set();resolve_media(page,missing)
    filename=('DRAFT-' if missing else '')+'SYNCs-Conference-Service-6988.json'
    save(ROOT/filename,page)
    draft=ROOT/'DRAFT-SYNCs-Conference-Service-6988.json'
    if not missing and draft.exists():draft.unlink()
    (ROOT/'sections').mkdir(exist_ok=True)
    records=[]
    for i,e in enumerate(page['content'],1):
        name=f"{i:02d}-"+e['settings']['_element_id']+'.json'
        save(ROOT/'sections'/name,dict(version='0.4',title='SYNC — '+e['settings']['_title'],type='container',page_settings=[],content=[e]))
        records.append(dict(file='sections/'+name,anchor=e['settings']['_element_id'],label=e['settings']['_title']))
    save(ROOT/'validation/manifest.json',dict(page=filename,source_archive=ARCHIVE.name,source_sha256=hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
        source_template='elementor-6988-2026-10-25.json',sections=records,content_blocks=14,top_level_sections=13,elements=len(list(walk(page['content']))),
        missing_original_media_urls=sorted(missing),ready_for_media_import=not missing,
        status='WordPress import/edit/re-export unavailable; original same-site media URLs pending' if missing else 'Native saved template; WordPress staging import pending'))
    print(json.dumps(dict(page=filename,sections=13,elements=len(list(walk(page['content'])))),ensure_ascii=False))
    print(json.dumps(dict(missing_original_media_urls=sorted(missing)),ensure_ascii=False))


if __name__=='__main__':main()
