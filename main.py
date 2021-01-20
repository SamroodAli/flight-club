"""Main module"""
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

# Instances needed
# To manage google sheets data
data_manager = DataManager()
# To search for destination iata codes and flights
flight_search = FlightSearch()
# To alert user via sms using Twilio api
notification_manager = NotificationManager()

# Get destination_data
destinations_data = data_manager.get_destinations_data()

if destinations_data[0]["iataCode"] == "":
    for row in destinations_data:
        row["iataCode"] = flight_search.get_iata_code(row["city"])
    # Update sheets data
    data_manager.destination_data = destinations_data
    data_manager.update_sheets_data()


# Get dates
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = tomorrow + timedelta(days=6*30)

# Flight constants
ORIGIN_CITY_CODE = "LON"
FLIGHT_DATA_CURRENCY = "GBP"


for destination in destinations_data:
    flight = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_CODE,
        destination_city_code=destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_now,
        curr=FLIGHT_DATA_CURRENCY
    )
    if flight is None:
        continue

    if flight["price"] < destination["lowestPrice"]:

        # Getting users data
        users_data = data_manager.get_users_data()
        emails =[row["email"] for row in users_data]
        names = [row["first"] for row in users_data]

        # Message to send

        message = f"Flight deal alert\n Only {FLIGHT_DATA_CURRENCY} {flight['price']} to fly from {flight['origin_city']}-{flight['origin_airport']} to {flight['destination_city']}-{flight['destination_airport']}, from {flight['travel_date']} to {flight['return_date']}."
        if flight["stop_overs"] > 0:
            message += f"\nThe flight has {flight['stop_overs']} stop over, via {flight['via_city']}."
        print(message)

        # Link to send to access flight via google
        google_link = f"https://www.google.co.uk/flights?hl=en#flt={flight['origin_airport']}.{flight['destination_airport']}.{flight['travel_date']}*{flight['destination_airport']}.{flight['origin_airport']}.{flight['return_date']}"

        # Sending emails to user
        notification_manager.send_mails(emails, message, google_link)

        # To send sms via TWILIO , Uncomment this line
        # notification_manager.send_sms(message=f"Flight deal alert\n Only {flight_data_currency} {flight['price']} to fly from {flight['origin_city']}-{flight['origin_airport']} to {flight['destination_city']}-{flight['destination_airport']}, from {flight['travel_date']} to {flight['return_date']}")
