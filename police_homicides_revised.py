from bs4 import BeautifulSoup
from pygeocoder import Geocoder
import pandas as pd
import requests
import sqlite3 as lite
import urllib.request as urllib
import zipfile as zf

#download the Counted database from the guardian
counted_data = urllib.urlretrieve("https://interactive.guim.co.uk/2015/the-counted/thecounted-data.zip", "counted/thecounted-data.zip")
zip_ref = zf.ZipFile("counted/thecounted-data.zip", 'r')
zip_ref.extractall(path = 'counted')
zip_ref.close()

print("Counted database successfully unzipped.")

counted = pd.read_csv('counted/the-counted.csv') #Guardian's The Counted Database

counted['fulladdress'] = counted['streetaddress'] + ', ' + counted['city'] + ' ' + counted['state']

#Grab geolocation from pygeocoder.  This needs checked for addresses with missing street numbers and for addresses as intersections.
apikey = 'get your own'

def geo(address):
	geocoder = Geocoder(api_key = apikey)
	try:
		location = Geocoder.geocode(address)
		coords = [location.latitude,location.longitude]
		if location.valid_address:
			print(coords)
			return coords, 'success'
		else:
			#print('1st pass: Invalid address: ' + address)
			return coords,'invalid address'
	except:
		#print('2nd pass: This one didn\'t work: ' + address)
		return [0.0,0.0], 'failure'		

#counted = counted[0:50] #Take a sample of the data so this crappy Ghanaian internet can handle it.

output = counted['fulladdress'].apply(geo)

counted['coordinates'] = [x[0] for x in output]
counted['result'] = [x[1] for x in output]

counted.to_csv('CSVs/police_homicide_gps.csv')

def fccblockfetch(coords): #Grab block numbers from the FCC
	if coords != [0.0,0.0]:
		url = 'http://data.fcc.gov/api/block/2010/find'
		params = {'latitude': str(coords[0]), 'longitude': str(coords[1]), 'censusYear': 2010, 'showall': 'false'}
		response = requests.get(url, params = params) #Get XML
		parsed = BeautifulSoup(response.content) #Parse XML
		try:
			blockFIPS = parsed.block['fips']
		except:
			blockFIPS = '000000000000000'
		print(blockFIPS)
		return blockFIPS
	else:
		return '000000000000000'

counted['blockFIPS'] = counted['coordinates'].apply(fccblockfetch)

counted.to_csv('CSVs/police_homicide_gps_blockFIPS.csv')

#Grab NHGIS data from SQL and merge into dataframe
print('Querying database...')

con = lite.connect('census blocks/nhgis.db')

FIPSdata = counted['blockFIPS'].unique()

columns = ['total', 'white', 'black', 'indian', 'asian', 'islander', 'other']

FIPSappend = pd.DataFrame(columns = columns)

for FIPS in FIPSdata: #Grab race data from SQL
	if FIPS:
		racedata = pd.read_sql_query('SELECT total, white, black, indian, asian, islander, other FROM race WHERE statecode = ' + FIPS[0:2] + ' AND countycode = ' + FIPS[2:5] + ' AND tracta = ' + FIPS[5:11] + ' AND blocka = ' + FIPS[11:15], con, coerce_float = False)
		racedata['blockFIPS'] = FIPS
		print(racedata)
		FIPSappend = FIPSappend.append(racedata)
	else:
		print('error')

con.close()		

counted = pd.merge(counted, FIPSappend, how = 'outer', left_on = 'blockFIPS', right_on = 'blockFIPS') #merge race data back in

counted.to_csv('CSVs/police_homicide_racedata.csv')