<?php
    set_time_limit(0);
    header("Access-Control-Allow-Origin: *");  
    header("Content-Type: application/json");
    date_default_timezone_set("Asia/Bangkok");
    include("../../../dbconfig/dbconfig.php");

    $l2Name = strtoupper($_GET["l2Name"]);
    if($l2Name === null) {
        http_response_code(400);
    }else {
        $objConnect = oci_connect($dbuser, $dbpass, $tnsname, "AL32UTF8");
        $sql = "SELECT
                    OLT_NAME, GPON_PORT, ONU_ID, L2_SPLITTER_OUT, L2_SERVICE_STATE, RUNNING_STATE,
                    L1_SPLITTER, L1_SPLITTER_OUT, LAN1, L2_LATITUDE, L2_LONGITUDE, L2_SUBDISTRICT,
                    L2_DISTRICT, L2_PROVINCE
                FROM
                    FTTX_INV_QRUN_L2
                WHERE
                    LAN1 IS NOT NULL
                    AND L2_SPLITTER_NAME = '$l2Name'";
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
            $err->message = "Splitter L2 not found.";
            echo json_encode($err);
        } else {
            $response["OLT_NAME"] = $res[0]["OLT_NAME"];
            $response["GPON_PORT"] = $res[0]["GPON_PORT"];
            $response["L1_SPLITTER"] = $res[0]["L1_SPLITTER"];
            $response["L1_SPLITTER_OUT"] = $res[0]["L1_SPLITTER_OUT"];
            $response["L2_LATITUDE"] = $res[0]["L2_LATITUDE"];
            $response["L2_LONGITUDE"] = $res[0]["L2_LONGITUDE"];
            $response["L2_SUBDISTRICT"] = $res[0]["L2_SUBDISTRICT"];
            $response["L2_DISTRICT"] = $res[0]["L2_DISTRICT"];
            $response["L2_PROVINCE"] = $res[0]["L2_PROVINCE"];
            $response["ONUs"] = array_map("mapOnuValue", $res);
            http_response_code(200);
            echo json_encode($response);
        }

    }
    function mapOnuValue($o) {
        $response["ONU_ID"] = $o["ONU_ID"];
        $response["L2_SPLITTER_OUT"] = $o["L2_SPLITTER_OUT"];
        $response["L2_SERVICE_STATE"] = $o["L2_SERVICE_STATE"];
        $response["RUNNING_STATE"] = $o["RUNNING_STATE"];
        $response["LAN1"] = $o["LAN1"];
        return $response;
    }
?>
