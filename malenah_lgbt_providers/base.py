#!/usr/bin/env python
import entities as Entity
import jinja2
import log as console
import os
import webapp2
from google.appengine.ext import ndb

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+'/templates'),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True
        )

    def render(self, template, template_variables={}):
        template = self.jinja2.get_template(template)
        self.response.write(template.render(template_variables))

    def get_all_providers(self):
        all_providers = [{'first_name':e.first_name,'last_name':e.last_name,'phone':e.phone,'email':e.email,'website':e.website,'best_time':e.best_time.strftime("%H:%M"),'designation':ndb.Key(urlsafe=e.designation).get().name,'services':[{'name':k.get().name} for k in e.services],'key':e.key.urlsafe()} for e in Entity.Provider.query(ancestor=ndb.Key(Entity.Provider,self.app.config.get('malenah-providers'))).fetch()]
        return all_providers

    def get_all_designations(self):
        #this step is essential when later extracting these keys from a form
        #retrieve entities from the database
        all_designations = [{'name':entity.name,'key':entity.key.urlsafe()} for entity in Entity.Designation.query(ancestor=ndb.Key(Entity.Designation,self.app.config.get('malenah-providers'))).order(Entity.Designation.name).fetch()]
        return all_designations

    def get_all_services(self):
        all_services = [{'name':entity.name,'key':entity.key.urlsafe()} for entity in Entity.Service.query(ancestor=ndb.Key(Entity.Service,self.app.config.get('malenah-providers'))).order(Entity.Service.name).fetch()]
        return all_services
