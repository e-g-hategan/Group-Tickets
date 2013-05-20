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
import model
import datetime

class MainHandler(AuthenticatedRequestHandler):
    def show_page(self):
        user_info = AuthenticatedRequestHandler.authenticate_user(self)
        if user_info:
            my_days = []
            today = datetime.date.today()
            monday = today + datetime.timedelta(days=-today.weekday())
            nickname = user_info[0]

            for i in range(0, 7):
            	date = monday + datetime.timedelta(days=i)
                day = model.get_day(date)

                my_day = dict()
                my_day['date'] = date.strftime('%A, %d %h')
                my_day['options'] = ['Norm','Late','No','?']
                
                if nickname in day['users']:
                    my_day['selected'] = day['users'][nickname]
                else:
                    my_day['selected'] = '?'

                my_days.append(my_day)

            template_values = {
                'title': 'My Schedule',
                'page': 'my',
                'nickname': user_info[0],
                'logout_url': user_info[1],
                'my_days': my_days
            }
            path = os.path.join(os.path.dirname(__file__), 'template.html')
            self.response.out.write(template.render(path, template_values)) 

    def get(self):   
        self.show_page()


    def post(self):
#        for key in self.request:
#            print key
        self.show_page()    

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
