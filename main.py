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
				taskurl = "/writemail"
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

		url3 = os.environ['FIREBASE_DB'] + "/users/" + myarbuid + "/arbmonths/" + myarbMonthID + ".json"
		amResult = urlfetch.fetch(url3)
		am = amResult.content
		# logging.info("??????????   " + am)
		amDict = json.decode(am)
		

		url999 = os.environ['FIREBASE_DB'] + "/users/" + myarbuid + "/assignments.json"
		assignmentResult = urlfetch.fetch(url999)
		assignments = assignmentResult.content
		# logging.info("ZZZZZZZZZ  1 " + assignments)
		assignmentsDict = json.decode(assignments)
		assignmentsKeys = assignmentsDict.keys()
		writeArray = []
		hearArray = []
		for a in assignmentsKeys:
			# logging.info("one more key, " + a)
			# logging.info("hearsched, " + str(assignmentsDict[a]))
			if 'hearsched' in assignmentsDict[a]:
				if myarbMonthID == assignmentsDict[a]['hearsched']:
					if 'tripID' in assignmentsDict[a]:
						thistripID = assignmentsDict[a]['tripID']
					else:
						thistripID = "no trip"
					if 'heard' in assignmentsDict[a]:
						thisheard = assignmentsDict[a]['heard']
					else:
						thisheard = "n/a"
					if 'hfee' in assignmentsDict[a]:
						thishfee = assignmentsDict[a]['hfee']
					else:
						thishfee = "30"
					if 'notheard' in assignmentsDict[a]:
						thisnotheard = assignmentsDict[a]['notheard']
					else:
						thisnotheard = " - "

					# logging.info("more hearsched, " + assignmentsDict[a]['hearsched'])
					hearArray.append({
						"caseID":assignmentsDict[a]['caseID'],
						"dateAssigned":assignmentsDict[a]['dateAssigned'],
						"notheard":thisnotheard,
						"tripID":thistripID,
						"heard":thisheard,
						"hfee":thishfee
					})
			else:
				logging.info("no hearsched, " + assignmentsDict[a]['caseID'])
			if 'writesched' in assignmentsDict[a]:
				if myarbMonthID == assignmentsDict[a]['writesched']:
					if 'written' in assignmentsDict[a]:
						thiswritten = assignmentsDict[a]['written']
					else:
						thiswritten = "n/a"
					if 'fee' in assignmentsDict[a]:
						thisfee = assignmentsDict[a]['fee']
					else:
						thisfee = "30"
					if 'notwritten' in assignmentsDict[a]:
						thisnotwritten = assignmentsDict[a]['notwritten']
					else:
						thisnotwritten = " - "

					# logging.info("more hearsched, " + assignmentsDict[a]['hearsched'])
					writeArray.append({
						"caseID":assignmentsDict[a]['caseID'],
						"dateAssigned":assignmentsDict[a]['dateAssigned'],
						"notwritten":thisnotwritten,
						"written":thiswritten,
						"fee":thisfee
					})
			else:
				logging.info("no writesched, " + assignmentsDict[a]['caseID'])

		template_values = {
			'nameyo': user_name,
			'arbmonth': amDict,
			'hearings': hearArray,
			'writings': writeArray
		}

		logging.info("this is very important, " + str(hearArray))


		subject = mytype+ ", 3 " + mydata
		
		template_url = "email-templates/" + mytype 
		body = template.render(template_url, template_values)

		mail.send_mail(sender_address, user_address, subject, body)
		logging.info("i am leaving the reqappmailer")





app = webapp2.WSGIApplication(
	[
	('/', HomeHandler),
	('/mail', MailHandler),
	('/writemail', ReqAppMailer)
	],
	debug=True)
