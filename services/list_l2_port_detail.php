<?php
    set_time_limit(0);
    header("Content-Type: application/json");
    date_default_timezone_set("Asia/Bangkok");
    include("../../dbconfig/dbconfig.php");

    $l2_name = $_GET["name"];

    $objConnect = oci_connect($dbuser, $dbpass, $tnsname,"AL32UTF8");

    $sqlSummary = "SELECT L2_SERVICE_STATE, COUNT(*) count FROM FTTX_INV_QRUN_L2 WHERE L2_SPLITTER_NAME = '$l2_name' GROUP BY L2_SERVICE_STATE";
    $sqlDetail = "SELECT LAN1, L2_SPLITTER_OUT, L2_SERVICE_STATE FROM FTTX_INV_QRUN_L2 WHERE L2_SPLITTER_NAME = '$l2_name'";

    $objParse = oci_parse($objConnect, $sqlSummary);
    oci_execute ($objParse, OCI_DEFAULT);
    $summary = array();
    while($objResult = oci_fetch_assoc($objParse)){
        $summary[] = $objResult;
    }

    $objParse = oci_parse($objConnect, $sqlDetail);
    oci_execute ($objParse, OCI_DEFAULT);
    $detail = array();
    while($objResult = oci_fetch_assoc($objParse)){
        $detail[] = $objResult;
    }

    oci_close($objConnect);

    $response->summary = $summary;
    $response->detail = $detail;
    echo json_encode($response);
    exit;
?>