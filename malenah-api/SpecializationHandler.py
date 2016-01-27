import Entities as E
import json
import webapp2
from google.appengine.ext import ndb

class SpecializationHandler(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('GET Specializations Handler\n')
        self.response.write('args: '+str(args)+'\n')
        self.response.write('kwargs: '+str(kwargs))
        #depending on whether there are args, display accordingly

    def post(self, *args, **kwargs): #add a specialization(s)

        if not self.request.get_all('specializations[]') or self.request.get_all('specializations[]') is None or self.request.get_all('specializations[]')=='':
            self.response.set_status(400, '- Invalid input. No specializations[] provided.')
            self.response.write(self.response.status)
            return

        existing_specializations = [{'name':qe.name,'key':qe.key.id()} for qe in E.Specialization.query(ancestor=ndb.Key(E.Specialization, self.app.config.get('M-S')))]
        print(existing_specializations)

        self.response.set_status(200, '- OK.')

        obj = {}
        obj['status'] = self.response.status
        obj['added'] = []
        obj['invalid'] = []
        obj['duplicate'] = []
        for s in self.request.get_all('specializations[]'):
            if s=='':
                obj['invalid'] = s
            else:
                if not any(es['name']==s for es in existing_specializations): #check if designation already in datastore
                    print('adding '+str(s))
                    parent_key = ndb.Key(E.Specialization, self.app.config.get('M-S')) #use malenah-specializtions as the key id
                    e = E.Specialization(parent=parent_key)
                    e.name = s
                    k=e.put()
                    o={}
                    o['name'] = s
                    o['key'] = k.id()
                    obj['added'].append(o)
                else:
                    match = next((es for es in existing_specializations if es['name']==s), None) #find the duplicate dictionary
                    obj['duplicate'].append(match)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(self.request.get_all('specializations[]')))
        self.response.write(json.dumps(obj))

    #def error(self, code, msg):
    #    self.response.status = code
    #    self.response.status_message = msg
    #    self.response.clear()
