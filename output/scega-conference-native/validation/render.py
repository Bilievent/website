"""Independent preview of native controls; no generated frontend enters the templates."""
import html
import json
import re
from pathlib import Path
from build import ROOT, PAGE

old = (ROOT.parent / 'scega-permit-native/validation/render_review.py').read_text()
prefix = old.split('\nbase = ', 1)[0].replace('from build_page import ROOT', 'ROOT = Path(' + repr(str(ROOT)) + ')')
ns = {}
exec(compile(prefix, '<existing-native-layout-review>', 'exec'), ns)
original_render = ns['render']


def icon(value):
    name = value.replace('fas fa-', '')
    source = Path('/tmp/syncs-conference-icons') / (name + '.svg')
    if source.exists():
        return re.sub(r'<svg\b', '<svg aria-hidden="true" fill="currentColor"', source.read_text(), count=1)
    return '◇'


def render(element):
    kind, s = element.get('widgetType'), element['settings']
    target = '[data-id="' + element['id'] + '"]'
    if kind not in {'image', 'posts', 'form', 'nested-accordion', 'icon-box', 'icon-list'}:
        return original_render(element)
    if kind == 'icon-box':
        return original_render(element).replace('◇', icon(s['selected_icon']['value']))
    if kind == 'icon-list':
        result = original_render(element)
        for item in s['icon_list']:
            if item['selected_icon']['value']:
                result = result.replace('✓</span>', icon(item['selected_icon']['value']) + '</span>', 1)
        return result
    ns['style'](element)
    attrs = ' data-id="' + element['id'] + '" class="elementor-widget elementor-widget-' + kind + '"'
    if kind == 'image':
        for device, media in (('', None), ('tablet', 1024), ('mobile', 767)):
            settings = ns['responsive'](s, device)
            ns['add'](target + ' .native-image-frame', ['height:' + ns['scalar'](settings['height']), 'border-radius:' + ns['dims'](settings['image_border_radius']),
                'border:1px solid ' + settings['image_border_color']], media)
        return '<div' + attrs + '><div class="native-image-frame"><span class="qa-media-label">SYNC conference photo · original URL retained</span><img src="' + html.escape(s['image']['url']) + '" alt="' + html.escape(s['image']['alt']) + '"></div></div>'
    if kind == 'nested-accordion':
        parts = []
        for i, (item, child) in enumerate(zip(s['items'], element['elements'])):
            opened = ' open' if s['default_state'] == 'expanded' and i == 0 else ''
            parts.append('<details name="' + element['id'] + '"' + opened + '><summary>' + html.escape(item['item_title']) + '<span aria-hidden="true">+</span></summary>' + render(child) + '</details>')
        return '<div' + attrs + '><div class="e-n-accordion">' + ''.join(parts) + '</div></div>'
    if kind == 'form':
        fields = []
        for field in s['form_fields']:
            key = field['custom_id']
            required = ' required' if field['required'] == 'true' else ''
            label = '<label for="qa-' + key + '">' + html.escape(field['field_label']) + '</label>'
            if field['field_type'] == 'select':
                options = ''.join('<option value="' + html.escape(line.split('|', 1)[1]) + '">' + html.escape(line.split('|', 1)[0]) + '</option>' for line in field['field_options'].splitlines())
                control = '<select id="qa-' + key + '"' + required + '>' + options + '</select>'
            elif field['field_type'] == 'textarea':
                control = '<textarea id="qa-' + key + '" rows="' + str(field['rows']) + '" placeholder="' + html.escape(field['placeholder']) + '"' + required + '></textarea>'
            else:
                control = '<input id="qa-' + key + '" type="' + field['field_type'] + '" placeholder="' + html.escape(field['placeholder']) + '"' + required + '>'
            fields.append('<div class="field field-' + key + '">' + label + control + '</div>')
        for device, media in (('', None), ('tablet', 1024), ('mobile', 767)):
            settings = ns['responsive'](s, device)
            ns['add'](target + ' textarea', ns['font'](settings, 'field_typography') + ['background:' + settings['field_background_color'], 'color:' + settings['field_text_color'],
                'border:1px solid ' + settings['field_border_color'], 'border-radius:' + ns['dims'](settings['field_border_radius']), 'padding:11px 14px'], media)
        return '<div' + attrs + '><form aria-label="SYNC Conference Permit Brief"><div class="fields">' + ''.join(fields) + '</div><button type="submit">' + html.escape(s['button_text']) + ' →</button></form></div>'
    if kind == 'posts':
        for device, media in (('', None), ('tablet', 1024), ('mobile', 767)):
            settings = ns['responsive'](s, device)
            ns['add'](target + ' .native-posts', ['display:grid', 'grid-template-columns:repeat(' + settings['classic_columns'] + ',minmax(0,1fr))', 'gap:' + ns['scalar'](settings['classic_column_gap'])], media)
            ns['add'](target + ' article', ['background:' + settings['classic_box_bg_color'], 'border-radius:' + ns['scalar'](settings['classic_box_border_radius'])], media)
            ns['add'](target + ' .post-image', ['width:' + ns['scalar'](settings['classic_image_width']), 'margin-right:' + ns['scalar'](settings['classic_image_spacing'])], media)
            ns['add'](target + ' .post-copy', ['padding:' + ns['dims'](settings['classic_content_padding'])], media)
            for tag, prefix, color in [('h3', 'title', 'title_color'), ('p', 'excerpt', 'excerpt_color'), ('a', 'read_more', 'read_more_color')]:
                ns['add'](target + ' ' + tag, ns['font'](settings, 'classic_' + prefix + '_typography') + ['color:' + settings['classic_' + color]], media)
        if s['posts_post_type'] == 'project':
            samples = [('Your latest conference project', 'Featured image, title and summary load from the selected project category on your WordPress site.')]
        else:
            samples = [('Conference Requirements', 'Your latest permit planning article.'), ('Application Corrections', 'Your latest application guidance.'), ('International Organizers', 'Your latest organizer guidance.')]
        cards = ''.join('<article><div class="post-image"><span>Dynamic featured image</span></div><div class="post-copy"><h3>' + title + '</h3><p>' + copy + '</p><a href="#cf-prepare">' + s['classic_read_more_text'] + '</a></div></article>' for title, copy in samples)
        return '<div' + attrs + '><div class="native-posts">' + cards + '</div></div>'
    raise ValueError(kind)


ns['render'] = render
document = json.loads((ROOT / PAGE).read_text())
body = render(document['content'][0])
base = re.search(r"\nbase = '''(.*?)'''\nscript =", old, re.S).group(1)
base += '''svg{display:block;width:1em;height:1em}.native-icon{display:inline-flex;vertical-align:middle}.ibox-description:empty{display:none}.native-image-frame{position:relative;background:#2B203D;overflow:hidden;width:100%}.native-image-frame img{position:relative;display:block;width:100%;height:100%;object-fit:cover}.native-image-frame img:not([data-loaded]){visibility:hidden}.qa-media-label{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:24px;color:#C9BCE3;font-size:12px;text-align:center}textarea{display:block;width:100%;max-width:100%;resize:vertical}input::placeholder,textarea::placeholder{color:#D8D8E0;opacity:1}.native-posts article{display:flex;min-width:0;overflow:hidden}.post-image{background:#3A3447;min-height:140px;flex-shrink:0;display:flex;align-items:center;justify-content:center;color:#C9BCE3;text-align:center;font-size:11px;padding:10px}.post-copy{flex:1;min-width:0}.post-copy p{margin:10px 0}.post-copy a{text-decoration:none}summary span{color:#C9BCE3}details[open]>summary span{font-size:0}details[open]>summary span:after{content:'−';font-size:15px}@media(max-width:767px){.native-posts article{flex-direction:column}.post-image{margin-right:0!important}.post-copy{padding:18px!important}}'''
fontfile = Path('/tmp/syncs-conference-manrope.ttf')
face = ''
if fontfile.exists():
    import base64
    face = '@font-face{font-family:Manrope;font-style:normal;font-weight:200 800;src:url(data:font/ttf;base64,' + base64.b64encode(fontfile.read_bytes()).decode() + ') format("truetype")}'
script = '''document.querySelector('form').addEventListener('submit',e=>{e.preventDefault();window.__prevented=(window.__prevented||0)+1});document.querySelectorAll('.native-image-frame img').forEach(img=>{img.addEventListener('load',()=>img.setAttribute('data-loaded','true'));if(img.complete&&img.naturalWidth)img.setAttribute('data-loaded','true')});'''
output = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Independent native conference layout review</title><style>' + face + base + ''.join(ns['rules']) + '</style><body>' + body + '<script>' + script + '</script></body></html>'
Path('/tmp/syncs-conference-review.html').write_text(output)
print('Built independent control-based review; not a WordPress render or shipped frontend.')
