from data_manager import DataManager
from flight_search import FlightSearch


# Instances needed
data_manager = DataManager()
flight_search = FlightSearch()


sheet_data = data_manager.get_sheets_data()

if sheet_data[0]["iataCode"]=="":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_iata_code(row["city"])
    # Update sheets data
    data_manager.sheets_data = sheet_data
    data_manager.update_sheets_data()
