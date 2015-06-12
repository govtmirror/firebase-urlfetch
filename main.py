from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2


import webservice as services
from nmbauthenticator import *


@nmbauthhtml
def gethomepage():
	page = open('client.html').read()
	# page = open('build.html').read()
	return page

"""handlers for client redirects"""
class HomeHandler(webapp2.RequestHandler):
	def get(self):
		# force a login even though no action is taken
		user = users.get_current_user()
		if user:
			# authentication decorated action
			# INDEX_HTML = gethomepage(permission='JOE FRED ADMIN')
			INDEX_HTML = gethomepage()
			self.response.out.write(INDEX_HTML)
		else:
			self.redirect(users.create_login_url(self.request.uri))


app = webapp2.WSGIApplication(
	[
	('/', HomeHandler)
	],
	debug=True)

services.add_routes(app)