from google.appengine.api import users
from google.appengine.api import datastore
from google.appengine.ext import ndb
import logging


class UserRole(ndb.Expando): 
	role = ndb.StringProperty()
	user = ndb.StringProperty()

def isOK(criteria):
	permlist = criteria.split()	
	rolelist = []

	user = users.get_current_user()

	# if user:
	# 	# self.redirect("static/index.html")
	try:
		useremail = user.email()
	except:
		useremail = "pubic2"
	# else:
	# 	self.redirect(users.create_login_url(self.request.uri))

	logging.info("<<<<<<<  user is " + useremail + "  >>>>>>>")

	userroleQry = UserRole.query(UserRole.user == useremail)
	userroles = userroleQry.fetch()
	logging.info("<<<<<<<<<<<  number of roles = " + str(len(userroles)) + "   >>>>>>>>>>")


	for userrole in userroles:
		rolelist.append(userrole.role)
		 

	# rolelist = ['ADMIN','FRIEND','NMB']

	result = False
	for p in permlist:
		if p in rolelist:
			result = True
	return result






# The inner function must return function which will be executed
#  this example substitutes bad() for goodfunc if the result doen't match criteria
def nmbauthjson(func):
	def inner(*args, **kwargs):
		def bad(*args, **kwargs):
			return {'rsp':'bad','msg':'no-permission'}

		#  get the permission parameter from the function
		#  needs to be in the use of the decorated function
		if 'permission' in kwargs:
			criteria = kwargs.pop('permission')
		else:
			# default behavior
			return func(*args, **kwargs)
			# return bad(*args, **kwargs)


		if isOK(criteria):
			return func(*args, **kwargs)
		else:
			return bad(*args, **kwargs)
	return inner

def nmbauthhtml(func):
	def inner(*args, **kwargs):
		def bad(*args, **kwargs):
			return "<html><body><h2>Permissions Failure</h2><h3>Try to login properly!</h3></body></html>"

		#  get the permission parameter from the function
		#  needs to be in the use of the decorated function
		if 'permission' in kwargs:
			criteria = kwargs.pop('permission')
		else:
			# default behavior
			return func(*args, **kwargs)


		if isOK(criteria):
			return func(*args, **kwargs)
		else:
			return bad(*args, **kwargs)
	return inner

