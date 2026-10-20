# Why Us — five native service cards

The user asks to replace the Why Us content/layout in the recolored #6941 export using the same widget types that already exist in that template, without custom HTML. The user confirmed the five visible services rather than eight. The section is fully assembled from native Containers, Heading, Text Editor, Icon List and Button widgets. There is no HTML widget, custom CSS, custom JavaScript, iframe, shortcode or new widget dependency.

## Observed reference and adaptation

The screenshot shows a large two-line introduction, a left service index (five visible entries), and a right stack of white service cards. The second card begins below the first, so this is a continuously visible card stack with anchor navigation rather than tabs that hide content. The first visible service supplies its title, sentence, four tags, three bullet points and a photo. The screenshot's browser chrome, logged-in WordPress toolbar and WhatsApp bubble are outside section scope.

The title now reads Five ways in. / One way of working., matching the confirmed service count. Service names are transcribed from the reference. Event Management copy follows the visible card. The other four descriptions/tags/points are new proposed copy based on their names; they do not add certifications, numerical claims or portfolio attribution.

The reference measured about 1296px of content in a 1440px viewport, with x≈72px left edge, a 410px index, a 70px gutter and an 817px card column. Native settings use a 1296px boxed Container, 31.5% navigation, 63.5% cards, space-between and a 40px minimum gap. The internal 1440px review measures a 408px index, a card starting at x≈545px, 823px card width and 488px first-card height. These are review-harness measurements, not a certified WordPress render.

## Native element map

- Root boxed section Container, then a title Container with two Heading widgets. First line is an H2; second is a native div heading. Service titles are H3; their small codes/captions use p.
- Row Container → nav Container with a native Icon List → card-stack Container.
- Each article Container → header row, description Text Editor, inline Icon List tags, a details/photo row, and a Button.
- Details panel → small Heading plus a bullet Icon List. Photo → native Container background image, as already used in #6941. All essential meaning is text; the background photos are decorative.
- Navigation links target native Advanced → CSS ID fields on the five article Containers. All five cards stay in the DOM and visible. No search/filter/query/cache logic is added.

The new section has 68 elements: 30 Containers, 17 Headings, 11 Icon Lists, 5 Text Editors and 5 Buttons. The full-page output preserves the first three original sections as identical JSON objects and replaces only the fourth section. All visual controls remain native editor settings.

## Palette and spacing

Light Gray #F5F5F7 section/details background; Soft White #FAFAFC nav; Pure White #FFFFFF cards/buttons; Graphite #4A4557 typography; Silver Gray #D8D8E0 dividers/button outline; Soft Lavender #C9BCE3 hover buttons; Deep Midnight #1D162A hover text; Dark Purple #2B203D photo fallback. These are the user's palette colors. Typography is native Manrope, 64/48/36px introductory headings and 28/23px service titles. Card padding 40/32/24px, 24px radii, inner panel/photo 16px radii, 18px card gaps, 205px desktop photo/detail minimum height. Native line-height gives nav links 48px touch targets without custom CSS.

## Responsive and interaction behavior

Desktop: left index with native Pro Sticky, desktop only, offset 120px and parent boundary enabled. Tablet (default ≤1024px): index above cards. Mobile (default ≤767px): title/code rows and detail/photo rows also stack, all full width; button aligns left. No animation or custom script is required for the section or its native fragment links. Site-specific breakpoints and sticky-header overlap need staging verification.

Service CTAs use the authorized contact URL https://syncs.com.sa/contact-us/ and truthful Discuss this service labels. Exact service detail URLs were not supplied; no slugs are invented. The user can replace each native Button link later.

## Images, ownership and compatibility

All five media references are exact HTTPS URLs already in the user's same-site exports/derived baseline. Four unique existing media records are used, including the original #6526 card's Watad BIG 5 stand photo for two illustrative panels. No image filenames/URLs are fabricated, no third-party stock is introduced, and no photo binaries are bundled. These are illustrative existing site assets, not verified images from the supplied screenshot or claims about specific projects delivered under each service.

Template document version 0.4 is retained; it is not the Elementor plugin version. Existing native widget schemas and the user's source motion/sticky fields are the baseline; additional native controls are corroborated against official Elementor source. Elementor/Pro versions, actual native import/editor/re-export, fonts, photo resolution and live-page layout remain unverified. Native background crops and Pro Sticky need staging. The internal browser DOM harness approximates native controls, uses Arial fallback when Manrope cannot load, and shows the declared solid photo fallback because site access is blocked. Its temporary HTML/CSS are test infrastructure, never part of the templates or download.
