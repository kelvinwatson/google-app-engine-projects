import base
import entities as Entity
import log as console
from datetime import datetime
from google.appengine.ext import ndb

class ViewHandler(base.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request,response)
        console.log(datetime.now().time())
        self.get_all_providers()
        self.get_all_designations()
        self.get_all_services()
        self.template_values = {
            'title': "Record Added",
            'header_title': "Record Added",
            'last_accessed': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            #'all_providers':
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
            self.template_values['best_time'] = e.best_time
            self.template_values['designation'] = ndb.Key(urlsafe=e.designation).get().name             #e.designation == key, use .get() to get entity, and .name to get the entity's name property
            self.template_values['services'] = e.services #TODO: on view.html, just needs to display, not prepopulate with checks
        elif t['type']=='designation':
            t['name']='Designation'
            console.log("view added designation")
            self.template_values['designation'] = e.name
            console.log(self.template_values['designation'])
        elif t['type']=='services':
            t['name']='Service(s)'
            console.log("view added services")
        else:
            console.log("wrong type")
        console.log('type='+str(t))
        base.BaseHandler.render(self, 'view.html', self.template_values) #call the overridden render (above)

    def get_all_providers(self):
        console.log("\n==Retrieving all providers...==")
        all_providers = Entity.Provider.query(ancestor=ndb.Key(Entity.Provider,self.app.config.get('malenah-providers'))).fetch()
        for p in all_providers:
            console.log('\n   '+str(p))
        return all_providers
