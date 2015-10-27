import webapp2
from webapp2_extras import json
import logging
from google.appengine.api import datastore
from google.appengine.ext import ndb
from datetime import datetime
from google.appengine.api import urlfetch
import os
from google.appengine.api import mail
from google.appengine.api import taskqueue
# import json


class TestHandler(webapp2.RequestHandler):
	def get(self):
		logging.info("<<<<<<<<   GET, in TestHandler   >>>>>>>>")

		# user_address = "wagner@nmb.gov"

		# sender_address = """firebase-1012@appspot.gserviceaccount.com"""
		# subject = "Confirm your registration"
		# body = """
		# Thank you for creating an account! Please confirm your email address by
		# clicking on the link below"""
		# mail.send_mail(sender_address, user_address, subject, body)



		url = os.environ['FIREBASE_DB'] + "/email.json"
		result = urlfetch.fetch(url)
		logging.info("ZZqqZZZ   3 " + result.content)
		emailDict = json.decode(result.content)
		emailKeys = emailDict.keys()
		for a in emailKeys:
			logging.info("hello yo 3, " + emailDict[a]['type'])
			mydata = emailDict[a]['type']
			taskqueue.add(url='/worker', params={'key': a})



class TestMailer(webapp2.RequestHandler):
	def post(self):
		logging.info("i am in the testmailer")

		mydata = self.request.get('key')
		user_address = "wagner@nmb.gov"

		sender_address = """firebase-1012@appspot.gserviceaccount.com"""
		subject = "Confirm " + mydata
		body = """
		Thank you for creating an account! Please confirm your email address by
		clicking on the link below"""
		mail.send_mail(sender_address, user_address, subject, body)

		logging.info("i am leaving the testmailer")

class TestMailer2(webapp2.RequestHandler):
	def post(self):
		logging.info("i am in the testmailer")

		user_address = "wagner@nmb.gov"

		sender_address = "firebase-1012@appspot.gserviceaccount.com"
		subject = "Confirm it" 
		body = """
		Thank you for creating an account! Please confirm your email address by
		clicking on the link below"""
		mail.send_mail(sender_address, user_address, subject, body)

		logging.info("i am leaving the testmailer")