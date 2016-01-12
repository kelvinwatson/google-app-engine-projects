#!/usr/bin/env python
import webapp2
import admin as a
import view as v

config = {'malenah-group':'malenah-data'}

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #LGBT providers enrolment form should go here, but for now, redirect to administrator portal
        admin.AdminHandler(self.request, self.response).get()

application = webapp2.WSGIApplication([
    ('/', a.AdminHandler),
    ('/admin', a.AdminHandler),
    ('/view', v.ViewHandler),
], debug=True, config=config)
