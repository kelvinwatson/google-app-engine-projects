import cgi
import json
import time
import urllib
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import urlfetch

#Sources:
#http://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/dynamic.html
#http://www.plus2net.com/javascript_tutorial/clock.php

weatherStr="no weather yet"

MAIN_PAGE_HTML = """\
<html style="font-family:Arial">
    <head>
        <title>HELLO CLOUD (CS496 Assignment 1)</title>
        <link href="http://fonts.googleapis.com/css?family=Inconsolata" rel="stylesheet"
        type="text/css"/>
        <script type="text/javascript">
    function refreshClock(){
        var t = new Date();
        var y = t.getFullYear();
        var m = t.getMonth();
        var mos = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        var d = t.getDate();
        var day = t.getDay();
        var days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
        var hr = t.getHours();
        hr = (hr>12)?hr-12:hr;
        hr = (hr==0)?12:hr;
        var min = t.getMinutes();
        min = (min<10?"0":"")+min;
        var sec = t.getSeconds();
        sec = (sec<10?"0":"")+sec;
        var meridiem=(hr<12)?"AM":"PM";
        day = days[day]+' ' +mos[m]+' ' +d+' '+y
        document.getElementById("day").innerHTML=day;
        time = hr+":"+min+":"+sec+" "+meridiem;
        document.getElementById("clock").innerHTML=time;
        setTimeout(refreshClock,1000);
    }</script>
    </head>
    <body onload="refreshClock(); setInterval('refreshClock()',1000)">
        <table>
            <tr>
                <th style="font-size:1.3em;border-right:solid thin green; padding-right:10px">CS 496 Assignment 1: Hello Cloud</th>
                <td style="font-size:0.9em;padding-left:10px">Programmed by Kelvin Watson</td>
            </tr>
        </table>
        <h4 style="width:36em;border-bottom:solid thin green;">Digital Clock</h4>
        It is currently <span id="clock" style="font-family:Inconsolata, Arial, Helvetica, san-serif;"></span>
        <script type="text/javascript">window.onload=refreshClock();</script> on
        <span id="day"></span>
        <h4 style="width:36em;border-bottom:solid thin green">Weather</h4>
        <p>To view the current weather in Oregon, complete the following:
        <form action="/weather" method="post">
            <select name="city">
                <option value="Aloha">Aloha</option>
                <option value="Beaverton">Beaverton</option>
                <option value="Cedar_Hills">Cedar Hills</option>
                <option value="Cedar_Mill">Cedar Mill</option>
                <option value="Gladstone">Gladstone</option>
                <option value="Gresham">Gresham</option>
                <option value="Hillsboro">Hillsboro</option>
                <option value="Lake_Oswego">Lake Oswego</option>
                <option value="Milwaukie">Milwaukie</option>
                <option value="Oak_Grove">Oak Grove</option>
                <option value="Oregon_City">Oregon City</option>
                <option value="Portland" selected="selected">Portland</option>
                <option value="Tigard">Tigard</option>
                <option value="Tualatin">Tualatin</option>
                <option value="West_Linn">West Linn</option>
            </select>
            <input type="submit" value="Submit">
        </form>
        <p>You can also go to <a href="/weather">hellocloud-1179.appspot.com/weather</a> to get today's weather.</p>
        <!--<p id="weather">The weather today is %s</p>-->

        <h4 style="width:36em;border-bottom:solid thin green">Guestbook</h4>
        <p>Please feel free to sign my guestbook</p>
        <form action="/guestbook" method="post">
            <input type="text" name="nickName" placeholder="Nickname" style="width:200px"><br>
            <textarea name="content" rows="3" style="width:200px"></textarea><br>
            <input type="submit" value="Sign Guestbook">
        </form>
    </body>
</html>
""" #%(weatherStr)

#request handler - processes requests and builds responses
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)
        #Check for active Google account session
        #user = users.get_current_user()
        #if user:
        #    self.response.headers['Content-Type'] = 'text/plain'
        #    self.response.write('Hello, '+user.nickname())
        #else: self.redirect(users.create_login_url(self.request.uri))

#class Guestbook(webapp2.RequestHandler):
#    def post(self):
#        self.response.write('<html><body>You wrote:<pre>')
#        self.response.write(cgi.escape(self.request.get('content')))
#        self.response.write('</pre></body></html>')

class CatchAll(webapp2.RequestHandler):
    def get(self):
        self.response.write('Invalid URL. Click <a href="/">here</a> to go to the home page.')


#WSGIApplication instance routes incoming requests to handlers based on URL
#MainPage is mapped to the root URL /
#Guestbook is mapped to /sign
#!!!TODO: set debug to false before final deploy!!!
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('.*', CatchAll),
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
