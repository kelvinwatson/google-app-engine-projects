import base
import log as console

class EditHandler(base.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request,response)
        self.template_values = {
            'title': "Edit Record (MALENAH Administrator Portal)",
            'header_title': "Edit Record",
            'last_accessed': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
            }

    def get(self):
        t = {}
        k = ndb.Key(urlsafe=self.request.get('key')) #get key string and construct key
        e = k.get()
        self.template_values['first_name'] = e.first_name #set template values
        self.template_values['last_name'] = e.last_name
        self.template_values['phone'] = e.phone
        self.template_values['email'] = e.email
        self.template_values['website'] = e.website
        self.template_values['best_time'] = e.best_time
        self.template_values['designation'] = ndb.Key(urlsafe=e.designation).get().name             #e.designation == key, use .get() to get entity, and .name to get the entity's name property
        self.template_values['services'] = e.services #TODO: on view.html, just needs to display, not prepopulate with checks
        base.BaseHandler.render(self, 'edit.html', self.template_values) #call the overridden render (above)
