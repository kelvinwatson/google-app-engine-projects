import Entities as E
import json
import webapp2
from google.appengine.ext import ndb

class UserHandler(webapp2.RequestHandler):
    def __init__ (self,request,response):
        self.initialize(request,response)
        print('init')
        self.existing_specializations = [{'name':qe.name,'key':qe.key.id()} for qe in E.Specialization.query(ancestor=ndb.Key(E.Specialization, self.app.config.get('M-S')))]

        self.existing_providers = []
        obj={}
        for qe in E.Provider.query(ancestor=ndb.Key(E.Provider, self.app.config.get('M-P'))):
            sps=[]
            if qe.specializations:
                for k in qe.specializations:
                    s = {}
                    s['key']=k.id()
                    for es in self.existing_specializations:
                        if es['key']==s['key']:
                            s['name']=es['name']
                            break
                    sps.append(s)
            obj = {
                'category':qe.category,
                'icon_url':qe.icon_url,
                'first_name':qe.first_name,
                'last_name':qe.last_name,
                'designation':qe.designation,
                'organization':qe.organization,
                'specializations':sps,
                'building': qe.building,
                'street': qe.street,
                'city': qe.city,
                'state': qe.state,
                'country': qe.country,
                'zipcode': qe.zipcode,
                'notes': qe.notes,
                'latitude': qe.latitude,
                'longitude': qe.longitude,
                'phone':qe.phone,
                'email':qe.email,
                'website':qe.website,
                'accepting_new_patients':qe.accepting_new_patients,
                'key':qe.key.id()
                }
            self.existing_providers.append(obj)

        #print(self.existing_providers)

        self.existing_users = []
        obj={}
        for qe in E.User.query(ancestor=ndb.Key(E.User, self.app.config.get('M-U'))):
            fvs=[]
            if qe.favorites:
                for k in qe.favorites:
                    print(k)
                    f = {}
                    f['key']=k.id()
                    for ep in self.existing_providers:
                        #print(ep)
                        sps=[]
                        if ep['specializations']:
                            for k2 in ep['specializations']:
                                print(k2)
                                s = {}
                                s['key']=k2['key']
                                for es in self.existing_specializations:
                                    if es['key']==s['key']:
                                        s['name']=es['name']
                                        break
                                sps.append(s)
                        if ep['key']==f['key']:
                            obj2 = {
                                'category':ep['category'],
                                'icon_url':ep['icon_url'],
                                'first_name':ep['first_name'],
                                'last_name':ep['last_name'],
                                'designation':ep['designation'],
                                'organization':ep['organization'],
                                'specializations':sps,
                                'building': ep['building'],
                                'street': ep['street'],
                                'city': ep['city'],
                                'state': ep['state'],
                                'country': ep['country'],
                                'zipcode': ep['zipcode'],
                                'notes': ep['notes'],
                                'latitude': ep['latitude'],
                                'longitude': ep['longitude'],
                                'phone':ep['phone'],
                                'email':ep['email'],
                                'website':ep['website'],
                                'accepting_new_patients':ep['accepting_new_patients'],
                                'key':ep['key']
                            }
                            fvs.append(obj2)
            obj = {
                'user_id':qe.user_id,
                'email':qe.email,
                'name':qe.name,
                'favorites':fvs,
                'key':qe.key.id(),
            }
            self.existing_users.append(obj)

        self.response.headers['Content-Type'] = 'application/json'
        #print(self.existing_users)

    def get(self, *args, **kwargs):
        '''
        Retrieves Provider entities based on URI
        '''
        print('get users')
        if not kwargs or kwargs is None: #GET /provider or /provider/
            if args:
                if args[0]:
                    if args[0]=='user':
                        if self.existing_users:
                            self.response.write(json.dumps(self.existing_users))
                        else:
                            self.error_status(200, '- OK. No users currently in database.')
            else: #datastore is empty
                if self.existing_providers: self.response.write(json.dumps(self.existing_providers))
                else: self.error_status(200, '- OK. No users currently in database.')
        else: #GET /user/uid or /user/pid (print only the requested provider)
            if kwargs['uid']:
                #search the existing_providers for a match to the provider ID provided
                match = next((eu for eu in self.existing_users if eu['key']==int(kwargs['uid'])), None) #find the duplicate dictionary
                if match:
                    self.response.write(json.dumps(match))
                else:
                    self.error_status(400, '- OK. No users matching the provided user id. ')
            else:
                self.error_status(400, '- OK. No users matching the provided user id. ')
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
        '''
        Adds a User entity to the NDB datastore
        '''
        #Construct properties
        properties = {
            'user_id': self.request.get('user_id'),
            'email': self.request.get('email'),
            'name': self.request.get('name'),
            'favorites': None,
          }
        #print(properties)

        #Santize input
        status_message = self.validate_input_post(properties)
        #print(status_message)

        #Store entity, or reject invalid input
        obj={}
        if 'Invalid' not in status_message: #check for empty fields
            parent_key = ndb.Key(E.User, self.app.config.get('M-U'))
            e = E.User(parent=parent_key)
            e.populate(**properties)
            e.put()
            obj = e.to_dict()
            self.response.set_status(200, status_message)
            obj['status'] = self.response.status
            self.expand_favorites(obj)
            print(obj)
        else:
            self.response.clear()
            self.response.set_status(400, status_message)
            obj['status'] = self.response.status
        self.response.write(json.dumps(obj))
        return

    def expand_favorites(self, obj):
        favorites_list = []
        for k in obj['favorites']:
            o={}
            match = next((ep for ep in self.existing_providers if ep['key']==int(k.id())), None) #find the duplicate dictionary
            o['category']=match['category']
            o['icon_url']=match['icon_url']
            o['first_name']=match['first_name']
            o['last_name']=match['last_name']
            o['designation']=match['designation']
            o['organization']=match['organization']
            o['specializations']=match['specializations']
            o['building']=match['building']
            o['street'] = match['street']
            o['city'] = match['city']
            o['state'] = match['state']
            o['country'] = match['country']
            o['zipcode'] = match['zipcode']
            o['notes']= match['notes']
            o['latitude'] = match['latitude']
            o['longitude'] = match['longitude']
            o['phone'] = match['phone']
            o['email'] = match['email']
            o['website'] = match['website']
            o['accepting_new_patients'] = match['accepting_new_patients']
            o['key']=int(k.id())
            favorites_list.append(o)
        obj['favorites'] = favorites_list



    def validate_input_post(self, obj):
        '''
        Checks for empty properties, duplicate providers, and invalid health-related specializations in a dictionary
        '''
        if not obj['user_id'] or obj['user_id'] is None or obj['user_id']=='':
            return '- Invalid input: missing user id.'

        #reject duplicate providers
        if any(eu['user_id']==obj['user_id'] for eu in self.existing_users):
            return '- Invalid input: user already exists in database.'

        #sanitize favorites:
        favorites = []
        for f in self.request.get_all('favorites[]'):
            fid_int = None
            try:
                fid_int = int(f)
            except ValueError:
                return '- Invalid input: favorite(provider) must be an integer id.'
            #provider ID's must exist in database
            if not any(ep['key']==fid_int for ep in self.existing_providers):
                return '- Invalid input: no provider with provided id.'
            else:
                k = ndb.Key(E.User, fid_int)
                favorites.append(k)
        obj['favorites'] = favorites #save the converted keys
        return '- OK'
