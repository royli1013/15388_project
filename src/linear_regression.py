import pandas as pd
import numpy as np
import scipy.linalg as la
import math
from sklearn.linear_model import LinearRegression
import csv

class LinearReg:

	def __init__(self):
		self.df_home = pd.read_csv("../data/pittsburgh_housing_data_2.csv")
		self.df_yelp = pd.read_csv("../data/yelp.csv")
		self.df = pd.merge(self.df_home, self.df_yelp, on=['addr', 'city', 'state'])

	def neighbor_amenity_index(self, restaurant_count, restaurant_rating, restaurant_price, shopping_count, shopping_rating, shopping_price):
		restaurant_index = math.ceil(float(restaurant_count) / 10) * restaurant_rating
		shopping_index = math.ceil(float(shopping_count) / 10) * shopping_rating
		return restaurant_index + shopping_index

	def preprocessing(self):
		self.df['neighbor_amenity_index'] = list(map(self.neighbor_amenity_index, self.df['restaurant_count'], self.df['restaurant_rating'], self.df['restaurant_price'],
			self.df['shopping_count'], self.df['shopping_rating'], self.df['shopping_price']))
		self.df['newness'] = self.df["date"].apply(lambda d: d - 1900) 

	def train(self):
		X = np.array([self.df['beds'], self.df['baths'], self.df['sqft'], self.df['neighbor_amenity_index'], self.df['newness']]).T
		y = self.df["price"].values.copy()
		self.model = LinearRegression(fit_intercept=True, normalize=False)
		self.model.fit(X, y)
		return self.model

	def predict(self, Xnew):
		return self.model.predict(Xnew)

	def error(self, labels, predictions):
		error = list(map(lambda l,p : abs(p - l) / l, labels, predictions))
		print(sum(error)/len(error))

	def output_prediction_and_error(self, labels, predictions):
		file_loc = "../data/linear_regression_output.csv"
		out_file = open(file_loc, 'wt', newline='')
		writer = csv.writer(out_file)
		writer.writerow(('label', 'prediction'))
		for index, label in enumerate(labels):
			writer.writerow((label, predictions[index]))


def main():
	lg = LinearReg()
	lg.preprocessing()
	model = lg.train()
	prediction = lg.predict(np.array([lg.df['beds'], lg.df['baths'], lg.df['sqft'], lg.df['neighbor_amenity_index'], lg.df['newness']]).T)
	lg.error(lg.df["price"], prediction)
	lg.output_prediction_and_error(lg.df["price"], prediction)

if __name__ == "__main__":
    main()