<?php
/*
    WordPress Sphinx Search Plugin by Ivinco (opensource@ivinco.com), 2011.
    If you need commercial support, or if you’d like this plugin customized for your needs, we can help.

    Visit plugin website for the latest news:
    http://www.ivinco.com/software/wordpress-sphinx-search-plugin  

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

/*
 * this is new indexing method, used since version 2.0
 * Wordpress Delta index update file
 * Add the following cron job to update delta index every 5 minutes:
 */
// */5 * * * * /usr/bin/php /home/www/MK_xunzhao/wp-content/uploads/sphinx/cron/cron_reindex_delta.php

define('PATH_TO_SPHINX_INDEXER', '/usr/local/sphinx-for-chinese/bin/indexer');
define('PATH_TO_SPHINX_CONFIG', '/home/www/MK_xunzhao/wp-content/uploads/sphinx/sphinx.conf');
define('SPHINX_INDEX_NAME', 'wp_');

$command = PATH_TO_SPHINX_INDEXER." --config ".PATH_TO_SPHINX_CONFIG." ".SPHINX_INDEX_NAME."delta --rotate ";
system($command, $retval);
