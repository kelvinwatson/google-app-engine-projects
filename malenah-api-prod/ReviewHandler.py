import json
import webapp2
import Entities as E
from google.appengine.ext import ndb

DEBUG = True

class ReviewHandler(webapp2.RequestHandler):
    def __init__ (self,request,response):
        self.initialize(request,response)
        self.existing_providers = [{'first_name':qe.first_name,'last_name':qe.last_name,'designation':qe.designation,'organization':qe.organization,'specializations':qe.specializations,'phone':qe.phone,'email':qe.email,'website':qe.website,'accepting_new_patients':qe.accepting_new_patients,'key':qe.key.id()} for qe in E.Provider.query(ancestor=ndb.Key(E.Provider, self.app.config.get('M-P')))]
        self.existing_reviews = [{'username':qe.username,'rating':qe.rating,'comment':qe.comment,'replies':[q.id() for q in qe.replies],'provider':qe.provider.id(),'key':qe.key.id()} for qe in E.Review.query()]
        self.response.headers['Content-Type'] = 'application/json'

    def get(self, *args, **kwargs):
        obj={}
        if not kwargs or kwargs is None: #GET /review or /review/
            if args:
                if args[0]:
                    if args[0]=='review':
                        if self.existing_reviews: self.response.write(json.dumps(self.existing_reviews))
                        else: self.error_status(200, '- OK. No reviews currently in database.')
            else:
                self.error_status(200, '- OK. No reviews currently in database.')
        else: #GET /provider/pid/review or /provider/pid/review
            if 'revid' in kwargs: #review/revid or review/revid/ or provider/pid/review/revid
                review_match = next((er for er in self.existing_reviews if er['key']==int(kwargs['revid'])),None)
                if review_match is not None:
                    self.response.write(json.dumps(review_match))
                else:
                    self.error_status(400, '- No match for review id.')
            elif 'pid' in kwargs: #GET /provider/pid/review or /provider/pid/review/
                #search the existing_providers for a match to the provider ID provided
                provider_match = next((ep for ep in self.existing_providers if ep['key']==int(kwargs['pid'])), None) #find the duplicate dictionary
                if provider_match is not None:
                    review_matches = [er for er in self.existing_reviews if er['provider']==int(kwargs['pid'])]
                    if review_matches:
                        self.response.write(json.dumps(review_matches))
                    else:
                        self.error_status(400, '- Invalid. No matches for the provided review id.')
                else: #no provider match
                    self.error_status(400, '- Invalid. No matches for the provided provider id.')
        return

    def error_status(self, code, msg):
        '''
        Clears the response attribute and prints error messages in JSON
        '''
        obj={}
        self.response.clear()
        self.response.set_status(code, msg)
        obj['status'] = self.response.status
        self.response.write(json.dumps(obj))

    def post(self, *args, **kwargs):
        properties = {
            'username': self.request.get('username'), #required
            'rating': self.request.get('rating'),     #required
            'comment': self.request.get('comment'),
            'replies': [], #when review is first posted, it does not have replies
            'provider':self.request.get('provider'), #required (int id)
          }
        status_message = self.validate_input_post(properties)
        obj={}
        if 'Invalid' not in status_message: #check for empty fields
            #no parent key needed as each Review entity should be in its own entity group
            e = E.Review(**properties)
            e.put()
            obj = e.to_dict()
            self.response.set_status(200, status_message)
            obj['status'] = self.response.status
            self.expand_provider(obj) #for json output
        else:
            self.response.clear()
            self.response.set_status(400, status_message)
            obj['status'] = self.response.status
        self.response.write(json.dumps(obj))
        return

    def validate_input_post(self, obj):
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

    def validate_input_put(self, obj):
        '''
        Checks for empty properties, and invalid health-care providers
        '''
        if not obj['rating'] or obj['rating'] is None or obj['rating']=='':
            return '- Invalid input: missing rating.'

        #sanitize rating
        rating_float = None
        try:
            rating_float = float(obj['rating'])
        except ValueError:
            return '- Invalid input: rating must be a valid number between 0 and 5.0 (e.g. 1, 2.5, 4.8).'
        if rating_float < 0 or rating_float > 5.0:
            return '- Invalid input: rating must be valid number between 0 and 5.0 (e.g. 1, 2.5, 4.8).'
        obj['rating'] = rating_float
        return '- OK'

    def put(self, *args, **kwargs):
        obj={}
        if not kwargs or kwargs is None or 'revid' not in kwargs: #GET /reply or /reply/
            self.response.clear()
            self.response.set_status(400, '- Invalid. No review id provided.')
            obj['status'] = self.response.status
        else: #reply id is in kwarg
            match = next((er for er in self.existing_reviews if er['key']==int(kwargs['revid'])), None) #
            if match is not None: #entity exists in database
                properties = {
                    #'username': self.request.get('username'), #cannot alter existing username
                    'rating': self.request.get('rating'),     #required
                    'comment': self.request.get('comment'),
                    #'replies': self.request.get_all('replies[]'), cannot alter existing replies, must remain same
                    #'provider':self.request.get('provider_key'), #cannot alter existing provider, must remain same
                  }
                status_message = self.validate_input_put(properties)
                obj={}
                if 'Invalid' not in status_message: #check for empty or invalid fields
                    e = E.Review.get_by_id(int(kwargs['revid']))
                    e.populate(**properties)
                    e.put()
                    obj = e.to_dict()
                    self.response.set_status(200, status_message)
                    obj['status'] = self.response.status
                    self.expand_provider(obj) #for json output
                else:
                    self.response.clear()
                    self.response.set_status(400, status_message)
                    obj['status'] = self.response.status
            else:
                 self.response.clear()
                 self.response.set_status(400, '- Invalid input. Unable to update entity. No match for review id.')
                 obj['status'] = self.response.status
        self.response.write(json.dumps(obj))
        return


    def delete(self, *args, **kwargs):
        obj={}
        if not kwargs or kwargs is None or 'revid' not in kwargs: #GET /reply or /reply/
            self.response.clear()
            self.response.set_status(400, '-Invalid. No review id provided.')
            obj['status'] = self.response.status
        else: #reply id is in kwarg
            match = next((er for er in self.existing_reviews if er['key']==int(kwargs['revid'])), None) #
            if match is not None: #entity exists in database
                E.Review.get_by_id(int(kwargs['revid'])).key.delete()
                self.response.set_status(200, '- Delete review successful.')
                obj['status'] = self.response.status
            else:
                self.response.clear()
                self.response.set_status(400, '- Invalid input. Unable to delete entity. No match for review id.')
                obj['status'] = self.response.status
        self.response.write(json.dumps(obj))
        return

    def expand_provider(self, obj):
        o={}
        match = next((ep for ep in self.existing_providers if ep['key']==obj['provider'].id()), None) #find the duplicate dictionary
        o['first_name']=match['first_name']
        o['last_name']=match['last_name']
        o['key']=match['key']
        obj['provider'] = o
