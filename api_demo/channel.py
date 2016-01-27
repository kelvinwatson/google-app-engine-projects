import webapp2
from google.appengine.ext import ndb
import db_models
import json

class Channel(webapp2.RequestHandler):
    def post(self):
        """Creates a Channel entity

        POST Body Variables:
        name - Required. Channel name
        mods[] = Array of Mod ids
        topics[] = Array of channel topics """
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = 'Not acceptable. API only supports application/json MIME type'
            return
        new_channel = db_models.Channel()
        name = self.request.get('name',default_value=None)
        mods = self.request.get_all('mods[]', default_value=None)
        topics = self.request.get_all('topics[]', default_value=None)
        if name: new_channel.name = name
        else:
            self.response.status = 400
            self.response.status_message = "Invalid request"
        if mods:
            for mod in mods:
                new_channel.mods.append(ndb.Key(db_models.Mod, int(mod)))
        if topics: new_channel.topics = topics
        for topic in new_channel.topics: print topic
        key=new_channel.put()
        out=new_channel.to_dict()
        self.response.write(json.dumps(out))
        return

class ChannelMods(webapp2.RequestHandler):
    def put(self, **kwargs): #modify a channel by adding a mod to it
        self.response.write("HERE!")
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = "Not acceptable. API only supports application/json MIME type"
        if 'cid' in kwargs:
            channel = ndb.Key(db_models.Channel, int(kwargs['cid'])).get() #construct key using the provided cid, and get the entity from the datastore
            if not channel: #if get() was unable to retrieve a channel with the cid
                self.response.status = 404
                self.response.status_message = "Channel not found"
                return
        if 'mid' in kwargs:
            mod = ndb.Key(db_models.Mod, int(kwargs['mid']))#construct key using the provided cid, and get the entity from the datastore
            if not mod:
                self.response.status = 404
                self.response.status_message = "Mod not found"
                return
        if mod not in channel.mods:
            self.response.write(mod)
            channel.put()
        self.response.write(json.dumps(channel.to_dict())) #to_dict() overridden to convert entity to dictionary AND include the key.id of the entity
        return
