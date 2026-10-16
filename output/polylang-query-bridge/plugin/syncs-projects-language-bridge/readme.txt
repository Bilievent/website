=== SYNCs Projects Language Bridge ===
Requires PHP: 7.4
Version: 1.0.0
License: GPL-2.0-or-later

Dedicated Elementor Query IDs:
  English page: syncs_projects_en
  Arabic page:  syncs_projects_ar

After activation open Tools > SYNCs Projects Languages and confirm the Polylang language mappings and that project/project_category translation is enabled. Set each Query ID in its corresponding translated Elementor Loop Grid. Do not use one fixed ID for a shared bilingual document.

Only these explicit Query IDs are affected. Missing Polylang or invalid mappings produce an empty result rather than an all-language result. Existing terms, ordering, pagination and caching are preserved. No content, language assignment or global cache settings are changed.

PHP syntax and API-contract simulations passed on PHP 7.4/8.3/8.5. Actual WordPress/Elementor Pro filtering remains untested. Install on staging and test both initial and filtered results before production use. Full Arabic instructions and evidence are in the accompanying repository output/polylang-query-bridge/.

Rollback: clear the two Query IDs, deactivate the plugin, then purge the affected page URLs.
