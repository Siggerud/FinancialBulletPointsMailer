# import packages
# below packages are built-in - no need to install anything new!
# yupi :)
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()
def send_email(to, subject, message):
    # set your email and password
    # please use App Password
    email_address = os.getenv("EMAIL_ADRESS")
    email_password = os.getenv("EMAIL_PASSWORD")

    # create email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = to
    msg.set_content(message)

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

#send_email("christian.siggerud@gmail.com", "stocks", "this is a test")