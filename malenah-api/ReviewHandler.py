import json
import webapp2
import Entities as E
from google.appengine.ext import ndb

DEBUG = True

class ReviewHandler(webapp2.RequestHandler):
    def __init__ (self,request,response):
        self.initialize(request,response)
        self.existing_providers = [{'first_name':qe.first_name,'last_name':qe.last_name,'designation':qe.designation,'organization':qe.organization,'specializations':qe.specializations,'phone':qe.phone,'email':qe.email,'website':qe.website,'accepting_new_patients':qe.accepting_new_patients,'key':qe.key.id()} for qe in E.Provider.query(ancestor=ndb.Key(E.Provider, self.app.config.get('M-P')))]

    def get(self, *args, **kwargs):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Review Handler\n')
        self.response.write('args: '+str(args)+'\n')
        self.response.write('kwargs: '+str(kwargs))

    def post(self, *args, **kwargs):
        # if DEBUG:
        #     print('args: '+str(args)+ ' type(args): '+str(type(args))+'\n') #TUPLE
        #     print('kwargs: '+str(kwargs)+ ' type(kwargs): '+str(type(kwargs))+'\n') #DICT

        properties = {
            'username': self.request.get('username'), #required
            'rating': self.request.get('rating'),     #required
            'comment': self.request.get('comment'),
            'replies': self.request.get('replies[]'),
            'provider_key':self.request.get('provider_id'), #required (int id)
          }
        status_message = self.validate_input(properties)
        print(status_message)

    def validate_input(self, obj):
        '''
        Checks for empty properties, and invalid health-care providers
        '''
        if not obj['username'] or obj['username'] is None or obj['username']=='' \
            or not obj['rating'] or obj['rating'] is None or obj['rating']=='' \
            or not obj['provider_key'] or obj['provider_key'] is None or obj['provider_key']=='':
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
            pid_int = int(obj['provider_key'])
        except ValueError:
            return '- Invalid input: Provider id must be an integer.'
        if not any(ep['key']==pid_int for ep in self.existing_providers):
            return '- Invalid input: no match for Provider id. Please double check Provider id.'
        obj['provider_key'] =  ndb.Key(E.Provider, pid_int)
        return '- OK'
