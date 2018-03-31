#!/usr/bin/python

import socket 
import threading
import os
import psycopg2
import www_py.login
import www_py.template
import www_py.lib.auth
import www_py.admin

L_PORT= 8000
PY_DIR = 'www_py'
ROUTE_DIR = 'www'



class Server:

 def __init__(self, port = 8000):
     self.host = ''
     self.port = port
     self.route_dir = ROUTE_DIR 

 def start(self):
     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

     try:
         self.socket.bind((self.host, self.port))
     except Exception as e:
         print "[*] Hmm: Can't get port: %d" % self.port
         try: 
             self.port += 1
             print "[*] Hmm: Trying %d..." % self.port
             self.socket.bind((self.host, self.port))
         except:
             self.shutdown()
             import sys
             sys.exit(1)

     print "[*] Listening on %s:%d ..." % (self.host,self.port)
     print "[*] Press Ctrl+C to shut down the server and exit."
     self._listen()

 def shutdown(self):
     try:
         s.socket.shutdown(socket.SHUT_RDWR)
     except Exception as e:
         print ""

 def _get_headers(self, code, fr=None, auth_data=None):
     h = 'HTTP/1.1 404 Not Found\n'
     if (code == 200):
         h = 'HTTP/1.1 200 OK\n'
         if ('img/' in fr):
             if ('.gif' in fr):
                 h += 'Content-Type: image/gif;\n'
             elif ('.png' in fr):
                 h += 'Content-Type: image/png;\n'
         elif ('css/' in fr):
             h += 'Content-Type: text/css; charset=utf-8\n'
         elif ('js/' in fr):
             h += 'Content-Type: text/plain; charset=utf-8\n'
         else:        
             h += 'Content-Type: text/html; charset=utf-8\n'
     if auth_data:
         h += www_py.lib.auth.set_cookie_headers(auth_data)
     h += 'Connection: close\n\n' 
     return h

 def _listen(self):
     while True:
         self.socket.listen(3)          
         conn,addr = self.socket.accept()
         print "[*] Connection from %s:%d" % (addr[0],addr[1])
         client_handler = threading.Thread(target=handle_rqst,args=(conn,))
         client_handler.start()


    
    
    
def handle_pyfile(file_requested, method, usrinput, auth_data):
    m = get_requested_module(file_requested)
    try:
        if "admin" in m:
            return www_py.admin.process_request(method, usrinput, auth_data)
        elif "login" in m:
            return www_py.login.process_request(method, usrinput, auth_data)
        else:
            return "<h1>Not Implemented</h1>"
    except Exception as e:
        print str(e)

def get_requested_module(file_requested):
    f = file_requested.split('/').pop().split('.')[0]
    ff = PY_DIR + "." + f
    return ff


def get_params(r, rm):
    if (rm in ['TRACE','OPTIONS','DELETE']):
        return '[*] Ignoring params due to method'
    elif (rm in ['GET','HEAD']):
        r = r.split(' ')[1].split('?',1)
    else:
        r = r.split('\r\n\r\n',1)
    if (len(r) == 2):
        return r[1]
    return ''
    
def get_requested_file_type(p):
    if (not os.path.exists(p)):
        return 'NotFound'
    if (os.path.isfile(p)):
        with open(p,'rb') as fh:
            fl = fh.readline().strip()
            if (fl in ['#!/usr/bin/env python','#!/usr/bin/python']):
                return 'Python'
        return 'Static'
    return 'Directory'

def get_options(fr):
    c = ", "
    allowed = "Allow: "
    allowed += 'OPTIONS'
    allowed += c+'GET'
    allowed += c+'HEAD'
    allowed += c+'POST'
    allowed += c+'PUT'
    allowed += c+'PATCH'
    allowed += c+'DELETE'
    allowed += c+'TRACE'
    allowed += c+'CONNECT'
    return allowed + '\r\n'

def get_headers_with_options(fr):
    h = 'HTTP/1.1 200 OK\n'
    h += get_options(fr)
    h += 'Connection: close\n\n'
    return h    

def handle_rqst(client_socket):
    data = None
    try:
        data = client_socket.recv(1024)
    except Exception as e:
        print "[*] Hmm: %s" % str(e)
        client_socket.close()
        return 
    if data is None:
        print "[*] No data recv from socket %s\n" % client_socket 
        client_socket.close()
        return
    decoded_data = None
    try:
        decoded_data = bytes.decode(data)
    except Exception as e:
        print "[*] Couldn't decode the junk they sent: \n" + data
        client_socket.close()
        return
    request_method = None
    file_requested = None
    try:
        request_method = decoded_data.split(' ')[0]
        file_requested = decoded_data.split(' ')[1].split('?')[0] 
    except Exception as e:
        print "[*] Couldn't parse the junk they sent: \n" + decoded_data
        client_socket.close()
        return
    if (None in [request_method,file_requested]):
        print "[*] Client forgot to send a verb or path in the request...\n"
        client_socket.close()
        return
    auth_data = None
    cookies = None
    try:
        cookies = [line for line in decoded_data.split('\n') if line.startswith('Cookie:')]
        if cookies:
            cookies = cookies[0].split(':',1)[1]
            if cookies:
                cookies = cookies.split(';')
    except Exception as e:
        print "[*] cookie processing exception: " + str(e) + "\n"
    if cookies:
        auth_data = www_py.lib.auth.process_cookies(cookies)
    else:
        print "[*] no cookies"
    params = get_params(decoded_data, request_method)
    print "[*] Requested File:  %s" % file_requested
    if params:
        print "[*] Parameters: %s\n" % params
    else:
        print "[*] no params"
    if (file_requested == '/'): 
        file_requested = '/index.html'
    file_requested = ROUTE_DIR + file_requested
    response_headers = s._get_headers( 200, file_requested, auth_data)    
    response =  response_headers.encode() 

    if (request_method in ['HEAD','GET','POST','OPTIONS','PUT','DELETE','PATCH']):
        try:
            file_requested_type = get_requested_file_type(file_requested)
            if (request_method in ['HEAD','GET','POST','OPTIONS']):
                if (file_requested_type == 'Python'):
                    response = handle_pyfile(file_requested, request_method, params, auth_data)
                elif (request_method == 'OPTIONS'):
                    response = get_headers_with_options(file_requested)
                elif (file_requested_type == 'Static'):
                    if (file_requested_type == 'Static'):
                        if request_method not in ['HEAD']:
                            with open(file_requested,'rb') as file_handler:
                                response += file_handler.read()
                else:
                    response = s._get_headers( 404)
            else:
                if (request_method == 'PATCH'):
                    if (file_requested_type == 'Python'):
                        response = handle_pyfile(file_requested, request_method, params, auth_data)
                    elif (file_requested_type == 'Static'):
                        with open(file_requested,'a') as f:
                            f.write(params)
                            f.close()
                        response = 'HTTP/1.1 204 OK\n'
                        response += 'Content-Location: %s\n' % file_requested 
	            else:
                        response = s._get_headers( 404)
                        response += 'PATCH Failed\n'
                elif (request_method == 'PUT'):
                    if (file_requested_type == 'NotFound'):
                        with open(file_requested,'w') as f:
                            f.write(params)
                            f.close()
                        response = 'HTTP/1.1 201 Created\n'
                        response = 'Content-Location: %s\n' % file_requested
                    elif (file_requested_type == 'Static'):
                        response = 'HTTP/1.1 204 No Content\n'
                        response = 'Content-Location: %s\n' % file_requested
                    else:
                        response = s._get_headers( 404)
                        response += 'PUT failed\n'
                elif (request_method == 'DELETE'):
                    if (file_requested_type in ['Directory','Python']):
                        response = 'HTTP/1.1 202 Accepted\n'
                    elif (file_requested_type == 'Static'):
                        os.remove(file_requested)
                        response = 'HTTP/1.1 204 No Content\n'
                        response = 'Content-Location: %s\n' % file_requested
                    else:
                        response = s._get_headers( 404)
                        response += 'DELETE failed\n' 
        except Exception as e:
            print str(e)
            response = s._get_headers( 404)
            response += '<pre>' + str(e) + '</pre>\n'
    elif (request_method == 'TRACE'):
        response = decoded_data
    elif (request_method == 'CONNECT'):
        response = 'HTTP/1.1 403 Forbidden\n'
    else:
        response = 'HTTP/1.1 405 Method Not Allowed\n'
    response = str(response)
    if len(response.split('\n')) < 3:
        print response
    client_socket.send(response)
    client_socket.close()


#############################  For better Ctrl+C exit  #########################
"""
import signal
def graceful_shutdown(sig, dummy):
    s.shutdown() 
    import sys
    sys.exit(1)
signal.signal(signal.SIGINT, graceful_shutdown)
"""
################################################################################


print ("Starting web server")
s = Server(L_PORT) 
s.start() 
