import json
import webapp2

DEBUG = True

class ProviderHandler(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('GET Provider Handler\n')

        if(DEBUG): #test writing out a JSON object
            provider = {}
            provider['first_name'] = self.request.get('first_name')
            provider['last_name'] = self.request.get('first_name')
            self.response.write(json.dumps(provider))


        self.response.write('args: '+str(args)+'\n')
        self.response.write('kwargs: '+str(kwargs))

        if(DEBUG):
            self.response.write("\n\n==DEBUG==\n")
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('GET Provider Handler\n')
            self.response.write('args: '+str(args)+'\n')
            self.response.write('kwargs: '+str(kwargs))
        #self.response.write(self.request.get('review'))

    def post(self, *args, **kwargs):
        self.response.headers['Content-Type'] = 'application/json'
        #if(DEBUG): print('POST Provider Handler\n')
        #if(DEBUG): print('args: '+str(args)+'\n')
        #if(DEBUG): print('kwargs: '+str(kwargs))

        obj = {
            'first_name': self.request.get('first_name'),
            'last_name': self.request.get('last_name'),
            'designation': self.request.get('designation'),
            'specializations': self.request.get_all('specializations[]'),
          }
        self.response.out.write(json.dumps(obj))
        #self.response.write(self.request.body)
        #if(DEBUG):
        #    self.response.write("==DEBUG==")
        #    self.response.headers['Content-Type'] = 'text/plain'
        #    self.response.write('POST Provider Handler\n')
        #    self.response.write('args: '+str(args)+'\n')
        #    self.response.write('kwargs: '+str(kwargs))

    def add_provider(self):
        if(DEBUG):
            self.response.write(self.request.get('first_name'))
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')


    #def post(self, *args, **kwargs):
