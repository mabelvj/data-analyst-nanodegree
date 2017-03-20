#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys

db_filename = 'Malaga2.db'


mapping = { u"Malaga": u"Málaga",
			u"MALAGA": u"Málaga",
			u"MÁLAGA": u"Málaga",
			u"Mälaga": u"Málaga",
			u"Rincon de la Victoria": u"Rincón de la Victoria"}

with sqlite3.connect(db_filename) as conn:
	cursor = conn.cursor()
	query_nodes = """UPDATE nodes_tags SET value = :value WHERE value = :value2 and key LIKE '%city'"""
	query_ways = """UPDATE ways_tags SET value = :value WHERE value = :value2 and key LIKE '%city'"""
	
	for key, value in mapping.items():
	    #iterate over the dict and update each value in each table
	    print (value, key)
	    cursor.execute(query_nodes, {'value':value, 'value2': key})
	    cursor.execute(query_ways, {'value':value, 'value2': key})
	    conn.commit()
conn.close()