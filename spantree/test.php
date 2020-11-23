<?php
$output=shell_exec('python test.py');
header('Content-Type: application/json');
echo $output;
?>
