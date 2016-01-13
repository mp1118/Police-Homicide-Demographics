import pandas as pd
import sqlite3 as lite
import os
import re

if os.path.exists("census blocks/nhgis.db"):
	os.system('del census blocks/nhgis.db')

con = lite.connect("census blocks/nhgis.db")

with con:
	cur = con.cursor()
	cur.execute("CREATE TABLE race(year INT, statecode INT, countycode INT, tracta INT, blocka INT, total INT, white INT, black INT, indian INT, asian INT, islander INT, other INT)")

	i = 0
	for line in open("census blocks/nhgis0001_ds172_2010_block.csv"):
		if i > 1:
			values = line.split(',')
			insert = tuple(int(float(re.subn(r'"', '', i)[0])) for i in (values[1], values[7], values[9], values[14], values[16], values[54], values[55], values[56], values[57], values[58], values[59], values[60]))
			sql = 'insert into race values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' % insert
			cur.execute(sql)

			if i % 1000 == 0:
				print('Processing block %s...' % i)

		i += 1

if con:
	con.close()