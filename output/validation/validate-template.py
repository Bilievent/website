"""Validate template structure; this does not validate Elementor import compatibility."""
import json
import re
from pathlib import Path

def main():
    root = Path(__file__).resolve().parents[1]
    template = json.loads((root / 'templates/syncs-selected-projects.json').read_text())
    assert template['version'] == '0.4'
    assert template['type'] == 'container'
    seen = set()
    counts = {}
    def visit(node):
        assert re.fullmatch(r'[a-f0-9]{7}', node['id'])
        assert node['id'] not in seen
        seen.add(node['id'])
        assert isinstance(node['settings'], dict)
        assert isinstance(node['elements'], list)
        kind = node.get('widgetType', node['elType'])
        assert kind in {'container', 'heading', 'image', 'button', 'html'}
        counts[kind] = counts.get(kind, 0) + 1
        if kind == 'heading':
            assert node['settings']['header_size'] in {'h2', 'h3', 'p'}
            assert node['settings']['title']
        if kind == 'image':
            name = node['settings']['image']['url'].rsplit('/', 1)[-1]
            assert (root / 'assets' / name).is_file()
        for child in node['elements']:
            visit(child)
    for node in template['content']:
        visit(node)
    assert counts == {'container': 7, 'heading': 10, 'image': 4, 'html': 1, 'button': 1}, counts
    print('PASS:', len(seen), 'unique elements;', counts)
    print('Image URLs are placeholders. Replace via Media Library. Elementor runtime import remains untested.')

if __name__ == '__main__':
    main()
