import requests
from bs4 import BeautifulSoup
import csv

class FactFinder:
	SUCCESS = 200
	URL_TEMPLATE = "https://factfinder.census.gov/rest/communityFactsNav/nav?N=0&searchTerm=<zipcode>&spotlightId=<term>"

	def retrieve_html(self, url):
		response = requests.get(url);
		return (response.status_code, response.content)

	def get_income(self, zipcode):
		query = self.URL_TEMPLATE.replace("<zipcode>", str(zipcode))
		query = query.replace("<term>", "INCOME")
		status_code, html = self.retrieve_html(query)
		if status_code == self.SUCCESS:
			root = BeautifulSoup(html, "html.parser")
			income = root.find("div", {'class':['datapoint']}).find("div", {'class':['value']}).text
			income = int("".join(income.strip().split(",")))
		return income

	def get_poverty(self, zipcode):
		query = self.URL_TEMPLATE.replace("<zipcode>", str(zipcode))
		query = query.replace("<term>", "POVERTY")
		status_code, html = self.retrieve_html(query)
		if status_code == self.SUCCESS:
			root = BeautifulSoup(html, "html.parser")
			poverty = root.find("div", {'class':['datapoint']}).find("div", {'class':['value']}).text
			poverty = float(poverty[0:-2])
		return poverty

	def get_education(self, zipcode):
		query = self.URL_TEMPLATE.replace("<zipcode>", str(zipcode))
		query = query.replace("<term>", "EDUCATION")
		status_code, html = self.retrieve_html(query)
		if status_code == self.SUCCESS:
			root = BeautifulSoup(html, "html.parser")
			education = root.find("div", {'class':['datapoint']}).find("div", {'class':['value']}).text
			education = float(education[0:-2])
		return education

	def run(self):
		file_loc = "../data/neighbor_data.csv"
		out_file = open(file_loc, 'wt', newline='')
		writer = csv.writer(out_file)
		writer.writerow(('zipcode', 'median_household_income', 'poverty', 'education_attainment'))
		zipcodes = set()
		home_csv = "../data/full_data_randomized.csv"
		with open(home_csv) as csvfile:
			cr = csv.reader(csvfile)
			for row in cr:
				if row[0] != "long":
					zipcodes.add(row[5])
		for zipcode in zipcodes:
			try:
				income = self.get_income(zipcode)
				poverty = self.get_poverty(zipcode)
				education = self.get_education(zipcode)
				writer.writerow((zipcode, income, poverty, education))
			except AttributeError:
				print(zipcode)

def main():
	ff = FactFinder()
	ff.run()


if __name__ == "__main__":
	main()