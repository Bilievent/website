# SYNCs palette adaptation — export #6941

Scope: recolor the user's supplied native Elementor page, preserving its four top-level sections and all original content, media, layout, responsive controls, icons, links and interactions. No new photography, image files, CSS/JS widgets or filters are inserted.

The reference is the attached export and the user's exact color table. A live site comparison was unavailable: HTTPS to syncs.com.sa returned a proxy CONNECT 403. The export already supplies ten unique HTTPS image URLs from the site's own WordPress uploads (18 media placements, including decorative overlays). All URL strings and attachment IDs are retained exactly; see validation/image-links.json. Live availability and image rights are not inferred from URL presence.

| Use | Native palette selection |
| --- | --- |
| First and third project sections | Deep Midnight #1D162A |
| About section | Soft White #FAFAFC |
| Why Choose Us section | Light Gray #F5F5F7 |
| Counter/contact panels and image fallbacks | Dark Purple #2B203D |
| Decorative dark separators | Charcoal #3A3447 |
| Buttons, icons, markers, quote accent | Royal Purple #8F7BB8 |
| Hover buttons, selected tabs, light highlights | Soft Lavender #C9BCE3 |
| Borders and dark-background body text | Silver Gray #D8D8E0 |
| Light-background headings / body | Deep Midnight / Graphite #4A4557 |
| Dark-background headings | Pure White #FFFFFF |

Colors formerly bound to the old global color IDs are now local native controls, so the old globals cannot restore the green palette. Typography global references remain intact. Original explicitly stored green values are replaced. Transparency and shadow colors use alpha variants of palette colors.

Buttons use Deep Midnight text on Royal Purple (4.74:1) and Soft Lavender on hover/focus (9.82:1). White text on Royal Purple would only reach 3.69:1, so it is not used for normal-size button labels. Light section highlighted words use Royal Purple for large headline text (3.54:1 on Soft White); check the installed global typography stays large enough (24px regular or about 19px bold). Other audited solid-background text pairs reach at least 4.5:1. Photo overlays retain the original opacity, positions and gradient stops; text contrast over actual photos still requires a real render.

Native structure: 50 Flexbox Containers, 63 native widgets, 113 elements total. Existing animated headlines and motion effects need Elementor Pro; nested tabs and Containers must be enabled/supported. The source uses the ekiticons icon font as well as Font Awesome; retain the site's existing icon library provider. Elementor and Pro plugin versions were not supplied. Template schema version 0.4 is a file-format version, not a plugin version.

The user requested color changes rather than a layout rewrite. Original desktop, tablet and mobile layout/typography/motion values are preserved byte-for-byte in the normalized non-color structure. The internal review at 1440/768/390px demonstrates palette states in an independent color harness, not an Elementor frontend or fidelity claim. No local font substitutions from this review are embedded in the templates.

All texts remain editable and retain their original English/demo wording, including source placeholder copy, the phone number and #/empty links. Project cards in this uploaded export remain its existing static native elements; this color-only adaptation does not convert them into Loop Grid queries. Previously delivered dynamic no-filter sections remain separate.
