<?php // vi:ts=4:et
set_magic_quotes_runtime(0);

// send the result back as text/plain, so that we don't have to care
// about html entities and such
header("Content-type: text/plain");

echo "[info: this is Content-type: text/plain, so you should get\n";
echo "       back exactly what I have received]\n\n";
echo "POST vars from HTTP request:\n\n";

if (is_array($_POST))
{
    while (list($k, $v) = each($_POST))
    {
        printf("  '%s': '%s'\n", $k, $v);
    }
}

echo "\n[end of file]\n";
