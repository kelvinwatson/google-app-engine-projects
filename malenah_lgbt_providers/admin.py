import base
import log as console
from datetime import datetime

class AdminHandler(base.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request,response)
        console.log(datetime.now().time())
        self.template_values = {
            'title': "MALENAH Administrator Portal",
            'header_title': "Welcome to the M.A.L.E.N.A.H. Administrator Portal",
            'last_accessed': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            }

    def get(self):
        self.render('admin.html', self.template_values) #call the overridden render (above)

    def post(self):
        action = self.request.get('action')
        if action=='add_provider':
            first_name = self.request.get('first-name')
            last_name = self.request.get('last-name')
            console.log(first_name)
            console.log(last_name)
            self.template_values['post_result'] = 'Provider successfully added'
        elif action=='add_designation':
            self.template_values['post_result'] = 'Designation successfully added'
        elif action=='add_service':
            self.template_values['post_result'] = 'Service successfully added'
        else:
            self.template_values['post_result'] = 'Unknown action'
        self.render('admin.html',self.template_values)

'''
        provider = {}
        provider.name = self.re
        self.template_values['message'] = 'Provider ' ++ ' successfully added'
        self.render('admin.html',self.template_values)

        action = self.request.get('action')
        if action == 'add_channel':
            #parent group for all channels is default-group
            k = ndb.Key(db_defs.Channel, self.app.config.get('default-group'))
            chan = db_defs.Channel(parent=k)
            chan.name = self.request.get('channel-name')
            #construct a key from a url safe string for every checkbox that was checked in the form
            #classes[] just denotes the group of classes that was checked
            #turn all of those checked classes into a list of keys (list comprehensions basically append to lists quickly)
            #recall from deb_defs.py that the Channel's classes property = ndb.KeyProperty(repeated=True) is repeated,
            #so it takes a list of keys
            chan.classes = [ndb.Key(urlsafe=x) for x in self.request.get_all('classes[]')]
            chan.active = True
            chan.icon = icon_key
            chan.put() #save the channel
            self.template_values['message'] = 'Added channel '+chan.name+' to the database.'
        elif action=='add_class':
            k=ndb.Key(db_defs.ChannelClass, self.app.config.get('default-group'))
            c=db_defs.ChannelClass(parent=k)
            c.name=self.request.get('class-name')
            c.put()
            #overwrites the message value in the template_values dictionary
            self.template_values['message'] = 'Added class '+c.name+' to the database.'
        else:
            self.template_values['message'] = 'Action '+action+' is unknown.'
        console.log([{'name':x.name,'key':x.key.urlsafe()} for x in db_defs.ChannelClass.query(ancestor=ndb.Key(db_defs.Channel, self.app.config.get('default-group'))).fetch()])
        self.render('admin.html')
'''
