"""Validate the full page against the user's actual export; not a WordPress import test."""
from pathlib import Path
import argparse,json,re

def walk(nodes):
    for node in nodes:
        yield node
        yield from walk(node.get('elements',[]))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    source=json.loads(args.source.read_text(encoding='utf-8'))
    result=json.loads((root/'SYNCs-Projects-Page.json').read_text(encoding='utf-8'))
    assert result['version']==source['version']=='0.4'
    assert result['type']==source['type']=='page'
    assert result['page_settings']==source['page_settings']
    nodes=list(walk(result['content']));ids=[n['id'] for n in nodes]
    assert len(ids)==len(set(ids)) and all(re.fullmatch('[a-f0-9]{7,8}',i) for i in ids)
    original_nodes=list(walk(source['content']))
    get=lambda nodes,kind:next(n for n in nodes if n.get('widgetType')==kind)
    old_grid=get(original_nodes,'loop-grid');grid=get(nodes,'loop-grid')
    old_filter=get(original_nodes,'taxonomy-filter');filter_=get(nodes,'taxonomy-filter')
    assert grid['id']==old_grid['id']
    assert filter_['settings']['selected_element']==grid['id']
    assert old_filter['settings']['selected_element'] not in {n['id'] for n in original_nodes}
    assert grid['settings']['template_id']==old_grid['settings']['template_id']==6526
    for key,value in old_grid['settings'].items():
        if key!='masonry':assert grid['settings'][key]==value,(key,value)
    assert grid['settings']['masonry']==''
    for key,value in old_filter['settings'].items():
        if key!='selected_element':assert filter_['settings'][key]==value,(key,value)
    assert filter_['settings']['taxonomy']=='project_category'
    assert grid['settings']['post_query_post_type']=='project'
    assert grid['settings']['posts_per_page']==30
    assert sum(n.get('settings',{}).get('header_size')=='h1' for n in nodes)==1
    assert not any(n.get('widgetType','').startswith('elementskit-') for n in nodes)
    assert get(nodes,'breadcrumbs')==get(original_nodes,'breadcrumbs')
    assert not any('http://' in json.dumps(n['settings']) for n in nodes)
    assert all(n.get('widgetType') in {None,'heading','breadcrumbs','loop-grid','taxonomy-filter','html','button'} for n in nodes)
    integration=get(nodes,'html')['settings']['html']
    assert (root/'assets/projects-page.css').read_text(encoding='utf-8') in integration
    assert (root/'assets/projects-page.js').read_text(encoding='utf-8') in integration
    assert 'demo-project' not in json.dumps(result)
    print('PASS',len(nodes),'unique native elements; one H1; source page type/settings preserved')
    print('PASS project query, count=30, template=6526, taxonomy=project_category preserved')
    print('PASS dangling filter target corrected to',grid['id'],'and incompatible masonry disabled')
    print('PENDING actual Elementor import, editor reopening, source card resolution and native filtering')

if __name__=='__main__':
    main()
