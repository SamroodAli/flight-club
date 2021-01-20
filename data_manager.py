import os
import requests


class DataManager:
    """This class is responsible for talking to google sheets"""
    def __init__(self):
        self.endpoint = os.environ.get("SHEETY_ENDPOINT")
        self.username = os.environ.get("SHEETY_USERNAME")
        self.password = os.environ.get("SHEETY_PASSWORD")

        # Destination Data
        self.destination_data = {}
        # Users data
        self.users_data = {}

    def get_destinations_data(self):
        response = requests.get(url=f"{self.endpoint}/prices", auth=(self.username, self.password))
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def get_users_data(self):
        response = requests.get(url=f"{self.endpoint}/users", auth=(self.username, self.password))
        response.raise_for_status()
        data = response.json()
        self.users_data = data["users"]
        return self.users_data

    def update_sheets_data(self):
        for city in self.destination_data:
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


