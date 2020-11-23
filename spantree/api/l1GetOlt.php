<?php
    set_time_limit(0);
    header("Access-Control-Allow-Origin: *");
    header("Content-Type: application/json");
    date_default_timezone_set("Asia/Bangkok");
    include("../../../dbconfig/dbconfig.php");

    $l1Name = strtoupper($_GET["l1Name"]);
    if($l1Name === null ) {
        http_response_code(400);
        $err = new \stdClass();
        $err->message = "Invalid query parameters.";
        echo json_encode($err);
    } else {
        $objConnect = oci_connect($dbuser, $dbpass, $tnsname, "AL32UTF8");
        $sql = "SELECT
                    DISTINCT l2.L2_SPLITTER_NAME, l1.OLT_NAME, l1.SPLITTER_OUT, l1.RUNNING_STATE,
                    l1.L1_LATITUDE, l1.L1_LONGITUDE, l1.L1_SUBDISTRICT, l1.L1_DISTRICT, l1.L1_PROVINCE
                FROM
                    FTTX_INV_QRUN_L1 l1
                LEFT JOIN
                    FTTX_INV_QRUN_L2 l2 ON
                        l2.L1_SPLITTER = l1.L1_SPLITTER_NAME
                        AND l2.GPON_PORT = l1.GPON_PORT
                        AND l1.SPLITTER_OUT = l2.L1_SPLITTER_OUT
                WHERE
                    l1.SERVICE_STATE = 'Active'
                    AND l2.LAN1 IS NOT NULL
                    AND l1.L1_SPLITTER_NAME = '$l1Name'
                ";
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
            $err->message = "Splitter L1 not found.";
            echo json_encode($err);
        } else {
            $response["OLT_NAME"] = $res[0]["OLT_NAME"];
            $response["RUNNING_STATE"] = $res[0]["RUNNING_STATE"];
            $response["L1_LATITUDE"] = $res[0]["L1_LATITUDE"];
            $response["L1_LONGITUDE"] = $res[0]["L1_LONGITUDE"];
            $response["L1_SUBDISTRICT"] = $res[0]["L1_SUBDISTRICT"];
            $response["L1_DISTRICT"] = $res[0]["L1_DISTRICT"];
            $response["L1_PROVINCE"] = $res[0]["L1_PROVINCE"];
            $response["L2_SPLITTER"] = array_map("mapSplitterL2Value", $res);
            http_response_code(200);
            echo json_encode($response);
        }
    }

    function mapSplitterL2Value($o) {
        $result["L2_SPLITTER_NAME"] = $o["L2_SPLITTER_NAME"];
        $result["SPLITTER_OUT"] = $o["SPLITTER_OUT"];
        return $result;
    }
?>
