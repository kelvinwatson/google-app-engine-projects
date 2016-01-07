import datetime
import webapp2
from google.appengine.ext import db

MAIN_PAGE_HTML = """
<html>
    <head>
        <title>Culturally-Competent Healthcare Providers</title>
    </head>
    <h1>Close the Health Disparity Gap</h1>
    <p>Add yourself to the growing list of providers who aim to provide
    quality care to LGBT people</p>
    <body>
        <form>
        </form>
    </body>
</html>"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type']='text/plain'
        self.response.write('Hello Kelvin!')

class Doctor(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    building_number = db.StringProperty()
    street_number = db.StringProperty()
    street_name = db.StringProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    zipcode = db.StringProperty()
    add_date = db.DateProperty()


app = webapp2.WSGIApplication([('/',MainPage),],debug=True)
