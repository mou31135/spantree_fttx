<?php
$exitcode = 997;
exec('python C:/xampp/htdocs/FTTX/spantree/vendorScript/HWNewDBG.py 10.238.39.2 0/2/1',$output,$rtc);
//$output=exec('python C:/xampp/htdocs/FTTX/spantree/vendorScript/HWTest.py 2>&1');
echo $rtc;
header('Content-Type: application/json');
$data = implode('', $output);
echo $data;
?>
