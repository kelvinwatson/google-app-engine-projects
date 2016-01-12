from google.appengine.ext import ndb

class Provider(ndb.Model):
    first_name = ndb.StringProperty(required=True)
    last_name =  ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    email =  ndb.StringProperty(required=True)
    website =  ndb.StringProperty()
    best_time = ndb.TimeProperty()
    designation = ndb.StringProperty()
    services = ndb.KeyProperty(repeated=True)
    accept_new_patients = ndb.BooleanProperty(required=True)

class Designation(ndb.Model):
    name = ndb.StringProperty(required=True)

class Service(ndb.Model):
    name = ndb.StringProperty(required=True)
