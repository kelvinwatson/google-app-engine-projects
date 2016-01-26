import Entities as E
import json
import webapp2
from google.appengine.ext import ndb

class SpecializationsHandler(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('GET Specializations Handler\n')
        self.response.write('args: '+str(args)+'\n')
        self.response.write('kwargs: '+str(kwargs))
        #view all specializations as JSON

    def post(self, *args, **kwargs): #add a specialization(s)
        existing_specializations = [qe.name for qe in E.Specialization.query(ancestor=ndb.Key(E.Specialization, self.app.config.get('M-S')))]
        print(existing_specializations)

        for s in self.request.get_all('specializations[]'):
            if s not in existing_specializations:
                print('adding'+str(s))
                parent_key = ndb.Key(E.Specialization, self.app.config.get('M-S')) #use malenah-specializtions as the key id
                e = E.Specialization(parent=parent_key)
                e.name = s
                e.put()

        self.response.headers['Content-Type'] = 'application/json'
        #check to see if specializations already exists in DB

        #add if not

        self.response.write(json.dumps(self.request.get_all('specializations[]')))
