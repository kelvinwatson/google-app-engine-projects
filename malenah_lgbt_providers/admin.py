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
