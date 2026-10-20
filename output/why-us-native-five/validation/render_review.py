"""Independent DOM layout review from native settings; not an Elementor runtime."""
import html
import json
from pathlib import Path

from build_native import ROOT

rules = []


def dim(value):
    return " ".join(str(value[k]) + value.get("unit", "px") for k in ("top", "right", "bottom", "left"))


def scalar(value):
    return str(value["size"]) + value.get("unit", "px")


def typography(settings, prefix):
    css = []
    names = {"font_family": "font-family", "font_size": "font-size", "font_weight": "font-weight",
             "line_height": "line-height", "letter_spacing": "letter-spacing"}
    for k, prop in names.items():
        v = settings.get(prefix + "_" + k)
        if v is not None:
            rendered = scalar(v) if isinstance(v, dict) else str(v)
            if k == "font_family":
                rendered = '"' + str(v) + '",Arial,sans-serif'
            css.append(prop + ":" + rendered)
    return css


def add(selector, props, media=None):
    if props:
        rule = selector + "{" + ";".join(props) + "}"
        rules.append("@media(max-width:" + str(media) + "px){" + rule + "}" if media else rule)


def responsive(settings, suffix):
    combined = dict(settings)
    for device in ("tablet", "mobile"):
        if suffix == "":
            break
        for k, v in settings.items():
            if k.endswith("_" + device):
                combined[k[:-len(device)-1]] = v
        if suffix == device:
            break
    return combined


def native_styles(element):
    settings = element["settings"]
    target = '[data-id="' + element["id"] + '"]'
    for suffix, max_width in (("", None), ("tablet", 1024), ("mobile", 767)):
        s = responsive(settings, suffix)
        props = []
        for key, prop in (("padding", "padding"), ("border_radius", "border-radius"),
                          ("_padding", "padding")):
            if key in s:
                props.append(prop + ":" + dim(s[key]))
        if element["elType"] == "container":
            for key, prop in (("width", "width"), ("min_height", "min-height")):
                if key in s:
                    props.append(prop + ":" + scalar(s[key]))
            for key, prop in (("flex_direction", "flex-direction"), ("flex_justify_content", "justify-content"),
                              ("flex_align_items", "align-items"), ("background_color", "background-color")):
                if key in s:
                    props.append(prop + ":" + str(s[key]))
            if "flex_gap" in s:
                props.append("gap:" + str(s["flex_gap"]["size"]) + "px")
            if s.get("background_image"):
                props.extend(['background-image:url("' + s["background_image"]["url"] + '")',
                              "background-size:" + s.get("background_size", "cover"),
                              "background-position:" + s.get("background_position", "center")])
            add(target, props, max_width)
            if s.get("content_width") == "boxed":
                add(target + ">.e-con-inner", ["max-width:" + scalar(s["boxed_width"])], max_width)
            if settings.get("sticky") and suffix == "":
                rules.append('@media(min-width:1025px){' + target + '{position:sticky;top:' + str(settings["sticky_offset"]) + 'px}}')
        else:
            if s.get("_element_width") == "auto":
                props.append("width:auto")
            add(target, props, max_width)
            kind = element["widgetType"]
            if kind == "heading":
                add(target + ' .elementor-heading-title', typography(s, "typography") + ["color:" + s["title_color"], "text-align:" + s.get("align", "left")], max_width)
            elif kind == "text-editor":
                add(target, typography(s, "typography") + ["color:" + s["text_color"]], max_width)
            elif kind == "icon-list":
                add(target + ' .elementor-icon-list-item>a,' + target + ' .elementor-icon-list-item>span', typography(s, "icon_typography") + ["color:" + s["text_color"]], max_width)
                space = s["space_between"]["size"]
                add(target + ' .elementor-icon-list-items:not(.elementor-inline-items) .elementor-icon-list-item:not(:last-child)', ["padding-bottom:" + str(space / 2) + "px"], max_width)
                add(target + ' .elementor-icon-list-items:not(.elementor-inline-items) .elementor-icon-list-item:not(:first-child)', ["margin-top:" + str(space / 2) + "px"], max_width)
                add(target + ' .elementor-inline-items', ["gap:" + str(space) + "px"], max_width)
                if s.get("divider") == "yes":
                    add(target + ' .elementor-icon-list-item:not(:last-child)', ["border-bottom:1px solid " + s["divider_color"]], max_width)
                add(target + ' .elementor-icon-list-item:hover a', ["color:" + s.get("text_color_hover", s["text_color"])], max_width)
            elif kind == "button":
                add(target, ["text-align:" + s.get("align", "right")], max_width)
                add(target + ' .elementor-button', typography(s, "typography") + ["background:" + s["background_color"], "color:" + s["button_text_color"], "padding:" + dim(s["text_padding"]), "border:1px solid " + s["border_color"], "border-radius:" + dim(s["border_radius"])], max_width)
                add(target + ' .elementor-button:hover,' + target + ' .elementor-button:focus', ["background:" + s["button_background_hover_color"], "color:" + s["hover_color"]], max_width)


def render(element):
    native_styles(element)
    s = element["settings"]
    attrs = ' data-id="' + element["id"] + '"'
    if s.get("_element_id"):
        attrs += ' id="' + html.escape(s["_element_id"]) + '"'
    if element["elType"] == "container":
        tag = s.get("html_tag", "div")
        children = ''.join(render(e) for e in element["elements"])
        if s.get("content_width") == "boxed":
            children = '<div class="e-con-inner">' + children + '</div>'
        if s.get("background_image"):
            children += '<span class="review-photo-note">Existing site photo URL<br>Image unavailable in local QA</span>'
        return '<' + tag + attrs + ' class="e-con">' + children + '</' + tag + '>'
    kind = element["widgetType"]
    if kind == "heading":
        tag = s["header_size"]
        content = '<' + tag + ' class="elementor-heading-title">' + html.escape(s["title"]) + '</' + tag + '>'
    elif kind == "text-editor":
        content = s["editor"]
    elif kind == "button":
        content = '<a class="elementor-button" href="' + html.escape(s["link"]["url"]) + '">' + html.escape(s["text"]) + ' <span aria-hidden="true">→</span></a>'
    elif kind == "icon-list":
        inline = ' elementor-inline-items' if s.get("view") == "inline" else ''
        parts = []
        for item in s["icon_list"]:
            text = html.escape(item["text"])
            if item.get("selected_icon", {}).get("value"):
                text = '<span aria-hidden="true" class="native-bullet">•</span>' + text
            if item.get("link"):
                text = '<a href="' + html.escape(item["link"]["url"]) + '">' + text + '</a>'
            else:
                text = '<span>' + text + '</span>'
            parts.append('<li class="elementor-icon-list-item">' + text + '</li>')
        content = '<ul class="elementor-icon-list-items' + inline + '">' + ''.join(parts) + '</ul>'
    else:
        raise ValueError(kind)
    return '<div' + attrs + ' class="elementor-widget elementor-widget-' + kind + '"><div class="elementor-widget-container">' + content + '</div></div>'


template = json.loads((ROOT / "SYNCs-Why-Us-Native-5-Services.json").read_text())
body = render(template["content"][0])
base = '''*{box-sizing:border-box}body{margin:0;background:#F5F5F7;font:16px/1.65 Manrope,Arial,sans-serif}.e-con{display:flex;flex-direction:column;flex-shrink:1;width:100%;min-width:0}.e-con-inner{display:flex;flex-direction:inherit;justify-content:inherit;align-items:inherit;gap:inherit;width:100%;min-width:0;margin-inline:auto}.elementor-widget{position:relative;width:100%;min-width:0}.elementor-heading-title,p{padding:0;margin:0}.elementor-icon-list-items{list-style:none;margin:0;padding:0}.elementor-icon-list-item{display:flex;position:relative;align-items:center}.elementor-icon-list-item a{display:flex;align-items:center;width:100%;text-decoration:none}.elementor-icon-list-item span{display:inline-block}.elementor-inline-items{display:flex;flex-wrap:wrap}.elementor-button{display:inline-flex;align-items:center;justify-content:center;gap:10px;text-decoration:none}.native-bullet{margin-right:10px;font-size:10px}.review-photo-note{margin:auto;color:#D8D8E0;text-align:center;font-size:11px;padding:12px}'''
page = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Internal native-setting layout review</title><style>' + base + ''.join(rules) + '</style><body>' + body + '</body></html>'
Path('/tmp/syncs-whyus-native-review.html').write_text(page)
print('Rendered native-setting layout harness to /tmp (not included in templates or ZIP).')
