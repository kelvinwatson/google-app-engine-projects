import Entities as E
import json
import webapp2
from google.appengine.ext import ndb

DEBUG = True

class ProviderHandler(webapp2.RequestHandler):
    def __init__ (self,request,response):
        self.initialize(request,response)
        self.existing_specializations = [{'name':qe.name,'key':qe.key.id()} for qe in E.Specialization.query(ancestor=ndb.Key(E.Specialization, self.app.config.get('M-S')))]
        self.existing_providers = [{'first_name':qe.first_name,'last_name':qe.last_name,'designation':qe.designation,'organization':qe.organization,'specializations':[k.id() for k in qe.specializations],'phone':qe.phone,'email':qe.email,'website':qe.website,'accepting_new_patients':qe.accepting_new_patients,'key':qe.key.id()} for qe in E.Provider.query(ancestor=ndb.Key(E.Provider, self.app.config.get('M-P')))]

        print(self.existing_providers)

    def get(self, *args, **kwargs):
        '''
        Retrieves Provider entities based on URI
        '''
        self.response.headers['Content-Type'] = 'application/json'

        #if(DEBUG):
            #print('args: '+str(args)+'\n')
            #print('kwargs: '+str(kwargs))
            #print type(args) #type TUPLE
            #print type(kwargs) #type DICT

        if not kwargs or kwargs is None: #GET /provider or /provider/
            if args[0]:
                if args[0]=='provider':
                    print('no kwargs, args only, provider only') #GET: /provider or provider/ (print all providers)
                    self.response.write(json.dumps(self.existing_providers))
        else: #GET /provider/pid or /provider/pid (print only the requested provider)
            print('kwarg!')
            if kwargs['pid']:
                #search the existing_providers for a match to the provider ID provided
                match = next((ep for ep in self.existing_providers if ep['key']==int(kwargs['pid'])), None) #find the duplicate dictionary
                self.response.write(json.dumps(match))
            #further URI's are handled by review and reply


    def post(self, *args, **kwargs):
        '''
        Adds a Provider entity to the NDB datastore
        '''
        self.response.headers['Content-Type'] = 'application/json'

        #Construct properties
        properties = {
            'first_name': self.request.get('first_name'),
            'last_name': self.request.get('last_name'),
            'designation': self.request.get('designation'),
            'organization': self.request.get('organization'),
            'specializations': self.request.get('specializations[]'),
            'phone': self.request.get('phone'),
            'email': self.request.get('email'),
            'website': self.request.get('website'),
            'accepting_new_patients': True if (self.request.get('accepting_new_patients')=="True") else False,
          }

        #Santize input
        status_message = self.validate_input(properties)

        #Store entity, or reject invalid input
        obj={}
        if 'Invalid' not in status_message: #check for empty fields
            parent_key = ndb.Key(E.Provider, self.app.config.get('M-P'))
            e = E.Provider(parent=parent_key)
            e.populate(**properties)
            e.put()
            obj = e.to_dict()
            self.response.set_status(200, status_message)
            obj['status'] = self.response.status
            self.expand_specializations(obj)
        else:
            self.response.clear()
            self.response.set_status(400, status_message)
            obj={}
            obj['status'] = self.response.status
        self.response.write(json.dumps(obj))

    def validate_input(self, obj):
        '''
        Checks for empty properties, duplicate providers, and invalid health-related specializations in a dictionary
        '''
        if not obj['first_name'] or obj['first_name'] is None or obj['first_name']=='' \
            or not obj['last_name'] or obj['last_name'] is None or obj['last_name']=='' \
            or not obj['designation'] or obj['designation'] is None or obj['designation']=='' \
            or not obj['phone'] or obj['phone'] is None or obj['phone']=='':
            return '- Invalid input: missing properties.'

        #reject duplicate providers
        if any(ep['first_name']==obj['first_name'] and ep['last_name']==obj['last_name'] and ep['designation']==obj['designation'] and ep['phone']==obj['phone'] for ep in self.existing_providers):
            return '- Invalid input: provider already exists in database.'
        #sanitize specializations:
        specializations = []
        for s in self.request.get_all('specializations[]'):
            sid_int = None
            try:
                sid_int = int(s)
            except ValueError:
                return '- Invalid input: specialization must be an integer id.'
            #specialization ID's must exist in database
            if not any(es['key']==sid_int for es in self.existing_specializations):
                return '- Invalid input: no specialization with provided id.'
            else:
                k = ndb.Key(E.Specialization, sid_int)
                specializations.append(k)
        obj['specializations'] = specializations #save the converted keys
        return '- OK'



    def expand_specializations(self, obj):
        specializations_list = []
        for k in obj['specializations']:
            o={}
            match = next((es for es in self.existing_specializations if es['key']==int(k.id())), None) #find the duplicate dictionary
            o['name']=match['name']
            o['key']=int(k.id())
            specializations_list.append(o)
        obj['specializations'] = specializations_list
