import csv
import sqlite3
import sys

import pprint
import random

db_filename = 'Malaga.db'

#List of csv files
data_filename = ['nodes.csv', 'nodes_tags.csv', 'ways.csv', 'ways_tags.csv', 'ways_nodes.csv']

# Dictionary of instructions per file
#"OR IGNORE" : to avoid: sqlite3.IntegrityError: UNIQUE constraint failed: 
SQL = {}
SQL["nodes.csv"] = """INSERT OR IGNORE INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) values (:id, :lat, :lon, :user, :uid, :version, :changeset, :timestamp)"""
#nodes_tags
SQL["nodes_tags.csv"] = """INSERT OR IGNORE INTO nodes_tags (id, key, value, type) values (:id, :key, :value, :type) """

#ways
SQL["ways.csv"] = """INSERT OR IGNORE INTO ways (id, user, uid, version, changeset, timestamp) values (:id, :user, :uid, :version, :changeset, :timestamp)  """


#ways_tags
SQL["ways_tags.csv"] = """INSERT OR IGNORE INTO ways_tags (id, key, value, type) values (:id, :key, :value, :type) """


#ways_nodes
SQL["ways_nodes.csv"] = """INSERT OR IGNORE INTO ways_nodes (id, node_id, position) values (:id, :node_id, :position)  """


for x in data_filename:
	print x
	with open(x, 'rt') as csv_file:
	    csv_reader = csv.DictReader(csv_file)
	    print SQL[x]
	    
	    with sqlite3.connect(db_filename) as conn:
	    	conn.text_factory = str
	        cursor = conn.cursor()
	        cursor.executemany(SQL[x], csv_reader)
	        conn.commit()
	    conn.close()