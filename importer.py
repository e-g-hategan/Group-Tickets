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
from model import User
import importer


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

def import_data():
    model.clean_model("User", model.user_key())
    model.clean_model("Schedule", model.schedule_key())
    model.clean_model("Price", model.price_key())

    data = fetch_data()

    users = []
    prices = []
    schedules = []

    user_by_index = dict()
    user_by_nickname = dict()

    for index, nickname in enumerate(data[0]):
        if not nickname in [None, "Date", "", "Group Ticket"]:
            user_id = nickname.lower() + "@swiftkey.net"
            if nickname == "James":
              user_id = "james.hay@swiftkey.net"

            user = User(parent=model.user_key())
            user.nickname = nickname
            user.user_id = user_id
            user.put()

            user_by_index[index] = user_id
            user_by_nickname[nickname] = user_id
            users.append({'nickname': nickname, 'user_id': user_id})

    return {'users': users, 'prices': prices, 'schedules': schedules, 'data': data}