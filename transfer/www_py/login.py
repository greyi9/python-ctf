#!/usr/bin/env python

VERBS_ACCEPTED = ['GET','POST']

def process_request(method, input):
    r = 'HTTP/1.1 404 Not Found\n'
    r += 'Connection: close\n\n'
    if (method in VERBS_ACCEPTED):
        if method == 'GET':
            r = do_get(input)
        elif method == 'HEAD':
            r = do_head(input)
        elif method == 'POST':
            r = do_post(input)
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

def do_get(input):
    rb = get_login_template()
    h = 'HTTP/1.1 200 OK\n' 
    h += 'Content-Type: text/html; charset=utf-8'
    h += 'Connection: close\n\n'
    return h + rb

def do_post(input):
    h = 'HTTP/1.1 200 OK\n'
    h += 'Content-Type: application/json;' 
    h += 'Connection: close\n\n'
    rb = "Unknown"
    if ('Bob' in input):
        rb = "Valid"
    return h  + rb



def get_login_template():
    return """
    <DOCTYPE html>
    <html><head><link rel="stylesheet" type="text/css" href="css/login.css"></head>
    <body><script src="js/login.js"></script>
    <form><div class="logo"><a href="#"><img src="/img/logo.png" alt="Puzzle Lock"></a></div>
    <input id="text_in" type="text" placeholder="Username" required>
    <button id="sub_btn" type="button">Next</button>
    <span id="help_prompt" class="helper"><a href="#">Having trouble logging in?</a>
    </span><div class="divider"><hr class="left"/> or <hr class="right" /></div>
    <button id="reg_btn" type="button" class="registerbtn">Register</button>
    </form><div id="debug" hidden></div></body></html>
    """
 
