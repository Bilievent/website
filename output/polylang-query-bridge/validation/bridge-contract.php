<?php
// Public WordPress/Elementor hook contract simulation, not a full WordPress or Pro runtime.
define('ABSPATH', '/test/');
$GLOBALS['hooks'] = array();
$GLOBALS['options'] = array();
$GLOBALS['errors'] = array();
$GLOBALS['slugs'] = array('ar', 'en');
$GLOBALS['post_translated'] = true;
$GLOBALS['tax_translated'] = true;
function add_action($name, $callback, $priority = 10, $args = 1) { $GLOBALS['hooks'][$name][] = $callback; }
function do_action($name, ...$args) { foreach ($GLOBALS['hooks'][$name] ?? array() as $fn) { call_user_func_array($fn, $args); } }
function get_option($name, $default = false) { return $GLOBALS['options'][$name] ?? $default; }
function sanitize_key($value) { return preg_replace('/[^a-z0-9_\-]/', '', strtolower($value)); }
function add_settings_error($name, $code, $message) { $GLOBALS['errors'][] = $code; }
class WP_Query {
    public $query_vars;
    public function __construct($args) { $this->query_vars = $args; }
    public function get($name) { return $this->query_vars[$name] ?? ''; }
    public function set($name, $value) { $this->query_vars[$name] = $value; }
}
$without = in_array('--without-polylang', $argv, true);
if (!$without) {
    function pll_languages_list($args = array()) { return $GLOBALS['slugs']; }
    function pll_is_translated_post_type($type) { return $type === 'project' && $GLOBALS['post_translated']; }
    function pll_is_translated_taxonomy($type) { return $type === 'project_category' && $GLOBALS['tax_translated']; }
    function pll_current_language($field = 'slug') { return 'en'; } // Deliberately conflicts with Arabic query.
}
require dirname(__DIR__) . '/plugin/syncs-projects-language-bridge/syncs-projects-language-bridge.php';
function check($condition, $message) { if (!$condition) { fwrite(STDERR, "FAIL: $message\n"); exit(1); } }
$base = array('post_type'=>'project', 'posts_per_page'=>30, 'paged'=>2, 'orderby'=>'date', 'order'=>'DESC', 'cache_results'=>true, 'tax_query'=>array(array('taxonomy'=>'project_category','terms'=>array(5,8),'operator'=>'IN')));
if ($without) {
    $query = new WP_Query($base);
    do_action('elementor/query/syncs_projects_ar', $query);
    check($query->get('post__in') === array(0), 'Missing Polylang must not return all languages');
    echo json_encode(array('mode'=>'without Polylang','safeEmptyResult'=>'passed')) . "\n";
    exit(0);
}
foreach (array('ar','en') as $slug) {
    $_GET['lang'] = $slug === 'ar' ? 'en' : 'ar';
    $_COOKIE['pll_language'] = $_GET['lang'];
    $query = new WP_Query($base);
    do_action('elementor/query/syncs_projects_' . $slug, $query);
    check($query->get('lang') === $slug, 'Query ID must override preferred/request language');
    check($query->get('suppress_filters') === false, 'Polylang filters stay enabled');
    foreach ($base as $key=>$value) { check($query->get($key) === $value, 'Native query setting changed: '.$key); }
}
$unrelated = new WP_Query($base);
do_action('pre_get_posts', $unrelated);
check($unrelated->query_vars === $base, 'Unrelated query changed');
check(!isset($GLOBALS['hooks']['pre_get_posts']), 'No global query interception');
$GLOBALS['options']['syncs_projects_language_bridge'] = array('ar'=>'ar-sa','en'=>'en-gb');
$GLOBALS['slugs'] = array('ar-sa','en-gb');
$query = new WP_Query($base);
do_action('elementor/query/syncs_projects_ar', $query);
check($query->get('lang') === 'ar-sa', 'Custom language slug mapping failed');
$GLOBALS['options']['syncs_projects_language_bridge']['ar'] = 'invalid';
$query = new WP_Query($base);do_action('elementor/query/syncs_projects_ar', $query);
check($query->get('post__in') === array(0), 'Unknown language must not fall back');
$GLOBALS['options'] = array();$GLOBALS['slugs'] = array('ar','en');
foreach (array('post_translated','tax_translated') as $flag) {
    $GLOBALS[$flag] = false;$query = new WP_Query($base);do_action('elementor/query/syncs_projects_en', $query);
    check($query->get('post__in') === array(0), 'Untranslated content type/taxonomy must not mix languages');$GLOBALS[$flag] = true;
}
$map = \Syncs\ProjectsLanguageBridge\sanitize_map(array('ar'=>array('x'),'en'=>'en<script>'));
check($map === array('ar'=>'ar','en'=>'en'), 'Malformed fields should retain safe mapping');
$map = \Syncs\ProjectsLanguageBridge\sanitize_map(array('ar'=>'en','en'=>'en'));
check($map === array('ar'=>'ar','en'=>'en'), 'Same-language mapping should be rejected');
check(count($GLOBALS['errors']) >= 3, 'Invalid mapping errors not reported');
$hooks = array_keys($GLOBALS['hooks']);sort($hooks);
check($hooks === array('admin_init','admin_menu','elementor/query/syncs_projects_ar','elementor/query/syncs_projects_en'), 'Unexpected global hooks');
echo json_encode(array('mode'=>'API contract simulation','explicitArabicAndEnglish'=>'passed','wrongCookieAndRequestLanguage'=>'ignored as intended','nativeTaxonomyAndPagination'=>'preserved','cacheResults'=>'unchanged','customSlugs'=>'passed','invalidConfiguration'=>'safe empty result','unrelatedQueries'=>'unchanged','sanitization'=>'passed','runtime'=>'PHP '.PHP_VERSION,'nativeElementorAndPolylangIntegration'=>'not executed')) . "\n";
