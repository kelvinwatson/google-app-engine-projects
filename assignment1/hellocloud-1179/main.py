import webapp2
from google.appengine.api import users

#request handler - processes requests and builds responses
class MainPage(webapp2.RequestHandler):
    def get(self):
        #Check for active Google account session
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Hello, '+user.nickname())
        else: self.redirect(users.create_login_url(self.request.uri))
        #self.response.write('\n' + str(self.response))
                    
#WSGIApplication instance routes incoming requests to handlers based on URL
#MainPage is mapped to the root URL /
#!!!TODO: set debug to false before final deploy!!!
app = webapp2.WSGIApplication([('/', MainPage),], debug=True)


#"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
#from flask import Flask
#app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


#@app.route('/')
#def hello():
#    """Return a friendly HTTP greeting."""
#    return 'Hello World!'


#@app.errorhandler(404)
#def page_not_found(e):
#    """Return a custom 404 error."""
#    return 'Sorry, Nothing at this URL.', 404


#@app.errorhandler(500)
#def application_error(e):
#    """Return a custom 500 error."""
#    return 'Sorry, unexpected error: {}'.format(e), 500
