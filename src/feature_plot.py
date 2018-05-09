import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

class FeaturePlotting:
	def __init__(self):
		self.df_home = pd.read_csv("../data/pittsburgh_housing_data_2.csv")
		self.df_yelp = pd.read_csv("../data/yelp.csv")
		self.df_neighbor = pd.read_csv("../data/neighbor_data.csv")
		self.df = pd.merge(self.df_home, self.df_yelp, on=['addr', 'city', 'state'])
		self.df = pd.merge(self.df, self.df_neighbor, on=['zip'])
		self.df.dropna(axis=0, how='any')

	def sqft_preprocess(self, a):
		if a <=1500:
			return a
		else:
			return a + math.log(a - 1500)

	def neighbor_amenity_index(self, restaurant_count, restaurant_rating, restaurant_price, shopping_count, shopping_rating, shopping_price):
		restaurant_index = math.ceil(float(restaurant_count) / 5) * restaurant_rating
		shopping_index = math.ceil(float(shopping_count) / 5) * shopping_rating
		return shopping_index + restaurant_index

	def generate_feature(self):
		self.df['neighbor_amenity_index'] = list(map(self.neighbor_amenity_index, self.df['restaurant_count'], self.df['restaurant_rating'], self.df['restaurant_price'],
			self.df['shopping_count'], self.df['shopping_rating'], self.df['shopping_price']))
		self.df["price_per_sqft"] = list(map(lambda x,y : float(x)/y, self.df['price'], self.df['sqft']))
		self.df['newness'] = self.df["date"].apply(lambda d: (d - 1850) ** 2)
		self.df['restaurant_count_sqrt'] = self.df["restaurant_count"].apply(lambda d: math.sqrt(d))
		self.df['processed_sqft'] = self.df['sqft'].apply(lambda a : self.sqft_preprocess(a))


	def plot_build(self):
		plt.scatter(self.df["date"],self.df["price"],s=10)
		plt.show()

	def plot_amenity(self):
		x_name = "median_household_income"
		y_name = "price"
		x = self.df[x_name]
		y = self.df[y_name]
		coef = np.corrcoef(x, y)[0,1]
		print(coef)
		fit = np.polyfit(x, y, deg=1)
		plt.title(y_name + '_against_' + x_name)
		plt.plot(x, fit[0] * x + fit[1], color='red')
		plt.ylabel(y_name)
		plt.xlabel(x_name)
		plt.scatter(x, y, s=10)
		plt.text(0.5, 0.5, "coef: " + str(coef), fontsize=15)
		#plt.show()
		plt.savefig("../resource/plots/" + y_name + '_against_' + x_name + str(coef) + '.png')

def main():
	fp = FeaturePlotting()
	fp.generate_feature()
	fp.plot_amenity()

if __name__ == "__main__":
    main()