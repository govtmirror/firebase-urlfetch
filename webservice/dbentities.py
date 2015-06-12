from google.appengine.ext import ndb

class Arbmonth(ndb.Expando): 
	arbmonthID = ndb.StringProperty()
	caseID = ndb.StringProperty()

class CaseX(ndb.Expando):
	cfno = ndb.StringProperty()
	arbit = ndb.StringProperty()
	stat = ndb.StringProperty()
	dateAssign = ndb.StringProperty()

class Obligation(ndb.Expando):
	cfno = ndb.StringProperty()
	arbit = ndb.StringProperty()
	BFSitem = ndb.StringProperty()
	action = ndb.StringProperty()
	stamp = ndb.StringProperty()
	

