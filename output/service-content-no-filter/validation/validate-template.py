"""Check native schema reuse, dynamic fields and removal of Taxonomy Filter."""
from pathlib import Path
import copy,json,re

def walk(nodes):
    for node in nodes:
        yield node
        yield from walk(node.get('elements',[]))

def main():
    root=Path(__file__).resolve().parents[1]
    original=json.loads((root.parent/'projects-page/SYNCs-Projects-Page.json').read_text())
    original_grid=next(n for n in walk(original['content']) if n.get('widgetType')=='loop-grid')
    all_ids=set()
    for file in sorted(root.glob('SYNCs-Service-*.json')):
        data=json.loads(file.read_text(encoding='utf-8'));nodes=list(walk(data['content']));ids=[n['id'] for n in nodes]
        assert len(ids)==len(set(ids)) and all(re.fullmatch('[a-f0-9]{7,8}',i) for i in ids)
        assert not all_ids.intersection(ids), 'Variant widget IDs overlap'
        all_ids.update(ids)
        assert data['version']=='0.4'
        assert all(n.get('widgetType')!='taxonomy-filter' for n in nodes)
        if data['type']=='container':
            grids=[n for n in nodes if n.get('widgetType')=='loop-grid'];assert len(grids)==1
            grid=grids[0];settings=grid['settings']
            kind='post' if 'Articles' in file.name else 'project'
            assert settings['post_query_post_type']==kind
            assert settings['posts_per_page']==original_grid['settings']['posts_per_page']==30
            assert settings['template_id']==6526
            assert settings['masonry']==''
            assert not settings.get('post_query_query_id')
            assert not any('taxonom' in n.get('widgetType','') for n in nodes)
            assert not any(n.get('settings',{}).get('header_size')=='h1' for n in nodes)
            for key,value in original_grid['settings'].items():
                if key not in ['_css_classes','post_query_post_type','pagination_prev_label','pagination_next_label','text','load_more_no_posts_custom_message','nothing_found_message_text']:
                    assert settings[key]==value,(file.name,key)
            markup=next(n for n in nodes if n.get('widgetType')=='html')['settings']['html']
            assert 'sx-native-filter' not in markup and 'e-filter-item' not in markup
            assert (root/'assets/section.css').read_text() in markup
            assert (root/'assets/section.js').read_text() in markup
        elif data['type']=='loop-item':
            image=next(n for n in nodes if n.get('widgetType')=='image')
            title=next(n for n in nodes if n.get('widgetType')=='icon-box')
            assert 'name="post-featured-image"' in image['settings']['__dynamic__']['image']
            assert 'name="post-title"' in title['settings']['__dynamic__']['title_text']
            assert title['settings']['title_size']=='h3'
            for n in [image,title]:assert 'name="post-url"' in n['settings']['__dynamic__']['link']
            assert 'acf-url' not in json.dumps(data)
        else:raise AssertionError(data['type'])
        assert 'demo-project' not in json.dumps(data)
        print('PASS',file.name,len(nodes),'native elements; no Taxonomy Filter')
    print('Service term selection and imported Loop Item ID must be configured in Elementor; runtime import not executed')

if __name__=='__main__':main()
