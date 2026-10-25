"""Build the supplied conference layout using native Elementor controls only."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "scega-permit-native/validation/build_page.py"
spec = importlib.util.spec_from_file_location("existing_native_components", SOURCE)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
b.uid = lambda text: hashlib.sha256(("syncs-conference-2026-10/" + text).encode()).hexdigest()[:8]
C = b.C
box, row, panel, size, dim, gap, width, font = b.box, b.row, b.panel, b.size, b.dim, b.gap, b.width, b.font
widget, paragraph, walk = b.widget, b.paragraph, b.walk
PAGE = "SYNCs-SCEGA-Conference-Native-Page.json"
CONTACT = "https://syncs.com.sa/contact-us/"
WHATSAPP = "https://api.whatsapp.com/send/?phone=966565006560"
BRIEF = "#cf-conference-brief"


def heading(label, text, n=32, tag="h2", color=None, **extra):
    return b.heading(label, text, n, tag, color,
                     **{"typography_font_size_mobile": size(min(n, 27)), **extra})


def action(label, text, url=BRIEF, secondary=False, **extra):
    return b.action(label, text, url, secondary,
        **{"background_color": C["bg"] + "00" if secondary else C["accent"],
           "button_text_color": C["lavender"] if secondary else C["bg"],
           "button_background_hover_color": C["lavender"], "hover_color": C["bg"],
           "border_color": C["accent"], "border_radius": dim(4), "text_padding": dim(12, 20), **extra})


def section(slug, title, children, alt=False, **extra):
    return b.section(slug, title, children,
        **{"background_color": C["panel"] if alt else C["bg"],
           "padding": dim(28, 24), "padding_mobile": dim(26, 20), "flex_gap": gap(20), **extra})


def icon_box(label, title, copy, icon, n=17, **extra):
    return b.icon_box(label, title, copy, icon, n,
        **{"primary_color": C["accent"], "icon_size": size(32), **extra})


def photo(label, media, height, **extra):
    return b.photo(label, media, height, **extra)


def accordion(label, entries):
    element = b.accordion(label, entries)
    element["settings"].update(default_state="expanded", normal_title_color=C["white"],
        active_title_color=C["white"], accordion_padding=dim(15, 18),
        accordion_background_hover_color=C["line"],
        accordion_item_title_icon={"value": "fas fa-plus", "library": "fa-solid"},
        accordion_item_title_icon_active={"value": "fas fa-minus", "library": "fa-solid"},
        accordion_item_title_space_between=size(0), accordion_border_radius=dim(3))
    return element


def header():
    logo = box("Header logo", [heading("Header wordmark", "SYNC", 28, "div")], **width(18, 40, 40))
    nav = box("Header navigation", [b.list_widget("Header links", ["Services", "SCEGA Permits", "Projects", "About"],
        inline=True, links=["#cf-services", "#cf-scope", "#cf-experience", "#cf-why-sync"],
        icon_typography_font_size=size(13), space_between=size(30))],
        **width(51), _flex_order_tablet="end", html_tag="nav")
    cta = box("Header CTA", [action("Header discuss", "Discuss Your Conference", arrow=False, align="right",
        typography_font_size=size(12), text_padding=dim(11, 18))], **width(26, 55, 55))
    return section("cf-header", "Header", [row("Header row", [logo, nav, cta], flex_direction_tablet="row",
        flex_wrap="wrap", flex_gap=gap(16), flex_align_items="center", flex_justify_content="space-between")],
        html_tag="header", padding=dim(15, 24), border_border="solid", border_width=dim(0, 0, 1, 0), border_color=C["line"])


def hero():
    left = box("Hero copy", [
        heading("Hero eyebrow", "SYNC · CONFERENCE PERMIT APPLICATION SUPPORT", 11, "p", C["lavender"], typography_letter_spacing=size(1.4)),
        heading("Conference H1", "SCEGA Conference Permit Support in Saudi Arabia", 52, "h1",
            typography_font_size_tablet=size(44), typography_font_size_mobile=size(35), typography_line_height=size(1.06, "em")),
        heading("Hero promise", "A clear plan for your conference application.", 21, "p"),
        paragraph("Hero description", "Classification review, document preparation and application follow-up for conferences in Saudi Arabia.", 15),
        row("Hero actions", [action("Discuss requirements", "Discuss Your Requirements"),
            action("Send conference brief", "Send Your Conference Brief", secondary=True, arrow=False)],
            flex_direction_tablet="row", flex_wrap="wrap", flex_gap=gap(14)),
    ], **width(47), flex_gap=gap(18), flex_justify_content="center")
    image = widget("image", "Conference hero photo", image={"url": "https://syncs.com.sa/wp-content/uploads/2026/09/CL-94.jpg", "id": "", "alt": "Conference event — SYNC"},
        image_size="full", width=size(100, "%"), height=size(390), height_mobile=size(260), **{"object-fit": "cover"},
        image_border_border="solid", image_border_width=dim(1), image_border_color=C["accent"], image_border_radius=dim(9))
    right = box("Hero media", [image], **width(50), flex_justify_content="center", background_background="classic", background_color=C["panel"], border_radius=dim(9))
    benefits = []
    for title, icon in [("Classification Review", "file-alt"), ("Document Preparation", "folder-open"), ("Application Follow-Up", "users")]:
        benefits.append(box("Hero benefit " + title, [icon_box("Hero benefit content " + title, title, "", icon, 14,
            position="left", icon_size=size(24), icon_space=size(12), title_bottom_space=size(0))], **width(31, 48, 100)))
    return section("cf-hero", "Conference hero", [row("Hero columns", [left, right], flex_gap=gap(30), flex_justify_content="space-between"),
        row("Hero benefit row", benefits, flex_direction_tablet="row", flex_wrap="wrap", flex_gap=gap(16))], padding=dim(34, 24, 24, 24))


def clients():
    # Text wordmarks avoid guessing media URLs lost in the uploaded ZIP export.
    names = [("DELL", 29), ("intel", 31), ("hp", 34), ("GROHE", 24), ("paloalto", 25)]
    items = [box("Client names intro", [heading("Clients label", "Businesses We Have Supported", 18, "p", C["silver"])], **width(29, 100, 100))]
    for name, n in names:
        items.append(box("Client name " + name, [heading("Client wordmark " + name, name, n, "div", align="center")],
            **width(12, 17, 45), flex_justify_content="center"))
    return section("cf-clients", "Business names", [row("Business names row", items, flex_direction_tablet="row", flex_wrap="wrap",
        flex_gap=gap(16), flex_align_items="center", flex_justify_content="space-between")], alt=True, padding=dim(28, 24))


def classification():
    intro = box("Classification introduction", [heading("Classification heading", "What Support Does Your Conference Need?", 32),
        paragraph("Classification intro", "Every conference is different. We review your plans to understand the right category and requirements for your application.")], **width(35), flex_gap=gap(14))
    cells = []
    data = [("Your event format", "Is it a local or international conference, and what is the main focus?"),
            ("Your organizing entity", "Are you a company, association or international organization?"),
            ("Your accompanying activities", "Will you have sponsor booths, exhibitions or additional activities?")]
    for i, (title, description) in enumerate(data, 1):
        cells.append(box("Classification point " + str(i), [heading("Classification number " + str(i), f"{i:02d}", 20, "p", C["lavender"]),
            heading("Classification title " + str(i), title, 18, "h3"), paragraph("Classification description " + str(i), description, 14)],
            **width(20), padding=dim(0, 0, 0, 22), padding_mobile=dim(0), flex_gap=gap(12),
            border_border="solid", border_width=dim(0, 0, 0, 1), border_color=C["line"]))
    return section("cf-classification", "Conference classification", [row("Classification columns", [intro] + cells, flex_gap=gap(24), flex_justify_content="space-between")])


def preparation():
    data = [("Organizer", "Details about your organizing entity and event partners.", "user"),
        ("Programme", "Conference theme, agenda and session details.", "file-alt"),
        ("Speakers", "List of local and international speakers.", "users"),
        ("Venue & Attendance", "Venue information and expected number of attendees.", "map-marker-alt"),
        ("Dates", "Proposed conference dates and duration.", "calendar-alt"),
        ("Sponsors & Activities", "Sponsor booths, exhibitions and accompanying activities.", "handshake")]
    cards = [panel("Preparation " + title, [icon_box("Preparation content " + title, title, copy, icon,
        position="left", icon_space=size(18))], **width(32, 48, 100), padding=dim(22), border_radius=dim(5)) for title, copy, icon in data]
    return section("cf-prepare", "Conference application preparation", [heading("Preparation heading", "What to Prepare for Your Application"),
        row("Six preparation cards", cards, flex_direction_tablet="row", flex_wrap="wrap", flex_gap=gap(18), flex_justify_content="space-between")], alt=True)


SCOPE = [("Classification & Eligibility", "We review your conference plans, including format, activities and organizing entity, to identify the applicable category and eligibility requirements."),
    ("Application File Preparation", "We help coordinate the organizer details, programme, speaker information, venue and supporting documents needed for the application."),
    ("Submission Coordination", "We support the submission process and keep the information consistent. The authority reviews the application and issues its decision."),
    ("Follow-Up & Corrections", "We help coordinate responses to additional information requests, application corrections and supporting documents during review."),
    ("Changes & Cancellation", "If the dates, venue or event scope change, we review the update and help coordinate the relevant amendment or cancellation steps.")]


def scope():
    intro = box("Scope introduction", [heading("Scope eyebrow", "OUR APPROACH", 11, "p", C["lavender"], typography_letter_spacing=size(1.5)),
        heading("Scope heading", "What Our Conference Permit Service Covers", 36),
        paragraph("Scope introduction copy", "We manage the key steps in your conference permit application, from classification and document preparation to submission and follow-up.", 17)],
        **width(43), flex_gap=gap(16))
    details = box("Scope accordion column", [accordion("Conference service scope", SCOPE)], **width(53))
    return section("cf-scope", "Conference permit scope", [row("Scope two columns", [intro, details], flex_gap=gap(32), flex_justify_content="space-between")])


def fees():
    data = [("Government fees", "Local: SAR 5,000 · International: SAR 10,000", "database"),
        ("SYNC service scope", "Quoted for your requirements.", "file-alt"),
        ("Published service time", "5 working days", "clock")]
    cards = [box("Fee column " + str(i), [icon_box("Fee content " + str(i), title, copy, icon, position="left",
        title_color=C["bg"], description_color=C["bg"], primary_color=C["panel"], icon_space=size(22))],
        **width(31), padding=dim(8, 12), flex_gap=gap(12)) for i, (title, copy, icon) in enumerate(data)]
    return section("cf-fees", "Conference fees and timelines", [heading("Fee heading", "Conference Permit Fees & Timelines", 32, color=C["bg"]),
        row("Three fee columns", cards, flex_gap=gap(20), flex_justify_content="space-between"),
        paragraph("Fee note", "Government fees and published service time are subject to the applicable category. Preparation and additional review may take longer.", 12, text_color=C["ink"])],
        background_color=C["lavender"], padding=dim(26, 24), flex_gap=gap(18))


def multi_activity():
    data = [("Overseas Organizers & Speakers", "Additional requirements for international participants.", "globe"),
        ("Sponsor Booths & Exhibitions", "Guidance on exhibiting and sponsorship activities.", "store"),
        ("Healthcare & Professional Events", "Support for sector-specific conference requirements.", "stethoscope"),
        ("Hybrid & Additional Activities", "Including virtual sessions and other related activities.", "desktop")]
    cards = [panel("Multi activity " + str(i), [icon_box("Multi activity content " + str(i), title, copy, icon, 16)],
        **width(23.5, 48, 100), padding=dim(20), border_radius=dim(5)) for i, (title, copy, icon) in enumerate(data)]
    return section("cf-multi-activity", "International and multi activity conferences", [heading("Multi activity heading", "Planning an International or Multi-Activity Conference?", 32),
        row("Four multi activity cards", cards, flex_direction_tablet="row", flex_wrap="wrap", flex_gap=gap(18), flex_justify_content="space-between")])


def why_sync():
    mark = box("Why SYNC marker", [heading("Why SYNC eyebrow", "OUR APPROACH / SYNC", 11, "p", C["lavender"]),
        heading("Why SYNC mark", "15+", 56, "div", C["lavender"], typography_font_size_mobile=size(44)), paragraph("Why SYNC marker copy", "Years in Events", 15)],
        **width(17), flex_gap=gap(14), flex_justify_content="center")
    intro = box("Why SYNC introduction", [heading("Why SYNC heading", "Permit Support with the Conference in Mind", 30),
        paragraph("Why SYNC copy", "We understand both the permit process and the practical needs of delivering a successful conference in Saudi Arabia.", 16)],
        **width(34), flex_gap=gap(16), flex_justify_content="center")
    options = [heading("Support options heading", "Choose the support that fits your plans:", 14, "p")]
    for i, text in enumerate(["Permit support only", "Permit + conference delivery", "Permit + sponsor booth build", "Permit + registration & guests"]):
        options.append(panel("Support option " + str(i), [b.list_widget("Support option content " + str(i), [text], icon="arrow-circle-right",
            links=[BRIEF], text_color=C["white"], icon_typography_font_size=size(13), space_between=size(0))],
            padding=dim(11, 15), border_radius=dim(3), background_color=C["line"] if i == 0 else C["panel"]))
    choices = box("Support options", options, **width(44), flex_gap=gap(0))
    return section("cf-why-sync", "Why SYNC", [row("Why SYNC columns", [mark, intro, choices], flex_gap=gap(26), flex_justify_content="space-between")], alt=True)


def services():
    data = [("Production & Sponsor Booths", "Design and build sponsor booths and branded environments.", "stand"),
        ("Registration & On-Site Coordination", "Delegate registration, badge collection and on-site support.", "meeting"),
        ("AVL & Technical Production", "Audio visual, lighting and full technical production.", "stand"),
        ("Delegate Acquisition", "Support with delegate marketing and acquisition.", "guests"),
        ("Hotel Booking & Visa Support", "Assistance with hotel accommodation and visa support for international guests.", "tables")]
    cards = []
    for i, (title, copy, media) in enumerate(data):
        image = photo("Conference service photo " + str(i), media, 135, min_height_mobile=size(175), border_radius=dim(0))
        content = box("Conference service copy " + str(i), [heading("Conference service title " + str(i), title, 18, "h3"),
            paragraph("Conference service description " + str(i), copy, 14),
            action("Conference service link " + str(i), "Discuss this service", secondary=True, typography_font_size=size(12), text_padding=dim(6, 10))],
            padding=dim(18), flex_gap=gap(10))
        cards.append(panel("Conference service card " + str(i), [image, content], **width(32 if i < 3 else 49, 48, 100),
            padding=dim(0), flex_gap=gap(0), border_radius=dim(5), overflow="hidden"))
    return section("cf-services", "Services beyond the conference permit", [heading("Services heading", "Conference Services Beyond the Permit", 32),
        row("Five conference service cards", cards, flex_direction_tablet="row", flex_wrap="wrap", flex_gap=gap(18), flex_justify_content="space-between")])


def posts(label, source, count, columns, image_percent, title_size):
    # Classic skin is a native presentation of the Posts widget present in #6970.
    return widget("posts", label, _skin="classic", posts_post_type=source,
        posts_select_date="anytime", posts_orderby="post_date", posts_order="desc", posts_include=[], posts_include_term_ids=[],
        classic_columns=str(columns), classic_columns_tablet="1" if columns == 1 else "2", classic_columns_mobile="1",
        classic_posts_per_page=count, classic_thumbnail="left", classic_thumbnail_size_size="large",
        classic_image_width=size(image_percent, "%"), classic_image_width_mobile=size(100, "%"),
        classic_item_ratio=size(.55), classic_masonry="", classic_image_spacing=size(20),
        classic_img_border_radius=dim(4), classic_show_title="yes", classic_title_tag="h3",
        classic_show_excerpt="yes", classic_excerpt_length=20 if columns == 1 else 13,
        classic_meta_data=[], classic_show_read_more="yes", classic_read_more_text="Explore the Project →" if source == "project" else "Read Guide →",
        classic_title_color=C["white"], classic_excerpt_color=C["silver"], classic_read_more_color=C["lavender"],
        classic_title_spacing=size(12), classic_excerpt_spacing=size(12),
        classic_column_gap=size(24), classic_row_gap=size(24),
        classic_box_bg_color=C["panel"] if columns == 1 else C["bg"],
        classic_box_border_color=C["line"], classic_box_border_width=dim(0),
        classic_box_border_radius=size(4), classic_content_padding=dim(12),
        pagination_type="",
        **font("classic_title_typography", title_size, "600", 1.25),
        **font("classic_excerpt_typography", 14, "400", 1.5),
        **font("classic_read_more_typography", 13, "600", 1.3))


def experience():
    return section("cf-experience", "Relevant conference experience", [heading("Experience heading", "Relevant Conference Experience", 32),
        posts("Dynamic conference project", "project", 1, 1, 55, 25)], alt=True)


FAQS = [("Does a one-day conference need a permit?", "The permit route depends on the conference category and activities, not only its duration. We review the event brief to identify the applicable requirements."),
    ("Can our company apply directly?", "The organizing entity’s eligibility and the application route depend on the relevant category. We help review those details and the supporting information."),
    ("What information should we prepare?", "Start with organizer details, the programme, speakers, proposed venue, attendance and dates, plus any sponsors or accompanying activities."),
    ("Can we include sponsor booths?", "Include all sponsor booths, exhibitions and accompanying activities in the brief so their requirements can be considered in the application review."),
    ("Can SYNC support overseas speakers?", "We can coordinate event information and relevant guest arrangements, including visa application support where applicable. Entry and permit decisions remain with the authorities."),
    ("What if our conference details change?", "Tell us when dates, venue, programme or activities change. We review the update and help coordinate the relevant correction, amendment or cancellation steps.")]


def conference_form():
    element = b.form()
    element["id"] = b.uid("Conference brief form")
    s = element["settings"]
    s.update(_title="Native conference brief form", form_name="SYNC Conference Permit Brief", button_text="Send Your Conference Brief",
        button_background_color=C["accent"], button_background_hover_color=C["lavender"],
        field_background_color=C["panel"], field_border_color=C["line"], row_gap=size(14), column_gap=size(16),
        label_spacing=size(6), button_text_padding=dim(13, 20))
    specs = [
        ("name", "text", "Full name", "Full name", True, "50"),
        ("email", "email", "Work email", "you@company.com", True, "50"),
        ("company", "text", "Company", "Company", True, "50"),
        ("city_date", "text", "City & event date", "City and proposed date", False, "50"),
        ("attendance", "select", "Expected attendance", "Select attendance", False, "50"),
        ("support", "select", "Support required", "Select support", True, "50"),
        ("brief", "textarea", "Conference brief", "Tell us about your conference, including format, proposed dates and any specific requirements.", True, "100"),
    ]
    fields = []
    for key, kind, label, placeholder, required, field_width in specs:
        field = {"_id": b.uid("Conference field " + key), "custom_id": key, "field_type": kind, "field_label": label,
            "placeholder": placeholder, "required": "true" if required else "", "width": field_width,
            "width_tablet": field_width, "width_mobile": "100"}
        if key == "attendance": field["field_options"] = "Select attendance|\nUnder 100|under_100\n100–300|100_300\n301–500|301_500\n501–1,000|501_1000\nOver 1,000|over_1000"
        if key == "support": field["field_options"] = "Select support|\nPermit support only|permit_only\nPermit + conference delivery|conference_delivery\nPermit + sponsor booth build|sponsor_booths\nPermit + registration & guests|registration_guests"
        if kind == "textarea": field["rows"] = 4
        fields.append(field)
    s["form_fields"] = fields
    return element


def faq_brief():
    left = box("Conference FAQ column", [heading("Conference FAQ heading", "SCEGA Conference Permit Questions", 32),
        accordion("Conference permit FAQs", FAQS)], **width(57), flex_gap=gap(20))
    right = box("Conference brief column", [heading("Conference brief eyebrow", "GET IN TOUCH", 11, "p", C["lavender"]),
        heading("Conference brief heading", "Tell Us About Your Conference", 32),
        paragraph("Conference brief introduction", "Share a few details and our team will discuss the next steps with you.", 14),
        conference_form(), paragraph("Authority decision note", "SYNC supports applications. The authority issues licences.", 12)],
        **width(39), flex_gap=gap(14), _element_id="cf-conference-brief")
    return section("cf-questions", "Conference questions and brief", [row("FAQ and conference brief", [left, right], flex_gap=gap(32), flex_justify_content="space-between")])


def guides():
    return section("cf-guides", "Conference permit planning guides", [heading("Guides heading", "Conference Permit Planning Guides", 32),
        paragraph("Guides introduction", "Helpful insights for a smoother application process.", 14),
        posts("Dynamic conference planning guides", "post", 3, 3, 35, 18)])


def final_cta():
    title = box("Final CTA title", [heading("Final CTA heading", "Discuss Your Conference Permit Requirements", 28, color=C["bg"])], **width(31))
    copy = box("Final CTA copy", [paragraph("Final CTA description", "Get expert support for your SCEGA conference application and start planning with confidence.", 15, text_color=C["bg"])], **width(34))
    actions = box("Final CTA actions", [action("Final talk to SYNC", "Talk to SYNC", CONTACT, background_color=C["bg"], button_text_color=C["white"],
        border_color=C["bg"], button_background_hover_color=C["panel"], hover_color=C["white"]),
        action("Final WhatsApp link", "Chat on WhatsApp", WHATSAPP, secondary=True, background_color=C["bg"] + "00", button_text_color=C["bg"],
            border_color=C["bg"], button_background_hover_color=C["soft"], hover_color=C["bg"], arrow=False)], **width(28), flex_gap=gap(12))
    return section("cf-final-cta", "Conference final CTA", [row("Final CTA row", [title, copy, actions], flex_gap=gap(24), flex_align_items="center", flex_justify_content="space-between")],
        background_color=C["lavender"], padding=dim(25, 24))


def footer():
    logo = box("Footer wordmark and promise", [heading("Footer logo", "SYNC", 26, "div"), paragraph("Footer promise", "Events that move people forward.", 12)],
        **width(44), flex_direction="row", flex_direction_mobile="column", flex_align_items="center", flex_gap=gap(18))
    nav = box("Footer navigation", [b.list_widget("Footer links", ["Services", "SCEGA Permits", "Projects", "About"], inline=True,
        links=["#cf-services", "#cf-scope", "#cf-experience", "#cf-why-sync"], icon_typography_font_size=size(12), space_between=size(24))], **width(40), html_tag="nav")
    site = box("Footer site", [paragraph("Footer site name", "syncs.com.sa", 12)], **width(12))
    return section("cf-footer", "Footer", [row("Footer row", [logo, nav, site], flex_gap=gap(20), flex_align_items="center", flex_justify_content="space-between")],
        html_tag="footer", padding=dim(20, 24), border_border="solid", border_width=dim(1, 0, 0, 0), border_color=C["line"])


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    (ROOT / "sections").mkdir(parents=True, exist_ok=True)
    sections = [header(), hero(), clients(), classification(), preparation(), scope(), fees(), multi_activity(), why_sync(),
        services(), experience(), faq_brief(), guides(), final_cta(), footer()]
    page = {"content": [box("SYNC conference complete page", sections, background_background="classic", background_color=C["bg"])],
        "page_settings": [], "version": "0.4", "title": "SYNC — SCEGA Conference Permit — Native Page", "type": "page"}
    save(ROOT / PAGE, page)
    index = []
    for i, element in enumerate(sections, 1):
        filename = f"{i:02d}-" + element["settings"]["_element_id"] + ".json"
        save(ROOT / "sections" / filename, {"content": [element], "page_settings": [], "version": "0.4", "type": "container", "title": "SYNC — " + element["settings"]["_title"]})
        index.append({"file": "sections/" + filename, "label": element["settings"]["_title"], "anchor": element["settings"]["_element_id"]})
    save(ROOT / "validation/manifest.json", {"page": PAGE, "sections": index, "elements": len(list(walk(page["content"]))), "palette": C,
        "source": str(SOURCE.relative_to(ROOT.parent)), "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "status": "native saved templates; WordPress import/edit/re-export untested"})
    print(json.dumps({"page": PAGE, "sections": len(sections), "elements": len(list(walk(page["content"])))}))


if __name__ == "__main__":
    main()
