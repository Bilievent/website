"""Internal visual harness from native controls; never shipped as page code."""
import base64
import html
import json
from pathlib import Path

from build_page import ROOT

rules = []


def scalar(v):
    return str(v["size"]) + v.get("unit", "px")


def dims(v):
    return ' '.join(str(v[k]) + v.get("unit", "px") for k in ("top", "right", "bottom", "left"))


def font(s, p="typography"):
    result = []
    for key, prop in (("font_size", "font-size"), ("font_weight", "font-weight"), ("line_height", "line-height"), ("letter_spacing", "letter-spacing")):
        v = s.get(p + "_" + key)
        if v is not None:
            result.append(prop + ':' + (scalar(v) if isinstance(v, dict) else str(v)))
    result.append('font-family:"Manrope",Arial,sans-serif')
    return result


def add(selector, props, media=None):
    if not props:
        return
    rule = selector + '{' + ';'.join(props) + '}'
    rules.append('@media(max-width:' + str(media) + 'px){' + rule + '}' if media else rule)


def responsive(settings, suffix):
    result = dict(settings)
    if suffix:
        for device in ('tablet', 'mobile'):
            for key, value in settings.items():
                if key.endswith('_' + device):
                    result[key[:-len(device)-1]] = value
            if suffix == device:
                break
    return result


def style(element):
    target = '[data-id="' + element['id'] + '"]'
    for suffix, media in (('', None), ('tablet', 1024), ('mobile', 767)):
        s = responsive(element['settings'], suffix)
        css = []
        for key, prop in (('padding', 'padding'), ('_padding', 'padding'), ('border_radius', 'border-radius')):
            if key in s:
                css.append(prop + ':' + dims(s[key]))
        if element['elType'] == 'container':
            for key, prop in (('width', 'width'), ('min_height', 'min-height')):
                if key in s:
                    css.append(prop + ':' + scalar(s[key]))
            for key, prop in (('flex_direction', 'flex-direction'), ('flex_wrap', 'flex-wrap'), ('flex_align_items', 'align-items'),
                              ('flex_justify_content', 'justify-content'), ('overflow', 'overflow'), ('background_color', 'background-color')):
                if key in s:
                    css.append(prop + ':' + str(s[key]))
            css.append('gap:' + str(s.get('flex_gap', {}).get('size', 0)) + 'px')
            if s.get('border_border'):
                css += ['border-style:' + s['border_border'], 'border-width:' + dims(s['border_width']), 'border-color:' + s['border_color']]
            if s.get('_flex_order'):
                css.append('order:' + ('99' if s['_flex_order'] == 'end' else '-1'))
            if s.get('background_image'):
                css += ['background-image:url("' + s['background_image']['url'] + '")', 'background-size:' + s['background_size'], 'background-position:' + s['background_position']]
            add(target, css, media)
            if s.get('content_width') == 'boxed':
                add(target + '>.e-con-inner', ['max-width:' + scalar(s['boxed_width'])], media)
            continue
        if s.get('_element_width') == 'auto':
            css.append('width:auto')
        add(target, css, media)
        kind = element['widgetType']
        if kind == 'heading':
            add(target + ' .elementor-heading-title', font(s) + ['color:' + s['title_color'], 'text-align:' + s.get('align', 'left')], media)
        elif kind == 'text-editor':
            add(target, font(s) + ['color:' + s['text_color']], media)
        elif kind == 'button':
            add(target, ['text-align:' + s.get('align', 'left')], media)
            add(target + ' .elementor-button', font(s) + ['background:' + s['background_color'], 'color:' + s['button_text_color'],
                'padding:' + dims(s['text_padding']), 'border:1px solid ' + s['border_color'], 'border-radius:' + dims(s['border_radius'])], media)
            add(target + ' .elementor-button:hover,' + target + ' .elementor-button:focus', ['background:' + s['button_background_hover_color'], 'color:' + s['hover_color']], media)
        elif kind == 'icon-list':
            add(target + ' .elementor-icon-list-item', font(s, 'icon_typography') + ['color:' + s['text_color']], media)
            add(target + ' .elementor-icon-list-item a', ['color:' + s['text_color']], media)
            add(target + ' .elementor-icon-list-item a:hover', ['color:' + s['text_color_hover']], media)
            add(target + ' .native-icon', ['color:' + s['icon_color']], media)
            space = s['space_between']['size']
            add(target + ' .elementor-icon-list-items', ['gap:' + str(space) + 'px'], media)
        elif kind == 'icon-box':
            add(target + ' .ibox', ['flex-direction:' + ('row' if s['position'] == 'left' else 'column'), 'text-align:' + s['text_align'], 'gap:' + scalar(s['icon_space'])], media)
            add(target + ' .ibox-icon', ['font-size:' + scalar(s['icon_size']), 'color:' + s['primary_color']], media)
            add(target + ' .ibox-title', font(s, 'title_typography') + ['color:' + s['title_color'], 'margin-bottom:' + scalar(s['title_bottom_space'])], media)
            add(target + ' .ibox-description', font(s, 'description_typography') + ['color:' + s['description_color']], media)
        elif kind == 'nested-tabs':
            mobile = s.get('tabs_direction') == 'block-start'
            add(target + '>.e-n-tabs', ['flex-direction:' + ('column' if mobile else 'row'), 'gap:16px'], media)
            add(target + ' .e-n-tabs-heading', ['width:' + ('100%' if mobile else scalar(s['tabs_width'])), 'flex-direction:' + ('row' if mobile else 'column'), 'flex-wrap:wrap', 'gap:8px'], media)
            add(target + ' .e-n-tab-title', font(s, 'title_typography') + ['padding:' + dims(s['padding']), 'border:1px solid ' + s['tabs_title_border_color'],
                'border-radius:' + dims(s['tabs_title_border_radius']), 'background:' + s['tabs_title_background_color_color'], 'color:' + s['title_text_color'], 'text-align:left'], media)
            add(target + ' .e-n-tab-title[aria-selected="true"]', ['background:' + s['tabs_title_background_color_active_color'], 'color:' + s['title_text_color_active']], media)
        elif kind == 'nested-accordion':
            add(target + ' .e-n-accordion', ['display:flex', 'flex-direction:column', 'gap:' + scalar(s['accordion_item_title_space_between'])], media)
            add(target + ' summary', font(s, 'title_typography') + ['padding:' + dims(s['accordion_padding']), 'background:' + s['accordion_background_normal_color'],
                'color:' + s['normal_title_color'], 'border:1px solid ' + s['accordion_border_normal_color'], 'border-radius:' + dims(s['accordion_border_radius'])], media)
            add(target + ' details[open] summary', ['color:' + s['active_title_color'], 'border-color:' + s['accordion_border_active_color']], media)
        elif kind == 'form':
            add(target + ' .fields', ['margin-inline:-' + str(s['column_gap']['size'] / 2) + 'px'], media)
            add(target + ' .field', ['padding-inline:' + str(s['column_gap']['size'] / 2) + 'px', 'margin-bottom:' + scalar(s['row_gap'])], media)
            add(target + ' label', font(s, 'label_typography') + ['color:' + s['label_color'], 'margin-bottom:' + scalar(s['label_spacing'])], media)
            add(target + ' input,' + target + ' select', font(s, 'field_typography') + ['color:' + s['field_text_color'], 'background:' + s['field_background_color'],
                'border:1px solid ' + s['field_border_color'], 'border-radius:' + dims(s['field_border_radius']), 'min-height:46px', 'padding:11px 14px'], media)
            add(target + ' button[type=submit]', font(s, 'button_typography') + ['padding:' + dims(s['button_text_padding']), 'border:0', 'border-radius:' + dims(s['button_border_radius']),
                'background:' + s['button_background_color'], 'color:' + s['button_text_color']], media)
            add(target + ' button[type=submit]:hover', ['background:' + s['button_background_hover_color'], 'color:' + s['button_hover_color']], media)
            for field in s['form_fields']:
                field_width = field.get('width_' + suffix, field['width']) if suffix else field['width']
                add(target + ' .field-' + field['custom_id'], ['width:' + field_width + '%'], media)


def render(element):
    style(element)
    s = element['settings']
    attrs = ' data-id="' + element['id'] + '"'
    if s.get('_element_id'):
        attrs += ' id="' + s['_element_id'] + '"'
    if element['elType'] == 'container':
        tag = s.get('html_tag', 'div')
        body = ''.join(render(e) for e in element['elements'])
        if s.get('background_image'):
            body = ('<span aria-hidden="true" class="qa-photo-note">SYNC site photo</span>' if not body else '') + body
        if s.get('content_width') == 'boxed':
            body = '<div class="e-con-inner">' + body + '</div>'
        return '<' + tag + attrs + ' class="e-con">' + body + '</' + tag + '>'
    kind = element['widgetType']
    if kind == 'heading':
        tag = s['header_size']; body = '<' + tag + ' class="elementor-heading-title">' + html.escape(s['title']) + '</' + tag + '>'
    elif kind == 'text-editor':
        body = s['editor']
    elif kind == 'button':
        body = '<a class="elementor-button" href="' + html.escape(s['link']['url']) + '">' + html.escape(s['text']) + (' <span aria-hidden="true">→</span>' if s['selected_icon']['value'] else '') + '</a>'
    elif kind == 'icon-list':
        parts = []
        for item in s['icon_list']:
            text = ('<span class="native-icon" aria-hidden="true">✓</span>' if item['selected_icon']['value'] else '') + html.escape(item['text'])
            if item.get('link'):
                text = '<a href="' + html.escape(item['link']['url']) + '">' + text + '</a>'
            parts.append('<li class="elementor-icon-list-item">' + text + '</li>')
        body = '<ul class="elementor-icon-list-items' + (' inline-items' if s['view'] == 'inline' else '') + '">' + ''.join(parts) + '</ul>'
    elif kind == 'icon-box':
        body = '<div class="ibox"><span aria-hidden="true" class="ibox-icon">◇</span><div><h3 class="ibox-title">' + html.escape(s['title_text']) + '</h3><p class="ibox-description">' + html.escape(s['description_text']) + '</p></div></div>'
    elif kind == 'nested-tabs':
        buttons, panels = [], []
        for i, (item, child) in enumerate(zip(s['tabs'], element['elements'])):
            panelid = 'qa-panel-' + element['id'] + '-' + str(i)
            buttons.append('<button type="button" class="e-n-tab-title" role="tab" aria-selected="' + ('true' if i == 0 else 'false') + '" aria-controls="' + panelid + '" tabindex="' + ('0' if i == 0 else '-1') + '">' + html.escape(item['tab_title']) + '</button>')
            panels.append('<div id="' + panelid + '" class="qa-tab-panel" role="tabpanel"' + (' hidden' if i else '') + '>' + render(child) + '</div>')
        body = '<div class="e-n-tabs"><div class="e-n-tabs-heading" role="tablist">' + ''.join(buttons) + '</div><div class="e-n-tabs-content">' + ''.join(panels) + '</div></div>'
    elif kind == 'nested-accordion':
        parts = []
        for item, child in zip(s['items'], element['elements']):
            parts.append('<details name="' + element['id'] + '"><summary>' + html.escape(item['item_title']) + '<span aria-hidden="true">⌄</span></summary>' + render(child) + '</details>')
        body = '<div class="e-n-accordion">' + ''.join(parts) + '</div>'
    elif kind == 'form':
        fields = []
        for item in s['form_fields']:
            key = item['custom_id']; required = ' required' if item['required'] == 'true' else ''
            label = '<label for="qa-' + key + '">' + html.escape(item['field_label']) + '</label>'
            if item['field_type'] == 'select':
                options = ''.join('<option value="' + html.escape(line.split('|', 1)[1]) + '">' + html.escape(line.split('|', 1)[0]) + '</option>' for line in item['field_options'].splitlines())
                control = '<select id="qa-' + key + '" name="' + key + '"' + required + '>' + options + '</select>'
            else:
                control = '<input id="qa-' + key + '" type="' + item['field_type'] + '" placeholder="' + html.escape(item['placeholder']) + '" name="' + key + '"' + required + '>'
            fields.append('<div class="field field-' + key + '">' + label + control + '</div>')
        body = '<form aria-label="SYNC SCEGA Event Brief"><div class="fields">' + ''.join(fields) + '</div><button type="submit">' + html.escape(s['button_text']) + ' →</button></form>'
    else:
        raise ValueError(kind)
    return '<div' + attrs + ' class="elementor-widget elementor-widget-' + kind + '">' + body + '</div>'


base = '''*{box-sizing:border-box}body{margin:0;background:#1D162A;font:15px/1.6 Manrope,Arial,sans-serif}.e-con{display:flex;flex-direction:column;flex-shrink:1;width:100%;min-width:0}.e-con-inner{display:flex;flex-direction:inherit;justify-content:inherit;align-items:inherit;flex-wrap:inherit;gap:inherit;width:100%;min-width:0;margin-inline:auto}.elementor-widget{position:relative;width:100%;min-width:0}h1,h2,h3,p{padding:0;margin:0}.elementor-button{display:inline-flex;align-items:center;justify-content:center;gap:12px;text-decoration:none}.elementor-icon-list-items{list-style:none;display:flex;flex-direction:column;margin:0;padding:0}.inline-items{flex-direction:row;flex-wrap:wrap}.elementor-icon-list-item{min-width:0}.elementor-icon-list-item a{text-decoration:none}.native-icon{margin-right:8px}.ibox{display:flex}.ibox-icon{line-height:1.2;flex-shrink:0}.e-n-tabs{display:flex;min-width:0}.e-n-tabs-heading{display:flex;flex-shrink:0;min-width:0}.e-n-tab-title{cursor:pointer;max-width:100%}.e-n-tabs-content{flex:1;min-width:0}.qa-tab-panel[hidden]{display:none}summary{display:flex;justify-content:space-between;align-items:center;gap:12px;cursor:pointer;list-style:none}summary::-webkit-details-marker{display:none}.fields{display:flex;flex-wrap:wrap}label{display:block}input,select{display:block;width:100%;max-width:100%}button[type=submit]{width:100%;cursor:pointer}.qa-photo-note{margin:auto;color:#C9BCE3;font-size:11px;text-align:center}button:focus-visible,a:focus-visible,summary:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #C9BCE3;outline-offset:4px}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}'''
script = '''document.querySelectorAll('.e-n-tabs').forEach(root=>{const buttons=[...root.querySelectorAll('[role=tab]')];function activate(button){buttons.forEach(b=>{const active=b===button;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;document.getElementById(b.getAttribute('aria-controls')).hidden=!active})}buttons.forEach((b,i)=>{b.addEventListener('click',()=>activate(b));b.addEventListener('keydown',e=>{let n=i;if(['ArrowDown','ArrowRight'].includes(e.key))n=(i+1)%buttons.length;else if(['ArrowUp','ArrowLeft'].includes(e.key))n=(i-1+buttons.length)%buttons.length;else if(e.key==='Home')n=0;else if(e.key==='End')n=buttons.length-1;else return;e.preventDefault();activate(buttons[n]);buttons[n].focus()})})});document.querySelector('form').addEventListener('submit',e=>{e.preventDefault();window.__qaSubmitPrevented=(window.__qaSubmitPrevented||0)+1});'''
document = json.loads((ROOT / 'SYNCs-SCEGA-Complete-Page.json').read_text())
body = render(document['content'][0])
fontfile = Path('/tmp/syncs-manrope-variable.ttf')
face = '@font-face{font-family:Manrope;font-style:normal;font-weight:200 800;src:url(data:font/ttf;base64,' + base64.b64encode(fontfile.read_bytes()).decode() + ') format("truetype")}' if fontfile.exists() else ''
page = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Internal SCEGA native-settings review</title><style>' + face + base + ''.join(rules) + '</style><body>' + body + '<script>' + script + '</script></body></html>'
Path('/tmp/syncs-scega-native-review.html').write_text(page)
print('Built independent native-settings review in /tmp. Preview HTML/CSS/JS is NOT in the templates or ZIP.')
