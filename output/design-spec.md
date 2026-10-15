# SYNCs selected projects

Reference: user-supplied screenshot of https://vividexperience.com.sa/en. Both that site and https://syncs.com.sa/ returned proxy access denials during inspection. No reference photographs, branding, fonts, or proprietary code were copied. SYNCs brand colors and typography could not be verified.

Observed: deep navy section; centered coral eyebrow; large white title; four photographic project cards; wider and taller third card; rounded corners; category pills; bottom gradient; carousel arrows; coral CTA. Header/navigation are outside the requested section.

Adaptation: original English copy and abstract event-stage demonstration artwork. Navy #071520, coral #f49376, white titles; system Arial typography. Content width approximately 1120px, desktop padding 84px/72px, 20px card gaps, 20px corner radii. Desktop cards 398px tall; featured card 444px and 2.9 times the other card widths. Controls are below the cards for predictable keyboard and mobile access. Hovering a card or using arrow controls changes the featured item. No autoplay. Four items remain visible on desktop; this is an expanding-card selector, not an infinite looping image slider.

1440px: four cards, third initially featured. 768px: four cards with smaller spacing, 340/390px card heights. 390px: horizontal touch scrolling with 86%-width cards and scroll snapping, 380px card height, first item initially selected. Reduced-motion preference removes card transitions and smooth programmatic scrolling.

Elementor structure: section Container > intro Container (paragraph eyebrow + H2 Heading), track Container > four card Containers (Image, paragraph category Heading, H3 Heading), one HTML widget for scoped CSS/controller/buttons, one native Button widget. No add-on widgets, background media dependencies, Pro carousel schema, or custom plugin. Container CSS classes and native widget settings are editable; detailed styling is in the HTML widget. This is not entirely no-code: controls and transitions use custom CSS/JS.

Accessibility: H2 section title, H3 projects, semantic button controls with accessible names, keyboard arrow navigation within the focusable track, visible focus, polite selection status, reduced motion, no timed rotation. Set useful alt text in the Media Library for final project images. Demo artwork is illustrative. Replace generic project copy and CTA destination before use. RTL is not implemented or validated.
