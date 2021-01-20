from twilio.rest import Client
import os
import smtplib

# Twilio API Authentication Data
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_no = os.environ["TWILIO_NO"]
user_no = os.environ["USER_NO"]

# Email id username and password
my_email = os.environ.get("EMAIL_ID")
password = os.environ.get("EMAIL_PASSWORD")


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

    def send_mails(self, emails, message, google_link):
        with smtplib.SMTP("smtp.live.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            for user in emails:
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs="samrood.kl@gmail.com",
                    msg=f"Subject:Flight deal from Flight Club\n\n{message}\nlink:{google_link}".encode("utf-8")
                )

