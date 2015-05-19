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

import webapp2
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

# exceptions ..
from google.appengine.runtime import DeadlineExceededError
from google.appengine.ext.db import Timeout

from django.utils import simplejson as json

from partsregistry import *
from part_id_list import *

class Front(webapp2.RequestHandler):
  def get(self):
    
    template_values = {}   
    template_values["nextpage"] = True
    
    path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
    self.response.out.write(template.render(path, template_values))
    
class PartPage(webapp2.RequestHandler):
  """
  Serves up the part page for the requested part.
  """
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
    
    renderPartPage(self, template_values)

class RandomPartPage(webapp2.RequestHandler):
  """
  Plucks a random part from the precompiled parts list and
  shows the user it's part page.
  """
  def get(self):
    template_values = {}
    part_name = random.choice(ALL_PART_IDS)
    part = Part(part_name)
    template_values["part"] = part
    
    renderPartPage(self, template_values)
    
def renderPartPage(req, template_values):
    """
    Does some error checking then renders the part page, or an error.
    """
    part = template_values['part']
    
    if part.error:
      template_values["error"] = part.error
      path = os.path.join(os.path.dirname(__file__), 'templates/part.html')
      req.response.out.write(template.render(path, template_values))
      return
    
    path = os.path.join(os.path.dirname(__file__), 'templates/part.html')
    req.response.out.write(template.render(path, template_values))

class getPart(webapp2.RequestHandler):
  def get(self):
    part_name = self.request.get("part")
    self.redirect("/html/part.%s" % part_name)

application = webapp2.WSGIApplication([('/', Front),
                                       ('/html/random', RandomPartPage),
                                       ('/html/part.(.*)', PartPage),
                                      ],
                                       debug=DEBUG_MODE)
