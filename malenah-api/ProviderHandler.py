import json
import webapp2

class ProviderHandler(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Provider Handler\n')
        self.response.write('args: '+str(args)+'\n')
        self.response.write('kwargs: '+str(kwargs))
        self.response.write(self.request.get('review'))
