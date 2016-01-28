import json
import webapp2
import Entities as E
from google.appengine.ext import ndb

DEBUG = True

class ReviewHandler(webapp2.RequestHandler):
    def __init__ (self,request,response):
        self.initialize(request,response)
        self.existing_providers = [{'first_name':qe.first_name,'last_name':qe.last_name,'designation':qe.designation,'organization':qe.organization,'specializations':qe.specializations,'phone':qe.phone,'email':qe.email,'website':qe.website,'accepting_new_patients':qe.accepting_new_patients,'key':qe.key.id()} for qe in E.Provider.query(ancestor=ndb.Key(E.Provider, self.app.config.get('M-P')))]
        self.existing_reviews = [{'username':qe.username,'rating':qe.rating,'comment':qe.comment,'replies':qe.replies,'provider':qe.provider.id()} for qe in E.Review.query()]
        print(self.existing_reviews)

    def get(self, *args, **kwargs):
        self.response.headers['Content-Type'] = 'application/json'
        if not kwargs or kwargs is None: #GET /review or /review/
            if args[0]:
                if args[0]=='review':
                    self.response.write(json.dumps(self.existing_reviews))
        else: #GET /provider/pid or /provider/pid (print only the requested provider)
            print('kwarg!')
            if kwargs['pid']:
                #search the existing_providers for a match to the provider ID provided
                provider_match = next((ep for ep in self.existing_providers if ep['key']==int(kwargs['pid'])), None) #find the duplicate dictionary
                if provider_match is not None:
                    review_matches = [(er if er['provider']==int(kwargs['pid']) else None) for er in self.existing_reviews]
                    self.response.write(json.dumps(review_matches))


    def expand_specializations(self, obj):
        specializations_list = []
        for k in obj['specializations']:
            o={}
            match = next((es for es in self.existing_specializations if es['key']==int(k.id())), None) #find the duplicate dictionary
            o['name']=match['name']
            o['key']=int(k.id())
            specializations_list.append(o)
        obj['specializations'] = specializations_list

    def post(self, *args, **kwargs):
        # if DEBUG:
        #     print('args: '+str(args)+ ' type(args): '+str(type(args))+'\n') #TUPLE
        #     print('kwargs: '+str(kwargs)+ ' type(kwargs): '+str(type(kwargs))+'\n') #DICT
        self.response.headers['Content-Type'] = 'application/json'
        properties = {
            'username': self.request.get('username'), #required
            'rating': self.request.get('rating'),     #required
            'comment': self.request.get('comment'),
            'replies': self.request.get_all('replies[]'),
            'provider':self.request.get('provider_key'), #required (int id)
          }
        status_message = self.validate_input(properties)
        print(status_message)
        print(properties)
        print type(properties['rating'])
        obj={}
        if 'Invalid' not in status_message: #check for empty fields
            #no parent key needed as each Review entity should be in its own entity group
            e = E.Review(**properties)
            e.put()
            obj = e.to_dict()
            self.response.set_status(200, status_message)
            obj['status'] = self.response.status
            print(obj)
            self.expand_provider(obj) #for json output
        else:
            self.response.clear()
            self.response.set_status(400, status_message)
            obj['status'] = self.response.status
        self.response.write(json.dumps(obj))
        return

    def validate_input(self, obj):
        '''
        Checks for empty properties, and invalid health-care providers
        '''
        if not obj['username'] or obj['username'] is None or obj['username']=='' \
            or not obj['rating'] or obj['rating'] is None or obj['rating']=='' \
            or not obj['provider'] or obj['provider'] is None or obj['provider']=='':
            return '- Invalid input: missing properties.'

        #sanitize rating
        rating_float = None
        try:
            rating_float = float(obj['rating'])
        except ValueError:
            return '- Invalid input: rating must be a valid number between 0 and 5.0 (e.g. 1, 2.5, 4.8).'
        if rating_float < 0 or rating_float > 5.0:
            return '- Invalid input: rating must be valid number between 0 and 5.0 (e.g. 1, 2.5, 4.8).'
        obj['rating'] = rating_float

        #check that provider_key exists in database
        try:
            pid_int = int(obj['provider'])
        except ValueError:
            return '- Invalid input: Provider id must be an integer.'
        if not any(ep['key']==pid_int for ep in self.existing_providers):
            return '- Invalid input: no match for Provider id. Please double check Provider id.'
        obj['provider'] =  ndb.Key(E.Provider, pid_int)
        return '- OK'

    def expand_provider(self, obj):
        o={}
        match = next((ep for ep in self.existing_providers if ep['key']==obj['provider'].id()), None) #find the duplicate dictionary
        o['first_name']=match['first_name']
        o['last_name']=match['last_name']
        o['key']=match['key']
        obj['provider'] = o
