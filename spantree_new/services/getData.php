<?php
    set_time_limit(960);
    header("Content-Type: application/json");
    date_default_timezone_set('Asia/Bangkok');
    include("../../../dbconfig/dbconfig.php");


    $data = json_decode(file_get_contents("php://input"), TRUE);

    if(isset($data["olt_n"])){
      $olt_n = $data["olt_n"];
      $l1_n =$data["l1_name"];
      $l2_n =$data["l2_name"];

    }
    else{
      if(!isset($_POST["olt_n"])){
          echo json_encode("Invaild");
          exit;
      }

      $olt_n = $_POST["olt_n"];
      $l1_n =$_POST["l1_name"];
      $l2_n =$_POST["l2_name"];

    }


    $req_olt =strtoupper($olt_n);
    $req_l1 =strtoupper($l1_n);
    $req_l2 =strtoupper($l2_n);

    // echo $after_json;

    // exec("python tr.py $ip $onuid $circuit $olt $gp 2>&1",$output);
    exec("python tr.py $req_olt $req_l1 $req_l2 2>&1",$output);

    $res = json_decode($output[sizeof($output)-1],true);

    echo json_encode($res);

    exit;
?>
