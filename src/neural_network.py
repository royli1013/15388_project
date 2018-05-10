import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation

class Network:

	def normalize(self, df):
		self.maxes = {}
		self.mins = {}
		df_new = pd.DataFrame()
		#df_new[self.label] = df[self.label]
		for attr in self.params_to_use + [self.label]:
			self.maxes[attr] = df[attr].max()
			self.mins[attr] = df[attr].min()
			df_new[attr] = (df[attr] - self.mins[attr]) / (self.maxes[attr] - self.mins[attr])
		return df_new

	def __init__(self, data_file, params_to_use, label, hidden_nodes=200, percent_train=0.8):
		self.data_file = data_file
		self.params_to_use = params_to_use
		self.label = label
		self.model = Sequential()
		self.layer1 = Dense(hidden_nodes, input_shape=(len(params_to_use),))
		self.model.add(self.layer1)
		self.model.add(Dense(64))
		self.model.add(Dense(32))
		self.layer2 = Dense(1)
		self.model.add(self.layer2)
		self.model.compile(optimizer='sgd', loss='mean_absolute_error')
		df = pd.read_csv(self.data_file)
		df = self.normalize(df)
		self.X = df.as_matrix(columns=params_to_use)
		self.y = df[label].values
		n = int(len(df)*percent_train)
		self.X_t = self.X[:n, :]
		self.y_t = self.y[:n]
		self.X_v = self.X[n:, :]
		self.y_v = self.y[n:]

	def train(self, epochs=200, batch_size=32, debug=False):
		if debug:
			self.model.fit(self.X_t, self.y_t, epochs=epochs, batch_size=batch_size)
		else:
			self.model.fit(self.X_t, self.y_t, epochs=epochs, batch_size=batch_size, verbose=0)

	def to_label(self, data):
		return data * (self.maxes[self.label] - self.mins[self.label]) + self.mins[self.label]

	def validate(self):
		y = self.to_label(self.model.predict(self.X_v)[:, 0])
		y_v = self.to_label(self.y_v)
		percent_error = abs((y - y_v) / y_v)
		return sum(percent_error) / len(percent_error)

	def predict(self, params):
		return self.to_label(self.model.predict(params))

def main():
	nn = Network('../data/full_data_randomized.csv', ['long', 'lat', 'sqft', 'beds', 'baths', 'date'], 'price')
	nn.train()
	print(nn.validate())

if __name__ == "__main__":
    main()