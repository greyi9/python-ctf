
var mode = window.location.hash.substr(1);
var debug_print;
var primary_btn;
var secondary_btn;
var text_in;

function dalert(input) {
    if (mode == 'debug') {
        alert(input);
    }
}

function callAjax(url, callback){
    var xmlhttp;
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            primary_btn.style.cursor = 'pointer';
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
            primary_btn.style.cursor = 'pointer';
       	    callback(xmlhttp.responseText);
        }
    }
    primary_btn.style.cursor = 'progress';
    xmlhttp.open("POST", url, true);
    xmlhttp.setRequestHeader("Content-type", "application/json");
    var requestbody_json = '{"input":"' + encodeURIComponent(text_in.value) + '"}';
    xmlhttp.send(requestbody_json);
}

function update_stuff() {
    primary_btn.innerHTML = "Submit";
    secondary_btn.innerHTML = "Register";
    text_in.value = "";
    text_in.placeholder = "Input";
    text_in.type = "text";
}

function test_response(response) {
    if (mode == 'debug') {
        debug_print.innerHTML = '<pre>' + response + '</pre>';
    }
}

function btn1_click_handler() {
    callAjaxMainForm("login",test_response);
}

function btn2_click_handler() {
    dalert('Not Implemented... ');
}

  
document.addEventListener('DOMContentLoaded', function() {
    debug_print = document.getElementById("debug"); 
    if (mode == 'debug') {
        debug_print.innerHTML = "<h1>Debugging Started...</h1>";
    }
    primary_btn = document.getElementById("btn1");
    secondary_btn = document.getElementById("btn2");
    text_in = document.getElementById("text_in");
    primary_btn.addEventListener("click", btn1_click_handler, false);
    secondary_btn.addEventListener("click", btn2_click_handler, false);
}, false);
