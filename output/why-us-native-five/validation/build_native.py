"""Native widgets only; replace Why Us, preserving the first three source sections."""
import copy
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "brand-sections-6941/SYNCs-Sections-6941-Brand-Colors.json"
SERVICES = json.loads((ROOT / "services.json").read_text())
COLORS = dict(midnight="#1D162A", royal="#8F7BB8", dark="#2B203D", charcoal="#3A3447",
              lavender="#C9BCE3", gray="#F5F5F7", soft="#FAFAFC", silver="#D8D8E0",
              white="#FFFFFF", graphite="#4A4557")
CONTACT = "https://syncs.com.sa/contact-us/"


def uid(label):
    return hashlib.sha256(("syncs-native-whyus-five-v1/" + label).encode()).hexdigest()[:7]


def scalar(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}


def dims(top=0, right=None, bottom=None, left=None):
    right = top if right is None else right
    bottom = top if bottom is None else bottom
    left = right if left is None else left
    return {"unit": "px", "top": str(top), "right": str(right), "bottom": str(bottom),
            "left": str(left), "isLinked": top == right == bottom == left}


def gap(size):
    return {"unit": "px", "column": str(size), "row": str(size), "isLinked": True, "size": size}


def typography(prefix="typography", size=16, weight="400", line=1.65):
    return {prefix + "_typography": "custom", prefix + "_font_family": "Manrope",
            prefix + "_font_size": scalar(size), prefix + "_font_weight": weight,
            prefix + "_line_height": scalar(line, "em")}


def container(label, children, **settings):
    base = {"content_width": "full", "flex_direction": "column", "flex_gap": gap(0),
            "padding": dims(0), "_title": label}
    base.update(settings)
    return {"id": uid(label), "elType": "container", "settings": base,
            "elements": children, "isInner": False}


def widget(kind, label, **settings):
    return {"id": uid(label), "elType": "widget", "widgetType": kind,
            "settings": {"_title": label, **settings}, "elements": [], "isInner": False}


def heading(label, title, tag="h3", size=28, weight="700", **extra):
    settings = {"title": title, "header_size": tag, "title_color": COLORS["graphite"],
                **typography(size=size, weight=weight, line=1.2), **extra}
    return widget("heading", label, **settings)


def icon_list(label, texts, bullet=False, links=None, **extra):
    items = []
    for i, text in enumerate(texts):
        item = {"_id": uid(label + str(i)), "text": text,
                "selected_icon": {"value": "fas fa-circle" if bullet else "",
                                  "library": "fa-solid" if bullet else ""}}
        if links:
            item["link"] = {"url": links[i], "is_external": "", "nofollow": "", "custom_attributes": ""}
        items.append(item)
    settings = {"icon_list": items, "text_color": COLORS["graphite"], "icon_color": COLORS["graphite"],
                "icon_size": scalar(4 if bullet else 0), "text_indent": scalar(10 if bullet else 0),
                "space_between": scalar(8), **typography("icon_typography", size=14), **extra}
    return widget("icon-list", label, **settings)


def card(service, index):
    slug = service["slug"]
    code = f"P.{index:02d}"
    title = heading(slug + " title", service["title"], typography_font_size_mobile=scalar(23),
                    _element_width="auto")
    meta = heading(slug + " code", code + " / SYNC SERVICES", tag="p", size=10, weight="500",
                   typography_letter_spacing=scalar(1), align="right", align_mobile="left",
                   _element_width="auto")
    header = container(slug + " header", [title, meta], flex_direction="row",
                       flex_justify_content="space-between", flex_align_items="center",
                       flex_gap=gap(16), flex_direction_mobile="column", flex_align_items_mobile="flex-start")
    body_text = widget("text-editor", slug + " description", editor="<p>" + html.escape(service["description"]) + "</p>",
                       text_color=COLORS["graphite"], **typography(size=16))
    tags = icon_list(slug + " tags", service["tags"], view="inline")
    notes = container(slug + " details", [
        heading(slug + " caption", "YOUR EVENT, CONNECTED /", tag="p", size=10, weight="500",
                typography_letter_spacing=scalar(1.1)),
        icon_list(slug + " points", service["points"], bullet=True),
    ], width=scalar(54, "%"), width_mobile=scalar(100, "%"), padding=dims(24),
       background_background="classic", background_color=COLORS["gray"], border_radius=dims(16),
       flex_gap=gap(12), min_height=scalar(205))
    photo = container(slug + " photo", [], width=scalar(42, "%"), width_mobile=scalar(100, "%"),
                      background_background="classic", background_color=COLORS["dark"],
                      background_image={"id": service["media_id"], "url": service["image_url"]},
                      background_size="cover", background_position="center center",
                      border_radius=dims(16), min_height=scalar(205), min_height_mobile=scalar(210))
    media = container(slug + " details and photo", [notes, photo], flex_direction="row",
                      flex_justify_content="space-between", flex_gap=gap(20), flex_align_items="stretch",
                      flex_direction_mobile="column")
    button = widget("button", slug + " contact", text="Discuss this service",
                    link={"url": CONTACT, "is_external": "", "nofollow": "", "custom_attributes": ""},
                    selected_icon={"value": "fas fa-arrow-right", "library": "fa-solid"},
                    icon_align="row-reverse", icon_indent=scalar(8), align="right", align_mobile="left",
                    background_background="classic", background_color=COLORS["white"],
                    button_text_color=COLORS["graphite"], button_background_hover_background="classic",
                    button_background_hover_color=COLORS["lavender"], hover_color=COLORS["midnight"],
                    border_border="solid", border_color=COLORS["silver"], border_width=dims(1),
                    border_radius=dims(30), text_padding=dims(14, 24),
                    **typography(size=14, weight="600", line=1.3))
    return container(slug + " service card", [header, body_text, tags, media, button],
                     html_tag="article", _element_id="sx-whyus-" + slug,
                     padding=dims(40), padding_tablet=dims(32), padding_mobile=dims(24),
                     background_background="classic", background_color=COLORS["white"],
                     border_radius=dims(24), flex_gap=gap(18))


def section():
    title = container("Why Us title", [
        heading("Why Us line one", "Five ways in.", tag="h2", size=64,
                typography_font_size_tablet=scalar(48), typography_font_size_mobile=scalar(36),
                typography_line_height=scalar(1.07, "em"), typography_letter_spacing=scalar(-2)),
        heading("Why Us line two", "One way of working.", tag="div", size=64,
                typography_font_size_tablet=scalar(48), typography_font_size_mobile=scalar(36),
                typography_line_height=scalar(1.07, "em"), typography_letter_spacing=scalar(-2)),
    ])
    navigation = icon_list("Five services navigation",
                           [f"P.{i:02d}\u2002 {s['title']}" for i, s in enumerate(SERVICES, 1)],
                           links=["#sx-whyus-" + s["slug"] for s in SERVICES],
                           link_click="full_width", divider="yes", divider_style="solid",
                           divider_weight=scalar(1), divider_color=COLORS["silver"],
                           divider_width=scalar(100, "%"), text_color_hover=COLORS["midnight"],
                           space_between=scalar(4), _padding=dims(2, 14),
                           icon_typography_font_size=scalar(16), icon_typography_font_weight="500",
                           icon_typography_line_height=scalar(3, "em"))
    nav = container("Service navigation", [navigation], html_tag="nav", width=scalar(31.5, "%"),
                    width_tablet=scalar(100, "%"), padding=dims(12), border_radius=dims(20),
                    background_background="classic", background_color=COLORS["soft"],
                    sticky="top", sticky_on=["desktop"], sticky_offset=120, sticky_parent="yes")
    cards = container("Service cards", [card(s, i) for i, s in enumerate(SERVICES, 1)],
                      width=scalar(63.5, "%"), width_tablet=scalar(100, "%"), flex_gap=gap(18))
    layout = container("Services two columns", [nav, cards], flex_direction="row", flex_gap=gap(40),
                       flex_justify_content="space-between", flex_align_items="flex-start",
                       flex_direction_tablet="column", flex_gap_tablet=gap(24),
                       flex_align_items_tablet="stretch")
    return container("Why Us — five services", [title, layout], html_tag="section", content_width="boxed",
                     boxed_width=scalar(1296), padding=dims(40, 24, 80, 24),
                     padding_tablet=dims(48, 24, 64, 24), padding_mobile=dims(36, 20, 48, 20),
                     background_background="classic", background_color=COLORS["gray"], flex_gap=gap(32))


def main():
    original = json.loads(SOURCE.read_text())
    result = copy.deepcopy(original)
    native = section()
    result["content"][-1] = native
    result["title"] = "SYNCs — All Sections + Native Why Us (5 Services)"
    result_file = ROOT / "SYNCs-All-Sections-Native-Why-Us.json"
    result_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    standalone = {"content": [native], "page_settings": [], "version": original["version"],
                  "title": "SYNCs — Native Why Us — 5 Services", "type": "container"}
    (ROOT / "SYNCs-Why-Us-Native-5-Services.json").write_text(json.dumps(standalone, ensure_ascii=False, indent=2) + "\n")
    print('Built complete template and standalone Why Us; native widgets only.')


if __name__ == "__main__":
    main()
