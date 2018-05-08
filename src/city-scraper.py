import requests
from bs4 import BeautifulSoup
import csv

class USCityScrapper:
	SUCCESS = 200
	URL = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"

	def retrieve_html(self, url):
		response = requests.get(url);
		return (response.status_code, response.content)

	def __init__(self, file_loc):
		self.out_file = open(file_loc, 'wt', newline='')
		self.writer = csv.writer(self.out_file)
		self.writer.writerow(('city', 'state', 'population_density', 'population_trend', 'lat', 'lon'))

	def run(self):
		status_code, html = self.retrieve_html(self.URL)
		if status_code == self.SUCCESS:
			root = BeautifulSoup(html, "html.parser")
			body_content = root.find("div", id="bodyContent").find("div", id="mw-content-text")
			tables = body_content.findAll("table", {'class':['wikitable', 'sortable','jquery-tablesorter']})
			city_table = tables[0]
			rows = city_table.findAll("tr")
			for row in rows:
				cols = row.findAll("td")
				if len(cols) < 8: continue
				city = cols[1].text.strip()
				index = city.find("[")
				if index != -1:
					city = city[:index]
				state = cols[2].text.strip()
				if len(cols[5].findAll("span")) < 2: continue
				population_trend = (cols[5].findAll("span"))[1].text
				if population_trend[0] != '+':
					population_trend = "-" + population_trend[1:-1] + "%"
				population_density = cols[8].text.split("/")[0]
				location = cols[-1].find("span", {'class' :['geo']}).text.split(";")
				lat = float(location[0].strip())
				lon = float(location[1].strip())
				self.writer.writerow((city, state, population_density, population_trend, lat, lon))


def main():
	scrapper = USCityScrapper("../data/cities.csv")
	scrapper.run()


if __name__ == "__main__":
    main()
