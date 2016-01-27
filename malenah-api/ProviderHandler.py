import Entities as E
import json
import webapp2
from google.appengine.ext import ndb

DEBUG = True

class ProviderHandler(webapp2.RequestHandler):
    def __init__ (self,request,response):
        self.initialize(request,response)
        self.existing_specializations = [{'name':qe.name,'key':qe.key.id()} for qe in E.Specialization.query(ancestor=ndb.Key(E.Specialization, self.app.config.get('M-S')))]
        self.existing_providers = [{'first_name':qe.first_name,'last_name':qe.last_name,'designation':qe.designation,'phone':qe.phone,'key':qe.key.id()} for qe in E.Provider.query(ancestor=ndb.Key(E.Provider, self.app.config.get('M-P')))]
        print(self.existing_providers)

    def get(self, *args, **kwargs):
        '''
        Retrieves Provider entities based on URI
        '''
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('GET Provider Handler\n')

        if(DEBUG): #test writing out a JSON object
            provider = {}
            provider['first_name'] = self.request.get('first_name')
            provider['last_name'] = self.request.get('first_name')
            self.response.write(json.dumps(provider))


        self.response.write('args: '+str(args)+'\n')
        self.response.write('kwargs: '+str(kwargs))

        print type(args) #type TUPLE
        print type(kwargs) #type DICT

        if not kwargs or kwargs is None: #/provider/ or #provider
            if args[0]:
                if args[0]=='provider':
                    print('no kwargs, args only, provider only') #YRI: provider or provider/
                    #print all providers
        else: #there is a kwarg
            print('kwarg!')
            if kwargs['pid']:
                print("there's a pid!")
                #print only the requested provider
            #further URI's are handled by review and reply


        if(DEBUG):
            self.response.write("\n\n==DEBUG==\n")
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('GET Provider Handler\n')
            self.response.write('args: '+str(args)+'\n')
            self.response.write('kwargs: '+str(kwargs))
        #self.response.write(self.request.get('review'))

        #if no args, then return a json list of all providers in the db

        #if there is a review and reply arg, then respond appropriately

    def post(self, *args, **kwargs):
        '''
        Adds a Provider entity to the NDB datastore
        '''


        self.response.headers['Content-Type'] = 'application/json'

        specializations = [int(x) for x in self.request.get_all('specializations[]')]

        properties = {
            'first_name': self.request.get('first_name'),
            'last_name': self.request.get('last_name'),
            'designation': self.request.get('designation'),
            'organization': self.request.get('organization'),
            'specializations': specializations,
            'phone': self.request.get('phone'),
            'email': self.request.get('email'),
            'website': self.request.get('website'),
            'accepting_new_patients': True if (self.request.get('accepting_new_patients')=="True") else False,
          }
        obj={}
        status_message = self.validate_input(properties)
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
        self.response.out.write(json.dumps(obj))

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

        #specialization ID's must exist in database
        #existing_specializations = [{'name':qe.name,'key':qe.key.id()} for qe in E.Specialization.query(ancestor=ndb.Key(E.Specialization, self.app.config.get('M-S')))]
        for sid in obj['specializations']:
            if not any(es['key']==int(sid) for es in self.existing_specializations):
                return '- Invalid input: no specialization with provided id.'
        return '- OK'



    def expand_specializations(self, obj):
        specializations_list = []
        for sid in obj['specializations']:
            o={}
            match = next((es for es in self.existing_specializations if es['key']==sid), None) #find the duplicate dictionary
            o['name']=match['name']
            o['key']=int(sid)
            specializations_list.append(o)
        obj['specializations'] = specializations_list
