#!/usr/bin/env python
import lib.auth
import base64
import json

VERBS_ACCEPTED = ['GET','POST']

def process_request(method, input, auth_data):
    r = 'HTTP/1.1 404 Not Found\n'
    r += 'Connection: close\n\n'
    if (method in VERBS_ACCEPTED):
        if method == 'GET':
            r = do_get(input, auth_data)
        elif method == 'HEAD':
            r = do_head(input)
        elif method == 'POST':
            r = do_post(input, auth_data)
        elif method == 'PUT':
            r = do_put(input)
        elif method == 'PATCH':
            r = do_patch(input)
        elif method == 'DELETE':
            r = do_delete(input)
        elif method == 'OPTIONS':
            r = do_options(input)
        else:
            r = lib_headers.get_response_by_code(500)
    else:
        r = lib_headers.get_response_by_code(405)    
    return r

def do_get(input, auth_data):
    rb = get_login_template()
    h = 'HTTP/1.1 200 OK\n' 
    h += 'Content-Type: text/html; charset=utf-8\n'
    h += lib.auth.set_cookie_headers(auth_data)
    h += 'Connection: close\n\n'
    return h + rb

def do_post(input, auth_data):
    rb = "Unknown"
    try:
        j = json.loads(input)["input"]
        session = auth_data["session"]
        if session:
            user_id = None
            user_id = auth_data["id"]
            if user_id:
                print "[*] authenticating as id=" + str(user_id)
            else:
                user_id = lib.auth.get_user_from_session(session)
                print "[*] tried to get user_id from session"
                print "[*] user_id=" + str(user_id)
        else:
            user_id = lib.auth.get_id_from_username(j)
            if user_id:
                new_cookie=["session",base64.standar_encode("username:"+j),1,0,None]
                auth_data["cookie_update"].append(new_cookie)
    except Exception as e:
        rb = "Oops: " + str(e)
    h = 'HTTP/1.1 200 OK\n'
    h += 'Content-Type: application/json;\n' 
    h += lib.auth.set_cookie_headers(auth_data)
    h += 'Connection: close\n\n'
    return h  + rb



def get_login_template():
    return """
    <DOCTYPE html>
    <html><head><link rel="stylesheet" type="text/css" href="css/default.css"></head>
    <body><script src="js/login.js"></script>
    <form><div class="logo"><a href="#"><img src="/img/logo.png" alt="logo"></a></div>
    <input id="text_in" type="text" placeholder="" required>
    <button id="btn1" type="button"></button>
    <span id="help_prompt" class="helper"></span>
    <div class="divider"><hr class="left"/> or <hr class="right" /></div>
    <button id="btn2" type="button" class="secondarybutton"></button>
    </form><div id="debug" hidden></div></body></html>
    """
 
