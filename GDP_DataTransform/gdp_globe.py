import json
import xlrd
import fetch_error
import geocode
from geo_coord import GeoCoord

GDP_DATA_FILE_PATH = 'world_GDP_2004_2013.xlsx'
MAX_VALUES = 1000

"""
Returns a dict as 
{'country1' : location_json, 'country2' : locaiton_json}
"""
def fetch_coutries_coords(file_path, sheet_name):
	gdp_data = xlrd.open_workbook(file_path)
	table = gdp_data.sheet_by_name(sheet_name)
	nrows = table.nrows
	
	countries_coords = {}
	for rownum in range(1, nrows):
		country_name = table.cell(rownum, 2).value
		print('Quering %s coord...' % country_name)
		coord = geocode.address_to_coords(country_name)
		countries_coords[country_name] = coord
		print 'done.'
	
	return countries_coords

def fetch_years_countries_gdp(file_path, sheet_name):
	gdp_data = xlrd.open_workbook(file_path)
	table = gdp_data.sheet_by_name(sheet_name)
	nrows = table.nrows
	
	years_countries_gdp = []
	for year_num in range(0, 10):
		countries_gdp = []
		for rownum in range(1, nrows):
			country_name = table.cell(rownum, 2).value
			gdp = table.cell(rownum, year_num + 4).value
			countries_gdp.append({"country" : country_name, "GDP" : gdp if (gdp != '..') else 0})
		years_countries_gdp.append(countries_gdp)
		
	return years_countries_gdp

"""Adds geographic coordinates with Google's geocoding API

return format example:

[{u'num_users': u'22582', 'coords': <geo_coord.GeoCoord instance>},
{u'num_users': u'16838', 'coords': <geo_coord.GeoCoord instance>}]

"""	
def add_coords(data, country_coord_dict):
	data = filter(lambda x: type(x) is dict, data)
	new = []

	for x in xrange(len(data)): 
		print('processing %s out of %s' % (x, len(data)))
		coords = country_coord_dict[data[x]['country']]

		if coords is not None:
			coords = GeoCoord(coords['lat'], coords['lng'])
			data[x]['coords'] = coords
			del data[x]['country']
			new.append(data[x])

	return new
	
def combine_duplicates(data):
	new = {}

	for el in data:
		el['coords'] = el['coords'].round(2)
		if el['coords'] in new:
			new[el['coords']] += int(el['GDP'])
		else:
			new[el['coords']] = int(el['GDP'])

	return new
	
def normalize_gdp(data):
	max_pop = max(data.values())
	    
	for x in data.keys():
		data[x] = float(data[x]) / max_pop

	return data

"""Translates data to the WebGL format

return format:

[label, [latitude, longitude, magnitude, latitude, longitude, magnitude]]

"""
def to_webgl_globe_format(data, label):
	data = map(lambda x: [x.lat, x.lng, data[x]], data.keys())
	data = [item for sublist in data for item in sublist]
	data = map(lambda x: float(x), data)
	return [label, data]

def main():
	years_countries_gdp_org = fetch_years_countries_gdp(GDP_DATA_FILE_PATH, u'Data')
	country_coord_dict = fetch_coutries_coords(GDP_DATA_FILE_PATH, u'Data')
	#countries_coords = []
	#for country_index in range(0, 2):
	#	countries_coords.append(geocode.address_to_coords(countries[country_index]))
	#print countries[0]
	years_countries_gdp = []
	for year in range(0, len(years_countries_gdp_org)):
		data = normalize_gdp(
			combine_duplicates(
			add_coords(
			years_countries_gdp_org[year], country_coord_dict)))

		data_globe_format = to_webgl_globe_format(data, '%d' % (year + 2004))
		years_countries_gdp.append(data_globe_format)

	with open('years_countries_gdp.json', 'w') as f:
		f.write(json.dumps(years_countries_gdp))
	

if __name__=="__main__":
	main()