import webapp2
from webapp2_extras import json
import logging
from google.appengine.api import datastore
from google.appengine.ext import ndb
from dbentities import *
from nmbauthenticator import *
from datetime import datetime



@nmbauthjson
def searchfunc(
              opencases=False,
              closedcases=False,
              arbit='',
              fromdate='',
              todate='',
              fetchoffset=500): # (permission='ADMIN'):

  qry1 = CaseX.query()
  if opencases and closedcases:
    qry2 = qry1
  elif closedcases:
    qry2 = qry1.filter(CaseX.stat == 'Closed')
  else:
    qry2 = qry1.filter(CaseX.stat == 'Open')

  if arbit != '':
    qry3 = qry2.filter(CaseX.arbit == arbit)
  else:
    qry3 = qry2



  results = qry3.fetch(500, offset=fetchoffset)
  resultlist = []
  for result1 in results:
    result = result1.to_dict()
    resultlist.append(result)


  logging.info("number of cases = " + str(len(resultlist)))
  rsp = { 
    'rsp' : 'OK',
    'handler' : 'ArbcaseHandler',
    'arbcases' : resultlist,
    'msg' : 'you are allowed to access this handler'
  }
  return rsp

class ArbcaseHandler(webapp2.RequestHandler):
  def post(self):
    logging.info("<<<<<<<<   GET, in ArbcaseHandler   >>>>>>>>")
    #  get the inputs, maybe validate later
    request_body_dict = json.decode(self.request.body)
    opencases = request_body_dict.get('open')
    closedcases = request_body_dict.get('closed')
    arbit = request_body_dict.get('arbit')
    fromdate = request_body_dict.get('fromdate')
    todate = request_body_dict.get('todate')
    fetchoffset = request_body_dict.get('fetchoffset')
  
    rspObj = searchfunc(
                        opencases=opencases,
                        closedcases=closedcases,
                        arbit=arbit,
                        fromdate=fromdate,
                        todate=todate,
                        fetchoffset=fetchoffset) #(permission='arb')
    # assemble and send the response
    self.response.content_type = 'application/json'
    self.response.write(json.encode(rspObj))