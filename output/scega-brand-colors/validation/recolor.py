"""Recolor the existing native page without changing any other exported control."""
import collections
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "scega-permit-native/SYNCs-SCEGA-Complete-Page.json"
TARGET = ROOT / "SYNCs-SCEGA-Complete-Page-Brand-Colors.json"
C = dict(midnight="#1D162A", purple="#8F7BB8", panel="#2B203D", charcoal="#3A3447",
         lavender="#C9BCE3", gray="#F5F5F7", soft="#FAFAFC", silver="#D8D8E0",
         white="#FFFFFF", graphite="#4A4557")
SECTIONS = {
    "Header": C["midnight"], "Hero": C["midnight"], "Event teams strip": C["midnight"],
    "Find the right permit": C["gray"], "Application preparation": C["soft"],
    "Permit service scope": C["gray"], "Event services": C["soft"],
    "Hotel and visa support": C["gray"], "Permit fees and timelines": C["soft"],
    "Event experience": C["gray"], "Permit questions": C["midnight"],
    "Event brief": C["midnight"], "Permit guides and resources": C["soft"],
    "Footer": C["midnight"],
}
DARK_FEATURES = {"Event teams strip panel", "Service scope panel", "Experience showcase panel", "Event brief panel"}
COLOR = re.compile(r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?$")
contexts = {}


def is_dark(color):
    return color in {C["midnight"], C["panel"], C["charcoal"]}


def recolor(element, inherited):
    s = element["settings"]
    title = s.get("_title", "")
    surface = inherited
    if element["elType"] == "container":
        if title == "SYNC SCEGA complete page":
            s["background_color"] = C["gray"]
        elif title in SECTIONS:
            s["background_color"] = SECTIONS[title]
        elif "background_image" in s or title in DARK_FEATURES:
            s["background_color"] = C["panel"]
        elif "background_color" in s:
            if is_dark(inherited):
                # Preserve explicitly light readiness card and dark answer surfaces.
                s["background_color"] = s["background_color"]
            else:
                s["background_color"] = C["white"] if s["background_color"] == C["panel"] else C["soft"]
        surface = s.get("background_color", inherited)
    dark = is_dark(surface)
    contexts[element["id"]] = surface
    ink = C["white"] if dark else C["midnight"]
    body = C["white"] if dark else C["graphite"]
    accent = C["lavender"] if dark else C["purple"]
    border = C["charcoal"] if dark else C["silver"]
    kind = element.get("widgetType")

    if element["elType"] == "container" and "border_color" in s:
        s["border_color"] = border
    if kind == "heading":
        s["title_color"] = C["lavender"] if dark and s["title_color"] in {C["lavender"], C["silver"]} else ink
    elif kind == "text-editor":
        s["text_color"] = body
    elif kind == "icon-list":
        s.update(text_color=body, text_color_hover=C["lavender"] if dark else C["midnight"], icon_color=accent)
    elif kind == "icon-box":
        s.update(title_color=ink, description_color=body, primary_color=accent)
    elif kind == "button":
        secondary = s["background_color"].endswith("00")
        s.update(
            background_color=s["background_color"] if secondary else C["purple"],
            button_text_color=(C["lavender"] if dark else C["panel"]) if secondary else C["midnight"],
            button_background_hover_color=C["lavender"], hover_color=C["midnight"],
            border_color=C["purple"],
        )
    elif kind == "nested-tabs":
        s.update(tabs_title_background_color_color=C["panel"] if dark else C["white"],
                 tabs_title_background_color_hover_color=C["lavender"],
                 tabs_title_background_color_active_color=C["purple"],
                 title_text_color=ink, title_text_color_hover=C["midnight"],
                 title_text_color_active=C["midnight"], tabs_title_border_color=border)
    elif kind == "nested-accordion":
        s.update(normal_title_color=C["lavender"] if dark else C["midnight"],
                 hover_title_color=ink, active_title_color=ink,
                 normal_icon_color=accent, hover_icon_color=accent, active_icon_color=accent,
                 accordion_background_normal_color=C["panel"] if dark else C["white"],
                 accordion_background_hover_color=C["charcoal"] if dark else C["gray"],
                 accordion_background_active_color=C["panel"] if dark else C["white"],
                 accordion_border_normal_color=border,
                 accordion_border_hover_color=C["purple"], accordion_border_active_color=C["purple"])
    elif kind == "form":
        s.update(label_color=ink, field_text_color=ink,
                 field_background_color=C["midnight"] if dark else C["soft"],
                 field_border_color=C["purple"], button_background_color=C["purple"],
                 button_text_color=C["midnight"], button_background_hover_color=C["lavender"],
                 button_hover_color=C["midnight"])
    for child in element["elements"]:
        recolor(child, surface)


def walk(elements):
    for element in elements:
        yield element
        yield from walk(element["elements"])


def differences(before, after, path=()):
    assert type(before) is type(after), path
    if isinstance(before, dict):
        assert before.keys() == after.keys(), path
        for key in before:
            yield from differences(before[key], after[key], path + (key,))
    elif isinstance(before, list):
        assert len(before) == len(after), path
        for index, (left, right) in enumerate(zip(before, after)):
            yield from differences(left, right, path + (index,))
    elif before != after:
        assert isinstance(before, str) and COLOR.fullmatch(before), (path, before)
        assert isinstance(after, str) and COLOR.fullmatch(after), (path, after)
        assert "settings" in path and "color" in str(path[-1]), path
        assert after[:7] in C.values(), after
        yield {"path": list(path), "from": before, "to": after}


def luminance(color):
    channels = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
    return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))


def ratio(a, b):
    lo, hi = sorted((luminance(a), luminance(b)))
    return (hi + .05) / (lo + .05)


if __name__ == "__main__":
    original = json.loads(SOURCE.read_text())
    revised = copy.deepcopy(original)
    for element in revised["content"]:
        recolor(element, C["gray"])
    changes = list(differences(original, revised))
    assert changes
    nodes = list(walk(revised["content"]))
    assert len(nodes) == 236 and len({e["id"] for e in nodes}) == 236
    assert len(revised["content"][0]["elements"]) == 14
    assert revised["type"] == "page" and revised["version"] == "0.4"
    assert not any(e.get("widgetType") in {"html", "shortcode", "taxonomy-filter"} for e in nodes)
    checks = []

    def check(element, name, foreground, background, minimum=4.5):
        value = ratio(foreground, background)
        checks.append({"element": element["settings"]["_title"], "state": name,
                       "foreground": foreground, "background": background,
                       "ratio": round(value, 2), "minimum": minimum})
        assert value >= minimum, checks[-1]

    for e in nodes:
        s, bg, kind = e["settings"], contexts[e["id"]], e.get("widgetType")
        if kind == "heading": check(e, "heading", s["title_color"], bg)
        elif kind == "text-editor": check(e, "body", s["text_color"], bg)
        elif kind == "icon-list":
            check(e, "list", s["text_color"], bg)
            check(e, "list hover", s["text_color_hover"], bg)
            if any(item["selected_icon"]["value"] for item in s["icon_list"]):
                check(e, "list icon", s["icon_color"], bg, 3)
        elif kind == "icon-box":
            check(e, "icon title", s["title_color"], bg)
            check(e, "icon body", s["description_color"], bg)
            check(e, "icon", s["primary_color"], bg, 3)
        elif kind == "button":
            check(e, "normal", s["button_text_color"], bg if s["background_color"].endswith("00") else s["background_color"])
            check(e, "hover", s["hover_color"], s["button_background_hover_color"])
        elif kind == "nested-tabs":
            for suffix, text in (("", "title_text_color"), ("_hover", "title_text_color_hover"), ("_active", "title_text_color_active")):
                key = "tabs_title_background_color" + suffix + "_color"
                check(e, "tab" + suffix, s[text], s[key])
        elif kind == "nested-accordion":
            for state in ("normal", "hover", "active"):
                background = s["accordion_background_" + state + "_color"]
                check(e, "accordion " + state, s[state + "_title_color"], background)
                check(e, "accordion icon " + state, s[state + "_icon_color"], background, 3)
        elif kind == "form":
            check(e, "label", s["label_color"], bg)
            check(e, "field", s["field_text_color"], s["field_background_color"])
            check(e, "submit", s["button_text_color"], s["button_background_color"])
            check(e, "submit hover", s["button_hover_color"], s["button_background_hover_color"])

    TARGET.write_text(json.dumps(revised, ensure_ascii=False, indent=2) + "\n")
    report = {"passed": True, "source": str(SOURCE.relative_to(ROOT.parent)),
              "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "output": TARGET.name, "output_sha256": hashlib.sha256(TARGET.read_bytes()).hexdigest(),
              "color_changes": len(changes), "non_color_changes": 0,
              "sections": 14, "elements": len(nodes),
              "types": dict(collections.Counter(e.get("widgetType", "container") for e in nodes)),
              "section_surfaces": SECTIONS, "contrast_checks": len(checks),
              "minimum_text_ratio": min(x["ratio"] for x in checks if x["minimum"] == 4.5),
              "actual_wordpress_import": "not run; installed Elementor/Pro versions and staging unavailable"}
    (ROOT / "validation/results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (ROOT / "validation/color-changes.json").write_text(json.dumps(changes, indent=2) + "\n")
    (ROOT / "validation/contrast.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))
