<?php
/**
 * Plugin Name: SYNCs Projects Language Bridge
 * Description: Explicit Polylang language constraints for two dedicated Elementor project Query IDs.
 * Version: 1.0.0
 * Requires PHP: 7.4
 * License: GPL-2.0-or-later
 */

namespace Syncs\ProjectsLanguageBridge;

defined( 'ABSPATH' ) || exit;

const OPTION = 'syncs_projects_language_bridge';

/** Read registered language slugs through the public Polylang API. */
function language_slugs() {
    if ( ! function_exists( 'pll_languages_list' ) ) {
        return array();
    }
    $slugs = pll_languages_list( array( 'hide_empty' => false, 'fields' => 'slug' ) );
    return is_array( $slugs ) ? array_values( array_filter( $slugs, 'is_string' ) ) : array();
}

/** Read this plugin's mapping; never fall back to a visitor cookie or preferred language. */
function language_map() {
    $value = get_option( OPTION, array() );
    $value = is_array( $value ) ? $value : array();
    $map = array( 'ar' => 'ar', 'en' => 'en' );
    foreach ( array( 'ar', 'en' ) as $key ) {
        if ( array_key_exists( $key, $value ) ) {
            $map[ $key ] = is_string( $value[ $key ] ) ? $value[ $key ] : '';
        }
    }
    return $map;
}

/** Validate the admin form against configured language slugs. */
function sanitize_map( $input ) {
    $current = language_map();
    $slugs   = language_slugs();
    foreach ( array( 'ar', 'en' ) as $key ) {
        $candidate = is_array( $input ) && isset( $input[ $key ] ) && is_string( $input[ $key ] ) ? sanitize_key( $input[ $key ] ) : '';
        if ( in_array( $candidate, $slugs, true ) ) {
            $current[ $key ] = $candidate;
        } else {
            add_settings_error( OPTION, 'invalid_' . $key, 'Choose a registered Polylang language for ' . $key . '.' );
        }
    }
    if ( $current['ar'] === $current['en'] ) {
        add_settings_error( OPTION, 'same_languages', 'Choose a different language for each Query ID.' );
        return language_map();
    }
    return $current;
}

/** Limit only queries explicitly assigned one of this plugin's two Elementor Query IDs. */
function constrain_query( $query, $key ) {
    if ( ! $query instanceof \WP_Query ) {
        return;
    }
    $map  = language_map();
    $lang = isset( $map[ $key ] ) && is_string( $map[ $key ] ) ? $map[ $key ] : '';
    $ready = function_exists( 'pll_is_translated_post_type' ) && function_exists( 'pll_is_translated_taxonomy' )
        && pll_is_translated_post_type( 'project' ) && pll_is_translated_taxonomy( 'project_category' )
        && in_array( $lang, language_slugs(), true );
    if ( ! $ready ) {
        // Do not fall back to an all-language result when the configuration is unavailable.
        $query->set( 'post__in', array( 0 ) );
        return;
    }
    $query->set( 'post_type', 'project' );
    $query->set( 'lang', $lang );
    $query->set( 'suppress_filters', false );
    // Keep native taxonomy, ordering, inclusion rules, pagination and caching unchanged.
}

function arabic_query( $query ) {
    constrain_query( $query, 'ar' );
}

function english_query( $query ) {
    constrain_query( $query, 'en' );
}

add_action( 'elementor/query/syncs_projects_ar', __NAMESPACE__ . '\\arabic_query' );
add_action( 'elementor/query/syncs_projects_en', __NAMESPACE__ . '\\english_query' );

add_action( 'admin_init', function () {
    register_setting( 'syncs_projects_languages', OPTION, array( 'type' => 'array', 'sanitize_callback' => __NAMESPACE__ . '\\sanitize_map' ) );
} );

add_action( 'admin_menu', function () {
    add_management_page( 'SYNCs Projects Languages', 'SYNCs Projects Languages', 'manage_options', 'syncs-projects-languages', __NAMESPACE__ . '\\settings_page' );
} );

/** Render a capability-protected settings form; options.php supplies nonce/capability checks. */
function settings_page() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }
    $slugs = language_slugs();
    $map   = language_map();
    $post_ok = function_exists( 'pll_is_translated_post_type' ) && pll_is_translated_post_type( 'project' );
    $tax_ok  = function_exists( 'pll_is_translated_taxonomy' ) && pll_is_translated_taxonomy( 'project_category' );
    echo '<div class="wrap"><h1>SYNCs Projects Languages</h1>';
    echo '<p dir="rtl">اختاري لغة كل Query ID، ثم عيّنيه يدويًا في Loop Grid داخل صفحة اللغة المناسبة. الإضافة لا تغيّر لغات المشاريع أو التصنيفات أو إعدادات الكاش.</p>';
    echo '<p>Elementor Pro: <strong>' . esc_html( defined( 'ELEMENTOR_PRO_VERSION' ) ? ELEMENTOR_PRO_VERSION : 'Not detected' ) . '</strong></p>';
    echo '<p>Polylang project translation: <strong>' . esc_html( $post_ok ? 'Enabled' : 'Missing / disabled' ) . '</strong><br>';
    echo 'Polylang project_category translation: <strong>' . esc_html( $tax_ok ? 'Enabled' : 'Missing / disabled' ) . '</strong></p>';
    echo '<p dir="rtl">لو أحد المتطلبات غير مفعّل، الاستعلامات المرتبطة بهذه الإضافة سترجع بدون نتائج بدل خلط اللغات. راجعي Languages → Settings وتعيين لغات المشاريع والتصنيفات أولًا.</p>';
    settings_errors( OPTION );
    if ( ! $slugs ) {
        echo '<p>Polylang has no available languages. Activate/configure Polylang first.</p></div>';
        return;
    }
    echo '<form method="post" action="options.php">';
    settings_fields( 'syncs_projects_languages' );
    echo '<table class="form-table" role="presentation">';
    foreach ( array( 'ar' => 'Arabic page', 'en' => 'English page' ) as $key => $label ) {
        echo '<tr><th scope="row"><label for="syncs-lang-' . esc_attr( $key ) . '">' . esc_html( $label ) . '</label><p><code>syncs_projects_' . esc_html( $key ) . '</code></p></th><td>';
        echo '<select id="syncs-lang-' . esc_attr( $key ) . '" name="' . esc_attr( OPTION ) . '[' . esc_attr( $key ) . ']">';
        echo '<option value="">Choose language</option>';
        foreach ( $slugs as $slug ) {
            echo '<option value="' . esc_attr( $slug ) . '"' . selected( $map[ $key ], $slug, false ) . '>' . esc_html( $slug ) . '</option>';
        }
        echo '</select></td></tr>';
    }
    echo '</table>';
    submit_button();
    echo '</form></div>';
}
