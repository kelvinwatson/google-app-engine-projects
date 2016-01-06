import datetime
import webapp2
from google.appengine.ext import ndb

MAIN_PAGE_HTML = """
<html style="font-family:Arial">
    <head>
        <title>Culturally-Competent Healthcare Providers</title>
    </head>
    <h1>Close the LGBT Health Disparity Gap</h1>
    <p>Add yourself to the growing list of providers who aim to provide
    quality care to LGBT people</p>
    <body>
        <form action="/" method="post">
            First name:<br><input type="text" name="firstname"><br>
            Last name:<br><input type="text" name="lastname"><br>
            Profession: <select name="profession">
                <option value="Physician">Physician</option>
                <option value="Dentist">Dentist</option>
                <option value="Pharmacist">Pharmacist</option>
                <option value="Counselor">Counselor</option>
            </select>
            <br><input type="reset" value="Reset" style="background-color:pink">
            <input type="submit" value="Submit">
        </form>
    </body>
</html>"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type']='text/plain'
        self.response.write(MAIN_PAGE_HTML)
        print("===TEST Query1===")
        results = Doctor.query().order(Doctor.last_name).fetch(10) #returns all Doctor objects
        for r in results:
            print(str(r.key)+" first_name="+r.first_name+" last_name="+r.last_name)
        print("===TEST Query1.1===")
        results = Doctor.query().order(-Doctor.last_name).fetch(10) #returns all Doctor objects
        for r in results:
            print(str(r.key)+" first_name="+r.first_name+" last_name="+r.last_name)
        print("===TEST Query2===")
        results = Doctor.query(Doctor.first_name == 'Jason').fetch(10)
        for r in results:
            print(str(r.key)+" first_name="+r.first_name)
        print("===TEST Query3===")
        results = Doctor.query(Doctor.first_name != 'Kelvin').fetch(10)
        for r in results:
            print(str(r.key)+" first_name="+r.first_name)
        print("===TEST Query4===")
        results = Doctor.query(Doctor.first_name.IN(['Jason','Bryce'])).fetch(10)
        for r in results:
            print(str(r.key)+" first_name="+r.first_name)

    def post(self):
        e = Doctor()
        e.first_name = self.request.get('firstname')
        e.last_name = self.request.get('lastname')
        e.profession = self.request.get('profession')
        e.add_date = datetime.datetime.now().date()
        print(e.first_name+" "+e.last_name+" "+e.profession+" "+str(e.add_date))
        e.put()
        self.redirect('/thanks')

class Doctor(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    profession = ndb.StringProperty()
    #company = db.StringProperty()
    #building_number = db.StringProperty()
    #street_number = db.StringProperty()
    #street_name = db.StringProperty()
    #city = db.StringProperty()
    #state = db.StringProperty()
    #country = db.StringProperty()
    #zipcode = db.StringProperty()
    add_date = ndb.DateProperty()


app = webapp2.WSGIApplication([('/',MainPage),],debug=True)
