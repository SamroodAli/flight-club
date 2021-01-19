import os
import requests


class DataManager:
    """This class is responsible for talking to google sheets"""
    def __init__(self):
        self.endpoint = os.environ.get("SHEETY_ENDPOINT")
        self.username = os.environ.get("SHEETY_USERNAME")
        self.password = os.environ.get("SHEETY_PASSWORD")

        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=self.endpoint, auth=(self.username, self.password))
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data
