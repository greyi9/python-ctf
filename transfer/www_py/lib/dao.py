#!/usr/bin/env python

import sys
import imp
import os
import psycopg2
import base64


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
            ret_rows = []
            debug_int = 0
            for row in rows:
                debug_int = debug_int + 1
                print "[**debug**] Query Result: \n %s " % str(row)
                ret_rows.append(str(row[0]))
                print "[**debug**] row " + str(debug_int) + " value " + str(row) + "\n"
            cur.close
            DBconn.close
            return ret_rows
        else:
            print "[**debug**] DB Connection is None"
    except Exception as e:
        print "[**debug**] Oops: %s\n" % str(e)
    return []


