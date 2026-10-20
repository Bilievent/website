"""Validate the recolored export against its source invariants, not a synthetic schema."""
import json
from pathlib import Path
import re
from urllib.parse import urlparse

from build_brand import ROOT, digest, noncolor, walk


def all_values(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from all_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from all_values(item)
    else:
        yield value


def luminance(color):
    rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
    return sum(v * w for v, w in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(fg, bg):
    lo, hi = sorted((luminance(fg), luminance(bg)))
    return (hi + 0.05) / (lo + 0.05)


manifest = json.loads((ROOT / "validation/manifest.json").read_text())
document = json.loads((ROOT / manifest["template"]).read_text())
assert digest(noncolor(document["content"])) == manifest["noncolor_content_sha256"]
assert len(document["content"]) == manifest["sections"] == 4
assert len(list(walk(document["content"]))) == manifest["elements"] == 113
palette = set(manifest["palette"].values())
files = [ROOT / manifest["template"], *sorted(ROOT.glob("SYNCs-0*.json"))]
assert len(files) == 5
widgets = set()
color_values = set()
for file in files:
    template = json.loads(file.read_text())
    assert template["version"] == "0.4"
    assert template["type"] in {"page", "container"}
    ids = []
    for element in walk(template["content"]):
        # The real source export includes a six-character ID; keep native IDs verbatim.
        assert re.fullmatch(r"[a-f0-9]{6,8}", element["id"])
        assert element["elType"] in {"container", "widget"}
        ids.append(element["id"])
        if element["elType"] == "widget":
            widgets.add(element["widgetType"])
        for value in all_values(element.get("settings", {})):
            if isinstance(value, str):
                assert not value.startswith("globals/colors?")
                if re.fullmatch(r"#[a-fA-F0-9]{6}([a-fA-F0-9]{2})?", value):
                    assert value[:7].upper() in palette, value
                    color_values.add(value)
                assert not re.search(r"rgba?\(", value), value
    assert len(ids) == len(set(ids))
assert "html" not in widgets and "taxonomy-filter" not in widgets
assert widgets == {"icon", "icon-box", "divider", "icon-list", "heading", "animated-headline",
                   "text-editor", "button", "counter", "image-carousel", "nested-tabs"}
for section, file in zip(document["content"], files[1:]):
    assert json.loads(file.read_text())["content"] == [section]
image_links = json.loads((ROOT / "validation/image-links.json").read_text())
assert len(image_links) == 18
assert len({record["url"] for record in image_links}) == 10
for record in image_links:
    location = document
    for segment in record["path"].split("/"):
        location = location[int(segment)] if isinstance(location, list) else location[segment]
    assert location["url"] == record["url"] and location.get("id") == record["id"]
    parsed = urlparse(location["url"])
    assert parsed.scheme == "https" and parsed.hostname == "syncs.com.sa"
    assert parsed.path.startswith("/wp-content/uploads/")

checks = [
    ("Button normal", "#1D162A", "#8F7BB8", 4.5),
    ("Button hover/focus", "#1D162A", "#C9BCE3", 4.5),
    ("Dark section heading", "#FFFFFF", "#1D162A", 4.5),
    ("Dark section body", "#D8D8E0", "#1D162A", 4.5),
    ("Light section body", "#4A4557", "#FAFAFC", 4.5),
    ("Light gray body", "#4A4557", "#F5F5F7", 4.5),
    ("Counter panel body", "#D8D8E0", "#2B203D", 4.5),
    ("Dark eyebrow", "#C9BCE3", "#2B203D", 4.5),
    ("Light eyebrow", "#2B203D", "#C9BCE3", 4.5),
    ("Tab normal", "#4A4557", "#F5F5F7", 4.5),
    ("Tab hover/selected", "#1D162A", "#C9BCE3", 4.5),
    ("Large highlighted headline", "#8F7BB8", "#FAFAFC", 3.0),
]
ratios = []
for label, fg, bg, minimum in checks:
    ratio = contrast(fg, bg)
    assert ratio >= minimum, (label, ratio)
    ratios.append({"label": label, "foreground": fg, "background": bg,
                   "ratio": round(ratio, 3), "minimum": minimum})
result = {"passed": True, "templates": len(files), "sections": 4, "elements": manifest["elements"],
          "native_widget_types": sorted(widgets), "retained_media_placements": len(image_links),
          "retained_unique_image_urls": 10, "colors": sorted(color_values), "contrast": ratios,
          "noncolor_content_unchanged": True,
          "not_run": ["WordPress import/editor/re-export", "installed plugin version compatibility",
                      "live images", "actual Elementor responsive layout and motion"]}
(ROOT / "validation/results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False))
