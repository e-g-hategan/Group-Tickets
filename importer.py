# coding=utf-8

#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import re, os

import model
from model import User, Day, Price
import importer
import datetime
import json


username        = ''
passwd          = ''
doc_name        = 'Group tickets'

def fetch_data():
    gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    gd_client.email = username
    gd_client.password = passwd
    gd_client.source = 'payne.org-example-1'
    gd_client.ProgrammaticLogin()

    q = gdata.spreadsheet.service.DocumentQuery()
    q['title'] = doc_name
    q['title-exact'] = 'true'
    feed = gd_client.GetSpreadsheetsFeed(query=q)
    spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
    feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
    worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]

    query = gdata.spreadsheet.service.CellQuery()
    query.return_empty = "true"
    query.max_col = "22"
    cells = gd_client.GetCellsFeed(spreadsheet_id, worksheet_id, query=query).entry

    table = [[None for x in xrange(22)] for x in xrange(2500)]
    for item in cells:
        cell = item.cell
        col = int(cell.col) - 1
        row = int(cell.row) - 1
        text = cell.text
        table[row][col] = unicode(text, 'utf-8').replace(u'£','') if text else None
    return table

def is_number(s):
    if s == None:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False

def import_data():
    model.clean_model("User", model.user_key())
    model.clean_model("Day", model.day_key())
    model.clean_model("Price", model.price_key())

    data = fetch_data()

    users = []
    days = []
    prices = []

    user_by_index = dict()
    user_by_nickname = dict()

    # extracting users
    for index, nickname in enumerate(data[0]):
        if not nickname in [None, "Date", "", "Group Ticket"]:
            user_id = nickname.lower() + "@swiftkey.net"
            if nickname == "James":
              user_id = "james.hay@swiftkey.net"

            user_by_index[index] = user_id
            user_by_nickname[nickname] = user_id
            users.append({'nickname': nickname, 'user_id': user_id})

            user = User(parent=model.user_key())
            user.nickname = nickname.strip()
            user.user_id = user_id.strip()
            user.put()

    # extracting days
    for row in data:
        if not row[0] in ['', None, 'Date', 'BALANCE']:
            date = None
            custom_price = None
            buyer = None
            users_for_day = {}
            guests = {}
            for index, val in enumerate(row):
                if index == 0:
                    date = datetime.datetime.strptime(val, "%m/%d/%Y").date()
                if index == 1 and is_number(val):
                    custom_price = float(val)
                if index > 1 and index < 20 and index % 2 == 0:
                    if val == 'Norm' or val == 'Yes' or val == 'Late' or val == 'No':
                        user_id = user_by_index[index]
                        users_for_day[user_id] = val
                if index == 20 and val != None and val != '---':
                    buyer = user_by_nickname[val.strip()]

            days.append({'date': date, 'price': custom_price, 'buyer': buyer, 'users': users_for_day, 'guests': guests})

            day = Day(parent=model.day_key())
            day.date = date
            day.price = custom_price
            day.buyer = buyer
            day.users = json.dumps(users_for_day)
            day.guests = json.dumps(guests)
            day.put()

    # extracting prices
    prices.append({'since': datetime.date(2013, 1, 1), 'prices': {3: 45.60, 4: 46.00, 5: 69.00, 6: 91.20, 7: 91.60, 8: 92.00}})

# TODO: remove when done
    return {'users': users, 'prices': prices, 'days': days}