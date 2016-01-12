import webapp2

config = {'default-group':'base-data'}

application = webapp2.WSGIApplication([
    ('/admin', 'admin.Admin'),
    ('/', 'base_page.BaseHandler'),
], debug=True, config=config)
