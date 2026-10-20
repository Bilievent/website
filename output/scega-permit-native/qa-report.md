# QA — complete native SCEGA page

Status: validated saved-template prototype; actual WordPress/Elementor staging import remains pending. Download is a bundle of saved-template JSON files, not an official Website Kit export.

## Passed

- Read AGENTS.md and all four local Elementor skills. Preserved the user's brand palette and native export schema. User explicitly approved adding native Form and Accordion widgets.
- Python/Chromium/Playwright were already installed. No new service, dependency installation, runtime startup configuration or environment configuration change was necessary. Existing repository changes were preserved; only new outputs and their index are changed.
- Seventeen valid JSON templates: full page, fourteen standalone sections, native guide Loop Item and optional article Loop Grid replacement.
- Main page: 14 sections, 236 elements, unique IDs, one H1, native semantic section/card headings. Widget names are from the user's exports except the approved Form and Nested Accordion. No custom HTML/CSS/JS, shortcode, taxonomy filter, generated image files or plugin code in the delivered templates.
- Five permit-tab entries match five native child panels; the three accordions contain 5+2+2 native answer Containers. All nine items default to all_collapsed with one open item per widget.
- Twenty photo placements use six exact known first-party media URLs. Zero guessed/unknown media URLs. Twenty-five same-page links resolve to actual CSS IDs; remaining links are the two known user site URLs, contact and project.
- Form has four unique fields, visible labels, email validation, a required event-type option with empty prompt and responsive widths. Its only action is save-to-database (Collect Submissions). No email address, external service endpoint or sending action is configured. Native Form controls and repeater field names passed a check against the retrieved compatibility schema.
- Optional dynamic grid is source post, four records, 4/2/1 columns, no custom Query ID/filter. Native Loop Item contains verified Post Title, Featured Image and Post URL bindings without an ACF URL dependency. Grid template_id is deliberately empty until the real imported document is selected; it is not used in the main page.
- Independent browser harness passed at 1440/768/390px: all fourteen sections, 15/15 tab-panel checks, 27/27 accordion-item open/close checks, keyboard navigation, native hero anchor jump, labeled browser form validation, no horizontal overflow, reduced-motion layout, zero page JavaScript errors and zero POST requests. Submit is prevented in the harness; it does not simulate successful storage or send a request.
- Desktop and mobile screenshots were visually inspected. The original five-cell strip wrapped its last cell due to panel padding; native widths were adjusted and a desktop one-row assertion now passes. Manrope was loaded for QA from the official Google Fonts source. Screenshots use the declared solid photo fallback because media requests are unavailable, so they are layout/type reviews rather than real-photo fidelity evidence.

## Not executed

Actual WordPress import; native editor reopening and editing; render/re-export/re-import; installed Elementor/Pro version inspection; native tabs/accordion frontend scripts and assistive technology; live image responses, crop quality or media importer behavior; site font loading; real native Form AJAX, database persistence, notifications/SMTP or server validation; actual post/category/language queries and cache invalidation.

HTTPS access to syncs.com.sa remains denied by the configured environment proxy (CONNECT 403). No WordPress runtime/credentials or exact Elementor/Pro version numbers were supplied. Public schema checks corroborate names but do not certify the user's installation. The PRO Elements compatibility source was read as text only; no code from that project was executed, installed or bundled.

## Intentional adaptations

The original hero permit photo is represented by an editable native readiness card. Header/footer wordmarks are editable text. Client placeholders become generic event types. Stay images are illustrative existing venue photos and captions do not identify unverified hotels or cities. Editorial resource cards link to real sections; the optional native Loop Grid is provided for live posts. Copy is editable; government fee amounts and fixed approval timelines are not invented.

## Reproduce

From this folder run `python3 validation/build_page.py`, `python3 validation/validate_page.py`, `python3 validation/render_review.py`, then `node validation/browser_check.cjs` with Playwright and Chromium available. The renderer writes an internal file under /tmp, not the user bundle. Temporary schema files strengthen checks when present; validation/control-sources.json records their retrieval URLs and SHA256 hashes. Reports are validation/results.json and validation/browser-results.json.

On staging, import the complete page into Elementor Canvas, inspect responsive states, reopen the editor, send a test brief and verify Elementor Submissions, configure notification email if desired, verify actual media and fonts, then export/re-import. For the optional Loop Grid select the imported Loop Item and the correct service category and language. Only an actual successful native kit export should be distributed as an official Website Kit.
