import os
import requests


class DataManager:
    """This class is responsible for talking to google sheets"""
    def __init__(self):
        self.endpoint = os.environ.get("SHEETY_ENDPOINT")
        self.username = os.environ.get("SHEETY_USERNAME")
        self.password = os.environ.get("SHEETY_PASSWORD")

        self.sheets_data = {}

    def get_sheets_data(self):
        response = requests.get(url=self.endpoint, auth=(self.username, self.password))
        response.raise_for_status()
        data = response.json()
        self.sheets_data = data["prices"]
        return self.sheets_data

    def update_sheets_data(self):
        for city in self.sheets_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{self.endpoint}/{city['id']}",
                json=new_data,
                auth=(self.username, self.password)
            )
            print(response.text)
