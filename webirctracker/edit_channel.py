import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
import db_defs

#actually does the editing of the channel, similar to making one in add_channel
class EditChannel(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        channel_key = ndb.Key(urlsafe=self.request.get('key')) #grab the key that's in the url and make it an actual key
        channel = channel_key.get() #get the entity associated with the key
        if self.request.get('image-action')=='remove':
            channel.icon = None
            #delete the blob HERE:
        elif self.request.get('image-action')=='change':
            upload_files = self.get_uploads('icon')
            if upload_files != []:
                blob_info = upload_files[0]
                channel.icon = blob_info.key()
        channel.classes = [ndb.Key(urlsafe=x) for x in self.request.get_all('classes[]')]
        channel.put() #updates this channel
        self.redirect('/edit?key='+ channel_key.urlsafe()+ '&type=channel')
