import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()
def send_email(subject, message):
    # set your email and password
    # please use App Password
    email_address = os.getenv("SENDER")
    email_password = os.getenv("SENDER_PASSWORD")

    # create email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = os.getenv("RECEIVER")
    msg.set_content(message)

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

