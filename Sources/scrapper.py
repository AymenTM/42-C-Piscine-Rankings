
# Version 0.1

from robobrowser import RoboBrowser
from bs4 import BeautifulSoup

import re
import os
import csv

from piscineSep2018 import PISCINE
from piscineSep2018 import LOGINS


# Login on Intra — — — — — — — — — — — — — — — — — — — — — — — — —

browser = RoboBrowser(parser='html5lib')
browser.open('https://signin.intra.42.fr/users/sign_in')

form = browser.get_form()
form['user[login]'] = os.environ.get('USER')
form['user[password]'] = os.environ.get('PASS')

browser.submit_form(form)


# Lookup, Retrieve and Store User Info — — — — — — — — — — — — — —

all_user_info = []

for login in LOGINS:

    # Look Up
    browser.open(f'https://profile.intra.42.fr/users/{login}')
    source = str(browser.parsed())
    # soup = BeautifulSoup(source, 'html5lib')

    # Retrieve
    match = re.search(r'"Piscine C":{"level":\d\.\d\d?', source)
    level = re.search(r'\d\.\d\d?', match[0])

    # Store
    all_user_info.append(
        {
            'login': login,
            'level': float(level[0])
        }
    )


# Sort Users by Level — — — — — — — — — — — — — — — — — — — — —

def get_user_lvl(user):
    return user['level']


all_user_info.sort(key=get_user_lvl, reverse=True)


# Write the Result to a CSV File — — — — — — — — — — — — — — — —

rank = 1

with open(f'../{PISCINE}_Rankings.csv', 'w') as f:

    csv_writer = csv.writer(f, delimiter=',')

    csv_writer.writerow(['Rank', 'Login', 'Level'])

    for user in all_user_info:
        csv_writer.writerow([rank, user['login'], f"{user['level']:.2f}"])
        rank += 1


# Done.
