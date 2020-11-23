<?php
$ip = $_GET["ip"];
$fsp = $_GET["fsp"];
$exitcode = 0;

if($ip == NULL or $fsp == NULL){
http_response_code(400);
echo "Incomplete args";
die();
}

exec("python OLT_EE4.py $ip $fsp 2>&1",$output,$exitcode);
if ($exitcode > 0){
echo $exitcode;
print_r ($output);
if ($exitcode == 4){
    http_response_code(400);
    exit(1);
}
elseif($exitcode == 2){
    http_response_code(408);
    die();
}
elseif($exitcode == 3){
    http_response_code(400);
    die();
}
elseif($exitcode == 5){
    http_response_code(401);
    die();
}
else{
    http_response_code(500);
    die();
}}
else{
header('Content-Type: application/json');
$data = implode('', $output);
echo $data;
}


?>
