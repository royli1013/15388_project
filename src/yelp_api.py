import requests
import json

class Yelp:
    def read_api_key(self):
        with open('api_key.txt', 'r') as f:
            return f.read().replace('\n','')

    def yelp_amenity_search(self, api_key, lat, lon, query):
        headers = {"Authorization":"Bearer " + api_key}
        params_restaurant = {}
        params_shopping = {}
        if lat == -1:
            params_restaurant = {"location":query, "radius":300, "categories":"restaurants"}
            params_shopping = {"location":query, "radius":300, "categories":"shopping"}
        else:
            params_restaurant = {"latitude":lat, "longitude":lon, "radius":300, "categories":"restaurants"}
            params_shopping = {"latitude":lat, "longitude":lon, "radius":300, "categories":"shopping"}
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

def main():
    yelp = Yelp()
    api = yelp.read_api_key()
    rest_count, rests, shop_count, shops = yelp.yelp_amenity_search(api, 40.473956, -79.960612, None)
    print(rest_count)
    print(shop_count)


if __name__ == "__main__":
    main()