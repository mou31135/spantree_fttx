<?php
		header("Access-Control-Allow-Origin: *");
    header("Content-Type: application/json");
    include("../../dbconfig/dbconfig.php");

    $olt = "";

    if(isset($_GET["oltname"])){
        $olt = $_GET["oltname"];
    }
    else{
        echo json_encode("Invalid Input.");
        exit;
    }

    $objConnect = oci_connect($dbuser,$dbpass,$tnsname,'AL32UTF8');

    $sql = "SELECT OLT_NAME,L1_SPLITTER,GPON_PORT,L2_SPLITTER_NAME,LAN1 FROM FTTX_INV_QRUN_L2 WHERE OLT_NAME='$olt'";

    $objParse = oci_parse($objConnect, $sql);
    oci_execute ($objParse,OCI_DEFAULT);

    $res = array();

    while($objResult = oci_fetch_assoc($objParse)){
        $res[] = $objResult;
    }

    oci_close($objConnect);

    $l1 = array();
    $l2 = array();
    for($i=0;$i<sizeof($res);$i++){
        $l1[] = $res[$i]["L1_SPLITTER"];
        $l2[] = $res[$i]["L2_SPLITTER_NAME"];
    }

    $uniq = array_unique($l1,SORT_REGULAR);
    $l1 = array_values($uniq);
    sort($l1);

    $uniq = array_unique($l2,SORT_REGULAR);
    $l2 = array_values($uniq);
    sort($l2);

    //mapping L1<=>L2
    $mapL1L2 = array();
    for($i=0;$i<sizeof($l2);$i++){
        for($j=0;$j<sizeof($res);$j++){
            if($l2[$i] == $res[$j]["L2_SPLITTER_NAME"]){
                $mapL1L2[$i] = array("L1"=>$res[$j]["L1_SPLITTER"],"L2"=>$res[$j]["L2_SPLITTER_NAME"]);
            }
        }
    } //echo sizeof($mapL1L2);

    //mapping L1<=>GPON_PORT
    $mapL1GP = array();
    for($i=0;$i<sizeof($l1);$i++){
        for($j=0;$j<sizeof($res);$j++){
            if($l1[$i] == $res[$j]["L1_SPLITTER"]){
                $mapL1GP[$i] = array("L1"=>$res[$j]["L1_SPLITTER"],"GP"=>$res[$j]["GPON_PORT"]);
            }
        }
    } //print_r($mapL1GP);

    //mapping circuit
    $mapcircuit = array(); $k=0;
    for($i=0;$i<sizeof($l2);$i++){
        for($j=0;$j<sizeof($res);$j++){
            if($l2[$i] == $res[$j]["L2_SPLITTER_NAME"]){
                $mapcircuit[$k] = array("L2"=>$res[$j]["L2_SPLITTER_NAME"],"CIRCUIT"=>$res[$j]["LAN1"]); $k++;
            }
        }
    } //print_r($mapcircuit);

    $root2 = array();
    for($i=0;$i<sizeof($l1);$i++){
        $root2[] = array("id"=>$l1[$i],"name"=>$l1[$i]." : ". $mapL1GP[$i]["GP"]);
    } //echo sizeof($root2);

    for($i=0;$i<sizeof($root2);$i++){
        $temp = array();
        for($j=0;$j<sizeof($mapL1L2);$j++){
            if($root2[$i]["id"] == $mapL1L2[$j]["L1"]){
                $temp[] = array("id"=>$mapL1L2[$j]["L2"],"name"=>$mapL1L2[$j]["L2"]);
            }

            if($j == sizeof($mapL1L2)-1){
                $root2[$i]["children"] =  $temp;
            }
        }
    } //echo json_encode($root2);

    for($i=0;$i<sizeof($root2);$i++){
        for($j=0;$j<sizeof($root2[$i]["children"]);$j++){
            $temp = array();
            for($k=0;$k<sizeof($mapcircuit);$k++){
                if($root2[$i]["children"][$j]["id"] == $mapcircuit[$k]["L2"]){
                    $temp[] = array("name"=>$mapcircuit[$k]["CIRCUIT"]);
                }

                if($k == sizeof($mapcircuit)-1){
                    $root2[$i]["children"][$j]["children"] =  $temp;
                }
            }
        }
    } //echo json_encode($root2);

    $root = array("id"=>$res[0]["OLT_NAME"],"name"=>$res[0]["OLT_NAME"],"children"=>$root2);

    echo json_encode($root);

    exit;
?>
