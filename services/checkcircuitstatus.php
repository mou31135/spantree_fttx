<?php
    set_time_limit(120);
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

    $sql = "select olt_ip from fttx_inv_qrun_olt where olt_name = '$olt'";

    $objParse = oci_parse($objConnect, $sql);
    oci_execute ($objParse,OCI_DEFAULT);

    $res = array();
    while($objResult = oci_fetch_assoc($objParse)){
        $res[] = $objResult;
    }

    if(sizeof($res) > 0){
        $olt_ip = $res[0]["OLT_IP"];
    }
    else{
        echo json_encode("OLT not found.");
        exit;
    }

    $sql = "select a.*,b.ifindex,'' as status from (
        select lan1 as circuit,ONU_ID,l2_splitter_name as l2,l1_splitter as l1,gpon_port,VENDOR
        from fttx_inv_qrun_l2
        where olt_name = '$olt'
        and onu_id is not null and lan1 is not null and L2_SERVICE_STATE = 'Active')a left join
        (select VENDOR,IFDESCR,ifindex from fttx_if_index)b on upper(b.vendor) = upper(a.vendor) and b.ifdescr = a.gpon_port";

    $objParse = oci_parse($objConnect, $sql);
    oci_execute ($objParse,OCI_DEFAULT);

    $res = array();
    while($objResult = oci_fetch_assoc($objParse)){
        $res[] = $objResult;
    }

    oci_close($objConnect);

    for($i=0;$i<sizeof($res);$i++){
        $res[$i]["STATUS"] = checkModemOnOff(strtolower($res[$i]["VENDOR"]),$olt_ip,$res[$i]["GPON_PORT"],$res[$i]["IFINDEX"],$res[$i]["ONU_ID"]);
    }

    $res1 = array();

    for($i=0;$i<sizeof($res);$i++){
        $res1[$i]["CIRCUIT"] = $res[$i]["CIRCUIT"];
        $res1[$i]["ONU_ID"] = $res[$i]["ONU_ID"];
        $res1[$i]["L2"] = $res[$i]["L2"];
        $res1[$i]["L1"] = $res[$i]["L1"];
        $res1[$i]["GPON_PORT"] = $res[$i]["GPON_PORT"];
        $res1[$i]["STATUS"] = $res[$i]["STATUS"];
    }

    $res = null;

    $l2_cut = array(
        ""
    );

    $l1_cut = array(
        ""
    );

    echo json_encode(array("circuit"=>$res1,"L2"=>$l2_cut,"L1"=>$l1_cut));

    exit;

    function checkModemOnOff($vendor,$olt_ip,$gponport,$ifindex,$onuid){
        $status = "";

        if($vendor == "huawei"){
            $walk = @snmpwalk($olt_ip, "public123", "1.3.6.1.4.1.2011.6.128.1.1.2.46.1.15.$ifindex.$onuid");
            $r = explode(":",$walk[0]);

            if(trim($r[0]) !== ""){//online
                if(trim($r[1]) == 1){
                    $status = "online";
                }
                else{
                    $status = "offline";
                }
            }
            else{
                $status = "offline";
            }
        }
        else if($vendor == "zte"){
            $walk = @snmpwalk($olt_ip, "public", '1.3.6.1.4.1.3902.1082.500.20.2.2.2.1.10.'.$ifindex.'.'.$onuid);
            $r = explode(":",$walk[0]);

            if(trim($r[0]) !== ""){//online
                if(trim($r[1]) < 65535){//online
                    $status = "online";
                }
                else{
                    $status = "offline";
                }
            }
            else{
                $status = "offline";
            }
        }
        else if($vendor == "dasan"){
            $olt_id = explode("/",$gponport);
            $olt_id = $olt_id[2];

            $walk = snmpwalk($olt_ip, "public", '1.3.6.1.4.1.6296.101.23.3.1.1.16.'.$olt_id.'.'.$onuid);
            $r = explode(":",$walk[0]);

            if(trim($r[1]) > -400){//online
                $status = "online";
            }
            else{
                $status = "offline";
            }
        }
        else if($vendor == "gcom"){
            $olt_id = explode("/",$gponport);

            $walk = @snmpwalk($olt_ip, 'public', '1.3.6.1.4.1.13464.1.14.2.4.1.4.1.5.'.$olt_id[1].'.'.$olt_id[2].'.'.$onuid);
            if($walk != false){//online
                $status = "online";
            }
            else{
                $status = "offline";
            }
        }
        else if($vendor == "raisecom"){
            $olt_id = explode("/",$gponport);
            $slot = $olt_id[1];

            if(strlen($olt_id[2])>1){
                $port = $olt_id[2];
            }
            else{
                $port = "0".$olt_id[2];
            }

            if(strlen($onuid)>1){
                $onuid = $onuid;
            }
            else{
                $onuid = "0".$onuid;
            }

            $walk = snmpwalk($olt_ip, 'public', '1.3.6.1.4.1.8886.18.3.6.3.1.1.16.'.$slot.$port.$onuid.'001');
            $r = explode(":",$walk[0]);

            if(trim($r[1]) > 0){//online
                $status = "online";
            }
            else{
                $status = "offline";
            }
        }
        else if($vendor == "fiberhome"){
            $olt_id = explode("/",$gponport);

            $ifindex = ($olt_id[1]*33554432)+($olt_id[2]*524288)+($onuid*256);

            $walk = snmpwalk($olt_ip, 'adsl', '1.3.6.1.4.1.5875.800.3.9.3.3.1.6.'.$ifindex);
            $r = explode(":",$walk[0]);

            if(trim($r[1]) !== 0){//online
                $status = "online";
            }
            else{
                $status = "offline";
            }
        }

        return $status;
    }
?>
