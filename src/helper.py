from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np

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

#add_coords_to_csv('../data/pittsburgh_housing_data.csv', '../data/pittsburgh_housing_data_coords.csv')
#create_geocode_addresses('../data/pittsburgh_housing_data.csv', '../data/addresses.txt')
add_coords('../data/partial_coords_1.csv', '../data/pittsburgh_housing_data.csv', '../data/pittsburgh_housing_data_coords.csv')