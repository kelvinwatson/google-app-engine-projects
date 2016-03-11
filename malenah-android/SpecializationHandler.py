import Entities as E
import json
import webapp2
from google.appengine.ext import ndb

class SpecializationHandler(webapp2.RequestHandler):
    def __init__(self,request,response):
        """Constructor"""
        self.initialize(request,response)
        self.existing_specializations = [{'name':qe.name,'key':qe.key.id()} for qe in E.Specialization.query(ancestor=ndb.Key(E.Specialization, self.app.config.get('M-S')))]
        self.response.headers['Content-Type'] = 'application/json'

    def get(self, *args, **kwargs):
        """Retrieves Specialization entities based on URI"""
        if not kwargs or kwargs is None: #GET /provider or /provider/
            if args:
                if args[0]:
                    if args[0]=='specialization':
                        if self.existing_specializations: self.response.write(json.dumps(self.existing_specializations))
                        else: self.error_status(200, '- OK. No specializations currently in database.')
            else: #datastore is empty
                if self.existing_specializations: self.response.write(json.dumps(self.existing_specializations))
                else: self.error_status(200, '- OK. No specializations currently in database.')
        else: #GET /provider/pid or /provider/pid (print only the requested provider)
            if kwargs['sid']:
                #search the existing_providers for a match to the provider ID provided
                match = next((es for es in self.existing_specializations if es['key']==int(kwargs['sid'])), None) #find the duplicate dictionary
                if match:
                    self.response.write(json.dumps(match))
                else:
                    self.error_status(400, '- OK. No specializations matching the provided specialization id. ')
            else:
                self.error_status(400, '- OK. No specializations matching the provided specialization id. ')
        return

    def error_status(self, code, msg):
        """Clears the response attribute and prints error messages in JSON"""
        obj={}
        self.response.clear()
        self.response.set_status(code, msg)
        obj['status'] = self.response.status
        self.response.write(json.dumps(obj))

    def post(self, *args, **kwargs):
        """Add Specialization entities to the NDB datastore"""
        if not self.request.get_all('specializations[]') or self.request.get_all('specializations[]') is None or self.request.get_all('specializations[]')=='':
            self.error_status(400, '- Invalid input. Empty specializations[] field(s).')
        else:
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
                    if not any(es['name']==s for es in self.existing_specializations):
                        parent_key = ndb.Key(E.Specialization, self.app.config.get('M-S'))
                        e = E.Specialization(parent=parent_key)
                        e.name = s
                        k=e.put()
                        o={}
                        o['name'] = s
                        o['key'] = k.id()
                        obj['added'].append(o)
                    else:
                        match = next((es for es in self.existing_specializations if es['name']==s), None) #find the duplicate dictionary
                        obj['duplicate'].append(match)
            self.response.write(json.dumps(self.request.get_all('specializations[]')))
            self.response.write(json.dumps(obj))
        return

    def put(self, *args, **kwargs):
        """Update Specialization entities in the NDB datastore"""
        obj={}
        if not kwargs or kwargs is None or 'sid' not in kwargs: #GET /specialization or /specialization/
            self.response.clear()
            self.response.set_status(400, '- Invalid. No specialization id provided.')
            obj['status'] = self.response.status
        else: #reply id is in kwarg
            match = next((es for es in self.existing_specializations if es['key']==int(kwargs['sid'])), None) #
            if match is not None: #entity exists in database
                properties = {
                    'name': self.request.get('name'), #required
                  }
                status_message = self.validate_input(properties)
                obj={}
                if 'Invalid' not in status_message: #check for empty or invalid fields
                    pk = ndb.Key(E.Specialization, self.app.config.get('M-S'))
                    e = E.Specialization.get_by_id(int(kwargs['sid']), parent=pk)
                    e.populate(**properties)
                    e.put()
                    obj = e.to_dict()
                    self.response.set_status(200, status_message)
                    obj['status'] = self.response.status
                else:
                     self.response.clear()
                     self.response.set_status(400, status_message)
                     obj['status'] = self.response.status
            else:
                 self.response.clear()
                 self.response.set_status(400, '- Invalid input. Unable to update entity. No match for specialization id.')
                 obj['status'] = self.response.status
        self.response.write(json.dumps(obj))
        return


    def delete(self, *args, **kwargs):
        """Delete Specialization entities from the NDB datastore"""
        obj={}
        if not kwargs or kwargs is None or 'sid' not in kwargs: #GET /reply or /reply/
            self.response.clear()
            self.response.set_status(400, '- Invalid. No specialization id provided.')
            obj['status'] = self.response.status
        else: #specialization id is in kwarg
            match = next((es for es in self.existing_specializations if es['key']==int(kwargs['sid'])), None) #
            if match is not None: #entity exists in database\
                pk=ndb.Key(E.Specialization, self.app.config.get('M-S'))
                E.Specialization.get_by_id(int(kwargs['sid']), parent=pk).key.delete()
                self.response.set_status(200, '- Delete specialization successful.')
                obj['status'] = self.response.status
            else:
                 self.response.clear()
                 self.response.set_status(400, '- Invalid input. Unable to delete entity. No match for specialization id.')
                 obj['status'] = self.response.status
        self.response.write(json.dumps(obj))
        return

    def validate_input(self,obj):
        """Validate Specialization entity property"""
        if not obj['name'] or obj['name'] is None or obj['name']=='':
            return '- Invalid input: missing name.'
        return '- OK'
