
# Version 0.1

from robobrowser import RoboBrowser
from bs4 import BeautifulSoup

import re
import os
import csv

from piscine import PISCINE
from piscine import USERNAMES


# Login on Intra — — — — — — — — — — — — — — — — — — — — — — — — —

browser = RoboBrowser(parser='html5lib')
browser.open('https://signin.intra.42.fr/users/sign_in')

form = browser.get_form()
form['user[login]'] = os.environ.get('USER')
form['user[password]'] = os.environ.get('PASS')

browser.submit_form(form)


# Lookup, Retrieve and Store User Info — — — — — — — — — — — — — —

all_user_info = []

for username in USERNAMES:

    # Look Up
    browser.open(f'https://profile.intra.42.fr/users/{username}')
    source = str(browser.parsed())
    # soup = BeautifulSoup(source, 'html5lib')

    # Retrieve
    match = re.search(r'"Piscine C":{"level":\d\.\d\d?', str(source))
    level = re.search(r'\d\.\d\d?', match[0])

    # Store
    all_user_info.append(
        {
            'username': username,
            'level': float(level[0])
        }
    )


# Sort Users by Level — — — — — — — — — — — — — — — — — — — — —

def get_user_lvl(user):
    return user['level']


all_user_info.sort(key=get_user_lvl, reverse=True)


# Write the Result to a CSV File — — — — — — — — — — — — — — — —

rank = 1

with open(f'{PISCINE}_Rankings.csv', 'w') as f:

    csv_writer = csv.writer(f, delimiter=',')

    csv_writer.writerow(['Rank', 'Username', 'Level'])

    for user in all_user_info:
        csv_writer.writerow([rank, user['username'], f"{user['level']:.2f}"])
        rank += 1


# Done.
