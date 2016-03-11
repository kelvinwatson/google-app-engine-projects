import Entities as E
import json
import sys
import urllib2
import webapp2
from oauth2client import client, crypt
from google.appengine.ext import ndb

class UserHandler(webapp2.RequestHandler):
    def __init__ (self,request,response):
        """Constructor"""
        self.ANDROID_CLIENT_ID='244305224411-3n7ir9uq20tfjv9n9ju2e3bhs40nu3uf.apps.googleusercontent.com'
        self.WEB_CLIENT_ID='244305224411-kcc9c6a3t5gbt265h3clkipddi4imjfs.apps.googleusercontent.com'
        self.CLIENT_ID='244305224411-kcc9c6a3t5gbt265h3clkipddi4imjfs.apps.googleusercontent.com'
        self.initialize(request,response)
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
        self.existing_users = []
        obj={}
        for qe in E.User.query(ancestor=ndb.Key(E.User, self.app.config.get('M-U'))):
            fvs=[]
            if qe.favorites:
                for k in qe.favorites:
                    f = {}
                    f['key']=k.id()
                    for ep in self.existing_providers:
                        sps=[]
                        if ep['specializations']:
                            for k2 in ep['specializations']:
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

    def get(self, *args, **kwargs):
        """Returns an message to inform users that this method is not supported"""
        obj = {
            "status": "Sorry, this action is not allowed."
        }
        self.response.write(json.dumps(obj))
        return

    def error_status(self, code, msg):
        """Clears the response attribute and prints error messages in JSON"""
        obj={}
        self.response.clear()
        self.response.set_status(code, msg)
        obj['status'] = self.response.status
        self.response.write(json.dumps(obj))

    def verify_token(self, url, token):
        """Verify integrity of OAuth2.0 token"""
        response = idinfo = userid = None
        try:
            response = urllib2.urlopen(url+token).read()
            idinfo = client.verify_id_token(token, self.CLIENT_ID)
            if idinfo['aud'] not in [self.ANDROID_CLIENT_ID, self.WEB_CLIENT_ID]:
                 raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
            userid = idinfo['sub']
        except Exception as e:
            return None
            self.error_status(400,'Invalid token.')
        return userid

    def check_user(self, userid, name, email):
        """Check if User entity exists in NDB datastore"""
        match = next((eu for eu in self.existing_users if eu['user_id']==userid), None) #find the duplicate dictionary
        if match:
            self.response.write(json.dumps(match))
        else:
            properties = {
                'user_id': userid,
                'email': email,
                'name': name,
                'favorites': [],
              }
            self.store_user(properties)

    def store_user(self, properties):
        """Store User entity in NDB datastore"""
        parent_key = ndb.Key(E.User, self.app.config.get('M-U'))
        e = E.User(parent=parent_key)
        e.populate(**properties)
        e.put()
        obj = e.to_dict()
        self.response.set_status(200, '- user added to database')
        obj['status'] = self.response.status
        self.response.write(json.dumps(obj))


    def post(self, *args, **kwargs):
        """Adds a User entity to the NDB datastore, Validates Token"""
        #Verify token and store new user
        if self.request.get('id_token'):
            url = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='
            userid = self.verify_token(url, self.request.get('id_token'))
            if userid is not None:
                obj={}
                self.response.set_status(200,'- token verified, user logged in')
                obj['userid']=userid
                obj['status']=self.response.status
                name=self.request.get('name')
                email=self.request.get('email')
                exists_user = self.check_user(userid,name,email)
            else:
                self.error_status(400,'Invalid token.')
            return
        elif self.request.get('post_action'): #User exists, append favorites to existing user
            #Find existing user record
            match = next((eu for eu in self.existing_users if eu['user_id']==self.request.get('user_id')), None)
            k=ndb.Key(E.User,int(match['key']),parent=ndb.Key(E.User, self.app.config.get('M-U'))) #get key from id
            if self.request.get('post_action') == 'add_favorite':
                properties = {
                    'user_id': match['user_id'],
                    'email': match['email'],
                    'name': match['name'],
                    'favorites':[ndb.Key(E.Provider,f['key']) for f in match['favorites']]
                }
                status_message = self.validate_input_post(properties) #append favorite to properties
                status_message += '- OK: favorites added successfully'
            elif self.request.get('post_action') == 'remove_favorite':
                new_favorites=[ndb.Key(E.Provider,f['key']) for f in match['favorites'] if(f.get('key')!=int(self.request.get('favorites[]')))]
                properties = {
                    'user_id': match['user_id'],
                    'email': match['email'],
                    'name': match['name'],
                    'favorites':new_favorites
                }
                status_message = '- OK: favorite removed successfully'
            elif self.request.get('post_action') == 'edit_user':
                status_message = '- OK: user profile updated successfully'
                properties = {
                    'user_id': self.request.get('user_id'),
                    'email': self.request.get('email'),
                    'name': self.request.get('name'),
                    'favorites':[ndb.Key(E.Provider,f['key']) for f in match['favorites']]
                }
            elif self.request.get('post_action') == 'get_user':
                e=k.get() # get entity
                obj = e.to_dict()
                self.response.set_status(200, "- OK")
                obj['status'] = self.response.status
                self.expand_favorites(obj)
                self.response.write(json.dumps(obj))
                return
        e=k.get() # get entity
        e.populate(**properties)
        e.put()
        obj = e.to_dict()
        self.response.set_status(200, status_message)
        obj['status'] = self.response.status
        self.expand_favorites(obj)
        self.response.write(json.dumps(obj))
        return

    def expand_favorites(self, obj):
        """Expand favorite Provider id's to their properties for output"""
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
        """Checks for empty properties, duplicate providers, and invalid health-related specializations in a dictionary"""
        if not obj['user_id'] or obj['user_id'] is None or obj['user_id']=='':
            return '- Invalid input: missing user id.'
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
                k = ndb.Key(E.Provider, fid_int)
                favorites.append(k)
        for f in favorites:
            if not any(f==fp for fp in obj['favorites']): #only add the favorite[] if not already in user's favorites array
                obj['favorites'].append(f)
        return '- OK'
