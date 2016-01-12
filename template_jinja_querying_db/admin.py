import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs
import logging_def as console

class Admin(base_page.BaseHandler):
    def __init__(self,request,response): #overwrite init
        self.initialize(request,response)
        self.template_values = {} #ensure we start with empty dictionary(cleaner than putting code in both get and post methods)

    def render(self,page): #override render
        #python list comprehension
        self.template_values['classes']=[{'name':x.name,'key':x.key.urlsafe()} for x in db_defs.ChannelClass.query(ancestor=ndb.Key(db_defs.ChannelClass, self.app.config.get('default-group'))).fetch()]
        console.log(self.template_values['classes'])
        #db_defs.Channel.query().fetch() gets a list of all channels stored in db
        #for each x in channels, we want to create a dict with name associated with the channel and a key
        #associated with a url safe string of the key (turns the key, a string that includes info about the class and its
        #identifier and turns it into something we can pass to a website without being mangled by html encoding
        #the outer [ ] makes the entire thing into a list
        #thus, we get a list of dictionaries {'name':x.name,'key':x.key.urlsafe()} of all channels
        #[{'name':x.name,'key':x.key.urlsafe()},{'name':x.name,'key':x.key.urlsafe()},{'name':x.name,'key':x.key.urlsafe()} etc]
        #which is assigned to channels
        self.template_values['channels']=[{'name':x.name,'key':x.key.urlsafe()} for x in db_defs.Channel.query(ancestor=ndb.Key(db_defs.Channel, self.app.config.get('default-group'))).fetch()]
        #db_defs.Channel.query().fetch() gets a list of all channels stored in db
        base_page.BaseHandler.render(self, page, self.template_values)

    def get(self):
        self.render('admin.html') #call the overridden render (above)

    def post(self):
        action = self.request.get('action')
        if action == 'add_channel':
            #parent group for all channels is default-group
            k = ndb.Key(db_defs.Channel, self.app.config.get('default-group'))
            chan = db_defs.Channel(parent=k)
            chan.name = self.request.get('channel-name')
            #construct a key from a url safe string for every checkbox that was checked in the form
            #classes[] just denotes the group of classes that was checked
            #turn all of those checked classes into a list of keys (list comprehensions basically append to lists quickly)
            #recall from deb_defs.py that the Channel's classes property = ndb.KeyProperty(repeated=True) is repeated,
            #so it takes a list of keys
            chan.classes = [ndb.Key(urlsafe=x) for x in self.request.get_all('classes[]')]
            chan.active = True
            chan.put() #save the channel
            self.template_values['message'] = 'Added channel '+chan.name+' to the database.'
        elif action=='add_class':
            k=ndb.Key(db_defs.ChannelClass, self.app.config.get('default-group'))
            c=db_defs.ChannelClass(parent=k)
            c.name=self.request.get('class-name')
            c.put()
            #overwrites the message value in the template_values dictionary
            self.template_values['message'] = 'Added class '+c.name+' to the database.'
        else:
            self.template_values['message'] = 'Action '+action+' is unknown.'
        console.log([{'name':x.name,'key':x.key.urlsafe()} for x in db_defs.ChannelClass.query(ancestor=ndb.Key(db_defs.Channel, self.app.config.get('default-group'))).fetch()])
        self.render('admin.html')
