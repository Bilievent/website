"""Internal palette review only; does not emulate Elementor layout or motion."""
import html
import json
from pathlib import Path

from build_brand import ROOT, walk

j = json.loads((ROOT / "SYNCs-Sections-6941-Brand-Colors.json").read_text())
parts = []
for number, section in enumerate(j["content"]):
    elements = list(walk([section]))
    find = lambda kind: next(e["settings"] for e in elements if e.get("widgetType") == kind)
    headline = find("animated-headline")
    button = find("button")
    background = {0: "#1D162A", 1: "#FAFAFC", 2: "#1D162A", 3: "#F5F5F7"}[number]
    paragraph = next(e["settings"] for e in elements if e.get("widgetType") == "text-editor" and isinstance(e["settings"], dict) and e["settings"].get("editor"))
    cards = [e["settings"] for e in elements if e.get("widgetType") == "icon-box"][:3]
    cards_html = "".join(
        '<article style="color:' + c["description_color"] + ';background:' + c["_background_color"] + '">'
        '<h3 style="color:' + c["title_color"] + '">' + html.escape(c["title_text"]) + '</h3>'
        '<p>' + html.escape(c["description_text"]) + '</p></article>' for c in cards)
    tabs_html = ""
    if number == 3:
        tabs = find("nested-tabs")
        tabs_html = '<div class="tabs" style="--tab-text:' + tabs["title_text_color"] + ';--tab-bg:' + tabs["tabs_title_background_color_color"] + ';--tab-hover:' + tabs["tabs_title_background_color_hover_color"] + ';--tab-hover-text:' + tabs["title_text_color_hover"] + ';--tab-border:' + tabs["tabs_title_border_color"] + '">' + ''.join('<button class="tab">' + html.escape(t["tab_title"]) + '</button>' for t in tabs["tabs"]) + '</div>'
    title = html.escape(headline["before_text"]) + ' <em style="color:' + headline["words_color"] + '">' + html.escape(headline["highlighted_text"]) + '</em> ' + html.escape(headline["after_text"])
    parts.append('<section style="background:' + background + ';color:' + headline["title_color"] + '">'
                 '<div class="inner"><small>SECTION ' + str(number + 1) + ' / NATIVE COLOR VALUES</small>'
                 '<h2>' + title + '</h2><div class="copy" style="color:' + paragraph["text_color"] + '">' + paragraph["editor"] + '</div>'
                 '<button class="cta" style="--button-bg:' + button["background_color"] + ';--button-text:' + button["button_text_color"] + ';--button-hover:' + button["button_background_hover_color"] + ';--button-hover-text:' + button["hover_color"] + '">' + html.escape(button["text"]) + ' ↗</button>'
                 + tabs_html + '<div class="cards">' + cards_html + '</div></div></section>')
css = '''*{box-sizing:border-box}body{margin:0;font:16px/1.6 Arial,sans-serif;background:#1D162A}.notice{padding:16px 24px;background:#C9BCE3;color:#1D162A;font-size:13px}section{padding:64px 24px}.inner{max-width:1120px;margin:auto;min-width:0}small{font-size:12px;letter-spacing:2px}h2{font-size:40px;line-height:1.2;max-width:800px;margin:24px 0}em{font-family:Georgia,serif}.copy{max-width:620px}button{font:700 15px Arial,sans-serif;cursor:pointer}.cta{background:var(--button-bg);color:var(--button-text);border:0;border-radius:28px;padding:16px 26px;margin-top:12px}.cta:hover,.cta:focus-visible{background:var(--button-hover);color:var(--button-hover-text)}button:focus-visible{outline:3px solid #8F7BB8;outline-offset:4px}.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:32px}article{border-radius:24px;padding:30px;min-width:0}article h3{font-size:23px;line-height:1.3;margin-top:0}.tabs{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}.tab{padding:16px;border:0;border-bottom:1px solid var(--tab-border);background:var(--tab-bg);color:var(--tab-text)}.tab:hover,.tab:focus-visible{background:var(--tab-hover);color:var(--tab-hover-text)}@media(max-width:900px){h2{font-size:34px}.cards{grid-template-columns:1fr 1fr}}@media(max-width:600px){section{padding:40px 20px}h2{font-size:30px}.cards{grid-template-columns:1fr}.tabs{flex-direction:column}.notice{padding:12px 20px}}'''
document = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Internal native color review</title><style>' + css + '</style><body><aside class="notice">INTERNAL COLOR REVIEW ONLY — native JSON values in a separate test layout; no photos loaded. This is not an Elementor render or a preview of the preserved layout, icons, typography or motion.</aside>' + ''.join(parts) + '</body></html>'
(ROOT / "validation/color-review.html").write_text(document)
print('Built independent color review from native JSON controls.')
