"""Solid-background text/icon contrast, including native interactive states."""
import json
from build import ROOT, PAGE, C


def luminance(color):
    rgb = [int(color[i:i+2], 16)/255 for i in (1, 3, 5)]
    linear = [v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    return sum(v*w for v, w in zip(linear, (.2126,.7152,.0722)))


checks=[]
def check(label, state, fg, bg, minimum=4.5):
    a,b=sorted((luminance(fg),luminance(bg)))
    value=(b+.05)/(a+.05)
    row=dict(element=label,state=state,foreground=fg,background=bg,ratio=round(value,2),minimum=minimum)
    checks.append(row)
    assert value>=minimum,row


def walk(es, surface):
    for e in es:
        s=e['settings'];kind=e.get('widgetType');label=s['_title']
        bg=s.get('background_color',surface) if e['elType']=='container' else surface
        if kind=='heading':check(label,'heading',s['title_color'],bg)
        elif kind=='text-editor':check(label,'body',s['text_color'],bg)
        elif kind=='button':
            normal=bg if s['background_color'].endswith('00') else s['background_color']
            check(label,'button',s['button_text_color'],normal)
            check(label,'button hover',s['hover_color'],s['button_background_hover_color'])
        elif kind=='icon-box':
            check(label,'title',s['title_color'],bg)
            if s['description_text']:check(label,'description',s['description_color'],bg)
            check(label,'icon',s['primary_color'],bg,3)
        elif kind=='icon-list':
            check(label,'list',s['text_color'],bg)
            check(label,'list hover',s['text_color_hover'],bg)
            if any(i['selected_icon']['value'] for i in s['icon_list']):check(label,'list icon',s['icon_color'],bg,3)
        elif kind=='nested-accordion':
            for state in ('normal','hover','active'):
                check(label,'accordion '+state,s[state+'_title_color'],s['accordion_background_'+state+'_color'])
                check(label,'accordion icon '+state,s[state+'_icon_color'],s['accordion_background_'+state+'_color'],3)
        elif kind=='form':
            check(label,'label',s['label_color'],bg)
            check(label,'field',s['field_text_color'],s['field_background_color'])
            check(label,'submit',s['button_text_color'],s['button_background_color'])
            check(label,'submit hover',s['button_hover_color'],s['button_background_hover_color'])
        elif kind=='posts':
            postbg=s['classic_box_bg_color']
            for part in ('title','excerpt','read_more'):check(label,'dynamic '+part,s['classic_'+part+'_color'],postbg)
        walk(e['elements'],bg)


page=json.loads((ROOT/PAGE).read_text())
walk(page['content'],C['bg'])
report={'passed':True,'checks':len(checks),'minimum_text_ratio':min(x['ratio'] for x in checks if x['minimum']==4.5),
        'minimum_icon_ratio':min(x['ratio'] for x in checks if x['minimum']==3),'results':checks,
        'limits':'Explicit solid colors only; native theme focus, placeholders, real photos and frontend require staging.'}
(ROOT/'validation/contrast.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='results'}))
