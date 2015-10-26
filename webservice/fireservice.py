import webapp2
from webapp2_extras import json
import logging
from google.appengine.api import datastore
from google.appengine.ext import ndb
from datetime import datetime
from google.appengine.api import urlfetch


class TestHandler(webapp2.RequestHandler):
  def get(self):
    logging.info("<<<<<<<<   GET, in TestHandler   >>>>>>>>")



    url = "https://awstest.firebaseio.com/unions.json"
    result = urlfetch.fetch(url)
    logging.info("ZZZZZZZ   " + result.content)

    # assemble and send the response
    self.response.content_type = 'application/json'
    self.response.write(json.encode(result.content))