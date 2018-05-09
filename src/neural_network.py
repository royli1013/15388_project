import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation

class Network:

	def normalize(self, df):
		self.maxes = {}
		self.mins = {}
		df_new = pd.DataFrame()
		df_new[self.label] = df[self.label]
		for attr in self.params_to_use:# + [self.label]:
			self.maxes[attr] = df[attr].max()
			self.mins[attr] = df[attr].min()
			df_new[attr] = (df[attr] - self.mins[attr]) / (self.maxes[attr] - self.mins[attr])
		return df_new

	def __init__(self, data_file, params_to_use, label, hidden_nodes=15, percent_train=0.8):
		self.data_file = data_file
		self.params_to_use = params_to_use
		self.label = label
		self.model = Sequential()
		self.model.add(Dense(hidden_nodes, input_shape=(len(params_to_use),)))#, activation='sigmoid'))
		#self.model.add(Activation('sigmoid'))
		#self.model.add(Dense(hidden_nodes//2))
		#self.model.add(Activation('softmax'))
		self.model.add(Dense(1, activation='softmax'))#, activation='sigmoid'))
		self.model.compile(optimizer='sgd', loss='mean_absolute_percentage_error')
		df = pd.read_csv(self.data_file)
		df = self.normalize(df)
		self.X = df.as_matrix(columns=params_to_use)
		self.y = df[label].values
		print(self.X[:10])
		print(self.y[:10])
		n = int(len(df)*percent_train)
		self.X_t = self.X[:n, :]
		self.y_t = self.y[:n]
		self.X_v = self.X[n:, :]
		self.y_v = self.y[n:]

	def train(self, epochs=10, batch_size=32):
		self.model.fit(self.X_t, self.y_t, epochs=epochs, batch_size=batch_size)

	def validate(self):
		#return self.model.evaluate(self.X_v, self.y_v)
		print(self.model.predict(self.X_v)[:10])

nn = Network('../data/full_data_randomized.csv', ['long', 'lat', 'sqft', 'beds', 'baths', 'date'], 'price')
nn.train()
print(nn.validate())
