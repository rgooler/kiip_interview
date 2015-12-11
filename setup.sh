#!/bin/bash
virtualenv .
source bin/activate
pip install -r requirements.txt
if [ ! -f services.db ]; then
    sqlite3 services.db < schema.sql
fi
