from twilio.rest import Client
import os

# Twilio API Authentication Data
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_no = os.environ["TWILIO_NO"]
user_no = os.environ["USER_NO"]


class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""
    def __init__(self):
        self.client = Client(account_sid, auth_token)

    def send_sms(self,message):
        message = self.client.messages.create(
            body=message,
            from_=twilio_no,
            to=user_no
        )
        print(message.sid)
