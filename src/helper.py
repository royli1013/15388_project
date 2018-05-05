from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np

def get_coords(geolocator, row):
	if row['long'] != -1 or row['lat'] != -1:
		return (row['long'], row['lat'])
	full_addr = row['addr'] + ', ' + row['city'] + ', ' + row['state'] + ' ' + str(row['zip'])
	location = geolocator.geocode(full_addr)
	print('ok')
	if location != None:
		return (location.longitude, location.latitude)
	return (np.nan, np.nan)

def add_coords_to_csv(in_file, out_file):
	df = pd.read_csv(in_file)
	geolocator = Nominatim()
	long_lat = df.apply(lambda row : get_coords(geolocator, row), axis=1)
	df['long'] = [long_lat_pair[0] for long_lat_pair in long_lat]
	df['lat'] = [long_lat_pair[1] for long_lat_pair in long_lat]
	df.to_csv(out_file)



add_coords_to_csv('../data/pittsburgh_housing_data.csv', '../data/pittsburgh_housing_data_coords.csv')