from google.appengine.ext import ndb

class Message(ndb.Model):
    channel = ndb.StringProperty(required=True)
    date_time = ndb.DateTimeProperty(required=True)
    count = ndb.IntegerProperty(required=True)

#Channel class is a subclass of ndb.Model (Channel extends ndb.Model)
class Channel(ndb.Model):
    name = ndb.StringProperty(required=True)
    classes = ndb.KeyProperty(repeated=True)
    active = ndb.BooleanProperty(required=True)

class ChannelClass(ndb.Model):
    name = ndb.StringProperty(required=True)
