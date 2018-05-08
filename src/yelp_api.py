import requests
import json
import csv

class Yelp:
    home_csv = "../data/pittsburgh_housing_data_2.csv"

    def read_api_key(self):
        with open('api_key_2.txt', 'r') as f:
            return f.read().replace('\n','')

    def yelp_amenity_search(self, api_key, lat, lon, query):
        headers = {"Authorization":"Bearer " + api_key}
        params_restaurant = {}
        params_shopping = {}
        if lat == -1:
            params_restaurant = {"location":query, "radius":1000, "categories":"restaurants"}
            params_shopping = {"location":query, "radius":1000, "categories":"shopping"}
        else:
            params_restaurant = {"latitude":lat, "longitude":lon, "radius":1000, "categories":"restaurants"}
            params_shopping = {"latitude":lat, "longitude":lon, "radius":1000, "categories":"shopping"}
        response_restaurant = requests.get("https://api.yelp.com/v3/businesses/search", 
            headers=headers,
            params=params_restaurant)
        response_shopping = requests.get("https://api.yelp.com/v3/businesses/search", 
            headers=headers,
            params=params_shopping)
        data_restaurants = json.loads(response_restaurant.content.decode("utf-8"))
        data_shopping = json.loads(response_shopping.content.decode("utf-8") )
        return (data_restaurants["total"], data_restaurants["businesses"], 
            data_shopping["total"], data_shopping["businesses"])

    def get_average_rating(self, businesses):
        total_rating = 0.0
        total_dollar_sign = 0.0
        missing_data = 0
        if len(businesses) == 0:
            return (-1.0, -1.0)
        for business in businesses:
            if ("rating" not in business) or ("price" not in business):
                missing_data += 1
                continue
            total_rating += business["rating"]
            total_dollar_sign += len(business["price"])
        count = len(businesses) - missing_data
        if count == 0:
            return (-1.0, -1.0)
        average_rating = float('%.3f'%(total_rating / count))
        average_dollar_sign = float('%.3f'%(total_dollar_sign / count))
        return (average_rating, average_dollar_sign)

    def run(self, api):
        file_loc = "../data/yelp.csv"
        out_file = open(file_loc, 'wt', newline='')
        writer = csv.writer(out_file)
        writer.writerow(('addr', 'city', 'state', 
            'restaurant_count', 'restaurant_rating', 'restaurant_price', 
            'shopping_count', 'shopping_rating', 'shopping_price'))
        with open(self.home_csv) as csvfile:
            cr = csv.reader(csvfile)
            count = 0
            for row in cr:
                count+=1
                if count <= 1005: continue
                if row[0] != "long":
                    query = row[2] + "," + row[3] + "," + row[4]
                    rest_count, rests, shop_count, shops = self.yelp_amenity_search(api, -1, -1, query)
                    rest_rating, rest_price = self.get_average_rating(rests)
                    shop_rating, shop_price = self.get_average_rating(shops)
                    writer.writerow((row[2], row[3], row[4],
                        rest_count, rest_rating, rest_price,
                        shop_count, shop_rating, shop_price))
                if count % 50 == 0:
                    print(str(count) + " homes done")

def main():
    yelp = Yelp()
    api = yelp.read_api_key()
    yelp.run(api)
    # rest_count, rests, shop_count, shops = yelp.yelp_amenity_search(api, 40.473956, -79.960612, None)
    # print(rest_count)
    # print(shop_count)
    # print(yelp.get_average_rating(rests))
    # print(yelp.get_average_rating(shops))


if __name__ == "__main__":
    main()