#!/bin/bash

# this script removes the database so a fresh database is initiliazed when:
# 'python3 app.py' is ran

rm -f ../data.db
echo db deleted
