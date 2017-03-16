#!/usr/bin/env python
# -*- coding: utf-8 -*-

## https://pymotw.com/2/sqlite3/


import os
import sqlite3

db_filename = 'Malaga.db'
schema_filename = 'data_wrangling.sql'

delete_db = True
#FORCE DELETION of DB
if delete_db:
	if os.path.exists(db_filename):
		print ("FORCING DATABASE to be DELETED")
		os.remove(db_filename)

db_is_new = not os.path.exists(db_filename)
with sqlite3.connect(db_filename) as conn:
    if db_is_new:
        print 'Creating schema'
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema) # Create db from the supplied schema
    else:
        print 'Database exists, assume schema does, too.'
conn.close()