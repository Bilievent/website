# Native control evidence

The attached same-site export is the baseline for element IDs, 0.4 document format, widget names, all original settings, global typography, nested structure, motion, responsive values and media records. The result preserves its normalized non-color content hash. Color keys already present in the source's __globals__ maps are native control names; their values are now local.

Added native button/text-editor colors were cross-checked against the public Elementor source retrieved over verified HTTPS on 2026-10-20:

- https://raw.githubusercontent.com/elementor/elementor/main/includes/widgets/traits/button-trait.php — SHA256 61c1aa88663851030ec5729ad0a3f8aa5d3d653e9b414be18afc167f8b4692e2. `button_text_color` and `hover_color` are Color controls. Background groups named `background` and `button_background_hover` expose their respective `*_background` and `*_color` fields. Normal and hover selectors include native focus styling for the hover text color.
- https://raw.githubusercontent.com/elementor/elementor/main/includes/widgets/text-editor.php — SHA256 c3a749434c4c820c91309eca6423d604cdc9543e7a21d01a239d62e911570e56. `text_color` is a native Color control.
- https://raw.githubusercontent.com/elementor/elementor/main/modules/nested-tabs/widgets/nested-tabs.php — SHA256 4d72ab8628a77aef2bf00bf581ec6275046a1039cf4c6d563d7845843de17773. Native groups `tabs_title_background_color_hover` and `tabs_title_background_color_active` default their background mode to `classic`, so the retained source group keys accept the local hover/selected colors without additional modes. The normal mode is already explicitly `classic` in the source export.

These are corroborating upstream schemas, not evidence of the site's installed plugin version. The source contains global color references but not the definitions of those old colors. Contextual native controls are set explicitly instead of assuming what those old definitions contain. No unofficial widget names or custom HTML/CSS/JS widgets are introduced. No plugins, core/theme settings or global site colors are modified on WordPress.

Validation checks IDs using the source's actual length range: its original `891cf6` ID has six characters, while the other IDs have seven/eight. IDs are preserved rather than rewritten to an invented fixed length.
