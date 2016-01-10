import webapp2
import os
import jinja2

#Read about these properties at http://jinja.pocoo.org/docs/dev/api/
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+'/templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
    )


class HelloWorld(webapp2.RequestHandler):
    template_variables = {}

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('helloworld.html')
        self.response.write(template.render())

    def post(self):
        self.template_variables['form_content'] = {}
        template = JINJA_ENVIRONMENT.get_template('helloworld.html')
        for key in self.request.arguments():
            print('key='+str(key)+': val='+str(self.request.get(key)))
            self.template_variables['form_content'][key] = self.request.get(key)
        print('self.template_variables'+str(self.template_variables))
        self.response.write(template.render(self.template_variables))
