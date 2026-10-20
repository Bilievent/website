"""Build a native, editable Elementor saved-template bundle; no custom frontend code."""
import copy
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / "brand-sections-6941/SYNCs-Sections-6941-Brand-Colors.json"
SOURCE = json.loads(BASE.read_text())
C = {"bg": "#1D162A", "accent": "#8F7BB8", "panel": "#2B203D", "line": "#3A3447",
     "lavender": "#C9BCE3", "gray": "#F5F5F7", "soft": "#FAFAFC", "silver": "#D8D8E0",
     "white": "#FFFFFF", "ink": "#4A4557"}
MEDIA = {
    "stand": {"id": 5608, "url": "https://syncs.com.sa/wp-content/uploads/2026/08/Watad-BIG-5-Exhibition-Stand.jpeg"},
    "banquet": {"id": "6342", "url": "https://syncs.com.sa/wp-content/uploads/2026/09/catering-for-events-banquet-decorated-table-table-setting-decoration.jpg"},
    "tables": {"id": "6341", "url": "https://syncs.com.sa/wp-content/uploads/2026/09/wedding-table-set-for-fine-dining-or-another-catered-event.jpg"},
    "guests": {"id": "6338", "url": "https://syncs.com.sa/wp-content/uploads/2026/09/organization-of-weddings-parties-catering-for-events-female-on-the-background-banquet-decorated-2.jpg"},
    "meeting": {"id": "6678", "url": "https://syncs.com.sa/wp-content/uploads/2026/10/couple-paying-for-catering.jpg"},
    "laptop": {"id": "6386", "url": "https://syncs.com.sa/wp-content/uploads/2026/09/young-handsome-waiter-servicing-black-girl-customer-with-laptop-in-cafe.jpg"},
}


def uid(label):
    return hashlib.sha256(("syncs-native-scega-page-v1/" + label).encode()).hexdigest()[:7]


def size(n, unit="px"):
    return {"unit": unit, "size": n, "sizes": []}


def dim(t=0, r=None, b=None, l=None):
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": t == r == b == l}


def gap(n):
    return {"unit": "px", "column": str(n), "row": str(n), "size": n, "isLinked": True}


def font(prefix="typography", n=15, weight="400", line=1.6):
    return {prefix + "_typography": "custom", prefix + "_font_family": "Manrope",
            prefix + "_font_size": size(n), prefix + "_font_weight": weight,
            prefix + "_line_height": size(line, "em")}


def box(label, children=None, **extra):
    settings = {"_title": label, "content_width": "full", "flex_direction": "column",
                "flex_gap": gap(0), "padding": dim(0), **extra}
    return {"id": uid(label), "elType": "container", "settings": settings, "elements": children or [], "isInner": False}


def widget(kind, label, **settings):
    return {"id": uid(label), "elType": "widget", "widgetType": kind,
            "settings": {"_title": label, **settings}, "elements": [], "isInner": False}


def heading(label, text, n=28, tag="h2", color=None, **extra):
    return widget("heading", label, **{"title": text, "header_size": tag, "title_color": color or C["white"],
                  **font(n=n, weight="600", line=1.18), **extra})


def paragraph(label, text, n=15, **extra):
    return widget("text-editor", label, **{"editor": "<p>" + html.escape(text) + "</p>",
                  "text_color": C["silver"], **font(n=n), **extra})


def action(label, text, url="#sx-event-brief", secondary=False, arrow=True, **extra):
    return widget("button", label, **{
        "text": text, "link": {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""},
        "selected_icon": {"value": "fas fa-arrow-right" if arrow else "", "library": "fa-solid" if arrow else ""},
        "icon_align": "row-reverse", "icon_indent": size(10), "align": "left",
        "_element_width": "inherit" if extra.get("align") == "right" else "auto",
        "background_background": "classic", "background_color": C["bg"] + "00" if secondary else C["lavender"],
        "button_text_color": C["lavender"] if secondary else C["bg"],
        "button_background_hover_background": "classic", "button_background_hover_color": C["accent"],
        "hover_color": C["bg"], "border_border": "solid", "border_width": dim(1),
        "border_color": C["accent"] if secondary else C["lavender"], "border_radius": dim(6),
        "text_padding": dim(13, 24), **font(n=14, weight="600", line=1.3), **extra})


def list_widget(label, texts, icon=None, inline=False, links=None, **extra):
    items = []
    for i, text in enumerate(texts):
        item = {"_id": uid(label + " item " + str(i)), "text": text,
                "selected_icon": {"value": "fas fa-" + icon if icon else "", "library": "fa-solid" if icon else ""}}
        if links:
            item["link"] = {"url": links[i], "is_external": "", "nofollow": "", "custom_attributes": ""}
        items.append(item)
    return widget("icon-list", label, **{"icon_list": items, "view": "inline" if inline else "traditional",
        "text_color": C["silver"], "text_color_hover": C["lavender"], "icon_color": C["lavender"],
        "icon_size": size(15), "text_indent": size(8 if icon else 0), "space_between": size(14 if inline else 10),
        "link_click": "full_width", **font("icon_typography", 14), **extra})


def panel(label, children, **extra):
    return box(label, children, **{"background_background": "classic", "background_color": C["panel"],
        "border_border": "solid", "border_width": dim(1), "border_color": C["line"],
        "border_radius": dim(10), "padding": dim(24), "flex_gap": gap(14), **extra})


def row(label, children, **extra):
    return box(label, children, **{"flex_direction": "row", "flex_direction_tablet": "column",
        "flex_gap": gap(24), "flex_align_items": "stretch", **extra})


def width(percent, tablet=100, mobile=100):
    return {"width": size(percent, "%"), "width_tablet": size(tablet, "%"), "width_mobile": size(mobile, "%")}


def section(slug, title, children, **extra):
    return box(title, children, **{"html_tag": "section", "_element_id": slug, "content_width": "boxed",
        "boxed_width": size(1296), "padding": dim(22, 24), "padding_mobile": dim(18, 20),
        "background_background": "classic", "background_color": C["bg"], "flex_gap": gap(20), **extra})


def photo(label, media="stand", height=240, **extra):
    return box(label, [], **{"background_background": "classic", "background_color": C["panel"],
        "background_image": copy.deepcopy(MEDIA[media]), "background_size": "cover",
        "background_position": "center center", "min_height": size(height),
        "border_radius": dim(8), **extra})


def icon_box(label, title, description, icon, n=17, **extra):
    return widget("icon-box", label, **{
        "selected_icon": {"value": "fas fa-" + icon, "library": "fa-solid"},
        "title_text": title, "description_text": description, "title_size": "h3",
        "position": "top", "text_align": "left", "icon_size": size(30), "icon_space": size(16),
        "primary_color": C["lavender"], "title_color": C["white"], "description_color": C["silver"],
        "title_bottom_space": size(10), **font("title_typography", n, "600", 1.3),
        **font("description_typography", 14, "400", 1.55), **extra})


def accordion(label, entries):
    items, children = [], []
    for i, (title, answer) in enumerate(entries, 1):
        items.append({"_id": uid(label + " item " + str(i)), "item_title": f"{i:02d}  {title}", "element_css_id": ""})
        children.append(box(label + " answer " + str(i), [paragraph(label + " answer copy " + str(i), answer, 14)],
                            padding=dim(18), background_background="classic", background_color=C["bg"]))
    element = widget("nested-accordion", label, items=items, default_state="all_collapsed", max_items_expended="one",
        title_tag="h3", accordion_item_title_position_horizontal="stretch",
        accordion_item_title_icon={"value": "fas fa-chevron-down", "library": "fa-solid"},
        accordion_item_title_icon_active={"value": "fas fa-chevron-up", "library": "fa-solid"},
        accordion_item_title_space_between=size(8), accordion_padding=dim(15, 18), accordion_border_radius=dim(6),
        normal_title_color=C["lavender"], hover_title_color=C["white"], active_title_color=C["white"],
        normal_icon_color=C["lavender"], hover_icon_color=C["white"], active_icon_color=C["white"],
        accordion_background_normal_background="classic", accordion_background_normal_color=C["panel"],
        accordion_background_hover_background="classic", accordion_background_hover_color=C["line"],
        accordion_background_active_background="classic", accordion_background_active_color=C["panel"],
        accordion_border_normal_border="solid", accordion_border_normal_width=dim(1), accordion_border_normal_color=C["line"],
        accordion_border_hover_border="solid", accordion_border_hover_width=dim(1), accordion_border_hover_color=C["accent"],
        accordion_border_active_border="solid", accordion_border_active_width=dim(1), accordion_border_active_color=C["accent"],
        **font("title_typography", 15, "500", 1.4))
    element["elements"] = children
    return element


def header(footer=False):
    prefix = "Footer" if footer else "Header"
    logo = heading(prefix + " wordmark", "SYNC", 24, "div", typography_letter_spacing=size(8), _element_width="auto")
    menu = list_widget(prefix + " navigation", ["Services", "About", "Projects", "Insights"], inline=True,
        links=["#sx-event-services", "#sx-service-scope", "#sx-experience", "#sx-permit-guides"],
        icon_typography_font_size=size(13), space_between=size(28), _element_width="auto")
    nav = box(prefix + " navigation wrapper", [menu], **width(58, 100, 100),
              html_tag="nav", _flex_order_tablet="end", flex_align_items="center")
    main = row(prefix + " row", [box(prefix + " logo", [logo], **width(20, 45, 45)), nav,
        box(prefix + " contact wrapper", [action(prefix + " contact", "Contact", "https://syncs.com.sa/contact-us/", arrow=False,
             align="right")], **width(18, 45, 45))],
        flex_direction_tablet="row", flex_wrap="wrap", flex_justify_content="space-between", flex_align_items="center", flex_gap=gap(16))
    result = section("sx-footer" if footer else "sx-header", prefix, [main], padding=dim(18, 24))
    result["settings"]["html_tag"] = "footer" if footer else "header"
    result["settings"].update(border_border="solid", border_color=C["line"], border_width=dim(1, 0, 0, 0) if footer else dim(0, 0, 1, 0))
    return result


def hero():
    copy_column = box("Hero copy", [
        heading("Hero eyebrow", "CONFERENCE & EXHIBITION PERMIT SUPPORT", 12, "p", C["lavender"], typography_letter_spacing=size(2)),
        heading("Page H1", "SCEGA Permit Support in Saudi Arabia", 54, "h1", typography_font_size_tablet=size(44), typography_font_size_mobile=size(36), typography_letter_spacing=size(-1)),
        heading("Hero promise", "Your next business event starts with a clear permit plan.", 20, "p", typography_line_height=size(1.4, "em")),
        paragraph("Hero description", "We help you navigate SCEGA permit requirements for conferences, exhibitions and business events across Saudi Arabia."),
        paragraph("Hero process", "From document preparation to submission and follow-up, our team helps you keep the application process clear and coordinated."),
        row("Hero actions", [action("Hero discuss event", "Discuss Your Event"), action("Hero permit review", "Permit Review", "#sx-service-scope", secondary=True, arrow=False)],
            flex_direction_tablet="row", flex_wrap="wrap", flex_gap=gap(16)),
        list_widget("Relevant authorities", ["Relevant authorities", "SCEGA", "GEA", "Ministry of Culture", "Balady"], inline=True,
                    icon_typography_font_size=size(11), space_between=size(22)),
    ], **width(48), flex_gap=gap(18))
    permit = panel("Editable permit readiness card", [
        icon_box("Permit readiness symbol", "Permit Readiness", "A clear checklist before you apply.", "file-alt", n=20,
                 title_color=C["bg"], description_color=C["ink"], primary_color=C["accent"]),
        list_widget("Permit card checklist", ["Event scope", "Application documents", "Venue and dates"], icon="check",
                    text_color=C["ink"], icon_color=C["accent"], icon_typography_font_size=size(12)),
    ], **width(53, 62, 80), background_color=C["soft"], border_color=C["silver"], padding=dim(24), border_radius=dim(10))
    image = photo("Hero event photo", height=490, min_height_mobile=size(350), **width(48),
                  padding=dim(24), flex_align_items="flex-end", flex_justify_content="flex-end")
    image["elements"] = [permit]
    return section("sx-permit-hero", "Hero", [row("Hero two columns", [copy_column, image], flex_justify_content="space-between", flex_align_items="center", flex_gap=gap(32))], padding=dim(34, 24, 26, 24))


def trust_strip():
    texts = ["Supporting event teams across Saudi Arabia", "Conferences", "Exhibitions", "Workshops", "Business Meetings"]
    cards = [box("Trust strip item " + str(i), [heading("Trust text " + str(i), text, 14, "p", C["silver"], align="center")],
                 **width(18.6, 48, 100), flex_justify_content="center") for i, text in enumerate(texts)]
    return section("sx-event-teams", "Event teams strip", [panel("Event teams strip panel", [row("Event types strip row", cards,
        flex_direction_tablet="row", flex_wrap="wrap", flex_gap=gap(16), flex_justify_content="space-between")], padding=dim(24))], padding=dim(0, 24, 10, 24))


PERMITS = [
    ("Conference", "Conference Permit Support", "Support for international and local conferences, from initial planning to permit approval.",
     ["Multi-day and single-day conferences", "Local and international participation", "Speaker, content and venue coordination"], "banquet"),
    ("Exhibition", "Exhibition Permit Support", "Coordinate your exhibition brief, exhibitor information and venue details for the appropriate permit route.",
     ["Trade and consumer exhibition formats", "Exhibitor and stand information", "Venue, dates and supporting documents"], "stand"),
    ("Workshop", "Workshop Permit Support", "Prepare a clear workshop brief covering its purpose, audience, programme and delivery arrangements.",
     ["Workshop scope and objectives", "Facilitator and attendee information", "Programme and venue coordination"], "meeting"),
    ("Training", "Training Event Support", "Review the event format and supporting information to identify the relevant application requirements.",
     ["Training format and intended audience", "Delivery schedule and speakers", "Review of the applicable permit route"], "laptop"),
    ("Business Meeting", "Business Meeting Support", "Bring the meeting brief, organizer information and venue arrangements into one coordinated plan.",
     ["Meeting purpose and scope", "Organizer and guest information", "Location, schedule and logistics"], "tables"),
]


def permits():
    tabs, children = [], []
    for i, (name, title, description, points, media) in enumerate(PERMITS, 1):
        tabs.append({"_id": uid("Permit tab " + str(i)), "tab_title": f"{i:02d}  {name}", "tab_icon": {"value": "", "library": ""}})
        text = box(name + " permit text", [heading(name + " permit title", title, 24, "h3"), paragraph(name + " permit description", description, 14),
            list_widget(name + " permit checklist", points, icon="check-circle", icon_typography_font_size=size(13)),
            action(name + " permit action", "Explore " + name + " Permit", "#sx-service-scope", secondary=True)],
            **width(48), padding=dim(28), flex_gap=gap(16))
        image = photo(name + " permit photo", media, 315, **width(50), min_height_mobile=size(230))
        children.append(row(name + " permit panel", [text, image], flex_gap=gap(0),
            background_background="classic", background_color=C["panel"], border_radius=dim(8), overflow="hidden"))
    settings = {
        "tabs": tabs, "tabs_direction": "inline-start", "tabs_direction_tablet": "inline-start", "tabs_direction_mobile": "block-start",
        "tabs_width": size(24, "%"), "tabs_width_tablet": size(28, "%"), "title_alignment": "start",
        "tabs_title_spacing": size(16), "tabs_title_spacing_mobile": size(10),
        "tabs_title_background_color_background": "classic", "tabs_title_background_color_color": C["panel"],
        "tabs_title_background_color_hover_background": "classic", "tabs_title_background_color_hover_color": C["line"],
        "tabs_title_background_color_active_background": "classic", "tabs_title_background_color_active_color": C["accent"],
        "title_text_color": C["silver"], "title_text_color_hover": C["white"], "title_text_color_active": C["bg"],
        "tabs_title_border_border": "solid", "tabs_title_border_width": dim(1), "tabs_title_border_color": C["line"],
        "tabs_title_border_radius": dim(6), "padding": dim(16), "box_padding": dim(0),
        **font("title_typography", 14, "500", 1.3),
    }
    tabs_widget = widget("nested-tabs", "Five permit types", **settings)
    tabs_widget["elements"] = children
    return section("sx-permit-types", "Find the right permit", [heading("Permit selector heading", "Find the Right Permit for Your Event"), tabs_widget])


def preparation():
    data = [("Organizer", "Company details and responsible contact", "user"), ("Event Type", "Clear event format and objectives", "file-alt"),
            ("Programme", "Agenda, speakers and key activities", "list-ul"), ("Venue", "Proposed venue details and capacity", "map-marker-alt"),
            ("Dates", "Preferred event dates and duration", "calendar-alt")]
    cards = [panel("Prepare " + title, [icon_box("Prepare " + title + " content", title, text, icon, text_align="center")],
                   **width(18.6, 48, 100), padding=dim(24, 18)) for title, text, icon in data]
    return section("sx-prepare", "Application preparation", [heading("Prepare heading", "What to Prepare Before You Apply"),
        row("Preparation checklist cards", cards, flex_direction_tablet="row", flex_wrap="wrap", flex_gap=gap(16), flex_justify_content="space-between")])


SCOPE = [("Requirements Review", "We review the event format, organizer details and proposed venue to identify the relevant authority and the information needed for the application."),
         ("Document Preparation", "We help organize the event brief, programme and supporting documents. Final requirements depend on the event and the authority handling the application."),
         ("Submission Coordination", "We coordinate the submission process and keep the application information consistent. Authority decisions and any additional requests remain with the relevant authority."),
         ("Application Follow-Up", "We track application requests and help coordinate responses, clarifications and updated documents during the review process."),
         ("Changes & Cancellation", "If event details change, we review the update and help coordinate the relevant amendment or cancellation steps with the organizer.")]


def scope():
    intro = box("Service scope introduction", [heading("Scope heading", "What Does Our SCEGA Permit Service Cover?", 26),
        paragraph("Scope description", "A coordinated service to manage your permit application, with clear communication at every stage.")], **width(28), flex_gap=gap(18))
    visual = photo("Scope event planning photo", "meeting", 300, **width(31))
    accord = box("Scope accordion column", [accordion("Service scope accordion", SCOPE)], **width(37))
    return section("sx-service-scope", "Permit service scope", [panel("Service scope panel", [row("Service scope row", [intro, visual, accord],
        flex_justify_content="space-between", flex_gap=gap(20))], padding=dim(24))])


EVENT_SERVICES = [("Event Management", "End-to-end event delivery with experienced local teams.", "banquet"),
    ("Booth Production", "Custom stand design and build for exhibitions.", "stand"),
    ("AVL & Technical", "Audio visual, lighting and technical production.", "stand"),
    ("Guest Registration", "Seamless on-site and online registration.", "meeting"),
    ("Delegate Acquisition", "Targeted delegate outreach to grow event attendance.", "guests")]


def editorial_card(label, title, description, media, url, percent=18.6):
    image = photo(label + " image", media, 210, min_height_mobile=size(220), border_radius=dim(0))
    content = box(label + " copy", [heading(label + " title", title, 17, "h3"), paragraph(label + " description", description, 13),
                  action(label + " action", "Learn more", url, secondary=True, text_padding=dim(10, 12), typography_font_size=size(12))],
                  padding=dim(18), flex_gap=gap(12))
    return panel(label, [image, content], **width(percent, 48, 100), padding=dim(0), flex_gap=gap(0), overflow="hidden", border_radius=dim(8))


def event_services():
    cards = [editorial_card("Event service " + name, name, text, media, "#sx-event-brief") for name, text, media in EVENT_SERVICES]
    return section("sx-event-services", "Event services", [heading("Event services heading", "Event Services Beyond the Permit"),
        row("Five event service cards", cards, flex_direction_tablet="row", flex_wrap="wrap", flex_gap=gap(16), flex_justify_content="space-between")])


def hotels():
    intro = box("Stay support intro", [heading("Stay support heading", "Hotel Booking & Visa Support", 32),
        paragraph("Stay support description", "Make it easy for your international guests. We assist with hotel reservations and visa application support so your attendees can focus on the event.", 15)], **width(56), flex_gap=gap(12))
    benefits = box("Stay support benefits", [icon_box("Hotel support icon box", "Hotel Reservations", "Reservation options coordinated around your event.", "hotel", 15, position="left", icon_size=size(24)),
        icon_box("Visa support icon box", "Visa Application Support", "Guidance and document support for international guests.", "passport", 15, position="left", icon_size=size(24))], **width(40), flex_gap=gap(20))
    cards = []
    for i, (title, media) in enumerate([( "Accommodation planning", "tables"), ("Guest reservations", "banquet"), ("Arrival coordination", "guests")]):
        cards.append(panel("Stay support card " + str(i), [photo("Stay illustration " + str(i), media, 220, border_radius=dim(0)),
            heading("Stay card title " + str(i), title, 14, "h3", _padding=dim(14))], **width(32, 48, 100), padding=dim(0), flex_gap=gap(0), overflow="hidden"))
    return section("sx-stay-support", "Hotel and visa support", [panel("Stay support panel", [
        row("Stay support header", [intro, benefits], flex_justify_content="space-between"),
        row("Stay support gallery", cards, flex_direction_tablet="row", flex_wrap="wrap", flex_gap=gap(16), flex_justify_content="space-between"),
        action("Plan guests stay", "Plan Your Guests’ Stay", align="right")], padding=dim(28), flex_gap=gap(24))])


def fees():
    data = [("Government Fees", "SCEGA charges government fees based on event type, scale and other official criteria. Fees are paid directly to the relevant authorities.", "layer-group"),
            ("SYNC Service Scope", "Our service covers requirements review, document preparation, submission coordination and follow-up until a decision is issued.", "clock")]
    return section("sx-permit-fees", "Permit fees and timelines", [heading("Fees heading", "Permit Fees & Application Timelines"),
        row("Fee explanation cards", [panel("Fee card " + title, [icon_box("Fee content " + title, title, text, icon, position="left")], **width(49)) for title, text, icon in data],
            flex_justify_content="space-between")])


def experience():
    visual = photo("Experience event photo", "stand", 260, **width(74), border_radius=dim(0))
    caption = box("Experience project caption", [heading("Experience caption title", "Selected event project", 16, "h3"),
        paragraph("Experience caption copy", "A SYNC exhibition project, bringing event planning and production together.", 14),
        action("Experience projects link", "View projects", "https://syncs.com.sa/project/", secondary=True, typography_font_size=size(12))],
        **width(24), padding=dim(24), flex_gap=gap(18), flex_justify_content="center")
    return section("sx-experience", "Event experience", [heading("Experience heading", "Event Experience Behind Your Application"),
        panel("Experience showcase panel", [row("Experience showcase row", [visual, caption], flex_gap=gap(0), flex_justify_content="space-between")], padding=dim(0), overflow="hidden")])


FAQS = [("How long does the SCEGA permit process take?", "Timing depends on the event type, the completeness of the application and the relevant authority’s review. We review your proposed dates and help you plan the application steps; a fixed approval date cannot be confirmed in advance."),
        ("What documents are required?", "Start with organizer details, the event format, a draft programme, venue information and proposed dates. We review the brief and help identify any additional documents requested for the relevant application."),
        ("Can SYNC manage the full application on our behalf?", "We can support requirements review, document preparation, submission coordination and follow-up. The organizer provides accurate information and authorizations, and the relevant authority makes the permit decision."),
        ("What happens if we need to change our event details?", "Tell us as soon as the venue, dates, programme or event scope changes. We review the update and help coordinate the relevant amendment or cancellation steps.")]


def faqs():
    return section("sx-permit-faq", "Permit questions", [heading("FAQ heading", "SCEGA Permit Questions, Answered"),
        row("FAQ two columns", [box("FAQ first column", [accordion("FAQ first two questions", FAQS[:2])], **width(49)),
                               box("FAQ second column", [accordion("FAQ next two questions", FAQS[2:])], **width(49))], flex_justify_content="space-between")])


def form():
    specs = [("name", "text", "Name", "Your name", True), ("company", "text", "Company", "Your company", False),
             ("email", "email", "Email", "you@company.com", True), ("event_type", "select", "Event type", "Select event type", True)]
    fields = []
    for key, kind, label, placeholder, required in specs:
        item = {"_id": uid("Brief field " + key), "custom_id": key, "field_type": kind, "field_label": label,
                "placeholder": placeholder, "required": "true" if required else "", "width": "50", "width_tablet": "50", "width_mobile": "100"}
        if kind == "select":
            item["field_options"] = "Select event type|\nConference|conference\nExhibition|exhibition\nWorkshop|workshop\nTraining|training\nBusiness Meeting|business_meeting"
        fields.append(item)
    return widget("form", "Native event brief form", form_name="SYNC SCEGA Event Brief", form_fields=fields,
        show_labels="true", input_size="md", button_size="md", button_text="Send Event Brief", button_width="100", submit_actions=["save-to-database"],
        form_validation="", column_gap=size(20), row_gap=size(18), label_spacing=size(8), label_color=C["silver"],
        field_text_color=C["white"], field_background_color=C["bg"], field_border_color=C["accent"],
        field_border_width=dim(1), field_border_radius=dim(6),
        button_background_color=C["lavender"], button_text_color=C["bg"], button_background_hover_color=C["accent"],
        button_hover_color=C["bg"], button_border_radius=dim(6), button_text_padding=dim(15, 24),
        **font("label_typography", 13), **font("field_typography", 14), **font("button_typography", 15, "600", 1.3))


def brief():
    copy_column = box("Brief introduction", [heading("Brief eyebrow", "LET’S PLAN TOGETHER", 11, "p", C["lavender"], typography_letter_spacing=size(2)),
        heading("Brief heading", "Tell Us About Your Event", 40), paragraph("Brief description", "Share a few details and our team will get back to you to discuss your permit and event support needs.")],
        **width(35), flex_gap=gap(16))
    return section("sx-event-brief", "Event brief", [panel("Event brief panel", [row("Event brief row", [copy_column, box("Brief form column", [form()], **width(60))],
        flex_justify_content="space-between", flex_align_items="center")], padding=dim(32), padding_mobile=dim(24))])


GUIDES = [("Requirements", "Key SCEGA permit requirements for business events.", "meeting", "#sx-prepare"),
          ("Exhibition Types", "A guide to exhibition formats and permit considerations.", "stand", "#sx-permit-types"),
          ("Application Corrections", "Common application updates and how to review them.", "laptop", "#sx-service-scope"),
          ("SCEGA vs GEA", "The right route depends on your event’s business or entertainment scope.", "banquet", "#sx-permit-faq")]


def resources():
    cards = [editorial_card("Resource " + title, title, copy, media, target, 23.5) for title, copy, media, target in GUIDES]
    return section("sx-permit-guides", "Permit guides and resources", [heading("Resource section heading", "Permit Guides & Resources"),
        row("Four permit guide cards", cards, flex_direction_tablet="row", flex_wrap="wrap", flex_gap=gap(16), flex_justify_content="space-between")])


def walk(elements):
    for e in elements:
        yield e
        yield from walk(e.get("elements", []))


def save(path, document):
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n")


def dynamic_extras():
    baseline = json.loads((ROOT.parent / "service-content-no-filter/SYNCs-Service-Card.json").read_text())
    image = copy.deepcopy(baseline["content"][0]["elements"][0])
    image["id"] = uid("Dynamic guide image")
    image["settings"].update(_title="Dynamic featured image", height=size(220), **{"object-fit": "cover"}, _margin=dim(0))
    content = copy.deepcopy(baseline["content"][0]["elements"][1])
    content["id"] = uid("Dynamic guide title")
    s = content["settings"]
    s.pop("__globals__", None)
    s.update(_title="Dynamic guide title", title_text="Permit Guide", description_text="Read this guide", title_color=C["white"],
             description_color=C["silver"], _padding=dim(20), **font("title_typography", 18, "600", 1.3), **font("description_typography", 13))
    card = panel("Dynamic guide loop card", [image, content], padding=dim(0), flex_gap=gap(0), overflow="hidden", border_radius=dim(8))
    save(ROOT / "extras/SYNCs-Permit-Guide-Loop-Item.json", {"content": [card], "page_settings": [], "version": "0.4", "type": "loop-item", "title": "SYNC — Permit Guide Loop Item"})
    source_page = json.loads((ROOT.parent / "projects-page/SYNCs-Projects-Page.json").read_text())
    old_grid = next(e for e in walk(source_page["content"]) if e.get("widgetType") == "loop-grid")
    grid = copy.deepcopy(old_grid)
    grid["id"] = uid("Optional native guide grid")
    grid["settings"].update(_title="Native article Loop Grid", template_id="", post_query_post_type="post", posts_per_page=4,
         columns=4, columns_tablet=2, columns_mobile=1, masonry="", _css_classes="")
    grid["settings"].pop("alternate_templates", None)
    replacement = section("sx-permit-guides", "Dynamic permit guides", [heading("Optional guide heading", "Permit Guides & Resources"), grid])
    save(ROOT / "extras/SYNCs-Permit-Guides-Dynamic-Loop-Grid.json", {"content": [replacement], "page_settings": [], "version": "0.4", "type": "container", "title": "SYNC — Dynamic Permit Guides (choose Loop Item first)"})


def main():
    sections = [header(), hero(), trust_strip(), permits(), preparation(), scope(), event_services(), hotels(), fees(), experience(), faqs(), brief(), resources(), header(True)]
    page = {"content": [box("SYNC SCEGA complete page", sections, background_background="classic", background_color=C["bg"])],
            "page_settings": [], "version": SOURCE["version"], "title": "SYNC — SCEGA Permit Support — Complete Page", "type": "page"}
    save(ROOT / "SYNCs-SCEGA-Complete-Page.json", page)
    index = []
    for i, element in enumerate(sections, 1):
        slug = element["settings"]["_element_id"]
        filename = f"{i:02d}-" + slug.replace("sx-", "") + ".json"
        save(ROOT / "sections" / filename, {"content": [element], "page_settings": [], "version": SOURCE["version"],
             "title": "SYNC — " + element["settings"]["_title"], "type": "container"})
        index.append({"file": "sections/" + filename, "anchor": slug, "label": element["settings"]["_title"]})
    dynamic_extras()
    save(ROOT / "validation/manifest.json", {"page": "SYNCs-SCEGA-Complete-Page.json", "sections": index,
        "elements": len(list(walk(page["content"]))), "palette": C, "media": MEDIA,
        "baseline": str(BASE.relative_to(ROOT.parent)), "baseline_sha256": hashlib.sha256(BASE.read_bytes()).hexdigest(),
        "status": "native saved-template bundle; WordPress staging import/edit/re-export pending"})
    print(json.dumps({"sections": len(sections), "elements": len(list(walk(page["content"]))), "html_widgets": 0, "custom_css_js": 0}))


if __name__ == "__main__":
    main()
