
# Version 0.1

from robobrowser import RoboBrowser

import re
import os
import csv
import itertools

from piscineSep2018 import PISCINE
from piscineSep2018 import LOGINS


# We'll need these later — — — — — — — — — — — — — — — — — — — — —

def still_swimming(user):
    return True if user['level'] > 0 else False


def get_average_level(swimmers):

    total_level = 0
    for user in swimmers:
        total_level += user['level']

    return total_level / len(swimmers)


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

    try:

        # Look Up
        browser.open(f'https://profile.intra.42.fr/users/{login}')
        source = str(browser.parsed())

        # Retrieve
        match = re.search(r'"Piscine C":{"level":\d\.\d\d?', source)
        level = re.search(r'\d\.\d\d?', match[0])

    except:
        continue

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

swimmers = list(itertools.takewhile(still_swimming, all_user_info))
drownees = list(itertools.dropwhile(still_swimming, all_user_info))

total_pisciners = len(all_user_info)
total_swimming = len(swimmers)
total_drowned = len(drownees)

average_level = f'{get_average_level(swimmers):.2f}'


# Write the Result to a CSV File — — — — — — — — — — — — — — — —

rank = 1

with open(f'../{PISCINE}_Rankings.csv', 'w') as f:

    csv_writer = csv.writer(f, delimiter=',')

    csv_writer.writerow(['Rank', 'Pisciner', 'Level'])

    for user in swimmers:
        csv_writer.writerow([rank, user['login'], f"{user['level']:.2f}"])
        rank += 1

    csv_writer.writerow(['', '', ''])

    for user in drownees:
        csv_writer.writerow(['unranked', user['login'], f"{user['level']:.2f}"])

    csv_writer.writerow(['', '', ''])
    csv_writer.writerow(['Total Pisciners', '', total_pisciners])
    csv_writer.writerow(['Total Survivors', '', total_swimming])
    csv_writer.writerow(['Total Drowned', '', total_drowned])
    csv_writer.writerow(['Piscine Level', '', average_level])


# Done.
