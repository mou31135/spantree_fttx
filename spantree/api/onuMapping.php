<?php
    set_time_limit(0);
        header("Access-Control-Allow-Origin: *");
    header("Content-Type: application/json");
    date_default_timezone_set("Asia/Bangkok");
    include("../../../dbconfig/dbconfig.php");

    $oltName = strtoupper($_GET["oltName"]);
    $port = $_GET["port"];
    if($oltName === null || $port === null) {
        http_response_code(400);
    }else {
        $objConnect = oci_connect($dbuser, $dbpass, $tnsname, "AL32UTF8");
        $sql = "SELECT LAN1, ONU_ID
                FROM FTTX_INV_QRUN_L2
                WHERE OLT_NAME = '$oltName' AND GPON_PORT = '$port' AND LAN1 IS NOT NULL";
        $objParse = oci_parse($objConnect, $sql);
        oci_execute ($objParse, OCI_DEFAULT);
        $res = array();
        while($objResult = oci_fetch_assoc($objParse)){
            $res[] = $objResult;
        }
        oci_close($objConnect);

        http_response_code(200);
        echo json_encode($res);
    }
?>
