<?php
	header("Access-Control-Allow-Origin: *");
	header("Content-Type: application/json; charset=UTF-8");
	header("Access-Control-Allow-Methods: POST");

	date_default_timezone_set('Asia/Bangkok');
	include("../../dbconfig/dbconfig.php");

	//get authen
	$token = "";
	$headers = apache_request_headers();

	if(isset($headers["token"])){
		$token = $headers["token"];
	}
	else{
		http_response_code(403);
		echo json_encode(array("code"=>403,"message"=>"token header required."));
		exit;
	}

	if($token !== "QQzTP=Qz5TJH1DanCQ6BJ1expmC2j7Q7Yo=LmPjrH06IEh3e6a"){
		http_response_code(403);
		echo json_encode(array("code"=>403,"message"=>"token header required."));
		exit;
	}

	// get posted data
	$data = json_decode(file_get_contents("php://input"),true);

	file_put_contents("log/addwork.log",$data,FILE_APPEND);

	$REF_NO = "";
	$PROJECTNAME = "";
	$STATUS = "";
	$REGION = "";
	$WORK_NO = "";
	$CONTRACTORNAME = "";
	$LOCATION = "";
	$DESCRIPTION = "";
	$CREATE_BY = "";
	$CREATE_DATE = "";
	$SOS = "";
	$SOS_SITENAME ="";

  if(isset($data["REF_NO"]) && isset($data["PROJECTNAME"]) && isset($data["STATUS"]) &&
		isset($data["REGION"]) && isset($data["WORK_NO"]) && isset($data["CONTRACTORNAME"]) &&
		isset($data["LOCATION"]) && isset($data["DESCRIPTION"]) && isset($data["CREATE_BY"]) &&
		isset($data["CREATE_DATE"]) && isset($data["SOS"]) && isset($data["SOS_SITENAME"])){

		$REF_NO = $data["REF_NO"];
		$PROJECTNAME = $data["PROJECTNAME"];
		$STATUS = $data["STATUS"];
		$REGION = $data["REGION"];
		$WORK_NO = $data["WORK_NO"];
		$CONTRACTORNAME = $data["CONTRACTORNAME"];
		$LOCATION = $data["LOCATION"];
		$DESCRIPTION = $data["DESCRIPTION"];
		$CREATE_BY = $data["CREATE_BY"];
		$CREATE_DATE = $data["CREATE_DATE"];
		$SOS = $data["SOS"];
		$SOS_SITENAME = $data["SOS_SITENAME"];
	}
	else{
		http_response_code(400);
    echo json_encode(array("message"=>"Invalid input."));
		exit;
	}

	$objConnect = oci_connect($dbuser,$dbpass,$tnsname,'AL32UTF8');

	if($objConnect){
		if(strtolower($STATUS) == "open"){

			$SQL2 = "insert into fttx_workorder_prom (REF_NO,PROJECTNAME,STATUS,REGION,WORK_NO,CONTRACTORNAME,LOCATION,DESCRIPTION,CREATE_BY,CREATE_DATE,SOS,SOS_SITENAME) values 
				('$REF_NO','$PROJECTNAME','$STATUS','$REGION','$WORK_NO','$CONTRACTORNAME','$LOCATION','$DESCRIPTION','$CREATE_BY',to_date('$CREATE_DATE','dd/mm/yyyy hh24:mi:ss'),'$SOS','$SOS_SITENAME') ";
			$objParse2 = oci_parse($objConnect, $SQL2);
			
			oci_execute ($objParse2,OCI_DEFAULT);

			oci_commit($objConnect);
			oci_close($objConnect);
			
			http_response_code(200);
      echo json_encode(array("message"=>"Complete."));
			exit;
		}
		else if(strtolower($STATUS) !== "open"){
			$SQL2 = "UPDATE fttx_workorder_prom SET STATUS = '$STATUS' where REF_NO='$REF_NO' ";
			$objParse2 = oci_parse($objConnect, $SQL2);
			
			oci_execute ($objParse2,OCI_DEFAULT);

			oci_commit($objConnect);
			oci_close($objConnect);
			
			http_response_code(200);
      echo json_encode(array("message"=>"Complete."));
			exit;
		}
		else{
			oci_close($objConnect);
			
			http_response_code(400);
      echo json_encode(array("message"=>"Invalid input."));
			exit;
		}
	}
	else{
		http_response_code(503);
		echo json_encode(array("message"=>"Database connection failed."));

    exit;
	}
?>