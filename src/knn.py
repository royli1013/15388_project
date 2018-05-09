import pandas as pd
import numpy as np

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

class KNN:

	def scale_data(self):
		self.maxes = {}
		self.mins = {}
		for attr in self.params_to_use:
			self.maxes[attr] = self.df_original[attr].max()
			self.mins[attr] = self.df_original[attr].min()
			self.df[attr] = (self.df_original[attr] - self.mins[attr]) / (self.maxes[attr] - self.mins[attr])
		self.df[self.label] = self.df_original[self.label]

	def __init__(self, data_file, params_to_use, label, k=5, percent_train=0.8):
		self.data_file = data_file
		self.k = k
		self.params_to_use = params_to_use
		self.label = label
		self.df_original = pd.read_csv(data_file)
		self.df = pd.DataFrame()
		self.scale_data()
		n = int(len(self.df) * percent_train)
		self.df_train = self.df[:n]
		self.df_val = self.df[n:]

	def train(self):
		return

	def euclidean_dist(self, rv, rt):
		total = 0
		for param in self.params_to_use:
			total += abs(rv[param] - rt[param])
		#print(rt)
		return (total, rt[self.label])

	def validate(self):
		percent_error = 0
		for i, row_v in self.df_val.iterrows():
			dists = list(self.df_train.apply(lambda row_t: self.euclidean_dist(row_v, row_t), axis=1))
			dists.sort(key=lambda x: x[0])
			estimate = sum([dist[1] for dist in dists[:self.k]]) / self.k
			percent_error += abs(row_v[self.label] - estimate) / row_v[self.label]
		mean_percent_error = percent_error / len(self.df_val)
		print(mean_percent_error)

	# params is a map with keys equal to elements in params_to_use
	def predict(self, params):
		normalized = {}
		for attr,val in params.items():
			normalized[attr] = (val - self.mins[attr]) / (self.maxes[attr] - self.mins[attr])
		dists = list(self.df.apply(lambda row_t: self.euclidean_dist(normalized, row_t), axis=1))
		dists.sort(key=lambda x: x[0])
		estimate = sum([dist[1] for dist in dists[:self.k]]) / self.k
		return estimate


for i in range(1, 11):
	knn = KNN('../data/full_data_randomized.csv', ['long', 'lat', 'sqft', 'beds', 'baths', 'date'], 'price', k=i)
	knn.validate()