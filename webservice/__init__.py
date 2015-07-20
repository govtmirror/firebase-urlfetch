# import getalldata as gad
# import userservice as us
import obligationservice as ob
import casexservice as am
import fireservice as fire
from webapp2_extras.routes import RedirectRoute
import logging

_routes = [
		# RedirectRoute('/getalldata', gad.GetAllDataHandler),		
		# RedirectRoute('/user/<ckfield>/<ckvalue>', us.UserHandler),	
		# RedirectRoute('/user', us.UserHandler),	
		RedirectRoute('/bfscsv', ob.BfscsvHandler),	
		RedirectRoute('/fire', fire.TestHandler),
		RedirectRoute('/postbfs', ob.BfspostHandler),
		RedirectRoute('/bfsentries', ob.BfsentriesHandler),		
		RedirectRoute('/arbcases', am.ArbcaseHandler)
		]

def add_routes(app):
	logging.info("<<<<<<<<<<<<<<<   in add_routes   >>>>>>>>>>>>>>>>")
	if app.debug:
		secure_scheme = 'http'
	for r in _routes:
		app.router.add(r)