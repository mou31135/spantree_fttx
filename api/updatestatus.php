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

    file_put_contents("log/updatestatus.log",$data,FILE_APPEND);

    $id = "";
    $status = "";

    if(isset($data["REF_NO"]) && isset($data["STATUS"])){
        $id = $data["REF_NO"];
        $status = $data["STATUS"];
    }
    else{
        http_response_code(400);
        echo json_encode(array("code"=>400,"message"=>"Invalid input."));
        exit;
    }

    if(strtolower($status) !== "reject" && strtolower($status) !== "approve"){
        http_response_code(400);
        echo json_encode(array("code"=>400,"message"=>"Unknow status."));
        exit;
    }
    
    if(strtolower($status) == "reject"){
        $objConnect = oci_connect($dbuser,$dbpass,$tnsname);
        if($objConnect){
            //check having work
            $SQL = "select work_no from fttx_workorder_pat where REF_NO = '$id' and P_STATUS='Submit' ";
            $objParse = oci_parse($objConnect, $SQL);
            oci_execute ($objParse,OCI_DEFAULT);

            $res = array();
            while($objResult = oci_fetch_array($objParse)){
                $res[] = $objResult;
            }

            if(sizeof($res)==0){
                oci_close($objConnect);

                //New connection
                $objConnect = oci_connect($dbuser1,$dbuser1,$tnsname);
                if($objConnect){
                    //check having work
                    $SQL = "select work_no from fttx_workorder_pat where REF_NO = '$id' and P_STATUS='Submit' ";
                    $objParse = oci_parse($objConnect, $SQL);
                    oci_execute ($objParse,OCI_DEFAULT);

                    $res = array();
                    while($objResult = oci_fetch_array($objParse)){
                        $res[] = $objResult;
                    }

                    if($res[0]["WORK_NO"] == ""){
                        oci_close($objConnect);

                        http_response_code(404);
                        echo json_encode(array("code"=>404,"message"=>"Ref_No not found."));

                        exit;
                    }
                    else{
                        $worn = $res[0]["WORK_NO"];

                        $SQL = "UPDATE fttx_workorder_pat SET P_STATUS='',VERIFY_EXPORT_SPLITTER1='',CAT_SUBMIT_DATE='',CAT_COMPLETE_DATE='',OTDR_FILE_PATH=''  where WORK_NO = '$worn' and lot is null";
                        $objParse = oci_parse($objConnect, $SQL);
                        oci_execute ($objParse,OCI_DEFAULT);
                        
                        $SQL = "UPDATE fttx_inventory_temp SET P_STATUS='' where WORK_NO = '$worn' and lot is null";
                        $objParse = oci_parse($objConnect, $SQL);
                        oci_execute ($objParse,OCI_DEFAULT);
                
                        $SQL = "insert into fttx_log(name,action,work_no,action_date) values ('ATTS', 'Reject', '$worn', SYSDATE) ";
                        $objParse = oci_parse($objConnect, $SQL);
                        oci_execute ($objParse,OCI_DEFAULT);
                    
                        oci_commit($objConnect);
                        
                        oci_close($objConnect);

                        http_response_code(200);
                        echo json_encode(array("code"=>200,"message"=>"Complete."));
                        exit;
                    }
                }
                else{
                    http_response_code(503);
                    echo json_encode(array("code"=>503,"message"=>"Database connection failed."));
                    exit;
                }
            }
            else{
                $worn = $res[0]["WORK_NO"];

                $SQL = "UPDATE fttx_workorder_pat SET P_STATUS='',VERIFY_EXPORT_SPLITTER1='',CAT_SUBMIT_DATE='',CAT_COMPLETE_DATE='',OTDR_FILE_PATH=''  where WORK_NO = '$worn' and lot is null";
                $objParse = oci_parse($objConnect, $SQL);
                oci_execute ($objParse,OCI_DEFAULT);
                
                $SQL = "UPDATE fttx_inventory_temp SET P_STATUS='' where WORK_NO = '$worn' and lot is null";
                $objParse = oci_parse($objConnect, $SQL);
                oci_execute ($objParse,OCI_DEFAULT);

                $SQL = "insert into fttx_log(name,action,work_no,action_date) values ('ATTS', 'Reject', '$worn', SYSDATE) ";
                $objParse = oci_parse($objConnect, $SQL);
                oci_execute ($objParse,OCI_DEFAULT);
            
                oci_commit($objConnect);
                
                oci_close($objConnect);

                http_response_code(200);
                echo json_encode(array("code"=>200,"message"=>"Complete."));
                exit;
            }
        }
        else{
            http_response_code(503);
            echo json_encode(array("code"=>503,"message"=>"Database connection failed."));
            exit;
        }
    }
    if(strtolower($status) == "approve"){
        $objConnect = oci_connect($dbuser,$dbpass,$tnsname);
        if($objConnect){
            //check having work
            $SQL = "select work_no from fttx_workorder_pat where REF_NO = '$id' and P_STATUS='Submit' ";
            $objParse = oci_parse($objConnect, $SQL);
            oci_execute ($objParse,OCI_DEFAULT);

            $res = array();
            while($objResult = oci_fetch_array($objParse)){
                $res[] = $objResult;
            }

            if(sizeof($res)==0){
                oci_close($objConnect);

                //New connection
                $objConnect = oci_connect($dbuser1,$dbuser1,$tnsname);
                if($objConnect){
                    //check having work
                    $SQL = "select work_no from fttx_workorder_pat where REF_NO = '$id' and P_STATUS='Submit' ";
                    $objParse = oci_parse($objConnect, $SQL);
                    oci_execute ($objParse,OCI_DEFAULT);

                    $res = array();
                    while($objResult = oci_fetch_array($objParse)){
                        $res[] = $objResult;
                    }

                    if(sizeof($res)==0){
                        oci_close($objConnect);
                        
                        http_response_code(404);
                        echo json_encode(array("code"=>404,"message"=>"Ref_No not found."));

                        exit;
                    }
                    else{
                        $worn = $res[0]["WORK_NO"];

                        $SQL = "UPDATE fttx_workorder_pat SET P_STATUS='Approve' where WORK_NO = '$worn' and lot is null";
                        $objParse = oci_parse($objConnect, $SQL);
                        oci_execute ($objParse,OCI_DEFAULT);
                        
                        $SQL = "UPDATE fttx_inventory_temp SET P_STATUS='Approve' where WORK_NO = '$worn' and lot is null";
                        $objParse = oci_parse($objConnect, $SQL);
                        oci_execute ($objParse,OCI_DEFAULT);
                
                        $SQL = "insert into fttx_log(name,action,work_no,action_date) values ('ATTS', 'Approve', '$worn', SYSDATE) ";
                        $objParse = oci_parse($objConnect, $SQL);
                        oci_execute ($objParse,OCI_DEFAULT);
                    
                        oci_commit($objConnect);
                        
                        oci_close($objConnect);

                        http_response_code(200);
                        echo json_encode(array("code"=>200,"message"=>"Complete."));
                        exit;
                    }
                }
                else{
                    http_response_code(503);
                    echo json_encode(array("code"=>503,"message"=>"Database connection failed."));
                    exit;
                }
            }
            else{
                $worn = $res[0]["WORK_NO"];

                $SQL = "UPDATE fttx_workorder_pat SET P_STATUS='Approve' where WORK_NO = '$worn' and lot is null";
                $objParse = oci_parse($objConnect, $SQL);
                oci_execute ($objParse,OCI_DEFAULT);
                
                $SQL = "UPDATE fttx_inventory_temp SET P_STATUS='Approve' where WORK_NO = '$worn' and lot is null";
                $objParse = oci_parse($objConnect, $SQL);
                oci_execute ($objParse,OCI_DEFAULT);

                $SQL = "insert into fttx_log(name,action,work_no,action_date) values ('ATTS', 'Approve', '$worn', SYSDATE) ";
                $objParse = oci_parse($objConnect, $SQL);
                oci_execute ($objParse,OCI_DEFAULT);
            
                oci_commit($objConnect);
                
                oci_close($objConnect);

                http_response_code(200);
                echo json_encode(array("code"=>200,"message"=>"Complete."));
                exit;
            }
        }
        else{
            http_response_code(503);
            echo json_encode(array("message"=>"Database connection failed."));
            exit;
        }
    }
?>