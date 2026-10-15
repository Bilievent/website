# Dynamic SYNCs selected projects

Reference: user screenshot of vividexperience.com.sa/en. Observed treatment: dark navy background, coral eyebrow, centered large heading, rounded portrait project cards, third card enlarged, bottom image gradient, category pills and navigation. No third-party photographs or code are copied. The reference and target site were not accessible through this machine's network policy; no live-site branding or runtime behavior is asserted.

The new source baseline is the user's actual Elementor Loop Item export #6526, schema version 0.4. Its featured-image, post-title and two ACF URL dynamic bindings are preserved exactly. The actual featured image URL and title in the export remain as preview/fallback data; they are not a hardcoded slide list. The separate local test harness uses abstract fixtures and simulated records, none of which are part of the native Loop Item data.

Native structure: Loop Item Container sx-live-card > Image (Featured Image + ACF URL link), native Icon Box without icon (Post Title, H3 + ACF URL link), HTML style widget. Removing the Themify arrow removes the original imported custom icon dependency. The same ACF field definition remains required.

Native section shell: Container sx-live-projects > native Heading intro + HTML layout/control widget. The user inserts a genuine Elementor Pro Loop Grid and Taxonomy Filter because their query/filter schema, runtime IDs, selected post type, and taxonomy were not supplied. No Pro widget settings were invented. The shell alone displays heading text and has no project query.

Query, publish status, ordering and taxonomy membership remain owned by Elementor/WordPress. The integration observes child replacements inside the native grid and preserves native links. It does not clone slides, synthesize posts, send AJAX, intercept native filter clicks, or change pagination. Active selection resets appropriately if its item disappears. Empty results hide carousel controls; one item disables navigation. Script re-execution reuses a page-level registry.

Desktop 1440px: up to four slots, 20px gaps, ratio 2.9:1 for active vs other items, 398/444px heights. Tablet 768px: four slots, 14px gaps, 340/390px heights. Mobile 390px: 86%-width cards, 380px height, horizontal scrolling and snap alignment. No autoplay; reduced-motion disables CSS transitions and smooth control scrolling. H2 section title, H3 project names, named navigation buttons, live status and keyboard focus styles. Only projects loaded by native pagination are navigable. Native filter styling remains in Elementor's Style controls.

Colors #071520/#f49376 come from the screenshot-inspired adaptation, not a verified SYNCs brand guide. The existing card font setting Outfit is retained with Arial fallback. Optional native Post Terms badge styling is included as sx-live-term, but its taxonomy must be selected in the actual editor. RTL arrow direction is handled, but full RTL visual validation is unrun.

This is a prototype saved-template bundle, not an official Elementor Website Kit and not a verified installation-specific import/re-export.
