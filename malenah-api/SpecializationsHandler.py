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

        if not self.request.get_all('specializations[]'):
            self.response.set_status(400, '- Invalid input. No specializations[] provided.')
            self.response.write(self.response.status)
            return

        existing_specializations = [qe.name for qe in E.Specialization.query(ancestor=ndb.Key(E.Specialization, self.app.config.get('M-S')))]
        print(existing_specializations)

        self.response.set_status(200, '- Valid input.')

        obj = {}
        obj['status'] = self.response.status
        obj['added'] = []
        obj['duplicateNotAdded'] = []
        for s in self.request.get_all('specializations[]'):
            if s not in existing_specializations:
                print('adding'+str(s))
                parent_key = ndb.Key(E.Specialization, self.app.config.get('M-S')) #use malenah-specializtions as the key id
                e = E.Specialization(parent=parent_key)
                e.name = s
                e.put()
                obj['added'].append(s)
            else:
                obj['duplicateNotAdded'].append(s)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(self.request.get_all('specializations[]')))
        self.response.write(json.dumps(obj))

    #def error(self, code, msg):
    #    self.response.status = code
    #    self.response.status_message = msg
    #    self.response.clear()
