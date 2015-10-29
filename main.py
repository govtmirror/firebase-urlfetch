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

class MailHandler(webapp2.RequestHandler):
	def get(self):
		logging.info("<<<<<<<<   GET, in TestHandler   >>>>>>>>")
		url = os.environ['FIREBASE_DB'] + "/email.json"
		result = urlfetch.fetch(url)
		# logging.info("ZZqqZZZ   3 " + result.content)
		emailDict = json.decode(result.content)
		emailKeys = emailDict.keys()
		for a in emailKeys:
			if emailDict[a]['pending'] == True:
				logging.info("hello yo 3, " + emailDict[a]['type'])
				yotype = emailDict[a]['type']
				yoarbmonthid = emailDict[a]['arbMonthID']
				yoarbuid = emailDict[a]['arbuid']
				yostamp = emailDict[a]['stamp']
				yoparams = {
					'arbMonthID': yoarbmonthid,
					'arbuid': yoarbuid,
					'stamp': yostamp,
					'type': yotype
				}
				taskurl = "/" + yotype
				taskqueue.add(url=taskurl, params=yoparams)
				params = '{"pending": false}'
				url2 = os.environ['FIREBASE_DB'] + "/email/" + a + "/.json"
				result = urlfetch.fetch(url=url2,
					payload=params,
					method=urlfetch.PATCH)
				logging.info("post result 2 = " + str(result.status_code))
			else:
				logging.info("not a pending email")

class ReqAppMailer(webapp2.RequestHandler):
	def post(self):
		logging.info("i am in the reqappmailer")
		mydata = self.request.get('stamp')
		mytype = self.request.get('type')
		myarbMonthID = self.request.get('arbMonthID')
		myarbuid = self.request.get('arbuid')
		# user_address = "wagner@nmb.gov"
		sender_address = "montague@nmb.gov"


		url9 = os.environ['FIREBASE_DB'] + "/users/" + myarbuid + "/correspondEmail.json"
		userResult = urlfetch.fetch(url9)
		user_address = userResult.content

		url99 = os.environ['FIREBASE_DB'] + "/users/" + myarbuid + "/name.json"
		userNameResult = urlfetch.fetch(url99)
		user_name = userNameResult.content
		

		url999 = os.environ['FIREBASE_DB'] + "/users/" + myarbuid + "/assignments.json"
		assignmentResult = urlfetch.fetch(url999)
		assignments = assignmentResult.content
		logging.info("ZZZZZZZZZ  1 " + assignments)
		assignmentsDict = json.decode(assignments)
		assignmentsKeys = assignmentsDict.keys()
		writeArray = []
		hearArray = []
		for a in assignmentsKeys:
			logging.info("one more key, " + a)
			logging.info("hearsched, " + str(assignmentsDict[a]))
			logging.info("more hearsched, " + assignmentsDict[a].hearsched)




		subject = mytype+ ", " + mydata
		template_values = {'nameyo': user_name}
		template_url = "email-templates/" + mytype 
		body = template.render(template_url, template_values)

		mail.send_mail(sender_address, user_address, subject, body)
		logging.info("i am leaving the reqappmailer")

class RptAppMailer(webapp2.RequestHandler):
	def post(self):
		logging.info("i am in the rptappmailer")
		mydata = self.request.get('stamp')
		mytype = self.request.get('type')
		user_address = "wagner@nmb.gov"
		sender_address = "montague@nmb.gov"
		subject = mytype+ ", " + mydata

		template_values = {'nameyo': 'Dean'}
		template_url = "email-templates/" + mytype 
		body = template.render(template_url, template_values)

		mail.send_mail(sender_address, user_address, subject, body)
		logging.info("i am leaving the rptappmailer")



app = webapp2.WSGIApplication(
	[
	('/', HomeHandler),
	('/mail', MailHandler),
	('/approve-request', ReqAppMailer),
	('/approved-report', RptAppMailer),
	],
	debug=True)
