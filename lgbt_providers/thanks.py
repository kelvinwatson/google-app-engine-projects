import webapp2

class Thanks(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type']='text/plain'
        self.response.write('Thank you! We appreciate your help in closing the\
        health dispary gap for LGBT people.')


app = webapp2.WSGIApplication([('/thanks',Thanks),],debug=True)
