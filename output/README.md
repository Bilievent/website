# Current delivery: complete dynamic projects page

Use `projects-page/SYNCs-Projects-Page.json` or `SYNCs-Projects-Page-Bundle.zip` for the latest full-page request. See `projects-page/import-instructions-ar.md`.

The full-page template preserves the user's real Loop Grid (post type project, external Loop Item 6526, 30 results) and project_category filter, repairs the filter's dangling grid reference, and applies the reference-inspired responsive design. It uses the existing card document on the same site; no per-project image replacement or shell setup is required. Actual Elementor import and native runtime validation remain pending staging tests.

Earlier `dynamic-projects/` files were the interim section shell/Loop Item integration. The initial static-card JSON and ZIP are superseded. All are retained for history; use the latest page bundle above.


For the reported stale filtering and Polylang issue, use `SYNCs-Filter-UI-Patch.zip` and read `projects-page/filter-polylang-notes-ar.md`. This presentation patch preserves translated page content and native queries. Server language/cache diagnosis remains blocked by live-site access (proxy 403) and missing runtime settings and filter-response evidence (Polylang + LiteSpeed Cache are identified).


An explicit-language server bridge is now available in `polylang-query-bridge/` and `syncs-projects-language-bridge.zip`. It adds two reserved Elementor Query ID hooks configured through Tools; it does not auto-install or change page queries. User confirmed mixed-language results persist under the LiteSpeed optimization-bypass comparison. Read the Arabic setup and staging limitations before applying.
