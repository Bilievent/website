# Full-page QA report

## Input and bindings

Inspected user export elementor-6818-2026-10-16.json (11,531 bytes), schema 0.4, type page. It includes exactly one native Loop Grid ID 5f2847bd using Loop Item 6526, post type project, and 30 posts per page. Its native Taxonomy Filter uses project_category and originally referenced ID 4938c73, absent from the export. This mismatch is repaired in the output. All other original query/filter settings are retained; masonry is disabled to support the horizontal layout. Earlier Loop Item export #6526 supplied the exact native card DOM structure and dynamic bindings.

## Static checks passed

The output JSON has 19 unique native element IDs, source type/page settings, one H1, a real existing Loop Grid/filter pair, source query count/post type/template ID, source taxonomy/child-term settings, and byte-identical breadcrumbs configuration. Filter selected_element resolves to the actual grid ID. No invented Pro query/filter settings or fixed list of project media is inserted. No old HTTP background image or ElementsKit heading remains in the page. The CSS and JS embedded in its HTML widget match the review copies under assets. Node syntax validation passes.

Core Container, global widget _css_classes and Button controls were checked against official Elementor 3.25.0 source (includes/elements/container.php, includes/widgets/common.php, includes/widgets/traits/button-trait.php). The user's exports remain the primary target-schema baseline; 3.25.0 is not asserted to be their installed version.

## Browser checks

See validation/browser-results.json for actual completed outcomes. The harness renders the new page JSON plus the original card's nested image/body/title/arrow structure, with representative source Elementor styling specificity. Abstract fixtures and mock WordPress records are explicit test data only. Mock filter clicks resolve the grid through the actual repaired selected_element setting before replacing the track, so a dangling reference breaks the harness.

Checks cover 1440/768/390px, original card styling and image crop/grayscale override, no page horizontal overflow, 30 loaded results, active state, arrows, keyboard, simulated native-filter DOM replacement, native link preservation, zero and one result, recovery to all results, newly rendered results, reduced motion, and avoiding duplicate initialization. Screenshots are local harness renderings, not screenshots of the user's WordPress website.

## Not executed / limitations

No WordPress/Elementor Pro runtime or admin/staging connection is available. Actual import, external Loop Item resolution, dynamic media and ACF links, native taxonomy-filter AJAX, plugin-generated CSS, Elementor editor reopening, export/re-import, cache behavior, native pagination/Load More and production functionality remain untested. Exact WordPress/Elementor/Pro/theme versions were not supplied. Template 6526 and its fields/taxonomy must exist on the destination site; JSON is not a database or subtemplate migration.

Original breadcrumb provider dependency remains. The existing Loop Item's custom icon is only visually hidden in this page, not deleted from the source document. Original H4 project title semantics remain; manual H3 adjustment is suggested in the guide. Only the currently loaded native results are navigable; the original cap is 30. Physical touch gestures, complete RTL, multiple copied page blocks and assistive-technology audits are unrun.

The user supplied https://syncs.com.sa/contact-us/ after the initial delivery. The native Button now reads Contact Us and uses that exact URL. Its link/text are checked in the template and local browser harness; destination availability was not tested. No production site change or WordPress publishing has occurred.

## Reproduction

Run validate-page.py with --source pointing to the original full-page export. Serve output/ on port 8766 and run browser-check.cjs with Playwright available (CHROMIUM_PATH may select an installed browser). PREVIEW_URL overrides the harness URL. These checks preserve the harness runner's exit status and do not replace the required staging checks in import-instructions-ar.md.
