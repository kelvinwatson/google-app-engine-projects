#!/usr/bin/env python
import webapp2
import admin as a
import edit as e
import view as v

config = {'malenah-providers':'malenah-data'}

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #LGBT providers enrolment form should go here, but for now, redirect to administrator portal
        admin.AdminHandler(self.request, self.response).get()

application = webapp2.WSGIApplication([
    ('/', a.AdminHandler),
    ('/admin', a.AdminHandler),
    ('/edit', e.EditHandler),
    ('/view', v.ViewHandler),
    ('.*', a.AdminHandler),
], debug=True, config=config)
