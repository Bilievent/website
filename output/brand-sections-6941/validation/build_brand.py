"""Recolor the user's native export; no photo assets or custom widgets are added."""
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PALETTE = {
    "midnight": "#1D162A", "royal": "#8F7BB8", "dark": "#2B203D",
    "charcoal": "#3A3447", "lavender": "#C9BCE3", "gray": "#F5F5F7",
    "soft": "#FAFAFC", "silver": "#D8D8E0", "white": "#FFFFFF",
    "graphite": "#4A4557",
}
TRANSPARENT = PALETTE["midnight"] + "00"
GLOBAL = {
    "primary": PALETTE["royal"], "secondary": PALETTE["lavender"],
    "accent": PALETTE["midnight"], "text": PALETTE["graphite"],
    "c546c7d": PALETTE["soft"], "4da9a17": PALETTE["midnight"],
    "131f790": PALETTE["dark"] + "00", "fdf12ae": PALETTE["silver"],
    "50b2a21": PALETTE["silver"], "b8a96f0": TRANSPARENT,
    "6b0ce64": PALETTE["gray"], "bcaa435": TRANSPARENT,
    "2d6a869": PALETTE["silver"],
}
MODE_KEYS = {"background_background", "button_background_hover_background"}


def walk(elements):
    for element in elements:
        yield element
        yield from walk(element.get("elements", []))


def noncolor(value):
    """Retain all content, media, typography, interactions, spacing and structure."""
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if key == "__globals__":
                retained = {k: v for k, v in item.items()
                            if "color" not in k and not str(v).startswith("globals/colors?")}
                if retained:
                    result[key] = retained
            elif key == "settings" and item == []:
                result[key] = {}
            elif "color" not in key and key not in MODE_KEYS:
                result[key] = noncolor(item)
        return result
    if isinstance(value, list):
        return [noncolor(item) for item in value]
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def recolor(element, dark):
    s = element.get("settings") or {}
    element["settings"] = s
    globals_ = s.get("__globals__", {})
    for key, ref in list(globals_.items()):
        if str(ref).startswith("globals/colors?id="):
            s[key] = GLOBAL[ref.split("=", 1)[1]]
            del globals_[key]
        elif "color" in key:
            del globals_[key]
    if not globals_:
        s.pop("__globals__", None)

    # Match the original section grouping and preserve all existing image records.
    if element["id"] in {"6920cdaf", "32401166", "2e792796"}:
        s.update(background_background="classic", background_color=PALETTE["midnight"])
    elif element["id"] in {"162d294b", "25a63319"}:
        s.update(background_background="classic", background_color=PALETTE["soft"])
    elif element["id"] == "74d4ace4":
        s["background_color"] = PALETTE["gray"]
    elif element["id"] == "25be13e5":
        s["background_color"] = PALETTE["dark"]
        dark = True

    if s.get("background_image", {}).get("url"):
        s["background_color"] = PALETTE["dark"]
        dark = True
    if s.get("background_overlay_background") == "gradient":
        s["background_overlay_color"] = PALETTE["dark"] + "00"
        s["background_overlay_color_b"] = PALETTE["midnight"]
    if s.get("background_overlay_hover_background") == "gradient":
        s["background_overlay_hover_color"] = PALETTE["dark"] + "00"
        s["background_overlay_hover_color_b"] = PALETTE["midnight"]

    kind = element.get("widgetType")
    if kind == "icon":
        s.update(primary_color=PALETTE["royal"], secondary_color=PALETTE["midnight"],
                 hover_primary_color=PALETTE["lavender"], hover_secondary_color=PALETTE["midnight"])
    elif kind == "icon-box":
        if element["id"] == "891cf6":
            dark = True
        s.update(primary_color=PALETTE["lavender" if dark else "royal"],
                 title_color=PALETTE["white" if dark else "midnight"],
                 description_color=PALETTE["silver" if dark else "graphite"],
                 _background_color=PALETTE["dark"])
    elif kind == "heading":
        if s.get("_background_background") == "classic":
            s.update(title_color=PALETTE["lavender" if dark else "dark"],
                     _background_color=PALETTE["dark" if dark else "lavender"])
        else:
            s["title_color"] = PALETTE["lavender" if dark else "midnight"]
    elif kind == "animated-headline":
        s.update(title_color=PALETTE["white" if dark else "midnight"],
                 words_color=PALETTE["lavender" if dark else "royal"], marker_color=PALETTE["royal"])
    elif kind == "divider":
        s["color"] = PALETTE["charcoal" if dark else "silver"] if s.get("style") == "dashed" else PALETTE["royal"]
    elif kind == "icon-list":
        s.update(icon_color=PALETTE["lavender" if dark else "royal"],
                 text_color=PALETTE["silver" if dark else "graphite"])
    elif kind == "text-editor":
        s["text_color"] = PALETTE["silver" if dark else "graphite"]
        if "_border_color" in s:
            s["_border_color"] = PALETTE["royal"]
    elif kind == "counter":
        s["number_color"] = PALETTE["white"]
    elif kind == "button":
        s.update(background_background="classic", background_color=PALETTE["royal"],
                 button_text_color=PALETTE["midnight"], hover_color=PALETTE["midnight"],
                 button_background_hover_background="classic", button_background_hover_color=PALETTE["lavender"])
    elif kind == "nested-tabs":
        s.update(tabs_title_background_color_color=TRANSPARENT,
                 tabs_title_background_color_hover_color=PALETTE["lavender"],
                 tabs_title_background_color_active_color=PALETTE["lavender"],
                 tabs_title_border_color=PALETTE["silver"],
                 tabs_title_border_hover_color=PALETTE["royal"],
                 tabs_title_border_active_color=PALETTE["royal"],
                 title_text_color=PALETTE["graphite"], title_text_color_hover=PALETTE["midnight"],
                 title_text_color_active=PALETTE["midnight"], icon_color=PALETTE["royal"],
                 icon_color_hover=PALETTE["midnight"], icon_color_active=PALETTE["midnight"])
    shadow = s.get("_box_shadow_box_shadow")
    if shadow:
        shadow["color"] = PALETTE["midnight"] + "0D"
    for child in element.get("elements", []):
        recolor(child, dark)


def main(source_path):
    source_file = Path(source_path)
    source = json.loads(source_file.read_text())
    edited = copy.deepcopy(source)
    edited["title"] = "SYNCs — Brand Sections — 6941"
    for i, section in enumerate(edited["content"]):
        recolor(section, i in {0, 2})
    assert noncolor(source["content"]) == noncolor(edited["content"])
    filename = "SYNCs-Sections-6941-Brand-Colors.json"
    (ROOT / filename).write_text(json.dumps(edited, ensure_ascii=False, indent=2) + "\n")
    labels = ["01-Projects-Stacked", "02-About", "03-Projects-Scroll", "04-Why-Choose-Us"]
    for label, section in zip(labels, edited["content"]):
        part = {"content": [section], "page_settings": [], "version": source["version"],
                "title": "SYNCs — " + label, "type": "container"}
        (ROOT / ("SYNCs-" + label + ".json")).write_text(json.dumps(part, ensure_ascii=False, indent=2) + "\n")
    manifest = {
        "source_filename": source_file.name,
        "source_sha256": hashlib.sha256(source_file.read_bytes()).hexdigest(),
        "noncolor_content_sha256": digest(noncolor(source["content"])),
        "sections": len(source["content"]), "elements": len(list(walk(source["content"]))),
        "palette": PALETTE, "template": filename,
        "status": "native export recolored; actual Elementor staging import pending",
    }
    (ROOT / "validation/manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    # Exact URL + attachment ID ledger; no assets are downloaded or bundled.
    records = []
    def media(value, path):
        if isinstance(value, dict):
            if isinstance(value.get("url"), str) and "/wp-content/uploads/" in value["url"]:
                records.append({"path": path, "id": value.get("id"), "url": value["url"]})
            for k, v in value.items():
                media(v, path + "/" + k)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                media(v, path + "/" + str(i))
    media(source["content"], "content")
    (ROOT / "validation/image-links.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
