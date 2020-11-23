<?php
    set_time_limit(0);
    header("Content-Type: application/json");
    date_default_timezone_set("Asia/Bangkok");
    include("../../../dbconfig/dbconfig.php");

    $lan1 = $_GET["lan1"];

    if($lan1 === null) {
        http_response_code(400);
    }else {
        $objConnect = oci_connect($dbuser, $dbpass, $tnsname, "AL32UTF8");
        $sql = "SELECT L2_SPLITTER_NAME, OLT_NAME, GPON_PORT, ONU_ID, L2_SPLITTER_NO, L2_SERVICE_STATE,
                    RUNNING_STATE, L1_SPLITTER, L2_SPLITTER_OUT
                FROM FTTX_INV_QRUN_L2
                WHERE LAN1 = '$lan1'";
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
            $err->message = "ONU not found.";
            echo json_encode($err);
        }else {
            http_response_code(200);
            echo json_encode($res[0]);
        }
    }
?>