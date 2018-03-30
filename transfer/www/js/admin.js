var debug_print = 'init' 
var debugging = window.location.hash.substr(1);

function test_response(response) {
    if (debugging == 'debug'){
        debug_print.innerHTML = '<pre>' + response + '</pre>';
    }
}

function FUNC() {
    callAjaxMainForm("admin",test_response);
}

document.addEventListener('DOMContentLoaded', function() {
    debug_print = document.getElementById("debug");
    if (debugging == 'debug'){
        debug_print.innerHTML = "<h1>Debugging...</h1>";
    }
}, false);

var sub_btn;
var text_in;

document.addEventListener('DOMContentLoaded', function() {
    sub_btn = document.getElementById("sub_btn");
    text_in = document.getElementById("text_in");
    sub_btn.addEventListener("click", FUNC, false);
}, false);


function callAjax(url, callback){
    var xmlhttp;
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            updateState('done_waiting')
            callback(xmlhttp.responseText);
        }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send(text_in.value);
}

function callAjaxMainForm(url, callback){
    var xmlhttp;
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            callback(xmlhttp.responseText);
        }
    }
    xmlhttp.open("POST", "admin", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(text_in.value);
}

