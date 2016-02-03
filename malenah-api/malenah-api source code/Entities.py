from google.appengine.ext import ndb

class Model(ndb.Model):
    def to_dict(self):#override to_dict() method
        d = super(Model, self).to_dict() #call the super(original) version of to_dict(), which doesn't include the key
        d['key'] = self.key.id() #and add the key by pulling out its id
        return d

class Provider(Model):
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    designation = ndb.StringProperty(required=True)
    organization = ndb.StringProperty()
    specializations = ndb.KeyProperty(repeated=True)
    phone = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    website = ndb.StringProperty()
    accepting_new_patients = ndb.BooleanProperty()

class Review(Model):
    username = ndb.StringProperty(required=True)
    rating = ndb.FloatProperty(required=True)
    comment = ndb.StringProperty()
    replies = ndb.KeyProperty(repeated=True)
    provider = ndb.KeyProperty(kind=Provider, required=True)

class Reply(Model):
    username = ndb.StringProperty(required=True)
    comment = ndb.StringProperty()
    review = ndb.KeyProperty(kind=Review, required=True)
    provider = ndb.KeyProperty(kind=Provider, required=True)

class Specialization(Model):
    name = ndb.StringProperty(required=True)
