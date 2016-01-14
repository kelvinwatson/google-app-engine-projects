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
            'header_title': "Record "+ self.request.get('action_done'),
            'last_accessed': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
            'all_providers': self.get_all_providers(),
            'all_designations': self.get_all_designations(),
            'all_services':self.get_all_services(),
            'action_done':self.request.get('action_done'),
            }

    def get(self):
        if self.request.get('key') and self.request.get('type') and self.request.get('action_done'):
            t = {}
            t['type'] = self.request.get('type')
            self.template_values['record_type'] = t
            if self.request.get('key'):
                try:
                    k = ndb.Key(urlsafe=self.request.get('key')) #get key string and construct key
                    e = k.get()
                except (TypeError, AttributeError) as ex:
                    k = e = None
                    self.redirect('/admin')
                if t['type']=='healthcare_provider':
                    t['name']='Healthcare Provider'
                    self.template_values['first_name'] = e.first_name #set template values
                    self.template_values['last_name'] = e.last_name
                    self.template_values['phone'] = e.phone
                    self.template_values['email'] = e.email
                    self.template_values['website'] = e.website
                    self.template_values['best_time'] = e.best_time.strftime("%H:%M")
                    #console.log(e.best_time.strftime("%H:%M"))
                    if e.designation is None or e.designation=='' or ndb.Key(urlsafe=e.designation).get() is None:
                        console.log('empty designation!')#(ndb.Key(urlsafe=e.designation).get().name)
                        self.template_values['designation'] = ''             #e.designation == key, use .get() to get entity, and .name to get the entity's name property
                    else:
                        self.template_values['designation'] = ndb.Key(urlsafe=e.designation).get().name             #e.designation == key, use .get() to get entity, and .name to get the entity's name property
                    try:
                        self.template_values['my_services'] = [{'name':k.get().name} for k in e.services]
                    except (TypeError,AttributeError) as ex:
                        self.template_values['my_services'] = None #k is a key!
                    self.template_values['accept_new_patients'] = e.accept_new_patients
                elif t['type']=='designation':
                    t['name']='Designation'
                    self.template_values['designation'] = e.name
                elif t['type']=='service':
                    t['name']='Service'
                    self.template_values['service'] = e.name
                else:
                    console.log("wrong type")
                self.template_values['all_providers'] =  self.get_all_providers()
                self.template_values['all_designations'] = self.get_all_designations()
                self.template_values['all_services'] =  self.get_all_services()
                base.BaseHandler.render(self, 'view.html', self.template_values) #call the overridden render (above)
        else:
            console.log("redirect GET!")
            self.redirect('/admin')
            return

    def post(self):
        if self.request.get('key') and self.request.get('type') and self.request.get('action_done'):
            t = {}
            t['type'] = self.request.get('type')
            self.template_values['record_type'] = t
            self.template_values['action_done'] = self.request.get('action_done')
            if t['type']=='healthcare_provider':
                t['name']='Healthcare Provider'
                k = ndb.Key(urlsafe=self.request.get('key')) #get key string and construct key
                e = k.get() #e is still the old entity
                #update the entity
                e.first_name = self.template_values['first_name'] = self.request.get('first_name')
                e.last_name = self.template_values['last_name'] = self.request.get('last_name')
                e.phone = self.template_values['phone'] = self.request.get('phone')
                e.email = self.template_values['email'] = self.request.get('email')
                e.website = self.template_values['website'] = self.request.get('website')
                e.best_time = datetime.strptime(self.request.get('best_time'), "%H:%M").time()
                self.template_values['best_time'] = e.best_time.strftime("%I:%M %p")
                e.designation = self.request.get('designation')
                self.template_values['my_services'] = [{'name':k.get().name} for k in e.services] #k is a key!

                if e.designation is None or e.designation=='':
                    console.log('empty designation!')#(ndb.Key(urlsafe=e.designation).get().name)
                    self.template_values['designation'] = ''             #e.designation == key, use .get() to get entity, and .name to get the entity's name property
                else:
                    self.template_values['designation'] = ndb.Key(urlsafe=e.designation).get().name
                e.services = [ndb.Key(urlsafe=k) for k in self.request.get_all('services[]')]
                e.accept_new_patients = True if (self.request.get('accept_new_patients')=="True") else False
                console.log('recording='+str(e.accept_new_patients))
                e.put()
            elif t['type']=='designation':
                t['name']='Designation'
                self.template_values['designation'] = e.name
            elif t['type']=='service':
                t['name']='Service'
                self.template_values['service'] = e.name
            else:
                console.log("wrong type")
            console.log('performing retrieval again in POST')
            self.template_values['all_providers'] =  self.get_all_providers()
            self.template_values['all_designations'] = self.get_all_designations()
            self.template_values['all_services'] =  self.get_all_services()
            base.BaseHandler.render(self, 'view.html', self.template_values) #call the overridden render (above)
        else:
            self.redirect('/admin')
            return
