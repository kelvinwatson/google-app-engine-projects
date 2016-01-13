import base
import entities as Entity
import log as console
from datetime import datetime
from google.appengine.ext import ndb

class ViewHandler(base.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request,response)
        self.template_values = {
            'title': "Record Added (MALENAH Administrator Portal)",
            'header_title': "Record Added",
            'last_accessed': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
            'all_providers': self.get_all_providers(),
            'all_designations': self.get_all_designations(),
            'all_services':self.get_all_services()
            }

    def get(self):
        t = {}
        t['type'] = self.request.get('type')
        self.template_values['record_type'] = t
        k = ndb.Key(urlsafe=self.request.get('key')) #get key string and construct key
        e = k.get()
        if t['type']=='healthcare_provider':
            t['name']='Healthcare Provider'
            self.template_values['first_name'] = e.first_name #set template values
            self.template_values['last_name'] = e.last_name
            self.template_values['phone'] = e.phone
            self.template_values['email'] = e.email
            self.template_values['website'] = e.website
            self.template_values['best_time'] = e.best_time.strftime("%H:%M")
            console.log(e.best_time.strftime("%H:%M"))
            self.template_values['designation'] = ndb.Key(urlsafe=e.designation).get().name             #e.designation == key, use .get() to get entity, and .name to get the entity's name property
            self.template_values['my_services'] = [{'name':k.get().name} for k in e.services] #k is a key!
        elif t['type']=='designation':
            t['name']='Designation'
            self.template_values['designation'] = e.name
        elif t['type']=='service':
            t['name']='Service'
            self.template_values['service'] = e.name
        else:
            console.log("wrong type")
        base.BaseHandler.render(self, 'view.html', self.template_values) #call the overridden render (above)
