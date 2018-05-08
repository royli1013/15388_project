from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
import requests
import csv

# Returns the coordinate of an address at row
# If coordinate cannot be found, return NaN
def get_coords(geolocator, row):
	if row['long'] != -1 or row['lat'] != -1:
		return (row['long'], row['lat'])
	full_addr = row['addr'] + ', ' + row['city'] + ', ' + row['state'] + ' ' + str(row['zip'])
	location = geolocator.geocode(full_addr)
	print('ok')
	if location != None:
		return (location.longitude, location.latitude)
	return (np.nan, np.nan)

# Creates new CSV file with updated coordinates using geocoders
def add_coords_to_csv(in_file, out_file):
	df = pd.read_csv(in_file)
	geolocator = Nominatim()
	long_lat = df.apply(lambda row : get_coords(geolocator, row), axis=1)
	df['long'] = [long_lat_pair[0] for long_lat_pair in long_lat]
	df['lat'] = [long_lat_pair[1] for long_lat_pair in long_lat]
	df.to_csv(out_file, index=False)
	return

# Creates full addresses from data in in_file and write them to out_file
# 1 address per line, created file can be geocoded manually
# Used https://www.doogal.co.uk/BatchGeocoding.php to generate coordinates
def create_geocode_addresses(in_file, out_file):
	df = pd.read_csv(in_file)
	out = open(out_file, 'w')
	for i, row in df.iterrows():
		if df.loc[i, 'long'] == -1:
			full_addr = row['addr'] + ', ' + row['city'] + ', ' + row['state'] + ' ' + str(row['zip']) + '\n'
			out.write(full_addr)
	out.close()
	return

# Reads from coords_file and data_file to add the coordinates to the data
# and writes everything to out_file
def add_coords(coords_file, data_file, out_file):
	df = pd.read_csv(data_file)
	coords = pd.read_csv(coords_file)
	for i, row in df.iterrows():
		if (i >= len(coords)):
			break
		address = coords.loc[i, 'Address']
		lon = coords.loc[i, 'Longitude']
		lat = coords.loc[i, 'Latitude']
		if not address.startswith(row['addr']):
			print('Row ' + str(i) + ': ' + address + '    ' + row['addr'])
		#row['long'] = lon
		#row['lat'] = lat
		df.ix[i, 'long'] = lon
		df.ix[i, 'lat'] = lat
	df.to_csv(out_file, index=False)
	return

def combine_data(data_with_coords_file, file2, out_file):
	df = pd.read_csv(data_with_coords_file)
	df2 = pd.read_csv(file2)
	df = df[df.long != -1]
	df = pd.concat([df, df2])
	df.to_csv(out_file, index=False)
	return

def is_float(n):
	try:
		float(n)
		return True
	except:
		return False

def make_address(row):
	#print(row)
	#print(row['addr'])
	#print(row['addr'] + ', ' + row['city'] + ', ' + row['state'] + ' ' + str(int(row['zip'])))
	try:
		return str(row['addr']) + ', ' + row['city'] + ', ' + row['state'] + ' ' + str(int(row['zip']))
	except:
		return ''

def get_coords(address, key):
	if len(address) == 0:
		return (np.nan, np.nan)
	url = 'http://www.mapquestapi.com/geocoding/v1/address'
	params = {'key' : key, 'location' : address}
	r = requests.get(url, params=params)
	data = r.json()
	if 'results' in data:
		result = data['results'][0]
		if 'locations' in result:
			location = result['locations'][0]
			if 'latLng' in location:
				lat_long = location['latLng']
				if 'lat' in lat_long and 'lng' in lat_long and \
				   is_float(lat_long['lat']) and is_float(lat_long['lng']):
				   return (lat_long['lat'], lat_long['lng'])
	print('NONE for ' + address)
	return (np.nan, np.nan)

def create_coords(data_file, out_file):
	key_file = open('api_key.txt', 'r')
	key = key_file.read().strip()
	key_file.close()
	out = open(out_file, 'wt', newline='')
	writer = csv.writer(out)
	writer.writerow(('long', 'lat', 'addr', 'city', 'state', 'zip', 'url', 'beds', 'baths', 'sqft', 'date', 'price'))
	df = pd.read_csv(data_file)
	rows = len(df) - 1
	for i, row in df.iterrows():
		if row['lat'] != -1:
			writer.writerow( (row['long'], row['lat'], row['addr'], row['city'], 
				              row['state'], row['zip'], row['url'], row['beds'], 
				              row['baths'], row['sqft'], row['date'], row['price']) )
		else:
			addr = row['addr'] + ', ' + row['city'] + ', ' + row['state'] + ' ' + str(int(row['zip']))
			lat, lon = get_coords(addr, key)
			writer.writerow( (lon, lat, row['addr'], row['city'], 
				              row['state'], row['zip'], row['url'], row['beds'], 
				              row['baths'], row['sqft'], row['date'], row['price']) )
		if i % 5 == 0:
			print('Completed row ' + str(i) + ' out of ' + str(rows))
	out.close()
	#coords = df.apply(lambda row: get_coords(make_address(row), key), axis=1)
	#df['lat'] = [coord[0] for coord in coords]
	#df['long'] = [coord[1] for coord in coords]
	#df.to_csv(out_file, index=False)
	


#add_coords_to_csv('../data/pittsburgh_housing_data.csv', '../data/pittsburgh_housing_data_coords.csv')
#create_geocode_addresses('../data/pittsburgh_housing_data.csv', '../data/addresses.txt')
#add_coords('../data/partial_coords_1.csv', '../data/pittsburgh_housing_data.csv', '../data/pittsburgh_housing_data_coords.csv')
#combine_data('../data/pittsburgh_housing_data_coords.csv', '../data/pittsburgh_housing_data_2.csv', '../data/full_data_with_partial_coord.csv')
#create_geocode_addresses('../data/full_data_with_partial_coord.csv', '../data/addresses.txt')
create_coords('../data/full_data_with_partial_coord.csv', '../data/full_data.csv')