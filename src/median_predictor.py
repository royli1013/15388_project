import pandas as pd
import numpy as np


# Predicts the house price as the median of the training examples
class Median:

	def __init__(self, data_file, label, percent_train=0.8):
		self.data_file = data_file
		self.label = label
		self.df = pd.read_csv(data_file)
		n = int(len(self.df) * percent_train)
		self.df_train = self.df[:n]
		self.df_val = self.df[n:]

	def train(self):
		self.median = self.df_train[self.label].median()
		print(self.median)


	def validate(self):
		y = self.df_val[self.label].values
		percent_error = abs(y - self.median) / y
		print(y[:10])
		print(percent_error[:10])
		print(sum(percent_error) / len(y))

	def predict(self, params):
		return self.median


m = Median('../data/full_data_randomized.csv', 'price')
m.train()
m.validate()