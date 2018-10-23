'''
eta.py sends a text to a cellphone number's email address. The text contains
information on when a user should arrive at a destination.
ETA is calculated with real time traffic conditions using mapquest.com's free api.

This script requires a gmail address and a free api key from mapquest.com
'''

# get request to mapquest api
import requests

# personal information
from secret import MAPQUEST_API_KEY as KEY
from secret import GMAIL_LOGIN as LOGIN
from secret import CELL_NUM_EMAIL as NUM

# 'latitude,longitude'
from secret import DEST
from secret import ORIGIN

# for password input
import getpass

# for email
import smtplib

# ETA Calculation
import math
from datetime import datetime
from datetime import timedelta

# used for sys.exit
import sys

#################################################


def get_eta():
    ''' Get ETA from mapquest.com using a get request. Sets eta, city_origin, and city_dest '''

    URL = f'https://www.mapquestapi.com/directions/v2/route?key={KEY}&from={ORIGIN}&to={DEST}'

    try:
        map_resp = requests.get(URL).json()
    except requests.exceptions.ConnectionError:
        # This is a more human readable error
        sys.exit('Unable to connect to the internet')

    # grab data
    eta = (map_resp['route']['realTime'])/60
    city_origin = map_resp['route']['locations'][0]['adminArea5']
    city_dest = map_resp['route']['locations'][1]['adminArea5']


def form_and_send_message():
    ''' Form and send an email message to the users's gmail account '''

    # get current time and add eta in minutes, then format
    time = (datetime.now()+timedelta(minutes=eta)).strftime('%-I:%M%p'))

    message=f'\nI just got on the bus in {CITY}. My current ETA is {math.floor(eta)} minutes. I should arrive by {time}'

    # connect to gmail email server
    server=smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(LOGIN, pw)
    except smtplib.SMTPAuthenticationError:
        # I prefer this error compared to the default
        sys.exit('Authenication failed: incorrect password.\nMessage not sent.')

    # send email message
    server.sendmail("ETA", NUM, message)
    print(f'Sent message to {NUM}\n"{message}"')


def send_eta():
    ''' Get a password for gmail account and run functions '''

    # get password from command line
    pw=getpass.getpass('password: ')
    eta=get_eta()
    form_and_send_message()


#################################################
# Run Script

# global variables
pw=''
eta=0
city_origin=''
city_dest=''

# run script
send_eta()

#################################################
