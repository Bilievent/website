"""Apply SYNC colours to a user-exported native Elementor page; retain its content/layout."""
import argparse
import collections
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = dict(purple="#8F7BB8", panel="#2B203D", charcoal="#3A3447", lavender="#C9BCE3",
         gray="#F5F5F7", soft="#FAFAFC", silver="#D8D8E0", white="#FFFFFF",
         midnight="#1D162A", graphite="#4A4557")
GLOBAL = {
    "primary": C["purple"], "secondary": C["lavender"], "accent": C["midnight"],
    "text": C["graphite"], "b8a96f0": C["midnight"] + "00",
    "c546c7d": C["white"], "0a9ffd1": C["panel"], "6b0ce64": C["gray"],
    "4da9a17": C["midnight"], "fdf12ae": C["silver"], "50b2a21": C["charcoal"],
    "bcaa435": C["gray"] + "00", "9c764db": C["lavender"],
    "2d6a869": C["silver"], "209bfaa": C["panel"], "f130dd2": C["midnight"],
    "131f790": C["midnight"],
}
# Section/card roles are derived from the actual exported element tree, not global ID guesses.
SURFACES = {
    "557b2c7": C["gray"], "aa82547": C["gray"],
    "591b73ab": C["midnight"], "5747e56c": C["soft"],
    "1524400b": C["panel"], "760a5f48": C["panel"],
    "5a94dd55": C["gray"], "53c84f1c": C["midnight"],
    "270042c4": C["soft"], "3d0cc97f": C["panel"], "7131a4c1": C["charcoal"],
    "5591466b": C["soft"], "1ea06251": C["gray"],
    "359b4caa": C["gray"], "6de5299a": C["panel"],
    "7c6f685f": C["panel"], "3f96980": C["panel"], "277967ac": C["midnight"],
}
DARK = {C["midnight"], C["panel"], C["charcoal"]}
HEX = re.compile(r"#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?$")
contexts = {}


def walk(nodes):
    for n in nodes:
        yield n
        yield from walk(n.get("elements", []))


def color_key(key):
    return "color" in str(key) or key in {"primary_color", "secondary_color"}


def replace_shadow_colours(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if k == "color" and isinstance(v, str) and v.startswith("rgba(0, 0, 0,"):
                x[k] = v.replace("rgba(0, 0, 0,", "rgba(29, 22, 42,")
            else:
                replace_shadow_colours(v)
    elif isinstance(x, list):
        for v in x:
            replace_shadow_colours(v)


def recolor(e, inherited):
    s = e["settings"]
    refs = s.get("__globals__", {})
    for key, ref in list(refs.items()):
        if isinstance(ref, str) and ref.startswith("globals/colors?id="):
            token = ref.split("=", 1)[1]
            assert token in GLOBAL, (e["id"], key, token)
            s[key] = GLOBAL[token]
            del refs[key]
        elif color_key(key) and ref == "":
            del refs[key]

    surface = inherited
    if e["elType"] == "container":
        if e["id"] in SURFACES:
            s["background_color"] = SURFACES[e["id"]]
            if e["id"] in {"557b2c7", "aa82547"}:
                s["background_background"] = "classic"
        if s.get("background_background") in {"classic", "gradient"}:
            candidate = s.get("background_color")
            if candidate and not candidate.endswith("00"):
                surface = candidate
        if e["id"] in {"6de5299a", "7c6f685f", "3f96980"}:
            # Solid-ended purple/midnight caption gradients: readable over any team image.
            s["background_color_b"] = C["midnight"]
        if e["id"] in {"591b73ab", "277967ac"}:
            s["background_overlay_color"] = C["panel"]
            s["background_overlay_color_b"] = C["midnight"]
        if "border_color" in s:
            s["border_color"] = C["charcoal"] if surface in DARK else C["silver"]

    if s.get("_background_background") == "classic":
        if e.get("widgetType") == "heading":
            # Existing subheading pills retain their own filled background.
            s["_background_color"] = C["panel"] if inherited in DARK else C["gray"]
        elif s.get("_background_color") == C["white"]:
            s["_background_color"] = C["soft"]
        own = s.get("_background_color")
        if own and not own.endswith("00"):
            surface = own

    dark = surface in DARK
    ink = C["white"] if dark else C["midnight"]
    body = C["white"] if dark else C["graphite"]
    accent = C["lavender"] if dark else C["purple"]
    contexts[e["id"]] = {"background": surface, "dark": dark}
    kind = e.get("widgetType")
    if kind == "heading":
        s["title_color"] = C["lavender"] if dark and s.get("title") in {"+", "01", "02", "Director"} else ink
    elif kind == "animated-headline":
        # Purple is decorative on light sections; the highlighted WORD remains readable.
        s.update(title_color=ink, words_color=C["lavender"] if dark else C["panel"], marker_color=accent)
        if e["id"] == "1809b101":
            # White text is robust even at the lightest pixels under the existing 70% photo overlay.
            s["words_color"] = C["white"]
    elif kind == "text-editor":
        s["text_color"] = body
    elif kind == "icon-box":
        s.update(title_color=ink, description_color=body, primary_color=accent)
    elif kind == "counter":
        s.update(number_color=ink, title_color=body)
    elif kind == "icon-list":
        s.update(text_color=body, text_color_hover=C["lavender"] if dark else C["panel"],
                 icon_color=accent, icon_color_hover=C["lavender"] if dark else C["panel"])
    elif kind == "button":
        s.update(background_color=C["purple"], button_text_color=C["midnight"],
                 button_background_hover_color=C["lavender"], hover_color=C["midnight"],
                 border_color=C["purple"], button_hover_border_color=C["lavender"])
    elif kind == "divider":
        s["color"] = C["lavender"] if dark else C["purple"]
        if e["id"] in {"1181d346", "3887fa3f"}:
            s["color"] = C["silver"] if not dark else C["lavender"]
    elif kind == "image-carousel":
        s.update(arrows_color=ink, dots_color=accent,
                 dots_inactive_color=C["silver"] if dark else C["graphite"])

    if "_border_color" in s:
        s["_border_color"] = accent
    replace_shadow_colours(s)
    for child in e.get("elements", []):
        recolor(child, surface)


def differences(a, b, path=()):
    if isinstance(a, dict) and isinstance(b, dict):
        for key in a.keys() | b.keys():
            if key not in a:
                yield {"path": [*path, key], "operation": "add", "after": b[key]}
            elif key not in b:
                yield {"path": [*path, key], "operation": "remove", "before": a[key]}
            else:
                yield from differences(a[key], b[key], (*path, key))
    elif isinstance(a, list) and isinstance(b, list):
        assert len(a) == len(b), path
        for i, (left, right) in enumerate(zip(a, b)):
            yield from differences(left, right, (*path, i))
    elif a != b:
        yield {"path": list(path), "operation": "replace", "before": a, "after": b}


def lum(hex_colour):
    c = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in c]
    return sum(v * w for v, w in zip(c, (.2126, .7152, .0722)))


def contrast(a, b):
    lo, hi = sorted((lum(a), lum(b)))
    return (hi + .05) / (lo + .05)


def verify(original, revised):
    old = list(walk(original["content"]))
    new = list(walk(revised["content"]))
    assert len(old) == len(new) == 109
    assert len({n["id"] for n in new}) == len(new)
    assert revised["version"] == original["version"] == "0.4"
    assert revised["type"] == original["type"] == "page"
    assert [(n["id"], n["elType"], n.get("widgetType")) for n in old] == [
        (n["id"], n["elType"], n.get("widgetType")) for n in new]
    changes = list(differences(original, revised))
    for delta in changes:
        path = delta["path"]
        assert "settings" in path, delta
        if "__globals__" in path:
            assert delta["operation"] == "remove", delta
            assert color_key(path[-1]), delta
        elif path[-1] == "background_background":
            assert delta["operation"] == "add" and delta["after"] == "classic", delta
        else:
            assert color_key(path[-1]), delta
            assert delta["operation"] in {"add", "replace"}, delta
            value = delta["after"]
            assert isinstance(value, str) and (HEX.fullmatch(value) or value.startswith("rgba(29, 22, 42,")), delta
            if HEX.fullmatch(value):
                assert value[:7] in C.values(), delta

    for n in new:
        assert not any(isinstance(v, str) and v.startswith("globals/colors?id=")
                       for v in n["settings"].get("__globals__", {}).values())
    checks = []
    def check(n, state, fg, bg, minimum=4.5):
        value = contrast(fg, bg)
        item = dict(element=n["id"], widget=n.get("widgetType"), state=state,
                    foreground=fg, background=bg, ratio=round(value, 2), minimum=minimum)
        checks.append(item)
        assert value >= minimum, item

    for n in new:
        s = n["settings"]; w = n.get("widgetType"); bg = contexts[n["id"]]["background"]
        if w == "heading": check(n, "title", s["title_color"], bg)
        elif w == "animated-headline":
            check(n, "title", s["title_color"], bg)
            check(n, "highlighted word", s["words_color"], bg)
        elif w == "text-editor": check(n, "body", s["text_color"], bg)
        elif w == "counter": check(n, "number", s["number_color"], bg)
        elif w == "icon-box":
            check(n, "title", s["title_color"], bg)
            check(n, "description", s["description_color"], bg)
            if s.get("selected_icon", {}).get("value"):
                check(n, "icon", s["primary_color"], bg, 3)
        elif w == "icon-list":
            check(n, "text", s["text_color"], bg)
            check(n, "text hover", s["text_color_hover"], bg)
            check(n, "icon", s["icon_color"], bg, 3)
            check(n, "icon hover", s["icon_color_hover"], bg, 3)
        elif w == "button":
            check(n, "normal", s["button_text_color"], s["background_color"])
            check(n, "hover", s["hover_color"], s["button_background_hover_color"])

    # Conservative colour-only bounds for the existing photo-overlay opacity.
    # Any source photo pixel is no brighter than pure white. Geometry remains a live-render check.
    indexed = {n["id"]: n for n in new}
    photo_bounds = []
    for eid in ("591b73ab", "277967ac"):
        n = indexed[eid]; s = n["settings"]; opacity = s["background_overlay_opacity"]["size"]
        for key in ("background_overlay_color", "background_overlay_color_b"):
            overlay = s[key]
            rgb = [round(opacity * int(overlay[i:i+2], 16) + (1-opacity) * 255) for i in (1, 3, 5)]
            composited = "#" + "".join(f"{v:02X}" for v in rgb)
            for fg in (C["white"], C["lavender"]):
                ratio = contrast(fg, composited)
                minimum = 3 if eid == "591b73ab" and fg == C["lavender"] else 4.5
                photo_bounds.append(dict(element=eid, endpoint=key, foreground=fg,
                                         lightest_background=composited, ratio=round(ratio,2),
                                         role="decorative accent" if minimum == 3 else "text",
                                         minimum=minimum))
                assert ratio >= minimum, photo_bounds[-1]
    return changes, checks, photo_bounds


def main():
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    args = p.parse_args()
    original = json.loads(args.source.read_text())
    revised = copy.deepcopy(original)
    for e in revised["content"]:
        recolor(e, C["gray"])
    changes, checks, photo_bounds = verify(original, revised)
    target = ROOT / "SYNCs-About-Us-7208-Brand-Colors.json"
    target.write_text(json.dumps(revised, ensure_ascii=False, indent=2) + "\n")
    (ROOT / "palette.json").write_text(json.dumps(C, indent=2) + "\n")
    validation = ROOT / "validation"
    for filename, data in (("color-changes.json", changes), ("contrast.json", checks),
                           ("photo-overlay-bounds.json", photo_bounds), ("contexts.json", contexts)):
        (validation / filename).write_text(json.dumps(data, indent=2) + "\n")
    report = dict(passed=True, source=args.source.name,
                  source_sha256=hashlib.sha256(args.source.read_bytes()).hexdigest(),
                  output=target.name, output_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                  top_level_containers=len(revised["content"]), elements=len(contexts),
                  changes=len(changes), solid_contrast_checks=len(checks),
                  minimum_solid_text_ratio=min(c["ratio"] for c in checks if c["minimum"]==4.5),
                  photo_overlay_endpoint_bounds=len(photo_bounds),
                  content_layout_media_links_typography_interactions_preserved=True,
                  widget_types=dict(collections.Counter(n.get("widgetType", "container") for n in walk(revised["content"]))),
                  global_colour_refs_remaining=0,
                  native_import_edit_reexport="not tested: no WordPress staging or installed plugin versions available")
    (validation / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
