import json
import webapp2
import Entities as E
from google.appengine.ext import ndb

class ReplyHandler(webapp2.RequestHandler):
    def __init__ (self,request,response):
        """Constructor"""
        self.initialize(request,response)
        self.existing_providers = [{'first_name':qe.first_name,'last_name':qe.last_name,'designation':qe.designation,'organization':qe.organization,'specializations':qe.specializations,'phone':qe.phone,'email':qe.email,'website':qe.website,'accepting_new_patients':qe.accepting_new_patients,'key':qe.key.id()} for qe in E.Provider.query(ancestor=ndb.Key(E.Provider, self.app.config.get('M-P')))]
        self.existing_reviews = [{'username':qe.username,'rating':qe.rating,'comment':qe.comment,'replies':qe.replies,'provider':qe.provider.id(),'key':qe.key.id()} for qe in E.Review.query()]
        self.existing_replies = [{'username':qe.username,'comment':qe.comment,'review':qe.review.id(),'provider':qe.provider.id(),'key':qe.key.id()} for qe in E.Reply.query()]
        self.response.headers['Content-Type'] = 'application/json'


    def get(self, *args, **kwargs):
        """Retrieves Reply entities from NDB datastore"""
        obj={}
        if not kwargs or kwargs is None: #GET /reply or /reply/
            if args:
                if args[0]:
                    if args[0]=='reply':
                        if self.existing_replies: self.response.write(json.dumps(self.existing_replies))
                        else: self.error_status(200, '- OK. No replies currently in database.')
            else:
                if self.existing_replies: self.response.write(json.dumps(self.existing_replies))
                else: self.error_status(200, '- OK. No replies currently in database.')
        else: #GET /provider/pid or /provider/pid (print only the requested provider)
            if 'repid' in kwargs:
                match = next((er for er in self.existing_replies if er['key']==int(kwargs['repid'])),None)
                if match is not None:
                    self.response.write(json.dumps(match))
                else:
                    self.error_status(400, '- No match for reply id.')
            elif 'revid' in kwargs:
                qrep=E.Reply.query(ancestor=ndb.Key(E.Review, int(kwargs['revid']))) #perform ancestor query
                replies = []
                for q in qrep:
                    obj={
                        'username': q.username,
                        'comment': q.comment,
                        'review': q.review.integer_id(),
                        'provider': q.provider.integer_id(),
                    }
                    replies.append(obj)
                self.response.write(json.dumps(replies))
        return

    def error_status(self, code, msg):
        """Clears the response attribute and prints error messages in JSON"""
        obj={}
        self.response.clear()
        self.response.set_status(code, msg)
        obj['status'] = self.response.status
        self.response.write(json.dumps(obj))

    def post(self, *args, **kwargs):
        """Adds Reply entities to NDB datastore"""
        properties = {
            'username': self.request.get('username'), #required
            'comment': self.request.get('comment'),
            'review': self.request.get('review'),
            'provider': self.request.get('provider'), #required (int id)
          }
        status_message = self.validate_input(properties)
        obj={}
        if 'Invalid' not in status_message: #check for empty fields
            parent_key = properties['review']
            e = E.Reply(parent=parent_key)
            e.populate(**properties)
            reply_key = e.put()
            self.update_review(parent_key, reply_key)
            obj = e.to_dict()
            self.response.set_status(200, status_message)
            obj['status'] = self.response.status
            self.expand_review(obj)
            self.expand_provider(obj) #for json output
        else:
            self.response.clear()
            self.response.set_status(400, status_message)
            obj['status'] = self.response.status
        self.response.write(json.dumps(obj))
        return

    def update_review(self, review_key, reply_key):
        """Updates a Review entity by adding a Reply entity"""
        review_entity = review_key.get()
        review_entity.replies.append(reply_key)
        review_entity.put()

    def validate_input(self, obj):
        """Checks for empty properties, and invalid review"""
        if not obj['username'] or obj['username'] is None or obj['username']=='' \
            or not obj['review'] or obj['review'] is None or obj['review']=='' \
            or not obj['provider'] or obj['provider'] is None or obj['provider']=='':
            return '- Invalid input: missing properties.'
        #check that the review id exists in database
        try:
            revid_int = int(obj['review'])
        except ValueError:
            return '- Invalid input: Review id must be an integer.'
        if not any(er['key']==revid_int for er in self.existing_reviews):
            return '- Invalid input: no match for Review id. Please double check Provider id.'
        obj['review'] =  ndb.Key(E.Review,revid_int)
        #check that provider_key exists in database
        try:
            pid_int = int(obj['provider'])
        except ValueError:
            return '- Invalid input: Provider id must be an integer.'
        if not any(ep['key']==pid_int for ep in self.existing_providers):
            return '- Invalid input: no match for Provider id. Please double check Provider id.'
        obj['provider'] =  ndb.Key(E.Provider, pid_int)
        return '- OK'

    def expand_review(self, obj):
        """Expands a Review entity for output"""
        o={}
        match = next((er for er in self.existing_reviews if er['key']==obj['review'].id()), None) #find the duplicate dictionary
        o['key']=match['key']
        obj['review'] = o

    def expand_provider(self, obj):
        """Expands a Provider entity for output"""
        o={}
        match = next((ep for ep in self.existing_providers if ep['key']==obj['provider'].id()), None) #find the duplicate dictionary
        o['first_name']=match['first_name']
        o['last_name']=match['last_name']
        o['key']=match['key']
        obj['provider'] = o

    #https://cloud.google.com/appengine/docs/python/tools/webapp/requesthandlerclass
    def put(self, *args, **kwargs):
        """Updates a Reply entity in the NDB datastore"""
        obj={}
        if not kwargs or kwargs is None or 'repid' not in kwargs: #GET /reply or /reply/
            self.response.clear()
            self.response.set_status(400, '- Invalid. No reply id provided.')
            obj['status'] = self.response.status
        else: #reply id is in kwarg
            match = next((er for er in self.existing_replies if er['key']==int(kwargs['repid'])), None) #
            if match is not None: #entity exists in database
                properties = {
                    'username': self.request.get('username'), #required
                    'comment': self.request.get('comment'),
                    'review': self.request.get('review'),
                    'provider': self.request.get('provider'), #required (int id)
                  }
                status_message = self.validate_input(properties)
                obj={}
                if 'Invalid' not in status_message: #check for empty or invalid fields
                    pk = ndb.Key(E.Review, int(match['review']))
                    e = E.Reply.get_by_id(int(kwargs['repid']), parent=pk)
                    e.populate(**properties)
                    e.put()
                    obj = e.to_dict()
                    self.response.set_status(200, status_message)
                    obj['status'] = self.response.status
                    self.expand_review(obj)
                    self.expand_provider(obj) #for json output
                else:
                     self.response.clear()
                     self.response.set_status(400, status_message)
                     obj['status'] = self.response.status
            else:
                 self.response.clear()
                 self.response.set_status(400, '- Invalid input. Unable to update entity. No match for reply id.')
                 obj['status'] = self.response.status
        self.response.write(json.dumps(obj))
        return


    def delete(self, *args, **kwargs):
        """Deletes a Reply entity from the NDB datastore"""
        obj={}
        if not kwargs or kwargs is None or 'repid' not in kwargs: #GET /reply or /reply/
            self.response.clear()
            self.response.set_status(400, '- Invalid. No reply id provided.')
            obj['status'] = self.response.status
        else: #reply id is in kwarg
            match = next((er for er in self.existing_replies if er['key']==int(kwargs['repid'])), None) #
            if match is not None: #entity exists in database
                pk=ndb.Key(E.Review, int(match['review'])) #must retrieve parent in order to delete
                E.Reply.get_by_id(int(kwargs['repid']),parent=pk).key.delete()
                self.response.set_status(200, '- Delete reply successful.')
                obj['status'] = self.response.status
            else:
                 self.response.clear()
                 self.response.set_status(400, '- Invalid input. Unable to delete entity. No match for reply id.')
                 obj['status'] = self.response.status
        self.response.write(json.dumps(obj))
        return
