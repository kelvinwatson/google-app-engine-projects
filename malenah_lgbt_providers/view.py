import base
import log as console
from datetime import datetime

class ViewHandler(base.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request,response)
        console.log(datetime.now().time())
        self.template_values = {
            'title': "Record Added",
            'header_title': "You added the following record:",
            'last_accessed': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            }

    def get(self):
        #get the key
        #get the entity using key.get()
        self.render('view.html', self.template_values) #call the overridden render (above)
