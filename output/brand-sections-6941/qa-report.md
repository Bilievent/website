# QA — palette adaptation of native export #6941

Status: recolored native saved-template prototype, pending a WordPress staging import. This is not an official Elementor Website Kit or a production deployment.

## Completed

- Read AGENTS.md and all four repository Elementor skills. Used the user's 2026-10-20 export as the exact structural baseline and the supplied color table as the palette source.
- Checked the cloud workflow: Python 3, Chromium and Playwright were already available. No dependency installation, new service or environment-configuration draft was needed for this file-editing workflow.
- Validated five JSON files: original page document plus four individual Container templates. All four sections, 113 original elements, widget types, IDs and hierarchy are preserved. A normalized non-color SHA256 comparison passes, covering responsive/layout controls, text, typography bindings, icons, all links, motion and media attachment metadata.
- All colors are from the supplied palette or alpha variants. Old color-global references and explicitly stored green values are absent. Global typography references remain intact. No HTML widgets, filters, new photography, encoded images or media files were inserted.
- All 18 media placements retain their exact original URL and attachment ID; the ten unique URLs use HTTPS on syncs.com.sa/wp-content/uploads/. The JSON references these URLs; no image payloads are bundled.
- Twelve representative foreground/background contrast checks pass. Normal button text reaches 4.743:1 and hover/focus text 9.818:1. Royal Purple large headline text reaches 3.538:1 on Soft White; the installed typography must remain large enough. Photo contrast cannot be certified without loading/rendering the photos.
- Independent browser color review passes at 1440, 768 and 390px: normal/hover/focus buttons, tab hover colors, four color groups, no review-page overflow, no page errors. Desktop and mobile review screenshots were visually inspected. This harness uses actual native color values in its own simple layout and deliberately loads no photos; it does not emulate Elementor's source layout, typography, icons, animation, tabs or sticky effects.
- Added button and text-editor controls were checked against official public Elementor source; native tab background group defaults were also checked. Evidence is in validation/control-sources.md. No Elementor plugin or widget schema is claimed to be installed here.

## Not executed / limitations

- Direct HTTPS to the site returned CONNECT 403 from the environment proxy. Live page inspection and image availability checks were not possible. Media paths are proven to be preserved from the user's export, not proven live responses.
- No WordPress runtime/credentials or exact Elementor/Pro versions were supplied. Import, editor reopening, editability in the real installation, render/re-export/re-import, global font resolution, real breakpoints, image crops, motion, touch and assistive-technology checks remain unexecuted.
- Native Pro animated headlines/motion, Containers, nested tabs and the source's ekiticons font need the same existing site capabilities. File-format version 0.4 is retained and must not be confused with the Elementor plugin version.
- Source placeholder wording, phone number and links are retained. This task changes colors; it does not connect the static project cards in this export to WordPress queries or change language/cache behavior. Existing dynamic no-filter deliverables are separate.

## Reproduce

Run `python3 validation/validate_brand.py` from this folder. To rebuild from the original user file, run `python3 validation/build_brand.py /path/to/elementor-6941-2026-10-20.json`. For the independent palette harness, run `python3 validation/build_color_review.py` and `node validation/browser_check.cjs` with Playwright and Chromium available. No local server is needed; no localhost links are provided as user previews.

Validation reports: validation/results.json, validation/browser-results.json, validation/manifest.json and validation/image-links.json. The downloadable ZIP contains the five templates and three instruction/design/QA documents, with no image files or harness screenshots.
