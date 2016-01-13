# Police-Homicide-Demographics

These files take the Guardian's Counted database (http://www.theguardian.com/thecounted) and calculate census-block level racial demographics for the location of each incident.

Data sources:
The Guardian - The Counted: http://www.theguardian.com/thecounted

National Historical Geographic Information System (NHGIS): http://www.nhgis.org

FCC Block numbers: https://www.fcc.gov/general/census-block-conversions-api


NHGIS data will have to be requested from NHGIS directly.  Code for converting the (very large - ~4 gig) .csv from NHGIS (nhgis_csv_to_sql.py) originated from https://github.com/masnick/census-blocks-in-urban-areas/blob/master/nhgis_csv_to_sqlite.py as he'd already done the work.

Analysis and iPython notebook coming sometime soon.
