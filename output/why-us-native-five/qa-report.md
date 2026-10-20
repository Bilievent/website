# QA — native Why Us, five services

Status: native saved-template prototype; actual staging import/editor/runtime validation pending. Not an official Elementor Website Kit and not deployed to WordPress.

## Verified

- Applied AGENTS.md and all four local Elementor skills, the user's same-site #6941 export/brand-color output, the new screenshot, and the user's explicit five-service/native-widget-only instruction.
- Two valid JSON templates: whole page and standalone Container. Source file-format version 0.4 is retained. All IDs are unique in each document. The first three page sections are identical to the previous brand-color file; only Why Us changes.
- All new widget types already occur in the user's template: Heading, Text Editor, Icon List and Button. Native Containers supply all layout and photo backgrounds. Zero HTML widgets, custom CSS/JS, shortcode widgets, iframes or new widget plugins. No hidden tabs, taxonomies or query logic.
- One H2, five service H3s, five card anchor IDs, five matching native menu links, all cards visible, five valid contact CTA links. Fifteen benefit points and separately spaced native tag lists. Zero guessed service URLs or invented media URLs. Colors come from the supplied palette.
- All five image references (four unique URLs) match known same-site exports/derived source records. No image payloads were downloaded, created or bundled. Existing media IDs retained. Photos are illustrative, not attributed as specific service work.
- Independent DOM harness at 1440/768/390px: 15/15 native fragment links jump to visible titles, keyboard Enter works, 48px menu targets and ≥44px contact buttons, desktop side-by-side columns, tablet/mobile stack, mobile detail/photo stack, hover color correct, no horizontal overflow and no JavaScript page errors. Page JavaScript is disabled for these checks, confirming no custom script is needed for the anchor navigation.
- Desktop/mobile screenshots were visually inspected. An initial review renderer used an unavailable font without fallback and was corrected to reflect Elementor's sans-serif fallback; that was a QA renderer issue, not a template change. Native screenshots remain unverified.
- Foreground/background contrast for Graphite on White/Soft White/Light Gray and Deep Midnight on Soft Lavender exceeds 4.5:1. Focus and real browser/theme behavior still need staging checks.

## Native control evidence

The same-installation export supplies Containers, Heading, Text Editor, Icon List, Button, native backgrounds, responsive fields and native Pro sticky fields. Additional control names were checked against the public official source over verified HTTPS:

- https://raw.githubusercontent.com/elementor/elementor/main/includes/elements/container.php — css_classes, _element_id, html_tag with section/article/nav options, content/background/flex settings.
- https://raw.githubusercontent.com/elementor/elementor/main/includes/widgets/icon-list.php — link_click=full_width, divider, divider_weight/width/color, text_color_hover, icon_typography and spacing selectors.
- https://raw.githubusercontent.com/elementor/elementor/main/includes/widgets/traits/button-trait.php — native button typography, padding, border/radius and hover colors. See prior brand-sections-6941/validation/control-sources.md for retrieval evidence.

Upstream sources corroborate native names; they do not establish the site's exact installed plugin versions.

## Unrun / limits

Site HTTPS inspection again returned a proxy CONNECT 403. Real images, actual service URLs and live typography could not be inspected. No WordPress runtime/credentials or Elementor/Pro version numbers were supplied. Native import, editor reopening, media resolution, export/re-import, full-page native rendering, default-vs-site breakpoints, Pro sticky/header/admin-bar offsets and touch/assistive-technology behavior remain unrun. Browser results are from a separate native-setting DOM approximation, not an Elementor runtime. The solid photo QA boxes and their diagnostic text are not in delivered JSON.

The five supplied service names are confirmed; additional copy for four panels is proposed editable text. CTAs intentionally use the already authorized contact page with Discuss this service labels until exact service links are available. The layout is editorial service content and does not replace previous dynamic project queries.

## Reproduce

From this folder, run `python3 validation/build_native.py`, then `python3 validation/validate_native.py`. For internal layout review run `python3 validation/render_review.py` and `node validation/browser_check.cjs` with Chromium and Playwright available. No service or localhost preview URL is needed. Validation scaffolding and screenshots are in the repository only; the user ZIP includes two native JSONs and the three documentation files, with no HTML/CSS/JS/photo files.
