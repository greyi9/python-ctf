

//-----------------
var debug_print = 'init' 
var debugging = window.location.hash.substr(1);
function test_response(response) {
    if (debugging == 'debug') {
        debug_print.innerHTML = '<pre>' + response + '</pre>';
    }
}

function FUNC() {
    callAjaxMainForm("login",test_response);
}

function dalert(input) {
    if (debugging == 'debug') {
        alert(input);
    }
}

var x = 0;
function FUNC2() {
    x += 1
    dalert('Fired ' + x + ' times');
}

document.addEventListener('DOMContentLoaded', function() {
    dalert("login.js has loaded");
    debug_print = document.getElementById("debug");
    if (debugging == 'debug') {
        debug_print.innerHTML = "<h1>Debugging Started...</h1>";
    }
}, false);
//-----------------   

var STATE = 'loaded';
var USERNAME = 'Username';
var PASSWORD = 'Password';
var SUBMIT_USERNAME = 'Next';
var SUBMIT_PASSWORD = 'Login';
var sub_btn;
var reg_btn;
var text_in;

document.addEventListener('DOMContentLoaded', function() {
    sub_btn = document.getElementById("sub_btn");
    reg_btn = document.getElementById("reg_btn");
    text_in = document.getElementById("text_in");
    sub_btn.addEventListener("click", FUNC, false);
    reg_btn.addEventListener("click", FUNC2, false);
}, false);


function callAjax(url, callback){
    var xmlhttp;
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            text_in.value = "";
            document.body.style.cursor = 'default';
            callback(xmlhttp.responseText);
        }
}
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function callAjaxMainForm(url, callback){
    var xmlhttp;
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            callback(xmlhttp.responseText);
        }
    }
    if (STATE == 'loaded') {
        sub_btn.innerHTML = "Next";
        reg_btn.innerHTML = "Register";
        text_in.value = "";
        text_in.placeholder = "Username";
        text_in.type = "text";
    } else if (STATE == 'uname_submitted') {
        sub_btn.innerHTML = "Authenticating...";
    }
    document.body.style.cursor = 'progress';
    xmlhttp.open("POST", "login", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var requestbody_json = '{"rb":[{"state":"' + STATE + '"},{"input":"' + text_in.value + '"}]}';
    xmlhttp.send(requestbody_json);
}

