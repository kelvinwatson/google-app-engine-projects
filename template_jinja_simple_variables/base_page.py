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
    def get(self):
        template_variables = {'foo':'The text with foo', 'bar':'BAR TEXT HERE!'}
        template = JINJA_ENVIRONMENT.get_template('helloworld.html')
        self.response.write(template.render(template_variables))
