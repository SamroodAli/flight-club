import os
import requests


class FlightSearch:
    def __init__(self):
        self.api_key = os.environ.get("TEQUILA_API_KEY")
        self.location_parameters = {
            "apikey": self.api_key,
            "locale": "en-US",
            "location_types": "airport",
            "limit": 1,
            "active_only": "true",
        }
        self.location_endpoint = "https://tequila-api.kiwi.com/locations/query"

        # flights search api and parameters data
        self.flights_search_api_endpoint = "https://tequila-api.kiwi.com/v2/search"

    def get_iata_code(self, airport_name):
        self.location_parameters["term"] = airport_name
        response = requests.get(self.location_endpoint, params=self.location_parameters)
        iata_code = response.json()["locations"][0]["id"]
        return iata_code