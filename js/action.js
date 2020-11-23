/***************************************
                login page
****************************************/
function login(){
    var username = $("#username_input").val();
    var password = $("#password_input").val();
    $.ajax({
        type: "post",
        data: {
            "username": username,
            "password": password,
        },
        url: "services/login.php",
        success: function (data) {
            if(data[0]==0){
                /* localStorage.clear();
                localStorage.setItem("token",data.id);

                var url = window.location.href;
                var param = getParameterFormURL(url);
            
                callPage(param["page"]); */

                location.replace("index.html");
            }
            else{
                alert("Plase check Username or Password");
            }
        },//end success
    });//end ajax
}







/***************************************
            Optional function
****************************************/

function getParameterFormURL(url){
    Url = {
        get get(){
            var vars= {};
            if(url.length!==0)
                url.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value){
                    key=decodeURIComponent(key);
                    if(typeof vars[key]==="undefined") {vars[key]= decodeURIComponent(value);}
                    else {vars[key]= [].concat(vars[key], decodeURIComponent(value));}
                });
            return vars;
        }
    };
    return Url.get;
}