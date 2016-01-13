import base
import log as console
import entities as Entity
import time
from datetime import datetime
from google.appengine.ext import ndb

class AdminHandler(base.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request,response)

        #console.log(datetime.now().time())
        self.template_values = {
            'title': "MALENAH Administrator Portal",
            'header_title': "Welcome to the M.A.L.E.N.A.H. Administrator Portal",
            'last_accessed': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
            'designations': self.get_all_designations(),
            }

    def get(self):
        self.render('admin.html', self.template_values) #call the overridden render (above)

    def post(self):
        action = self.request.get('action')
        if action=='add_provider':
            k = ndb.Key(Entity.Provider, self.app.config.get('malenah-providers')) #create key
            console.log(k)
            provider = Entity.Provider(parent=k)
            console.log(provider)
            provider.first_name = self.request.get('first_name')
            provider.last_name = self.request.get('last_name')
            provider.phone = self.request.get('phone')
            provider.email = self.request.get('email')
            provider.website = self.request.get('website')
            provider.best_time = datetime.strptime(self.request.get('best_time'), "%H:%M").time()
            #console.log(provider.best_time)
            provider.designation = self.request.get('designation')
            provider.services = [ndb.Key(urlsafe=x) for x in self.request.get_all('services[]')]
            #console.log(self.request.get('accept_new_patients'))
            provider.accept_new_patients = True if (self.request.get('accept-new-patients') == "True") else False
            console.log(provider.accept_new_patients)
            new_key = provider.put()
            record_type = 'healthcare_provider'
            self.template_values['post_result'] = 'Provider '+provider.first_name+' '+provider.last_name+' successfully added'
        elif action=='add_designation':
            new_key = self.record_designation()
            designation = self.request.get('designation')
            self.template_values['post_result'] = 'Designation "'+designation+'" successfully added'
            record_type = 'designation'
        elif action=='add_services':
            service = self.request.get('service')
            self.template_values['post_result'] = service+' service successfully added'
            record_type = 'service'
        else:
            self.template_values['post_result'] = 'Unknown action'
        self.redirect('/view?key='+ new_key.urlsafe()+ '&type='+record_type)

    def record_designation(self):
        k = ndb.Key(Entity.Designation, self.app.config.get('malenah-providers'))
        console.log(k)
        designation = Entity.Designation(parent=k)
        console.log(designation)
        designation.name = self.request.get('designation')
        console.log(designation.name)
        return designation.put()

'''

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
            chan.icon = icon_key
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
'''
