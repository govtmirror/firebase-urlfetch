# import getalldata as gad
# import userservice as us
import fireservice as fire
from webapp2_extras.routes import RedirectRoute
import logging

_routes = [
		RedirectRoute('/mail', fire.TestHandler),
		]

def add_routes(app):
	logging.info("<<<<<<<<<<<<<<<   in add_routes   >>>>>>>>>>>>>>>>")
	if app.debug:
		secure_scheme = 'http'
	for r in _routes:
		app.router.add(r)