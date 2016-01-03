import cgi
import webapp2
from google.appengine.api import users

MAIN_PAGE_HTML = """\
<html>
    <head><title>Hello Cloud (CS496 Assignment 1)</title></head>
    <body>
        <table>
            <tr>
                <td>CS 496 Assignment 1: Hello Cloud</td>
                <td>Programmed by Kelvin Watson</td>
            </tr>
        </table>
        <h4> Welcome. Please feel free to sign the guestbook.</h4>
        <form action="/sign" method="post">
            <div><textarea name="content" rows="3" cols"60"></textarea></div>
                <div><input type="submit" value="Sign Guestbook"></div>
        </form>
    </body>
</html>
"""

#request handler - processes requests and builds responses
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML) #write HTML form
        #Check for active Google account session
        #user = users.get_current_user()
        #if user:
        #    self.response.headers['Content-Type'] = 'text/plain'
        #    self.response.write('Hello, '+user.nickname())
        #else: self.redirect(users.create_login_url(self.request.uri))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')



#WSGIApplication instance routes incoming requests to handlers based on URL
#MainPage is mapped to the root URL /
#Guestbook is mapped to /sign
#!!!TODO: set debug to false before final deploy!!!
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)

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
