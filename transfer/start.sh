#!/bin/bash
/etc/init.d/postgresql start
psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';"
createdb -O docker docker
psql -U postgres -d docker -a -f init.sql
./srv.py
 
