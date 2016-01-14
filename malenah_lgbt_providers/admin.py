import base
import log as console
import entities as Entity
import time
from datetime import datetime
from google.appengine.ext import ndb

class AdminHandler(base.BaseHandler):
    """
    Administrator portal containing forms for addition(s) to database.
    """
    def __init__(self, request, response):
        self.initialize(request,response)
        self.curr_services =  self.get_all_services()
        self.curr_designations = self.get_all_designations()
        self.template_values = {
            'title': "MALENAH Administrator Portal",
            'header_title': "Welcome to the M.A.L.E.N.A.H. Administrator Portal",
            'last_accessed': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
            'all_providers': self.get_all_providers(),
            'all_designations': self.get_all_designations(),
            'all_services':self.get_all_services(),
            'error_messages': None,
            }

    def get(self):
        """
        Overrides parent get method. Renders admin.html template.
        """
        self.render('admin.html', self.template_values)

    def post(self):
        """
        Overrides parent post method, creates and stores provider entity into database.
        """
        action = self.request.get('action')
        if action=='add_provider':
            if self.validate_provider_form() is False:
                self.render('admin.html',self.template_values)
                return
            k = ndb.Key(Entity.Provider, self.app.config.get('malenah-providers')) #create key
            provider = Entity.Provider(parent=k)
            provider.first_name = self.request.get('first_name')
            provider.last_name = self.request.get('last_name')
            provider.phone = self.request.get('phone')
            provider.email = self.request.get('email')
            provider.website = self.request.get('website')
            provider.best_time = datetime.strptime(self.request.get('best_time'), "%H:%M").time()
            provider.designation = self.request.get('my_designation') #self.request.get('designation') is a urlsafe KEY
            provider.services = [ndb.Key(urlsafe=x) for x in self.request.get_all('services[]')]
            console.log("SOOOO?????")
            console.log(self.request.get('accept_new_patients'))
            provider.accept_new_patients = True if (self.request.get('accept_new_patients') == "True") else False
            new_key = provider.put()
            record_type = 'healthcare_provider'
        elif action=='add_designation':
            if self.validate_designation_form() is False:
                self.render('admin.html',self.template_values)
                return
            new_key = self.record_designation()
            designation = self.request.get('designation')
            record_type = 'designation'
        elif action=='add_service':
            if self.validate_service_form() is False:
                self.render('admin.html',self.template_values)
                return
            new_key = self.record_service()
            service = self.request.get('service')
            record_type = 'service'
        else:
            self.template_values['post_result'] = 'Unknown action'
        action_done = self.request.get('action_done')
        self.redirect('/view?key='+ new_key.urlsafe()+ '&type='+record_type+'&action_done='+action_done)

    def record_designation(self):
        """
        Creates a new designation entity and stores it in the database.
        """
        k = ndb.Key(Entity.Designation, self.app.config.get('malenah-providers'))
        designation = Entity.Designation(parent=k)
        designation.name = self.request.get('designation')
        return designation.put()

    def record_service(self):
        """
        Creates a new service entity and stores it in the database.
        """
        k=ndb.Key(Entity.Service, self.app.config.get('malenah-providers')) #create a Service key
        service=Entity.Service(parent=k) #create an entity with parent as the malenah-providers group key
        service.name = self.request.get('service')
        return service.put()

    def validate_provider_form(self):
        """
        Checks for empty form fields in add provider form and appends error messages for rendering as necessary.
        """
        e_messages = []
        valid = True
        if not self.request.get('first_name') or self.request.get('first_name') is None or self.request.get('first_name')=='' or self.request.get('first_name').isspace():
            e_messages.append('You did not enter a first name.')
            valid = False
        if not self.request.get('last_name') or self.request.get('last_name')=="" or self.request.get('last_name') is None  or self.request.get('last_name').isspace():
            e_messages.append('You did not enter a last name.')
            valid = False
        if not self.request.get('phone') or self.request.get('phone')=="" or self.request.get('phone') is None or self.request.get('phone').isspace():
            e_messages.append('You did not enter a phone number.')
            valid = False
        if not self.request.get('email') or self.request.get('email')=="" or self.request.get('email') is None or self.request.get('email').isspace():
            e_messages.append('You did not enter an email.')
            valid = False
        if not self.request.get('website') or self.request.get('website')=="" or self.request.get('website') is None:
            e_messages.append('You did not enter a website.')
            valid = False
        if not self.request.get('best_time') or self.request.get('best_time')=="" or self.request.get('best_time') is None:
            e_messages.append('You did not enter a contact time.')
            valid = False
        if not self.request.get('accept_new_patients') or self.request.get('accept_new_patients')=="" or self.request.get('accept_new_patients') is None:
            e_messages.append('You did not enter whether or not new patients are being accepted.')
            valid = False
        self.template_values['error_messages'] = e_messages
        return valid

    def validate_designation_form(self):
        """
        Checks for empty form field in add designation form and appends error messages for rendering as necessary.
        Also checks and rejects entry if designation already exists in database.
        """
        e_messages = []
        valid = True
        if not self.request.get('designation') or self.request.get('designation') is None or self.request.get('designation')=='':
            e_messages.append('You did not enter a designation to add.')
            valid = False
        else: #check for duplicate already in database
            for d in self.curr_designations:
                if self.request.get('designation') == d['name']:
                    e_messages.append('The designation you are trying to add already exists in the database.')
                    valid = False
                    break
        self.template_values['error_messages'] = e_messages
        return valid

    def validate_service_form(self):
        """
        Checks for empty form field in add service form and appends error messages for rendering as necessary.
        Also checks and rejects entry if service already exists in database.
        """
        e_messages = []
        valid = True
        if not self.request.get('service') or self.request.get('service') is None or self.request.get('service')=='':
            e_messages.append('You did not enter a service to add.')
            valid = False
        else: #check for duplicate already in database
            for s in self.curr_services:
                if self.request.get('service') == s['name']:
                    e_messages.append('The service you are trying to add already exists in the database.')
                    valid = False
                    break
        self.template_values['error_messages'] = e_messages
        return valid
