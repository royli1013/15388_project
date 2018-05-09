import pandas as pd
import numpy as np
import scipy.linalg as la
import math
from sklearn.linear_model import LinearRegression
import csv

class LinearReg:
	def get_data(self):
		df_home = pd.read_csv("../data/pittsburgh_housing_data_2.csv")
		df_yelp = pd.read_csv("../data/yelp.csv")
		df_neighbor = pd.read_csv("../data/neighbor_data.csv")
		df = pd.merge(df_home, df_yelp, on=['addr', 'city', 'state'])
		df = pd.merge(df, df_neighbor, on=['zip'])
		df.dropna(axis=0, how='any')
		return df

	def neighbor_amenity_index(self, restaurant_count, restaurant_rating, restaurant_price, shopping_count, shopping_rating, shopping_price):
		restaurant_index = math.ceil(float(restaurant_count) / 10) * restaurant_rating
		shopping_index = math.ceil(float(shopping_count) / 10) * shopping_rating
		return restaurant_index + shopping_index

	def sqft_preprocess(self, a):
		# if a <=2000:
		# 	return a
		# else:
		# 	return a + math.log(a - 2000)
		return a

	def preprocessing1(self, df):
		df['neighbor_amenity_index'] = list(map(self.neighbor_amenity_index, df['restaurant_count'], df['restaurant_rating'], df['restaurant_price'],
			df['shopping_count'], df['shopping_rating'], df['shopping_price']))
		df['newness'] = df["date"].apply(lambda d: (d - 1850)**2)
		df['sqft'] = df['sqft'].apply(lambda a : self.sqft_preprocess(a))
		X = np.array([df['sqft'], df['neighbor_amenity_index'], df['newness'], df['poverty']]).T
		y = df["price"].values.copy()
		return (X, y)

	def preprocessing2(self, df):
		df['neighbor_amenity_index'] = list(map(self.neighbor_amenity_index, df['restaurant_count'], df['restaurant_rating'], df['restaurant_price'],
			df['shopping_count'], df['shopping_rating'], df['shopping_price']))
		df['newness'] = df["date"].apply(lambda d: (d - 1850)**2)
		df["price_per_sqft"] = list(map(lambda x,y : float(x)/y, df['price'], df['sqft']))
		X = np.array([df['neighbor_amenity_index'], df['newness'], 
			df['median_household_income'], df['education_attainment']]).T
		y = df["price_per_sqft"].values.copy()
		return (X, y)

	def getPricePerSqftData(self, df):
		df["price_per_sqft"] = list(map(lambda x,y : float(x)/y, df['price'], df['sqft']))
		X = np.array([df['price_per_sqft']]).T
		y = df["price"].values.copy()
		return (X, y)

	def split_data(self, n, k):
		n_k = n // k
		permutation = np.random.permutation(n)
		blocks = []
		index = 0
		for i in range(k):
			start = index
			end = start + n_k if i < (k - 1) else n
			blocks.append(permutation[start:end])
			index = end
		return blocks

	def train(self, X, y):
		model = LinearRegression(fit_intercept=True, normalize=False)
		model.fit(X, y)
		return model

	def k_folds_validation(self, X, y, blocks):
		k = len(blocks)
		total_error = 0.0
		for validation_indexes in blocks:
			X_v = X[validation_indexes]
			y_v = y[validation_indexes]
			training_indexes = []
			for block in blocks:
				if not np.array_equal(block, validation_indexes):
					training_indexes = np.append(training_indexes, [block])
					training_indexes = [int(i) for i in training_indexes]
			X_t = X[training_indexes]
			y_t = y[training_indexes]
			model = self.train(X_t, y_t)
			y_v_p = model.predict(X_v)
			error = self.error(y_v, y_v_p)
			total_error += error
		return total_error / k

	def predict(self, model, Xnew):
		return model.predict(Xnew)

	def error(self, labels, predictions):
		error = list(map(lambda l,p : abs(p - l) / l, labels, predictions))
		return sum(error)/len(error)
		# for index, err in enumerate(error):
		# 	if err >= 1:
		# 		print(str(index) + ":" + str(labels[index]) + "," + str(predictions[index]))
		# 		row = self.df.iloc[index]
		# 		print("sqft: " + str(row['sqft']) + ", amenity: " + str(row.neighbor_amenity_index) + \
		# 			", newness: " + str(row.newness) + ", poverty: " + str(row.poverty))

	def output_prediction_and_error(self, labels, predictions):
		file_loc = "../data/linear_regression_output.csv"
		out_file = open(file_loc, 'wt', newline='')
		writer = csv.writer(out_file)
		writer.writerow(('label', 'prediction'))
		for index, label in enumerate(labels):
			writer.writerow((label, predictions[index]))

	def regression_against_price(self):
		df = self.get_data()
		X, y = self.preprocessing1(df)
		n,params = X.shape
		blocks = self.split_data(n, 10)
		error = self.k_folds_validation(X, y, blocks)
		print(error)
		model = self.train(X, y)

	def regression_against_price_per_sqft(self):
		df = self.get_data()
		X, y = self.preprocessing2(df)
		n,params = X.shape
		blocks = self.split_data(n, 10)
		error = self.k_folds_validation(X, y, blocks)
		print(error)
		model1 = self.train(X, y)

		#regress between price_per_sqft and sqft
		price_per_sqfts, price = self.getPricePerSqftData(df)
		print(price_per_sqfts.shape)
		model2 = self.train(price_per_sqfts, price)

		y_layer1 = model1.predict(X)
		y_layer1 = y_layer1.reshape((len(y_layer1), 1))
		y_pred = model2.predict(y_layer1)
		print(y_pred)
		print(price)
		error = self.error(price, y_pred)
		print(error)


def main():
	lg = LinearReg()
	lg.regression_against_price()
	lg.regression_against_price_per_sqft()

if __name__ == "__main__":
    main()