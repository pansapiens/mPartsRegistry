#!/usr/bin/env python
#
#    This file is part of the mPartsRegistry erver 
#    Copyright (C) 2010, Andrew Perry (ajperry@pansapiens.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

DEBUG_MODE = True

import logging, sys, base64, md5
from datetime import datetime, timedelta
log = logging.getLogger()

import os, time, random

import cgi, wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
# exceptions ..
from google.appengine.runtime import DeadlineExceededError
from google.appengine.ext.db import Timeout

# for appstats
from google.appengine.ext.webapp.util import run_wsgi_app

from django.utils import simplejson as json

from partsregistry import *

class Front(webapp.RequestHandler):
  def get(self):
    
    template_values = {}   
    template_values["nextpage"] = True
    
    path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
    self.response.out.write(template.render(path, template_values))
    
class PartPage(webapp.RequestHandler):
  def get(self, part_name):
    template_values = {}
    
    # if part_name is in the URL like:
    # /html/part.?part={part_name} 
    # then take the query value rather than
    # the usual form /html/part.{part_name}
    if self.request.get("part_name"):
      part_name = self.request.get("part_name")
      
    part = Part(part_name)
    template_values["part"] = part
    
    if part.error:
      template_values["error"] = part.error
      path = os.path.join(os.path.dirname(__file__), 'templates/part.html')
      self.response.out.write(template.render(path, template_values))
      return
    
    path = os.path.join(os.path.dirname(__file__), 'templates/part.html')
    self.response.out.write(template.render(path, template_values))

class getPart(webapp.RequestHandler):
  def get(self):
    part_name = self.request.get("part")
    self.redirect("/html/part.%s" % part_name)

def main():
  application = webapp.WSGIApplication([('/', Front),
                                        ('/html/part.(.*)', PartPage),
                                        ],
                                       debug=DEBUG_MODE)
  
  # old way, without app stats
  #wsgiref.handlers.CGIHandler().run(application)
  
  # new way, so appstats can be used
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()