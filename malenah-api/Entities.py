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
    #license_number = ndb.StringProperty(required=True)
    specializations = ndb.StringProperty(repeated=True)
    phone = ndb.StringProperty(repeated=True)
    email = ndb.StringProperty()
    website = ndb.StringProperty()
    accepting_new_patients = ndb.BooleanProperty()

class Review(Model):
    username = ndb.StringProperty(required=True)
    rating = ndb.StringProperty(required=True)
    comment = ndb.StringProperty()
    replies = ndb.KeyProperty(repeated=True)
    #user_key = ndb.KeyProperty(kind=User, required=True)
    provider_key = ndb.KeyProperty(kind=Provider, required=True)

class Review(Model):
    username = ndb.StringProperty(required=True)
    rating = ndb.StringProperty(required=True)
    comment = ndb.StringProperty()
    replies = ndb.KeyProperty(repeated=True)
    #user_key = ndb.KeyProperty(kind=User, required=True)
    provider_key = ndb.KeyProperty(kind=Provider, required=True)

class Specialization(Model):
    name = ndb.StringProperty(required=True)