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



