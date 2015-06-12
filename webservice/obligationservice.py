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
              arbit='',
              cfno='',
              yoaction='',
              bfsitem='',
              fromdate='',
              todate='',
              fetchoffset=500):
  qry1 = Obligation.query()
  if arbit != '':
    qry2 = qry1.filter(Obligation.arbit == arbit)
  else:
    qry2 = qry1
    logging.info("at qry2")
  if cfno != '':
    qry3 = qry2.filter(Obligation.cfno == cfno)
  else:
    qry3 = qry2
    logging.info("at qry3")
  if yoaction != '':
    qry4 = qry3.filter(Obligation.action == yoaction)
  else:
    qry4 = qry3
    logging.info("at qry4")
  if bfsitem != '':
    qry5 = qry4.filter(Obligation.BFSitem == bfsitem)
  else:
    qry5 = qry4
    logging.info("at qry5")

  if fromdate != '0':
    logging.info("at 6 " + fromdate)
    qry6 = qry5.filter(Obligation.stamp >= fromdate)
  else:
    qry6 = qry5
  if todate != '0':
    logging.info("at 7 " + todate)
    qry7 = qry6.filter(Obligation.stamp < todate)
  else:
    qry7 = qry6

  results = qry7.fetch(500, offset=fetchoffset)
  resultlist = []
  for result1 in results:
    result = result1.to_dict()
    resultlist.append(result)
  logging.info("number of cases = " + str(len(resultlist)))
  rsp = { 
    'rsp' : 'OK',
    'handler' : 'BfsentriesHandler',
    'bfsentries' : resultlist,
    'msg' : 'you are allowed to access this handler'
  }
  return rsp

class BfsentriesHandler(webapp2.RequestHandler):
  def post(self):
    logging.info("<<<<<<<<   GET, in BfsentriesHandler   >>>>>>>>")
    #  get the inputs, maybe validate later
    request_body_dict = json.decode(self.request.body)
    arbit = request_body_dict.get('arbit')
    cfno = request_body_dict.get('cfno')
    yoaction = request_body_dict.get('yoaction')
    bfsitem = request_body_dict.get('bfsitem')
    fromdate = request_body_dict.get('fromdate')
    todate = request_body_dict.get('todate')
    fetchoffset = request_body_dict.get('fetchoffset')
  
    rspObj = searchfunc(
                        arbit=arbit,
                        cfno=cfno,
                        yoaction=yoaction,
                        bfsitem=bfsitem,
                        fromdate=fromdate,
                        todate=todate,
                        fetchoffset=fetchoffset) #(permission='arb')

    # assemble and send the response
    self.response.content_type = 'application/json'
    self.response.write(json.encode(rspObj))


@nmbauthjson
def modifyBfsitem(bfsitem='',items=[]):
  myrsp = {"rsp": "ok", "msg": "that is the way we roll"}
  test = len(items)
  logging.info("test = " + str(test) + "  " + str(items))
  try:
    for item in items:
      logging.info("in the modifyGfsitem method 1 " + str(item))
      qry1 = Obligation.query()
      qry2 = qry1.filter(Obligation.cfno == item['cfno'])
      qry3 = qry2.filter(Obligation.stamp == item['stamp'])
      result = qry3.get()
      if result:
        result.BFSitem = bfsitem
        result.put()
  except:
    logging.info
    myrsp = {"rsp": "fail", "msg": "database error"}
  return myrsp


class BfspostHandler(webapp2.RequestHandler):
  def post(self):
    logging.info("i am in the post method of BfsentriesHandler")
    request_body_dict = json.decode(self.request.body)
    bfsitem = request_body_dict.get('bfsitem')
    items = request_body_dict.get('items')


    rspObj = modifyBfsitem(
                           bfsitem=bfsitem,
                           items=items) #(permission='arb')

    self.response.content_type = 'application/json'
    self.response.write(json.encode(rspObj))



@nmbauthhtml
def csvfunc(
              arbit='',
              cfno='',
              yoaction='',
              bfsitem='',
              fromdate='',
              todate='',
              fetchoffset=500):
  qry1 = Obligation.query()
  if arbit != '':
    qry2 = qry1.filter(Obligation.arbit == arbit)
  else:
    qry2 = qry1
    logging.info("at qry2")
  if cfno != '':
    qry3 = qry2.filter(Obligation.cfno == cfno)
  else:
    qry3 = qry2
    logging.info("at qry3")
  if yoaction != '':
    qry4 = qry3.filter(Obligation.action == yoaction)
  else:
    qry4 = qry3
    logging.info("at qry4")
  if bfsitem != '':
    qry5 = qry4.filter(Obligation.BFSitem == bfsitem)
  else:
    qry5 = qry4
    logging.info("at qry5")

  if fromdate != '0':
    logging.info("at 6 " + fromdate)
    qry6 = qry5.filter(Obligation.stamp >= fromdate)
  else:
    qry6 = qry5
  if todate != '0':
    logging.info("at 7 " + todate)
    qry7 = qry6.filter(Obligation.stamp < todate)
  else:
    qry7 = qry6

  results = qry7.fetch()
  resultStr = "cfno,bfsitem,arbitrator,action,amount,userID,stamp,\n\r"

  for result1 in results:
    if isinstance(result1.stamp, int):
      k = str(result1.stamp)
    else:
      k = result1.stamp

    resultStr = resultStr + "\"" + str(result1.cfno) + "\",\"" + str(result1.BFSitem) + "\",\"" + str(result1.arbit) + "\",\"" + str(result1.action) + "\",\"" + str(result1.obligation) + "\",\"" + str(result1.userID) + "\",\"" + str(k) + "\",\r"
  return resultStr


  # for result1 in results:
  #   try:
  #     k = datetime.fromtimestamp(int(result1.stamp)/1000)
  #   except:
  #     logging.info("bad date for " + result1.cfno)
  #     k = "no date"
  #   resultStr = resultStr + "\"" + str(result1.cfno) + "\",\"" + str(result1.BFSitem) + "\",\"" + str(result1.arbit) + "\",\"" + str(result1.action) + "\",\"" + str(result1.obligation) + "\",\"" + str(result1.userID) + "\",\"" + str(k) + "\",\r"
  # return resultStr

class BfscsvHandler(webapp2.RequestHandler):
  def post(self):
    logging.info("<<<<<<<<   GET, in BfscsvHandler   >>>>>>>>")
    #  get the inputs, maybe validate later
    request_body_dict = json.decode(self.request.body)
    arbit = request_body_dict.get('arbit')
    cfno = request_body_dict.get('cfno')
    yoaction = request_body_dict.get('yoaction')
    bfsitem = request_body_dict.get('bfsitem')
    fromdate = request_body_dict.get('fromdate')
    todate = request_body_dict.get('todate')
    fetchoffset = request_body_dict.get('fetchoffset')
  
    rsp = csvfunc(
                        arbit=arbit,
                        cfno=cfno,
                        yoaction=yoaction,
                        bfsitem=bfsitem,
                        fromdate=fromdate,
                        todate=todate,
                        fetchoffset=fetchoffset) #(permission='arb')

    # assemble and send the response
    self.response.content_type = 'application/csv'
    self.response.write(rsp)