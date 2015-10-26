from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2
import webservice as services



"""handlers for client redirects"""
class HomeHandler(webapp2.RequestHandler):
	def get(self):
		INDEX_HTML = open('client.html').read()
		self.response.out.write(INDEX_HTML)



app = webapp2.WSGIApplication(
	[
	('/', HomeHandler)
	],
	debug=True)

services.add_routes(app)