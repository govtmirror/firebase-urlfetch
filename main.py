from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2
from webapp2_extras import json
import logging
from google.appengine.api import urlfetch
import os
from google.appengine.api import mail
from google.appengine.api import taskqueue
import urllib



"""handlers for client redirects"""
class HomeHandler(webapp2.RequestHandler):
	def get(self):
		INDEX_HTML = open('client.html').read()
		self.response.out.write(INDEX_HTML)

class TestHandler(webapp2.RequestHandler):
	def get(self):
		logging.info("<<<<<<<<   GET, in TestHandler   >>>>>>>>")
		url = os.environ['FIREBASE_DB'] + "/email.json"
		result = urlfetch.fetch(url)
		logging.info("ZZqqZZZ   3 " + result.content)
		emailDict = json.decode(result.content)
		emailKeys = emailDict.keys()
		for a in emailKeys:
			logging.info("hello yo 3, " + emailDict[a]['type'])
			mydata = emailDict[a]['type']
			taskqueue.add(url='/worker', params={'key': a})

			params = '{"pending": "false","whatever": "no"}'
			# putData = urllib.urlencode(params)
			url2 = os.environ['FIREBASE_DB'] + "/email/" + a + "/.json"
			result = urlfetch.fetch(url=url2,
				payload=params,
				method=urlfetch.PATCH)
			logging.info("post result = " + str(result.status_code))

class TestMailer(webapp2.RequestHandler):
	def post(self):
		logging.info("i am in the testmailer")
		mydata = self.request.get('key')
		user_address = "wagner@nmb.gov"
		sender_address = "montague@nmb.gov"
		subject = "Confirm " + mydata
		body = """Thank you for creating an account! Please confirm your email address by clicking on the link below"""
		mail.send_mail(sender_address, user_address, subject, body)
		logging.info("i am leaving the testmailer")

class TestMailer2(webapp2.RequestHandler):
	def post(self):
		logging.info("i am in the testmailer2")
		user_address = "wagner@nmb.gov"
		sender_address = "firebase-1012@appspot.gserviceaccount.com"
		subject = "Confirm it" 
		body = """Thank you for creating an account! Please confirm your email address byclicking on the link below"""
		mail.send_mail(sender_address, user_address, subject, body)
		logging.info("i am leaving the testmailer2")


app = webapp2.WSGIApplication(
	[
	('/', HomeHandler),
	('/mail', TestHandler),
	('/worker', TestMailer),
	('/wtf', TestMailer2)
	],
	debug=True)
