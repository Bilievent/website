# Booth Design & Production — visual proposal

Source: `elementor-7181-2026-11-01.json` and the user's accompanying English booth content. Stage: image review before preparing an Elementor import. No live site changes.

## Observed baseline

The supplied export has nine top-level containers. Existing widgets include core Heading, Text Editor, Icon Box, Icon, Icon List, Button, Divider and Spacer; Pro Animated Headline and Posts; ElementsKit Heading, Image Comparison and Accordion; and an external MetForm instance. The form field definitions are absent. The hero has 350 px desktop top padding and 250 px tablet top padding, with no explicit mobile override. Several headings refer to stages or permits; some contain stray braces. Posts uses old date limits and unrelated permit copy. These are observed control/data findings, not a live browser audit.

## Proposed direction

Eight content sections, using only existing widget types. Use the existing site header/footer outside this template. Combine repetitive introductory copy into the hero/services. Remove the unrelated permit-article block; retain the user's real exhibition-planning guide as an inline link in the quotation/FAQ area. No added statistics, testimonials, fabricated credentials, visitor filters or new section types.

1. Hero: a concise service heading, one introductory paragraph, the four existing capabilities as text, one primary quote button, and a real Watad project photo. Desktop split layout; mobile heading/copy/button/photo order. No oversized empty banner.
2. Services: design and rental explained together, followed by twelve concise existing Icon Box capability entries. Editorial rows rather than twelve heavy cards. Link technical/media services in their relevant existing text.
3. Design to build: retain the existing ElementsKit Image Comparison widget type, two selected examples rather than four repetitive panels. A paired 3D/build example must use its real source pair, never an invented project claim. Concept visual may illustrate the slider's placement; unresolved comparison assets require verification at implementation.
4. Booth formats: six existing Icon Boxes, short descriptions and the user's SVG line icons. Group within one light section.
5. Workflow: the existing five numbered steps, slim dividers and concise descriptions. Vertical on phones; desktop split image and steps. All five remain visible.
6. Projects: Watad, SIRA and Athar, with their real photos, truthful delivery scope and existing project links. One larger card plus two supporting cards on desktop; one full-width sequence on phones.
7. FAQ and quote: existing ElementsKit Accordion and MetForm, no new widget type. Include the eight existing questions and pricing/inclusions guidance in their answers. Proposed form arrangement: explicit labels, one field per row on phones, sensible input types and large submit button. Actual MetForm fields require reviewing the referenced form inside WordPress.
8. Final CTA: a compact lavender band using the existing Heading and Button types. No additional full-screen contact section.

## Design tokens

Deep Midnight `#1D162A`; Royal Purple `#8F7BB8`; Dark Purple `#2B203D`; Charcoal `#3A3447`; Lavender `#C9BCE3`; Light Gray `#F5F5F7`; Soft White `#FAFAFC`; Silver `#D8D8E0`; White `#FFFFFF`; Graphite `#4A4557`. Pair dark text with lavender buttons; use white text on Midnight. Purple is an accent, not small body copy on light backgrounds.

Manrope headings and legible sans-serif body type, derived from the supplied export. One H1. Body 16–18 px with 1.5–1.65 line height. Desktop content max 1200 px. Space scale 8/12/16/24/32/48/64/80; restrained 12–20 px image corners. Avoid decorative gradients and ornamental card walls.

## Responsive intent

- 390 px: 20 px side gutters, 34–38 px H1, 26–30 px section titles, full-width primary button with at least 48 px height, single-column photography and form, two-column short capability/format entries only where readable, no horizontal page overflow. Image comparisons must allow touch and keyboard operation with clear labels and usable handles.
- 768 px: 28 px gutters, two-column compact service/format groups, stack any text/image composition that makes body copy narrow. No fixed attachment or scroll hijacking.
- 1440 px: 48 px gutters, max 1200 px content, 58–64 px H1, mixed editorial layouts, generous but controlled spacing.

## Preview limits

The requested image is a design proposal, not a WordPress/Elementor runtime screenshot. Generated visuals cannot verify source widget interactions, responsive behavior, real MetForm fields or installed plugin compatibility. Photographs supplied to the visual generator are the user's actual Watad, SIRA and Athar images recovered from their attached ZIP. Native editable JSON and import/re-export QA belong to the next implementation step after visual review.
