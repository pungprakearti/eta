# get request to mapquest api
import requests

# personal information
from secret import CONSUMER_KEY as KEY
from secret import LOGIN
from secret import NUM
from secret import DEST
from secret import ORIGIN
from secret import CITY

# for password input
import getpass

# for email
import smtplib

# ETA Calculation
import math
from datetime import datetime
from datetime import timedelta

#################################################


def get_ETA(city, nav_param):

    URL = f'https://www.mapquestapi.com/directions/v2/route?key={KEY}&from={ORIGIN}&to={DEST}'

    try:
        map_resp = requests.get(URL).json()
    except requests.exceptions.ConnectionError:
        print('Unable to connect to the internet')
        return

    eta = (map_resp['route']['realTime'])/60
    return [eta, city]


def form_and_send_message():

    time = (datetime.now()+timedelta(minutes=eta)).strftime('%-I:%M%p')
    print(time)

    message = f"\nI just got on the bus in {CITY}. My current ETA is {math.floor(eta)} minutes. I should arrive by {time}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(LOGIN, pw)
    except smtplib.SMTPAuthenticationError:
        print('Authenication failed: incorrect password.\nMessage not sent.')

    server.sendmail("ETA", NUM, message)
    print(f'Sent message to {NUM}\n"{message}"')


#################################################

pw = getpass.getpass("password: ")

eta, city = get_ETA(city, nav_param)

form_and_send_message()

#################################################
