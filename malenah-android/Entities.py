from google.appengine.ext import ndb

class Model(ndb.Model):
    def to_dict(self):
        """Overridden  method to convert entity to Python dictionary"""
        d = super(Model, self).to_dict()
        d['key'] = self.key.id()
        return d

class User(Model):
    """NDB Model for User entity"""
    user_id = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    name  = ndb.StringProperty()
    favorites = ndb.KeyProperty(repeated=True)

class Provider(Model):
    """NDB Model for Provider entity"""
    category = ndb.StringProperty(required=True)
    icon_url = ndb.StringProperty()
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    designation = ndb.StringProperty(required=True)
    specializations = ndb.KeyProperty(repeated=True)
    organization = ndb.StringProperty()
    building = ndb.StringProperty()
    street = ndb.StringProperty()
    city = ndb.StringProperty()
    state = ndb.StringProperty()
    country = ndb.StringProperty()
    zipcode = ndb.StringProperty()
    notes = ndb.StringProperty()
    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()
    phone = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    website = ndb.StringProperty()
    accepting_new_patients = ndb.BooleanProperty()

class Review(Model):
    """NDB Model for Review entity"""
    username = ndb.StringProperty(required=True)
    rating = ndb.FloatProperty(required=True)
    comment = ndb.StringProperty()
    replies = ndb.KeyProperty(repeated=True)
    provider = ndb.KeyProperty(kind=Provider, required=True)

class Reply(Model):
    """NDB Model for Reply entity"""
    username = ndb.StringProperty(required=True)
    comment = ndb.StringProperty()
    review = ndb.KeyProperty(kind=Review, required=True)
    provider = ndb.KeyProperty(kind=Provider, required=True)

class Specialization(Model):
    """NDB Model for Specialization entity"""
    name = ndb.StringProperty(required=True)

class Category(Model):
    """NDB Model for Category entity"""
    name = ndb.StringProperty(required=True)
