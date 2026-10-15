# Validation report — dynamic-project prototype

## Input inspected

User export: elementor-6526-2026-10-15.json, 5,283 bytes. Type `loop-item`, schema version `0.4`, title `Elementor Loop Item #6526`. It contains native Containers, Image, Icon Box, and an Icon using a third-party Themify library. It contains no Loop Grid, Taxonomy Filter, post-type query, selected taxonomy, installed plugin versions, or native tag for category terms.

## Passed

- New Loop Item JSON: 4 elements with unique IDs; native Image, Icon Box and HTML style widget inside a Container. The original featured-image, post-title, and both ACF URL dynamic-tag strings match the supplied export exactly. ACF key `field_69d0254b84115:project_url` is retained.
- Section shell JSON: 5 unique elements, native Container/Heading/HTML only. No guessed Pro Loop Grid/Taxonomy Filter schema or made-up taxonomy has been inserted.
- The custom Themify Icon was removed; Image/title links retain the original dynamic destination. No package demo artwork or fixed list of projects is used by the native Loop Item. The original post image/title remain preview fallback values as in Elementor exports.
- Card CSS embedded in the Loop Item equals assets/loop-card.css. Node syntax checks pass for layout controller and browser validation script.
- Native core Container/Image/HTML and Icon Box controls were reviewed against Elementor 3.25.0 public source, including Icon Box title_size/title_text/link and selected_icon. The user's own export is the main native-schema baseline, not a declaration that their installed version is 3.25.0.
- Chromium/Playwright local native-wrapper harness at 1440, 768, and 390px: no document horizontal overflow, one selected card, working next/previous and keyboard navigation, native project-link attributes preserved, simulated native-filter track replacement, empty results, recovery from empty results, one project, and eight newly rendered projects all pass. Mobile programmatic horizontal scrolling updates selection. Reduced-motion and duplicate-script initialization checks pass. No uncaught page JavaScript errors.
- Desktop and mobile screenshots inspected. Abstract test artwork is confined to validation fixtures and preview.html. Mock filter buttons exist only in the harness; they are not represented as the user's real Taxonomy Filter.

## Pending actual site validation

WordPress, Elementor/Pro and theme versions are unknown. No authenticated staging runtime or full section export was supplied. Actual native import, media resolution, ACF tag resolution, Loop Grid query, taxonomy association, frontend native AJAX filter operation, pagination, editor lifecycle, editor reopening, accessibility with assistive technology, and export/re-import have not been executed. The supplied export is evidence of actual dynamic bindings, not proof the new template has rendered in Elementor. No production changes were made.

The native Loop Grid/Taxonomy Filter must be added and configured once in Elementor per import-instructions-ar.md. The section shell alone has no project query. A taxonomy name/slug cannot be inferred from the Loop Item. Optional category badge styles exist, but its Post Terms dynamic tag must be configured in the user's editor.

Keyboard/motion behavior was checked in the harness; real touch gestures, complete RTL layout, customized site breakpoints, multiple section copies, CSP/security optimizers and native load-more integration remain untested. Arrows navigate loaded posts only and do not fetch another page. Actual auto-updating remains governed by WordPress query rules, publish status, taxonomy assignment, sorting, caching and native pagination.

## Repeat checks

`python3 output/dynamic-projects/validation/validate-template.py --source /path/to/original-export.json`

Serve `output/` on 127.0.0.1:8765, make Playwright available in a tooling environment, then run `CHROMIUM_PATH=/usr/bin/chromium node output/dynamic-projects/validation/browser-check.cjs` (or omit CHROMIUM_PATH to use Playwright's installed browser). PREVIEW_URL can override the harness URL. These checks use simulated data only; use the staging checklist in the Arabic guide for actual runtime compatibility.

## Delivery

Saved-template prototype bundle, not an official Elementor Website Kit. JSON must be imported through Templates/Saved Templates. The ZIP is a companion download containing the two templates, editable CSS/JS, instructions, design spec and validation evidence; it is not intended for the Website Kit importer.
