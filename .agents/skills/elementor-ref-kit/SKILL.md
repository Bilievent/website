---
name: elementor-ref-kit
description: Convert reference URLs, screenshots, or Figma designs to creative, responsive, editable WordPress Elementor templates and validated website kits.
---

# Elementor Reference → Creative Template Kit

## Preflight
1. Inspect user reference and brand assets; distinguish observed design from interpretation.
2. Determine ownership and avoid copying third-party branding/assets.
3. Inspect WordPress, Elementor/Pro versions, theme, installed widgets, global styles and importer availability.
4. If site exists, make a backup and export native Elementor JSON from the SAME installation as schema baseline.
5. Specify output: saved-template JSON, official Elementor website kit, Envato kit or draft page. These are not interchangeable.

## Companion workflows
- Creative frontend art direction (Astra Frontend Design style): distinctive composition, typography, spacing scale, responsive grids, accessible motion.
- UI from Image: inspect screenshot at multiple breakpoints and compare screenshot renders, iterating.
- Elementor Headless: where installed, inspect actual widgets/control schemas and validate settings/structure.
- Kit packaging: prefer official Elementor export from tested WordPress environment; never rename generic ZIP an Elementor Kit.

## Execution
1. Produce design-spec.md: sections, grid, colors, fonts, spacing, images, active interactions, mobile adaptation.
2. Map each section to Elementor Flexbox Containers and native widgets; favor editable controls, not giant HTML widgets.
3. Implement sticky/scroll sections in smallest safe custom CSS/JS where native widgets are insufficient.
4. Maintain semantic H1/H2, alt text, descriptive links, keyboard focus, reduced-motion and contrast.
5. Validate with actual installed Elementor version. Do NOT hallucinate JSON control names.
6. Build at widths 1440px / 768px / 390px; compare against reference visually.
7. Import template into LocalWP/staging, render, reopen in Elementor editor to ensure editing works.
8. Only export official website kit after actual successful test; if not possible, label as untested prototype.

## Deliverables
output/design-spec.md
output/templates/*.json
output/assets/
output/import-instructions.md
output/qa-report.md
output/kit.zip (ONLY when packaged and validated for the specific importer)

Never overwrite production without user approval. In the completion report list exact files, versions, native vs custom elements, dependencies, test evidence and blockers.
