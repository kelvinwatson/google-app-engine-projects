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
        #console.log("\n==Retrieving all providers...==")
        all_providers = [{'first_name':e.first_name,'last_name':e.last_name,'key':e.key.urlsafe()} for e in Entity.Provider.query(ancestor=ndb.Key(Entity.Provider,self.app.config.get('malenah-providers'))).fetch()]
#        for p in all_providers:
#            console.log('\n   '+str(p))
        return all_providers

    def get_all_designations(self):
        #console.log("\n== BASE HANDLER Retrieving all designations...==")
        #this step is essential when later extracting these keys from a form
        #retrieve entities from the database
        all_designations = [{'name':entity.name,'key':entity.key.urlsafe()} for entity in Entity.Designation.query(ancestor=ndb.Key(Entity.Designation,self.app.config.get('malenah-providers'))).fetch()]
        #console.log(str(all_designations))
        return all_designations

    def get_all_services(self):
        #console.log("\n== BASE HANDLER Retrieving all services...==")
        all_services = [{'name':entity.name,'key':entity.key.urlsafe()} for entity in Entity.Service.query(ancestor=ndb.Key(Entity.Service,self.app.config.get('malenah-providers'))).fetch()]
        #console.log(all_services)
        return all_services
