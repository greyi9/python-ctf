#!/usr/bin/env python

import sys
import imp
import os
import psycopg2

dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()

modules = []
for n in os.listdir(dir_path + "/" + "lib"):
    extension = n.split('.').pop()
    if (extension == "py" and 'init' not in n):
        modules.append(imp.load_source(n, dir_path + "/" + "lib" + "/" + n))


def do_auth_tests():
    for m in modules:
         if 'auth' in str(m):      
             print "[**TEST1**] \n"
             m.test1()
             print "[**TEST2**] \n"
             m.test2()
             print "[**TEST3**] \n"
             m.test3()
             print "[**TEST4**] \n"
             m.test4()
   
do_auth_tests()




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
    rb = get_admin_template()
    h = 'HTTP/1.1 200 OK\n' 
    h += 'Content-Type: text/html; charset=utf-8'
    h += 'Connection: close\n\n'
    return h + rb

def do_post(input):
    h = 'HTTP/1.1 200 OK\n'
    h += 'Content-Type: text/html; charset=utf-8' 
    h += 'Connection: close\n\n'
    rb = "Setup Succeeded\n"
     
    q = "%s" % input
    
    DBconn = None
    try:
        DBconn = psycopg2.connect("dbname='docker' \
                                   user='docker' \
                                   host='localhost' \
                                   password='docker'")
        if DBconn is not None:
            DBconn.autocommit = True
            cur = DBconn.cursor()
            cur.execute(q)
            rows = cur.fetchall()  
            rb += "\nShow me the results:\n"
            for row in rows:
                rb += "   " + str(row[0]) + "<br>\n"
                rb += str(row) + "<br>\n"
            cur.close()
            DBconn.close()
        else:
            rb = "DB Connection is None"
    except Exception as e:
        rb = "Query Failed\n"
        rb += "Oops: %s\n" % e
    return h + rb

def get_admin_template():
    return """
    <html>
    <head>
    <link rel="stylesheet" type="text/css" href="css/admin.css">
    </head>

    <body>
    <script src="js/admin.js"></script>
    <form>
    <div class="logo">
    <a href="#"><img src="/img/logo.png" alt="Puzzle Lock"></a>
    </div>
    <input id="text_in" type="text" placeholder="Authorized use only!" required>
    <button id="sub_btn" type="button">Go</button>
    <span id="help_prompt" class="helper" hidden>
    </span>
    </form>
    <div id="debug" hidden></div>
    </body>
    </html>
    """




