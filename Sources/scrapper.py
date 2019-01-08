
# Version 0.1

from robobrowser import RoboBrowser

import re
import os
import csv

from piscineOct2018 import PISCINE
from piscineOct2018 import LOGINS


# We'll need these later — — — — — — — — — — — — — — — — — — — — —

def get_dropouts():
    dropouts = 0
    for user in all_user_info:
        if user['level'] == 0:
            dropouts += 1
    return dropouts


def get_average_level():
    total_level = 0
    for user in all_user_info:
        total_level += user['level']
    return total_level // (total_pisciners - total_dropouts)


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


# Get some Statistics — — — — — — — — — — — — — — — — — — — — —

total_pisciners = len(all_user_info)
total_dropouts = get_dropouts()
average_level = get_average_level()


# Write the Result to a CSV File — — — — — — — — — — — — — — — —

rank = 1

with open(f'../{PISCINE}_Rankings.csv', 'w') as f:

    csv_writer = csv.writer(f, delimiter=',')

    csv_writer.writerow(['Rank', 'Login', 'Level'])
    csv_writer.writerow(['Total Pisciners', '', total_pisciners])
    csv_writer.writerow(['Total Drowned', '', total_dropouts])
    csv_writer.writerow(['Average Level', '', average_level])

    for user in all_user_info:
        csv_writer.writerow([rank, user['login'], f"{user['level']:.2f}"])
        rank += 1


# Done.
