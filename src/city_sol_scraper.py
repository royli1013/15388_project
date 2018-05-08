import requests
from bs4 import BeautifulSoup
import csv
from helper_alvin import Helper2

class CitySOLScrapper:
	SUCCESS = 200
	base_url = "https://www.zillow.com/<city>-<state>/home-values/"
	base_url_2 = "https://www.zillow.com/<state>/home-values/"
	kiplinger_url = "https://www.kiplinger.com/tool/real-estate/T010-S003-home-prices-in-100-top-u-s-metro-areas/index.php"
	city_csv = "../data/cities.csv"

	def retrieve_html(self, url):
		response = requests.get(url)
		return (response.status_code, response.content)

	def __init__(self, file_loc):
		self.out_file = open(file_loc, 'wt', newline='')
		self.writer = csv.writer(self.out_file)
		self.writer.writerow(('city', 'media_home_price'))
		self.state_to_abbre = Helper2().state_abbre_map()

	def run_zillow(self):
		# Not working, anti-scraping in place
		cities = []
		states = []
		with open(self.city_csv) as csvfile:
			cr = csv.reader(csvfile)
			for row in cr:
				if row[0] != "city":
					cities.append(row[0].lower())
					states.append(row[1].lower())
		state_abbres = list(self.state_to_abbre[state] for state in states)
		for index, city in enumerate(cities):
			query_url = ""
			if city == "new york":
				query_url = self.base_url_2.replace("<state>", state_abbres[index])
			else:
				query_url = self.base_url.replace("<city>", city).replace("<state", state_abbres[index])
				city = city.replace(" ", "-")
			print(query_url)
			status_code, html = self.retrieve_html(query_url)
			print(status_code)
			print(html)
			break

	def run_kiplinger(self):
		status_code, html = self.retrieve_html(self.kiplinger_url)
		if status_code == self.SUCCESS:
			root = BeautifulSoup(html, "html.parser")
			table = root.find("div", {'class':['kip-content']}).find("table", {'class':['kip-table', 'sortable']})
			for row in table.findAll("tr"):
				cols = row.findAll("td")
				if len(cols) < 5: continue
				city = cols[0].text.lower().split(",")[0]
				median_price = int(cols[1].text[1:-1].strip().replace(",", ""))
				self.writer.writerow((city, median_price))



def main():
	scrapper = CitySOLScrapper("../data/city_sol.csv")
	scrapper.run_kiplinger()


if __name__ == "__main__":
    main()

