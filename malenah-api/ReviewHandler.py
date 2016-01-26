import webapp2

class ReviewHandler(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Review Handler')
        self.response.write('args: '+str(args)+'\n')
        self.response.write('kwargs: '+str(kwargs))
