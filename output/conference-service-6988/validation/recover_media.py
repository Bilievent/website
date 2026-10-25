"""Recover exact same-site URLs from public WordPress responses; never guess date paths."""
import concurrent.futures
import hashlib
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from build import ROOT, CONTENT

HOST='https://syncs.com.sa'
ASSETS=Path('/tmp/syncs-service-source/images')
PAGE=json.loads((ROOT/'validation/manifest.json').read_text())
TARGETS=PAGE['missing_original_media_urls']
headers={'User-Agent':'Mozilla/5.0 (compatible; SYNC-template-review)'}


def fetch(url):
    request=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(request,timeout=25) as response:
        body=response.read(12_000_000)
        return body,response.headers.get('Content-Type',''),response.geturl()


def candidates(value):
    found=set()
    if isinstance(value,dict):
        for v in value.values():found|=candidates(v)
    elif isinstance(value,list):
        for v in value:found|=candidates(v)
    elif isinstance(value,str):
        value=html.unescape(value.replace('\\/','/'))
        for match in re.findall(r'https?://[^\s"<>\\]+',value):
            u=urllib.parse.urlparse(match)
            if u.hostname in {'syncs.com.sa','www.syncs.com.sa'} and '/wp-content/uploads/' in u.path:
                found.add(match.rstrip('),;'))
    return found


def filename(url):return urllib.parse.unquote(Path(urllib.parse.urlparse(url).path).name)
def find_name(name,urls):return [url for url in urls if filename(url)==name]


def main():
    records=[];mapping=json.loads((ROOT/'media-urls.json').read_text());urls=set();errors=[]
    # A single probe isolates an environment/proxy denial instead of issuing 16 doomed requests.
    try:
        body,ctype,final=fetch(CONTENT['project']['url'])
        urls|=candidates(body.decode('utf8','replace'))
        records.append(dict(source=final,sha256=hashlib.sha256(body).hexdigest(),method='page HTML'))
    except Exception as error:
        report=dict(resolved=False,blocked=True,probe=CONTENT['project']['url'],error=str(error),missing=TARGETS,
                    requirement='Apply saved environment domain additions for syncs.com.sa; then rerun this script.')
        (ROOT/'validation/media-resolution.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(report,ensure_ascii=False));return 2

    def search(name):
        query=urllib.parse.urlencode(dict(search=Path(name).stem,per_page=100,_fields='source_url,media_details,slug'))
        url=HOST+'/wp-json/wp/v2/media?'+query
        try:
            body,ctype,final=fetch(url);data=json.loads(body)
            return name,candidates(data),dict(source=final,sha256=hashlib.sha256(body).hexdigest(),method='WordPress media search'),None
        except Exception as error:return name,set(),None,dict(source=url,error=str(error))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for name,found,evidence,error in pool.map(search,[n for n in TARGETS if not find_name(n,urls)]):
            urls|=found
            if evidence:records.append(evidence)
            if error:errors.append(error)
    # Other existing first-party pages can expose image URLs when public media search is restricted.
    remaining=[n for n in TARGETS if not find_name(n,urls)]
    if remaining:
        pages=[HOST+'/',CONTENT['page_url']]+[d['url'] for d in CONTENT['services'] if urllib.parse.urlparse(d['url']).hostname=='syncs.com.sa']
        for url in pages:
            try:
                body,ctype,final=fetch(url);urls|=candidates(body.decode('utf8','replace'))
                records.append(dict(source=final,sha256=hashlib.sha256(body).hexdigest(),method='existing page HTML'))
            except Exception as error:errors.append(dict(source=url,error=str(error)))
    verified=[]
    for name in TARGETS:
        matches=find_name(name,urls)
        for url in sorted(matches,key=lambda u:('/2026/' not in u,len(u))):
            try:
                body,ctype,final=fetch(url)
                if not ctype.startswith('image/'):continue
                mapping[name]=final
                local=ASSETS/name
                verified.append(dict(filename=name,url=final,content_type=ctype,sha256=hashlib.sha256(body).hexdigest(),
                    exact_uploaded_bytes=local.exists() and local.read_bytes()==body))
                break
            except Exception as error:errors.append(dict(source=url,error=str(error)))
    (ROOT/'media-urls.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n')
    missing=[n for n in TARGETS if n not in mapping]
    report=dict(resolved=not missing,blocked=False,verified=verified,missing=missing,sources=records,errors=errors,
                guessed_media_urls=0,external_hosted_media=0)
    (ROOT/'validation/media-resolution.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(resolved=not missing,verified=len(verified),missing=missing),ensure_ascii=False))
    return 0 if not missing else 2


if __name__=='__main__':raise SystemExit(main())
