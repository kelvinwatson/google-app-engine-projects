import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import admin

class AddChannel(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('icon') #get the uploaded file
        #get_uploads is built into the BlobstoreUploadHandler

        #if there is something in the list of uploaded files
        if upload_files != []:
            blob_info = upload_files[0] #grab the first as there should only ever be one file
            #make a new instance of Admin handler, pass it the request and response, call its post function and pass it the key
            #this AddChannel handler is used to handle the file (above code), so it calls another handler (Admin handler)
            #to handle the channel adding part. File uploads add this extra step (in this case, the AddChannel handler)
            #in between the post and the Admin handler
            admin.Admin(self.request,self.response).post(icon_key=blob_info.key())
        else:
            admin.Admin(self.request, self.response).post()
