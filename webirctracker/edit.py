import webapp2
import base_page
import google.appengine.ext import ndb
import google.appengine.api import images
import google.appengine.ext import blobstore
import db_defs


class Edit(base_page.BaseHandler):
    def __init__(self,request,response):
        self.initialize(request,response)
        self.template_values={}
        self.template_values['edit_url'] = blobstore.create_upload_url('/edit/channel')

    #displays the edit page!
    def get(self):
        if self.request.get('type') == 'channel':
            channel_key = ndb.Key(urlsafe=self.request.get('key')) #pull out the key string from the url and turn it into an actual key for ndb database
            channel = channel_key.get() #from the key, we can retrieve the channel object (entity) associated with it https://cloud.google.com/appengine/docs/python/ndb/keyclass

            #if there is a channel icon associated with this entity, then use the get service to get a url for that image in order to render it
            # to use the get_serving_url, pass it the blobkey
            if channel.icon:
                self.template_values['img_url'] = images.get_serving_url(channel.icon,crop=True,size=64)
                #cropping only happens on the deployed version, not the localhosty
            self.template_values['channel'] = channel

            #populating is tricky
            #need to find all of the keys

            #first, get all classess
            classes = db_defs.ChannelClass.query(ancestor=ndb.Key(db_defs.ChannelClass,self.app.config.get('default-group'))).fetch()
            class_boxes = []

            for c in clases:
                #from all the classes, we only want those classes that are associated with our channel
                if c.key in channel.classes:
                    #if associated, add a checked mark
                    class_boxes.append({'name':c.name,'key':c.key.urlsafe(),'checked':True})
                else:
                    class_boxes.append({'name':c.name,'key':c.key.urlsafe(),'checked':False})
            self.template_values['classes']=class_boxes
        self.render('edit.html',self.template_values)
