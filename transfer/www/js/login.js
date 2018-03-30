

//-----------------
var debug_print = 'init' 
var debugging = window.location.hash.substr(1);
function test_response(response) {
    if (debugging == 'debug') {
        debug_print.innerHTML = '<pre>' + response + '</pre>';
    }
    updateStateWithResponse(response);
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
            updateState('done_waiting')
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
        updateState('uname_submitted');
    } else if (STATE == 'uname_submitted') {
        updateState('passwd_submitted'); 
    }
    updateState('waiting');
    xmlhttp.open("POST", "login", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var requestbody_json = '{"rb":[{"state":"' + STATE + '"},{"input":"' + text_in.value + '"}]}';
    xmlhttp.send(requestbody_json);
}

function updateState(new_state) {
    var debug = STATE;
    if (new_state == 'loaded') {
        sub_btn.innerHTML = "Next";
        reg_btn.innerHTML = "Register";
        text_in.value = "";
        text_in.placeholder = "Username";
        text_in.type = "text";
    } else if (new_state == 'uname_submitted') {
        STATE = 'uname_submitted';
        sub_btn.innerHTML = "Login";
        text_in.placeholder = "Password";
        text_in.type = "password";
    } else if (new_state == 'passwd_submitted') {
        sub_btn.innerHTML = "Authenticating...";
    } else if (new_state == 'waiting') {
        var old_state = STATE;
        document.body.style.cursor = 'progress';
        new_state = new_state + ":" + old_state;
    } else if (new_state == 'done_waiting') {
        text_in.value = "";
        document.body.style.cursor = 'default';
        new_state = STATE.split(':').pop()
    } else if (new_state == 'uname_failed') {
        dalert("Oops. Unknown Username!");
    } else if (new_state == 'passwd_failed') {
        dalert("Oops. Wrong Password! ");
    } else if (new_state == 'logged_in') {
        dalert("Congrats, you've authenticated! Not implemented yet though.");
    } else if (new_state == 'unexpected') {
        dalert("Oops. Maybe try again in a new browser? ");
    }
    STATE = new_state;
    debug += " ---> " 
    debug += STATE
    dalert(debug);
    if (['uname_failed','passwd_failed','logged_in'].indexOf(STATE) !== -1) {
        updateState('loaded');
    }
}


function updateStateWithResponse(response) {
    updateState('done_waiting');
    if (response.indexOf('Valid') !== -1 ) {
        if (STATE == 'passwd_submitted') {
            updateState('logged_in');
        } 
    } else if (response.indexOf('Unknown') !== -1 ) {
        if (STATE == 'passwd_submitted') {
            updateState('passwd_failed');
        } else {
            updateState('uname_failed');
        }
    }
}
