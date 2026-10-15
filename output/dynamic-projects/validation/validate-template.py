"""Validate exported structure and dynamic bindings, without claiming runtime compatibility."""
from pathlib import Path
import argparse
import json
import re

def walk(nodes):
    for node in nodes:
        yield node
        yield from walk(node.get('elements', []))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, help='Original Elementor Loop Item export for binding comparison')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    docs = {}
    for name in ['syncs-dynamic-loop-item.json', 'syncs-projects-section-shell.json']:
        doc = json.loads((root / 'templates' / name).read_text(encoding='utf-8'))
        assert doc['version'] == '0.4'
        nodes = list(walk(doc['content']))
        ids = [node['id'] for node in nodes]
        assert len(ids) == len(set(ids))
        assert all(re.fullmatch(r'[a-f0-9]{7,8}', element_id) for element_id in ids)
        assert all(node['elType'] in {'container', 'widget'} for node in nodes)
        assert all(isinstance(node['settings'], dict) for node in nodes)
        assert not any(node.get('widgetType') in {'loop-grid', 'taxonomy-filter'} for node in nodes), 'Unknown target-installation query/filter schema must not be fabricated'
        docs[name] = doc
        print('PASS structure:', name, len(nodes), 'elements')
    loop = docs['syncs-dynamic-loop-item.json']
    assert loop['type'] == 'loop-item'
    nodes = list(walk(loop['content']))
    assert [node.get('widgetType') for node in nodes if node['elType'] == 'widget'] == ['image', 'icon-box', 'html']
    image = next(n for n in nodes if n.get('widgetType') == 'image')
    title = next(n for n in nodes if n.get('widgetType') == 'icon-box')
    assert 'name="post-featured-image"' in image['settings']['__dynamic__']['image']
    assert 'name="post-title"' in title['settings']['__dynamic__']['title_text']
    for node in [image, title]:
        assert 'name="acf-url"' in node['settings']['__dynamic__']['link']
        assert 'field_69d0254b84115' in node['settings']['__dynamic__']['link']
    assert title['settings']['title_size'] == 'h3'
    assert title['settings']['selected_icon']['value'] == ''
    styles = next(n for n in nodes if n.get('widgetType') == 'html')['settings']['html']
    assert styles == '<style>' + (root / 'assets/loop-card.css').read_text(encoding='utf-8') + '</style>'
    assert 'demo-project' not in json.dumps(loop), 'No placeholder artwork in dynamic template'
    if args.source:
        source = json.loads(args.source.read_text(encoding='utf-8'))
        source_nodes = list(walk(source['content']))
        for kind, new in [('image', image), ('icon-box', title)]:
            old = next(n for n in source_nodes if n.get('widgetType') == kind)
            assert new['settings']['__dynamic__'] == old['settings']['__dynamic__']
        print('PASS original image/title/link dynamic bindings preserved byte-for-byte')
    print('PASS native template and dynamic binding checks; WordPress import not executed')

if __name__ == '__main__':
    main()
