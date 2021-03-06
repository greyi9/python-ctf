#!/usr/bin/env python

import sys
import imp
import os
import psycopg2
import base64
import dao


def query(SQL,data=None):
    try:
        return dao.query(SQL, data)
    except Exception as e:
        print "[**debug**] Oops: %s\n" % str(e)
    return []

def authenticate(user_name,hashofsecret):
    print 1
    session_token = None
    user_id = None
    user_id = check_hash_match(user_name,hashofsecret)
    if user_id:
        session_token = get_new_session(user_id)
    return user_id, session_token

def process_cookies(cookies):
    print 2
    userid = None
    session_token = ""
    cookie_update = []
    #[["temp_cookie","12345",0,0,"/login"],["other_cookie","axaxaxa",1,0,"/admin"]]
    for cookie in cookies:
        if cookie.split('=')[0] == 'session':
            session_token = cookie.split('=')[1]
            if session_token == "":
                print "[*] no session"
            else:
                auth_profile = get_session(session_token)
                if auth_profile:
                    print "got an auth profile!"
                    print str(auth_profile)
                    print "now need to parse this into the return value..."
                else:
                    print "[*] clearing session token on client"
                    new_cookie = ["session","",1,0,""]
                    cookie_update.append(new_cookie)
    return {"id":userid,"session":session_token,"cookie_update":cookie_update}

def get_user_from_session(token):
    print 3
    ret_user = None
    try:
        user_name = base64.standard_decode(token)
        if user_name.startswith('username:'):
            user_name = user_name.split(':',1)
            ret_user = get_id_from_username(user_name)
    except Exception as e:
        print str(e)
    print "ret_user..."
    print str(ret_user)
    return ret_user



def set_cookie_headers(auth_data):
     print 4
     h = ''
     if auth_data:
         print 4.01
         if auth_data == None:
             print "ah, that's bad"
         if auth_data["cooke_update"]:
             print 4.02
             for cookie_update in auth_data["cookie_update"]:
                 print "[*] cookie update: " + str(cookie_update)
                 h += 'Set-Cookie: ' + cookie_update[0] + "=" + cookie_update[1] + "; "
                 if cookie_update[2]:
                     h += 'HttpOnly; '
                 if cookie_update[3]:
                     h += 'Secure; '
                 if cookie_update[4]:
                     h += 'Path=' + cookie_update[4] + ";"
                 h += '\n'
     return h

def is_session_token_in_db(token):
    print 5
    SQL = "SELECT COUNT(*) FROM SESSIONS WHERE TOKEN=(%s)"
    data = (token,)
    x = query(SQL,data)
    if not '0' in str(x):
        return True
    return False

def generate_new_session_token():   
    print 6
    import random
    x = str(int(random.random() * 1000000000))
    if is_session_token_in_db(x):
        x = generate_new_session_token()
    return x
    
def get_session(token):
    print 7
    SQL = "SELECT * FROM SESSIONS WHERE TOKEN=(%s)"
    data = (token,)
    x = query(SQL,data)
    print "session check..."
    print str(x)
    return x

def get_new_session(user_id):
    print 8
    new_session = generate_new_session_token()
    SQL = "INSERT INTO SESSIONS (TOKEN, USER_ID) VALUES (%s,%s)"
    data = (new_session, user_id)
    debug = query(SQL,data)
    return new_session,debug

def check_session(session_token):
    print 9
    SQL = "SELECT USER_ID FROM SESSIONS WHERE TOKEN=(%s)"
    data = session_token
    debug = query(SQL,data)
    print debug

def get_id_from_username(user_name):
    print 10
    SQL = "SELECT ID FROM USERS WHERE NAME=(%s)"
    data = str(user_name)
    print "[*] debugging... user_name: " + data
    print "[*] debugging... SQL: " + SQL
    debug = query(SQL,data)
    print "[*] debugging... query result: " + str(debug)
    return debug

def check_username_exists(user_name):
    print 11
    SQL = "SELECT COUNT(*) FROM USERS WHERE NAME=(%s)"
    data = user_name
    debug = query(SQL,data)
    return debug

def check_hash_match(user_name,hashofsecret):
    print 12
    SQL = "SELECT USER_ID FROM USERS WHERE NAME=(%s) AND PW_HASH=(%s)"
    debug = query(SQL,user_name,hashofsecret)
    return debug

