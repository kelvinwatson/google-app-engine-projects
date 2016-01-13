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
            'all_providers': self.get_all_providers(),
            'all_designations': self.get_all_designations(),
            'all_services':self.get_all_services(),
            }

    def get(self):
        self.render('admin.html', self.template_values) #call the overridden render (above)

    def post(self):
        action = self.request.get('action')
        if action=='add_provider':
            k = ndb.Key(Entity.Provider, self.app.config.get('malenah-providers')) #create key
            provider = Entity.Provider(parent=k)
            provider.first_name = self.request.get('first_name')
            provider.last_name = self.request.get('last_name')
            provider.phone = self.request.get('phone')
            provider.email = self.request.get('email')
            provider.website = self.request.get('website')
            provider.best_time = datetime.strptime(self.request.get('best_time'), "%H:%M").time()
            provider.designation = self.request.get('designation') #self.request.get('designation') is a urlsafe KEY
            provider.services = [ndb.Key(urlsafe=x) for x in self.request.get_all('services[]')]
            provider.accept_new_patients = True if (self.request.get('accept-new-patients') == "True") else False
            new_key = provider.put()
            record_type = 'healthcare_provider'
            self.template_values['post_result'] = 'Healthcare Provider '+provider.first_name+' '+provider.last_name+' successfully added'
        elif action=='add_designation':
            new_key = self.record_designation()
            designation = self.request.get('designation')
            self.template_values['post_result'] = 'Designation "'+designation+'" successfully added'
            record_type = 'designation'
        elif action=='add_service':
            new_key = self.record_service()
            service = self.request.get('service')
            self.template_values['post_result'] = service+' service successfully added'
            record_type = 'service'
        else:
            self.template_values['post_result'] = 'Unknown action'
        self.redirect('/view?key='+ new_key.urlsafe()+ '&type='+record_type)

    def record_designation(self):
        k = ndb.Key(Entity.Designation, self.app.config.get('malenah-providers'))
        designation = Entity.Designation(parent=k)
        designation.name = self.request.get('designation')
        return designation.put()

    def record_service(self):
        k=ndb.Key(Entity.Service, self.app.config.get('malenah-providers')) #create a Service key
        console.log(k)
        service=Entity.Service(parent=k) #create an entity with parent as the malenah-providers group key
        service.name = self.request.get('service')
        console.log('SERV='+service.name)
        return service.put()
