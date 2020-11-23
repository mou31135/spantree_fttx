<?php
    header("Content-Type: application/json");
    date_default_timezone_set('Asia/Bangkok');
    
    $username =  $_POST["username"];
    $pass = $_POST["password"];

    if($username !== "scgsusr"){
        $url = "http://10.50.64.171/hrauthen/service.asmx?wsdl";
        $client = new SoapClient($url);

        $params = array(
            'Username' => $username,
            'Password' => $pass
        );

        $data = $client->Authen($params);

        if($data->AuthenResult == "Please check user/password"){
            echo json_encode(array(1,"id"=>null));
        }
        else{
            $id = substr($data->AuthenResult,0,8);
            updateLog($id);
        }
    }

    exit;

    function updateLog($id){
        /* $conn = new mysqli("localhost", "root", "","fttc");
        mysqli_set_charset($conn,"utf8");
        //check login
        $sql = "select id from login_table where empId='$id'";
        $result = $conn->query($sql);

        $res = array();
        while($row = $result->fetch_assoc()){
            $res[] = $row;
        }

        if(sizeof($res)>0){
            $sql = "update login_table set lastLogin=SYSDATE() where empID='$id'";
            $result = $conn->query($sql);
        }
        else{
            $sql = "insert into login_table (empID) values ('$id')";
            $result = $conn->query($sql);
        }

        $conn->close(); */
        echo json_encode(array(0,"id"=>$id));
    }
?>