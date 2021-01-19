import os
import requests


class FlightSearch:
    def __init__(self):
        self.api_key = os.environ.get("TEQUILA_API_KEY")

        # location code endpoint
        self.location_endpoint = "https://tequila-api.kiwi.com/locations/query"

        # flights search api
        self.flights_search_api_endpoint = "https://tequila-api.kiwi.com/v2/search"

        # Api authentication header data
        self.headers = {
            "apikey": self.api_key
        }
        self.location_parameters = {
            "locale": "en-US",
            "location_types": "airport",
            "limit": 1,
            "active_only": "true",
        }

    def get_iata_code(self, airport_name):
        self.location_parameters["term"] = airport_name
        response = requests.get(self.location_endpoint, params=self.location_parameters, headers=self.headers)
        iata_code = response.json()["locations"][0]["id"]
        return iata_code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, curr):
        api_parameters = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flights_type": "round",
            "curr": curr
        }

        response = requests.get(
            url=f"{self.flights_search_api_endpoint}",
            params=api_parameters,
            headers=self.headers
        )

        data = response.json()["data"][0]

        print(data["price"])
        print(data["route"][0]["cityFrom"])
        # Flight data
        flight_data = {
            "price": data["price"],
            "origin_city": data["route"][0]["cityFrom"],
            "origin_airport": data["route"][0]["flyFrom"],
            "destination_city": data["route"][0]["cityTo"],
            "destination_airport": data["route"][0]["flyTo"],
            "travel_date": data["route"][0]["local_departure"].split("T")[0],
            "return_date": data["route"][1]["local_departure"].split("T")[0],
        }
        print(f"{flight_data['destination_city']},{flight_data['price']}")
        return flight_data
