# SCEGA page — color-only brand revision

Source: `../scega-permit-native/SYNCs-SCEGA-Complete-Page.json`.
Request: retain the complete original layout and native widgets, apply the supplied SYNC palette. The rejected generated design proposal is not used as the layout source.

The original export already used the supplied palette, predominantly on dark surfaces. This revision changes its distribution: Deep Midnight #1D162A for header, hero, event-team strip, FAQ, event brief and footer; alternating Light Gray #F5F5F7 and Soft White #FAFAFC for main content; White #FFFFFF for light cards; Dark Purple #2B203D for selected feature panels and photo fallbacks. Silver Gray #D8D8E0 separates light cards, and Charcoal #3A3447 separates dark surfaces.

All solid primary buttons and active tabs use Royal Purple #8F7BB8 with Deep Midnight text. Hover fills use Soft Lavender #C9BCE3 and dark text. Outline links use dark text on light surfaces and lavender on dark surfaces. Light headings are Deep Midnight; supporting copy is Graphite #4A4557. Dark surfaces use white text and lavender accents. This keeps small button labels readable; white text on Royal Purple would not pass 4.5:1 at their existing sizes.

Only existing color controls change. No settings, IDs, widget names, content, images, links, queries, form actions, typography, spacing, dimensions, order, responsive breakpoints or interactions are added or removed. The original 14 sections and 236 native elements remain. Images remain the original first-party URL records.

Validation: recursive original/revised comparison permits only hexadecimal color changes in existing settings; explicit solid-color text/icon contrast checks; independent DOM review at 1440/768/390px. These are not actual Elementor renders. Exact installed Elementor/Pro versions and WordPress staging are unavailable, so native import/edit/re-export compatibility remains untested.
