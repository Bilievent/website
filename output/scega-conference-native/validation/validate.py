"""Validate the native export contract and corroborate new control names."""
import collections
import hashlib
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import urlparse
from build import ROOT, PAGE, C, walk

page = json.loads((ROOT / PAGE).read_text())
nodes = list(walk(page["content"]))
sections = page["content"][0]["elements"]
manifest = json.loads((ROOT / "validation/manifest.json").read_text())
assert page["version"] == "0.4" and page["type"] == "page"
assert len(sections) == 15 and len(nodes) == 213
ids = [e["id"] for e in nodes]
assert len(set(ids)) == len(ids) and all(re.fullmatch(r"[a-f0-9]{8}", i) for i in ids)

with zipfile.ZipFile('/workspace/attachments/dd280ded-925f-445c-a865-7d358661e8a5/sc_elementor_template.zip') as z:
    baseline = json.loads(z.read('elementor-6970-2026-10-21.json'))
source_types = {e.get("widgetType") for e in walk(baseline["content"])}
types = collections.Counter(e.get("widgetType", "container") for e in nodes)
assert set(types) - {"container"} <= source_types | {"form", "nested-accordion"}
assert types["posts"] == 2 and types["form"] == 1 and types["nested-accordion"] == 2
assert not set(types) & {"html", "shortcode", "taxonomy-filter"}
assert len([e for e in nodes if e.get("widgetType") == "heading" and e["settings"]["header_size"] == "h1"]) == 1
anchors = [e["settings"]["_element_id"] for e in nodes if e["settings"].get("_element_id")]
assert len(anchors) == len(set(anchors)) == 16


def leaves(o):
    if isinstance(o, dict):
        for k, v in o.items():
            yield k, v
            yield from leaves(v)
    elif isinstance(o, list):
        for v in o: yield from leaves(v)


known_photos = set()
for document in (baseline, json.loads((ROOT.parent / 'scega-permit-native/SYNCs-SCEGA-Complete-Page.json').read_text())):
    known_photos |= {v for k, v in leaves(document) if k == 'url' and isinstance(v, str) and '/uploads/' in v}
image_urls = []
for k, v in leaves(page):
    assert k not in {"html", "custom_css", "custom_js"}, k
    if isinstance(v, str):
        assert not re.search(r'<(?:script|style|iframe|div|table)\b', v, re.I)
        assert '[uc_local]' not in v and 'Lorem ipsum' not in v and 'globals/colors?' not in v
        if re.fullmatch(r'#[A-Fa-f0-9]{6}(?:[A-Fa-f0-9]{2})?', v): assert v[:7] in C.values(), v
        if k == 'url':
            if v.startswith('#'): assert v[1:] in anchors, v
            elif '/uploads/' in v:
                assert v in known_photos and urlparse(v).hostname == 'syncs.com.sa', v
                image_urls.append(v)
            else: assert v in {'https://syncs.com.sa/contact-us/', 'https://api.whatsapp.com/send/?phone=966565006560'}, v

for section, record in zip(sections, manifest['sections']):
    assert json.loads((ROOT / record['file']).read_text())['content'] == [section]
for path in [ROOT / PAGE] + sorted((ROOT / 'sections').glob('*.json')):
    document = json.loads(path.read_text())
    doc_ids = [e['id'] for e in walk(document['content'])]
    assert len(doc_ids) == len(set(doc_ids))


def schema(name):
    text = Path('/tmp/syncs-conference-' + name + '.php').read_text()
    controls = set(re.findall(r"add_(?:responsive_)?control\(\s*['\"]([^'\"]+)", text))
    groups = set(re.findall(r"['\"]name['\"]\s*=>\s*['\"]([^'\"]+)", text))
    return text, controls, groups


def valid(key, controls, groups):
    key = re.sub(r'_(mobile|tablet)$', '', key)
    return key in controls or any(key.startswith(group + '_') for group in groups)


for kind in ('form', 'image'):
    _, controls, groups = schema(kind)
    for element in [e for e in nodes if e.get('widgetType') == kind]:
        for key in element['settings']:
            assert key == '_title' or valid(key, controls, groups), (kind, key)
form = next(e['settings'] for e in nodes if e.get('widgetType') == 'form')
_, controls, groups = schema('form')
for field in form['form_fields']:
    assert all(key == '_id' or valid(key, controls, groups) for key in field)
assert form['submit_actions'] == ['save-to-database'] and 'email_to' not in form
assert len(form['form_fields']) == 7
assert len({f['custom_id'] for f in form['form_fields']}) == 7
assert all(f['width_mobile'] == '100' for f in form['form_fields'])
assert next(f for f in form['form_fields'] if f['field_type'] == 'textarea')['rows'] == 4
for field in form['form_fields']:
    if field['field_type'] == 'select': assert field['field_options'].splitlines()[0].endswith('|')

skin_text, skin_controls, skin_groups = schema('skin-base')
_, more_controls, more_groups = schema('skin-classic')
skin_controls |= more_controls
skin_groups |= more_groups
query = Path('/tmp/syncs-conference-query-base.php').read_text()
query_fields = set(re.findall(r"\$fields\[['\"]([^'\"]+)", query))
for element in [e for e in nodes if e.get('widgetType') == 'posts']:
    s = element['settings']
    for key in s:
        if key.startswith('classic_'): assert valid(key[8:], skin_controls, skin_groups), key
        elif key.startswith('posts_'): assert key[6:] in query_fields, key
        else: assert key in {'_title', '_skin', 'pagination_type'}, key
    assert s['_skin'] == 'classic' and s['posts_select_date'] == 'anytime'
    assert 'posts_date_after' not in s and 'posts_date_before' not in s and not s.get('posts_query_id')
    assert s['classic_columns_mobile'] == '1'
assert {e['settings']['posts_post_type'] for e in nodes if e.get('widgetType') == 'posts'} == {'project', 'post'}
for e in [e for e in nodes if e.get('widgetType') == 'nested-accordion']:
    assert len(e['settings']['items']) == len(e['elements'])
    assert e['settings']['default_state'] == 'expanded' and e['settings']['max_items_expended'] == 'one'

sources = []
for name, path in {
    'Official Elementor image': '/tmp/syncs-conference-image.php',
    'Official Elementor nested accordion': '/tmp/syncs-conference-accordion.php',
    'GPL compatibility fork Form (not installed Elementor Pro)': '/tmp/syncs-conference-form.php',
    'GPL compatibility fork Posts classic skin': '/tmp/syncs-conference-skin-classic.php',
    'GPL compatibility fork Posts base skin': '/tmp/syncs-conference-skin-base.php',
    'GPL compatibility fork query group': '/tmp/syncs-conference-query-base.php',
}.items():
    sources.append({'source': name, 'sha256': hashlib.sha256(Path(path).read_bytes()).hexdigest()})
report = {'passed': True, 'page': PAGE, 'sections': len(sections), 'elements': len(nodes), 'templates': 16,
    'native_types': dict(types), 'custom_html_css_js': 0, 'anchors': len(anchors),
    'image_placements': len(image_urls), 'unique_image_urls': len(set(image_urls)), 'all_image_urls_from_user_exports': True,
    'form_fields': 7, 'form_submit_action': form['submit_actions'], 'dynamic_projects': True, 'dynamic_articles': True,
    'service_taxonomy_selection_required': True, 'schema_checks': sources,
    'not_tested': ['actual WordPress import/edit/re-export', 'installed Elementor/Pro versions', 'live media',
                   'real Posts/language/category queries', 'form database persistence and email']}
(ROOT / 'validation/results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(report, ensure_ascii=False))
