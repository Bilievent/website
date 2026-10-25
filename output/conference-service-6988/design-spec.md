# Conference service — adaptation of the user's parent template #6988

The authoritative design baseline is `scega_elementor_template.zip` / `elementor-6988-2026-10-25.json`, not the earlier generated conference layout. The supplied English-page outline is content input. Its references and editorial notes were not treated as executable instructions or permission to change WordPress.

Only the first subservice, conferences, is produced. The parent contains Conferences, Exhibitions, Workshops, Training Courses and Business Meetings; the other four subservice pages remain for later review and content. The first page's content is independently editable in `service-content.json` and the resulting native export.

## Parent design retained

The Midnight outer hero with a rounded Light Gray inner panel, Royal Purple business-logo strip, white/lavender classification cards, dark preparation/scope/service cards on light sections, light Why SYNC panel, dark featured project and FAQ/contact areas, rounded Posts cards and white/purple lectern CTA all come from the supplied parent. Original widgets and container settings are cloned rather than recreating the page as HTML. Existing source fonts are retained where specified; new text and key headings use Poppins. No new off-brand artwork is created.

There are 14 content blocks arranged in 13 top-level sections because FAQ and the brief retain the parent's side-by-side layout. There is no added header/footer; the page uses the site's existing theme/Elementor header and footer. Native mobile settings explicitly stack the hero, project, FAQ/form and card groups without the parent's excessive tablet hero top spacing. The former three-project scrolling stack becomes one readable conference case; its fade/blur/scale and sticky effects are removed, and client-carousel autoplay is disabled.

## Content mapping

1. Hero: the parent Animated Headline is the single H1, supported by conference-specific copy, two native Buttons and three Icon List points. The photo is the real Agentic AI Forum image. The SCEGA logo identifies the licensing authority without suggesting that unrelated venue authorities issue the conference licence.
2. Business clients: the same six original client-logo files in the existing Image Carousel, now with an explicit heading.
3. Support needs: the same Nested Tabs and rounded detail-card design, specialized to Conference Format, Organizer and Activities. These are informational panels, not taxonomy/result filters.
4. Preparation: six source-style Icon Box cards, three/two/one columns, using the supplied information requirements and distinguishing initial review from an official document checklist.
5. Scope: the parent's document-photo panel and five-item Nested Accordion, explaining SYNC's task, the client's inputs and the authority's role.
6. Fees: a separate native three-card comparison for government charges, SYNC professional fees and published service period. SAR 5,000/10,000, five working days and 15+ years were explicitly confirmed by the user; fees/time remain category-dependent.
7. Special cases: four cloned native Icon Box cards for overseas participants, accompanying exhibitions, professional/medical requirements and hybrid activities.
8. Why SYNC: the parent's About layout, editable 15+ native Counter, and four linked support-scope options. Scope choice is collected by the real form dropdown, not simulated radio controls.
9. Complementary services: five original-style photo/content cards, specialized to conference production/booths, registration, AVL, delegate acquisition and guest accommodation/visa support.
10. Experience: the real Middle East Agentic AI Forum KSA 2026 case and supplied scope. The user supplied the exact project URL; all detail links point there.
11–12. FAQ/brief: the existing ElementsKit Accordion now holds ten conference questions and direct answers. Its FAQ schema setting is retained with matching visible content. The external MetForm reference has no field definition in the source ZIP and contains a nonportable form ID; it is replaced with the previously authorized self-contained Elementor Pro Form, seven fields, Collect Submissions only.
13. Guides: the parent's native Posts widget selects the three existing guides requested in the content: requirements (post 4647), corrections (6879) and international organizers (5655). Their IDs, English language, URLs and featured images were confirmed from public WordPress records. The old date window and Load More are removed; columns are 3/2/1 and post titles/images/URLs come from WordPress. A live category-158 feed currently includes exhibition articles, and there is no dedicated conference category. Manual Selection therefore keeps this page's guide selection relevant; adding a different guide later requires changing that selection or choosing a future conference category.
14. CTA: the parent's lectern background, readable heading, brief anchor and existing WhatsApp destination.

## Media provenance

The ZIP rewrites original media paths as `[uc_local]` and clears attachment IDs. No such paths, bundled photos, data URIs, third-party image hosting or guessed WordPress date directories are delivered in the final template. Exact URLs were recovered from public same-site WordPress media records/page HTML and checked as image responses. The user explicitly requested same-site URLs; no asset mirror was published.

The portrait `syncs-event-agency.png` crop could not be located in public media search. Its column reuses the verified same-site wide photograph of the identical white/purple lectern, positioned to the right through the native background control. Two byte-identical decorative texture copies use the same verified original texture URL. All mappings and live checks are recorded in validation.

## Scope of validation

The output uses Containers, Heading, Animated Headline, Text Editor, Button, Image, Image Carousel, Icon List, Icon Box, Counter, Divider, Icon, Nested Tabs, Nested Accordion, Posts, existing ElementsKit Accordion/Heading and the previously approved Elementor Pro Form. There is no HTML Widget or custom frontend CSS/JS. Temporary renderer HTML and interaction handlers are QA infrastructure only.

Structure, content, responsive native settings, source widget types, repeaters, links, media references, form fields and contrast are checked. An independent browser review runs at 1440/768/390 with exact attached media and a public article snapshot where available. It is not a WordPress/Elementor render and cannot certify the installed version, native frontend scripts, submissions storage or editor reopening. Actual import/edit/re-export remains for staging. This is a saved-template bundle, not an official Website Kit export.
