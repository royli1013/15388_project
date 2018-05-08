import requests
from bs4 import BeautifulSoup
import csv

class Helper2:
	def state_abbre_map(self):
		url = "http://www.stateabbreviations.us"
		response = requests.get(url)
		rtn = {}
		if response.status_code == 200:
			root = BeautifulSoup(response.content, "html.parser")
			tables = (root.findAll("table", {'class':['f']}))
			# States
			for row in tables[0].findAll('tr'):
				cols = row.findAll("td")
				if len(cols) == 4:
					if cols[0].text != "State":
						rtn[cols[0].text.strip().lower()] = cols[2].text.strip().lower()
			# Districts
			for row in tables[1].findAll('tr'):
				cols = row.findAll("td")
				if len(cols) == 4:
					if cols[0].text != "Subdivision":
						rtn[cols[0].text.strip().lower()] = cols[2].text.strip().lower()
		return rtn


def main():
	h = Helper2()
	print(h.state_abbre_map())


if __name__ == "__main__":
    main()
