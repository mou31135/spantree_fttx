<?php
    set_time_limit(0);
    header("Content-Type: application/json");
    date_default_timezone_set("Asia/Bangkok");
    include("../../../dbconfig/dbconfig.php");

    $oltName = strtoupper($_GET["oltName"]);

    if($oltName === null) {
        http_response_code(400);
    }else {
        $objConnect = oci_connect($dbuser, $dbpass, $tnsname, "AL32UTF8");
        $sql = "SELECT OLT_IP, OLT_VENDOR, RUNNING_STATE, SERVICE_STATE, SUBDISTRICT, DISTRICT,
                PROVINCE, OLT_LATITUDE, OLT_LONGITUDE, AREA,SITE, OLT_MODEL,QR_OLT_ID 
                FROM FTTX_INV_QRUN_OLT WHERE OLT_NAME = '$oltName'";
        $objParse = oci_parse($objConnect, $sql);
        oci_execute ($objParse, OCI_DEFAULT);
        $res = array();
        while($objResult = oci_fetch_assoc($objParse)){
            $res[] = $objResult;
        }
        oci_close($objConnect);
        if(count($res) <= 0) {
            http_response_code(400);
            $err = new \stdClass();
            $err->message = "OLT not found.";
            echo json_encode($err);
        }else {
            http_response_code(200);
            echo json_encode($res[0]);
        }
    }
?>