"""Contract audit of the complete native page, sections, form and optional dynamic resources."""
import collections
import hashlib
import json
import re
from urllib.parse import urlparse

from build_page import ROOT, BASE, C, MEDIA, walk


def leaves(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield key, value
            yield from leaves(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from leaves(value)


page = json.loads((ROOT / "SYNCs-SCEGA-Complete-Page.json").read_text())
manifest = json.loads((ROOT / "validation/manifest.json").read_text())
nodes = list(walk(page["content"]))
sections = page["content"][0]["elements"]
assert len(sections) == len(manifest["sections"]) == 14
assert page["type"] == "page" and page["version"] == "0.4"
assert len(nodes) == manifest["elements"]
source_types = {e["widgetType"] for e in walk(json.loads(BASE.read_text())["content"]) if "widgetType" in e}
types = collections.Counter(e.get("widgetType", "container") for e in nodes)
assert set(types) - {"container"} <= source_types | {"form", "nested-accordion"}
assert types["form"] == 1 and types["nested-tabs"] == 1 and types["nested-accordion"] == 3
assert types.get("html", 0) == types.get("shortcode", 0) == types.get("taxonomy-filter", 0) == 0
headings = [e["settings"] for e in nodes if e.get("widgetType") == "heading"]
assert len([s for s in headings if s["header_size"] == "h1"]) == 1
assert next(s["title"] for s in headings if s["header_size"] == "h1") == "SCEGA Permit Support in Saudi Arabia"
anchor_ids = [e["settings"].get("_element_id") for e in nodes if e["settings"].get("_element_id")]
assert len(anchor_ids) == len(set(anchor_ids)) == 14
photo_origins = set()
for source in (BASE, ROOT.parent / "service-content-no-filter/SYNCs-Service-Card.json"):
    for key, value in leaves(json.loads(source.read_text())):
        if key == "url" and isinstance(value, str) and "/wp-content/uploads/" in value:
            photo_origins.add(value)
links, images = [], []
for key, value in leaves(page["content"]):
    assert key not in {"html", "custom_css", "custom_js"}
    if isinstance(value, str):
        assert not re.search(r"<(script|style|iframe|div|table)\b", value, re.I)
        assert "Lorem ipsum" not in value and "Client 01" not in value
        assert not value.startswith("globals/colors?")
        if re.fullmatch(r"#[a-fA-F0-9]{6}([a-fA-F0-9]{2})?", value):
            assert value[:7].upper() in set(C.values()), value
        if key == "url":
            if value.startswith("#"):
                assert value[1:] in anchor_ids, value
                links.append(value)
            elif "/wp-content/uploads/" in value:
                assert value in photo_origins, value
                assert urlparse(value).hostname == "syncs.com.sa"
                images.append(value)
            else:
                assert value in {"https://syncs.com.sa/contact-us/", "https://syncs.com.sa/project/"}, value
                links.append(value)

all_files = [ROOT / "SYNCs-SCEGA-Complete-Page.json"] + sorted((ROOT / "sections").glob("*.json")) + sorted((ROOT / "extras").glob("*.json"))
assert len(all_files) == 17
for file in all_files:
    document = json.loads(file.read_text())
    ids = [e["id"] for e in walk(document["content"])]
    assert len(ids) == len(set(ids)), file.name
    assert all(re.fullmatch(r"[a-f0-9]{6,8}", id_) for id_ in ids)
    for key, value in leaves(document["content"]):
        assert key not in {"html", "custom_css", "custom_js"}
for element, part in zip(sections, manifest["sections"]):
    assert json.loads((ROOT / part["file"]).read_text())["content"] == [element]

tabs = next(e for e in nodes if e.get("widgetType") == "nested-tabs")
assert len(tabs["settings"]["tabs"]) == len(tabs["elements"]) == 5
assert [t["tab_title"].split("  ", 1)[1] for t in tabs["settings"]["tabs"]] == ["Conference", "Exhibition", "Workshop", "Training", "Business Meeting"]
accordions = [e for e in nodes if e.get("widgetType") == "nested-accordion"]
assert sorted(len(e["settings"]["items"]) for e in accordions) == [2, 2, 5]
for e in accordions:
    assert len(e["settings"]["items"]) == len(e["elements"])
    assert e["settings"]["default_state"] == "all_collapsed"
    assert e["settings"]["max_items_expended"] == "one"

form = next(e["settings"] for e in nodes if e.get("widgetType") == "form")
assert form["submit_actions"] == ["save-to-database"]
assert "email_to" not in form and "email" not in form["submit_actions"]
assert form["show_labels"] == "true" and len(form["form_fields"]) == 4
assert [f["custom_id"] for f in form["form_fields"]] == ["name", "company", "email", "event_type"]
assert next(f for f in form["form_fields"] if f["custom_id"] == "email")["field_type"] == "email"
assert next(f for f in form["form_fields"] if f["custom_id"] == "email")["required"] == "true"
assert all(f["width_mobile"] == "100" for f in form["form_fields"])
assert not form["form_fields"][-1]["field_options"].splitlines()[0].split("|", 1)[1]

# Public compatibility source corroborates Form controls; it is NOT installed Elementor Pro.
schema_path = __import__('pathlib').Path('/tmp/elementor-form-schema.php')
if schema_path.exists():
    schema = schema_path.read_text()
    controls = set(re.findall(r"add_(?:responsive_)?control\(\s*['\"]([^'\"]+)", schema))
    groups = set(re.findall(r"['\"]name['\"]\s*=>\s*['\"]([^'\"]+)", schema))
    for key in form:
        assert key == "_title" or key in controls or any(key.startswith(g + "_") for g in groups), key
    for field in form["form_fields"]:
        for key in field:
            assert key == "_id" or key in controls or re.sub(r"_(mobile|tablet)$", "", key) in controls, key

extra_grid = json.loads((ROOT / "extras/SYNCs-Permit-Guides-Dynamic-Loop-Grid.json").read_text())
grid = next(e["settings"] for e in walk(extra_grid["content"]) if e.get("widgetType") == "loop-grid")
assert grid["template_id"] == "" and grid["post_query_post_type"] == "post" and grid["posts_per_page"] == 4
assert grid["columns"] == 4 and grid["columns_tablet"] == 2 and grid["columns_mobile"] == 1
assert not any("query_id" in key and value for key, value in grid.items())
loop_item = json.loads((ROOT / "extras/SYNCs-Permit-Guide-Loop-Item.json").read_text())
assert loop_item["type"] == "loop-item"
dynamic_strings = [v for k, v in leaves(loop_item) if isinstance(v, str) and '[elementor-tag ' in v]
assert any('name="post-title"' in v for v in dynamic_strings)
assert any('name="post-featured-image"' in v for v in dynamic_strings)
assert any('name="post-url"' in v for v in dynamic_strings)

result = {"passed": True, "templates": len(all_files), "main_sections": 14, "main_elements": len(nodes),
          "native_types": dict(types), "custom_html_css_js": 0, "same_page_links": len([x for x in links if x.startswith('#')]),
          "image_placements": len(images), "unique_image_urls": len(set(images)), "unknown_media_urls": 0,
          "form_submission_action": form["submit_actions"], "email_notifications_configured": False,
          "optional_dynamic_articles": True, "optional_loop_item_selection_required": True,
          "not_run": ["actual WordPress import/edit/re-export", "Elementor Pro form submission persistence and emails", "native tabs/accordion JS and assistive technology", "live image availability"]}
(ROOT / "validation/results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False))
