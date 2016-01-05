import cgi
import json
import time
import urllib
import webapp2
import guestbook
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import urlfetch

#Sources:
#http://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/dynamic.html
#http://www.plus2net.com/javascript_tutorial/clock.php

MAIN_PAGE_HEADER_HTML = """\
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
        <p>Welcome! This dynamic website was made using Google App Engine (Python) and features a running digital clock, interaction with the
        wunderground.org weather API, and a guestbook.</p>
        <h4 style="border-bottom:solid thin green;">DIGITAL CLOCK</h4>
        It is currently <span id="clock" style="font-family:Inconsolata, Arial, Helvetica, san-serif;"></span>
        <script type="text/javascript">window.onload=refreshClock();</script> on
        <span id="day"></span>
        <h4 style="border-bottom:solid thin green">WEATHER</h4>
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
                <h4 style="border-bottom:solid thin green">GUESTBOOK</h4>\
                <table width="50%" style="float:left">
                    <tr>
                        <td>Please feel free to sign my guestbook
                        <form action="/guestbook" method="post">
                            <input type="text" name="nick_name" placeholder="Nickname" style="width:200px" required><br>
                            <textarea name="content" rows="3" placeholder="Your comment here" style="width:200px" required></textarea><br>
                            <input type="submit" value="Sign Guestbook">
                        </form>
                        </td>
                    <tr>
                </table>
                <table width="50%" style="float:left">
                    <tr>
                        <th style="width:36em;border-bottom:solid thin green">Past Guestbook Entries</th>
                    <tr>"""

MAIN_PAGE_FOOTER_HTML = """</table></body></html>"""

#request handler - processes requests and builds responses
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HEADER_HTML)
        self.display_guestbook_entries()
        self.response.write(MAIN_PAGE_FOOTER_HTML)

    def display_guestbook_entries(self):
        guestbook_name = self.request.get('guestbook_name',guestbook.DEFAULT_GUESTBOOK_NAME)
        greetings_query = guestbook.Greeting.query(
            ancestor=guestbook.guestbook_key(guestbook_name)).order(-guestbook.Greeting.date)
        greetings = greetings_query.fetch(10)
        for greeting in greetings:
            if greeting.author:
                format = "On %a %b %d, %Y at %H:%M:%S,"
                dt = greeting.date
                dt = dt.strftime(format)
                self.response.write('<tr><td>%s <b>%s</b> wrote:' % (dt, greeting.author.identity))
            else: self.response.write('An anonymous person wrote:')
            self.response.write('<blockquote style="font-style:italic">%s</blockquote></td></tr>' %cgi.escape(greeting.content))
        sign_query_params = urllib.urlencode({'guestbook_name':guestbook_name})
        self.response.write(MAIN_PAGE_FOOTER_HTML)


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
