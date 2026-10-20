"""Native-only contract, source preservation, anchors, content, URLs and structure."""
import collections
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from build_native import ROOT, SOURCE, SERVICES, CONTACT, COLORS


def walk(elements):
    for element in elements:
        yield element
        yield from walk(element.get("elements", []))


def values(value):
    if isinstance(value, dict):
        for k, v in value.items():
            yield k, v
            yield from values(v)
    elif isinstance(value, list):
        for v in value:
            yield from values(v)


source = json.loads(SOURCE.read_text())
full = json.loads((ROOT / "SYNCs-All-Sections-Native-Why-Us.json").read_text())
single = json.loads((ROOT / "SYNCs-Why-Us-Native-5-Services.json").read_text())
assert full["content"][:3] == source["content"][:3]
assert len(full["content"]) == 4 and full["content"][-1:] == single["content"]
assert full["page_settings"] == source["page_settings"] and full["type"] == "page"
assert single["type"] == "container"
existing_types = {e["widgetType"] for e in walk(source["content"]) if "widgetType" in e}
section = single["content"]
nodes = list(walk(section))
new_types = {e["widgetType"] for e in nodes if "widgetType" in e}
assert new_types <= existing_types
assert new_types == {"heading", "text-editor", "icon-list", "button"}
for template in (single, full):
    ids = []
    for e in walk(template["content"]):
        assert re.fullmatch(r"[a-f0-9]{6,8}", e["id"])
        ids.append(e["id"])
        assert e["elType"] in {"widget", "container"}
        assert e.get("widgetType") not in {"html", "shortcode", "taxonomy-filter"}
    assert len(ids) == len(set(ids))
    assert template["version"] == "0.4"
for key, value in values(section):
    assert key not in {"html", "custom_css", "custom_js", "__dynamic__"}
    if isinstance(value, str):
        assert not re.search(r"<(script|style|iframe|div|table)\b", value, re.I)
        assert "Lorem ipsum" not in value and "globals/colors?" not in value
        if re.fullmatch(r"#[a-fA-F0-9]{6}", value):
            assert value.upper() in set(COLORS.values())
assert len(SERVICES) == 5
by_title = {e["settings"].get("_title"): e for e in nodes}
nav = by_title["Five services navigation"]["settings"]["icon_list"]
assert len(nav) == 5
native_ids = {e["settings"].get("_element_id") for e in nodes}
headers = [e["settings"] for e in nodes if e.get("widgetType") == "heading"]
assert len([s for s in headers if s["header_size"] == "h2"]) == 1
assert [s["title"] for s in headers if s["header_size"] == "h3"] == [s["title"] for s in SERVICES]
assert all(e["settings"]["link"]["url"] == CONTACT for e in nodes if e.get("widgetType") == "button")
assert all(e["settings"]["text"] == "Discuss this service" for e in nodes if e.get("widgetType") == "button")
for service, item in zip(SERVICES, nav):
    assert item["link"]["url"][1:] in native_ids
    assert item["link"]["url"] == "#sx-whyus-" + service["slug"]
    assert service["title"] in item["text"]
    card = by_title[service["slug"] + " service card"]
    assert card["settings"]["html_tag"] == "article"
    points = by_title[service["slug"] + " points"]["settings"]["icon_list"]
    assert len(points) == 3 and all(x["selected_icon"]["value"] == "fas fa-circle" for x in points)
    photo = by_title[service["slug"] + " photo"]["settings"]
    assert photo["background_image"]["url"] == service["image_url"]
    assert photo["background_image"]["id"] == service["media_id"]

# Media must already occur in the user's same-site exports/derived baseline.
allowed = set()
for p in (SOURCE, ROOT.parent / "service-content-no-filter/SYNCs-Service-Card.json"):
    for key, value in values(json.loads(p.read_text())):
        if key == "url" and isinstance(value, str) and "/wp-content/uploads/" in value:
            allowed.add(value)
for service in SERVICES:
    parsed = urlparse(service["image_url"])
    assert parsed.scheme == "https" and parsed.hostname == "syncs.com.sa"
    assert service["image_url"] in allowed
    assert "demo-project" not in service["image_url"]

def luminance(color):
    values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    values = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values]
    return sum(v * w for v, w in zip(values, (0.2126, 0.7152, 0.0722)))

ratios = []
for fg, bg in (("graphite", "white"), ("graphite", "soft"), ("graphite", "gray"), ("midnight", "lavender")):
    lo, hi = sorted((luminance(COLORS[fg]), luminance(COLORS[bg])))
    ratio = (hi + 0.05) / (lo + 0.05)
    assert ratio >= 4.5
    ratios.append({"foreground": COLORS[fg], "background": COLORS[bg], "ratio": round(ratio, 3)})

report = {
    "passed": True, "section_elements": len(nodes),
    "section_types": dict(collections.Counter(e.get("widgetType", "container") for e in nodes)),
    "only_existing_native_widget_types": True, "custom_html_css_js_widgets": 0,
    "services": [s["title"] for s in SERVICES], "anchors": [x["link"]["url"] for x in nav],
    "images": len(SERVICES), "new_image_files": 0, "first_three_sections_unchanged": True,
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "contact_fallback": CONTACT,
    "solid_background_contrast": ratios,
    "not_run": ["WordPress import/edit/re-export", "live media availability", "native Pro sticky runtime",
                "actual installed Elementor/Pro version compatibility"],
}
(ROOT / "validation/results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False))
