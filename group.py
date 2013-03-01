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

import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users
from helper import AuthenticatedRequestHandler
import csv
import importer

class MainHandler(AuthenticatedRequestHandler):
    def get(self):
        user_info = AuthenticatedRequestHandler.authenticate_user(self)
        if user_info:
            imported = importer.import_data()
            users = imported['users']
            prices = imported['prices']
            days = imported['days']

            template_values = {
                'title': 'Group Schedule',
                'page': 'group',
                'nickname': user_info[0],
                'logout_url': user_info[1],
                'users': users,
                'prices': prices,
                'days': days,
            }

            path = os.path.join(os.path.dirname(__file__), 'template.html')
            self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/group', MainHandler)
], debug=True)
