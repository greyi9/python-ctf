#!/usr/bin/env python

import sys
import imp
import os
import psycopg2

def test1():
    print "query('SELECT * FROM PUZZLES')" 
    print query("SELECT * FROM PUZZLES")

def test2():
    print "generate_new_session_token()"
    print generate_new_session_token()

def test3():
    print "is_session_token_in_db('abcdefg')"
    print is_session_token_in_db('abcdefg')

def test4():
    session, debug = get_new_session(1)
    print is_session_token_in_db(session)

def query(SQL,data=None):
    try:
        DBconn = psycopg2.connect("dbname='docker' user='docker' password='docker' host='localhost'")
        if DBconn is not None and SQL is not None:
            DBconn.autocommit = True
            cur = DBconn.cursor()
            if data is not None:
                cur.execute(SQL,data)
            else:
                cur.execute(SQL)
            rows = cur.fetchall()
            print "[**debug**] Query Result: \n %s \n" % str(rows)
            cur.close
            DBconn.close
            return rows
        else:
            print "[**debug**] DB Connection is None"
    except Exception as e:
        print "[**debug**] Oops: %s\n" % e
    return []

def process_cookies(cookies):
    print "lib.auth.process_cookies not yet implemented"
    print "printing cookies to be processed, then returning arbitrary auth_data"
    for cookie in cookies:
        print cookie.split('=')
    return {"id":0,"cookie_update":[["temp_cookie","12345",0,0,"/login"],["other_cookie","axaxaxa",1,0,"/admin"]]}

def set_cookie_headers(auth_data):
     h = ''
     if auth_data==None:
         h += 'Set-Cookie: other_cookie=""; HttpOnly; Path=/admin;\n'
     else:
         for cookie_update in auth_data["cookie_update"]:
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
    SQL = "SELECT COUNT(*) FROM SESSIONS WHERE TOKEN=(%s)"
    data = (token,)
    x = query(SQL,data)
    if not '0' in str(x):
        return True
    return False

def generate_new_session_token():   
    import random
    x = str(int(random.random() * 1000000000))
    if is_session_token_in_db(x):
        x = generate_new_session_token()
    return x
    

def get_new_session(user_id):
    new_session = generate_new_session_token()
    SQL = "INSERT INTO SESSIONS (TOKEN, USER_ID) VALUES (%s,%s)"
    data = (new_session, user_id)
    debug = query(SQL,data)
    return [new_session,debug]

def check_session(session_token):
    SQL = "SELECT USER_ID FROM SESSIONS WHERE TOKEN=(%s)"
    data = session_token
    debug = query(SQL,data)
    print debug

def check_username_exists(user_name):
    SQL = "SELECT COUNT(*) FROM USERS WHERE NAME=(%s)"
    data = user_name
    debug = query(SQL,data)
    return debug

def check_hash_match(user_name,hashofsecret):
    SQL = "SELECT USER_ID FROM USERS WHERE NAME=(%s) AND PW_HASH=(%s)"
    debug = query(SQL,user_name,hashofsecret)
    return debug


