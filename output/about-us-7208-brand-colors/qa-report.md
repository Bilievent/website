# QA — colour revision

- Source: `elementor-7208-2026-11-03.json`, SHA-256 `5b5a2dd018b76a039c612b395e6d0fbd9bd8c9b9dd069f6db0c38e0e0e54152e`.
- Format remains native saved-template JSON version `0.4`, type `page`.
- Five top-level containers, 109 elements and unique element IDs preserved.
- Widget types and hierarchy unchanged. No HTML widget or custom CSS/JS added.
- Recursive comparison allows only colour settings, removal of external Global Color bindings, and two native Classic background selectors activating wrapper colours. All content, media objects/URLs, links, typography, spacing, responsive values, animations and interactions are unchanged.
- 267 recorded colour/binding/colour-activation differences. Existing Global Typography bindings are retained. Zero external Global Color bindings remain.
- 60 solid colour checks passed. Minimum tested ordinary text contrast: 4.74:1. Text uses at least 4.5:1; meaningful icon colours use at least 3:1.
- Eight conservative overlay endpoint bounds passed against a pure-white source-photo pixel at the original overlay opacities. The hero's lavender decorative accents use a 3:1 bound; actual hero text is white and passes 4.5:1. These are colour calculations, not measured screenshots or proof of overlay geometry in a live frontend.
- Existing shadow offsets, blur, spread and opacity remain unchanged; only the shadow RGB changes to the brand's Deep Midnight.

Validation files record per-control changes, contexts, contrast and checksums. The build script accepts the original JSON as its source argument.

Not run: WordPress import, Elementor editor reopening/re-export, native frontend rendering, responsive screenshots, carousel/sticky/motion behaviour. The installed WordPress/Elementor/Pro versions and a staging installation are unavailable. These limits do not prevent providing the requested native colour-edited template; verify the imported draft on the user's existing installation before publishing. This download is not an official Website Kit export.
