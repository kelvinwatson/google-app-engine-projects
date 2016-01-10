import cgi
import json
import time
import webapp2
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
    </head>
    <body>
        <table>
            <tr>
                <th style="font-size:1.3em;border-right:solid thin green; padding-right:10px">CS 496 Assignment 1: Hello Cloud</th>
                <td style="font-size:0.9em;padding-left:10px">Programmed by Kelvin Watson</td>
            </tr>
        </table>
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
    <p><a href="http://hellocloud-1179.appspot.com">Back to Home</a>
    </body>
    <footer style="clear:both;"><br><div style="font-size:0.85em;clear:both;border-top:solid thin green">Last Modified: 4 Jan 2015, 19:22hr</div></footer>
</html>
"""

#request handler - processes requests and builds responses
class Weather(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)

    def post(self):
        self.html_top()
        #Source: https://cloud.google.com/appengine/docs/python/tools/webapp/requestclass
        city="OR/"+str(self.request.get("city"))
        url = "http://api.wunderground.com/api/c64e493b9a36a7b7/conditions/q/"+city+".json"
        try:
            result = urlfetch.fetch(url)
            parsed = json.loads(result.content)
            c = parsed['current_observation']
            print()
            if c is not None:
                self.response.write("The current weather in "+str(c['display_location']['city'])+ " is:<br>")
                self.response.write('<table><tr>')
                self.response.write('<td><br>'+c['weather']+' '+c['temperature_string'])
                self.response.write('<br><em>Feels like</em> '+c['feelslike_string']+'<td>')
                self.response.write('<td>'+'<img src="'+c['icon_url']+'">'+'</td>')
                self.response.write('</tr></table>')
        except Exception as e:
            print(e)
            self.response.write("Sorry, there is no weather information available for this city.")
        self.response.write('<br><a href="http://hellocloud-1179.appspot.com/weather">Back to Weather</a>')
        self.response.write('<br><a href="http://hellocloud-1179.appspot.com">Back to Home</a>')
        self.html_bottom()

    def html_top(self):
        self.response.write('<html style="font-family:Arial">\
            <head><title>HELLO CLOUD (CS496 Assignment 1)</title></head>\
                <body>\
                <table>\
                    <tr>\
                        <th style="font-size:1.3em;border-right:solid thin green; padding-right:10px">CS 496 Assignment 1: Hello Cloud</th>\
                        <td style="font-size:0.9em;padding-left:10px">Programmed by Kelvin Watson</td>\
                    </tr>\
                </table>\
                <h4 style="border-bottom:solid thin green">WEATHER</h4>')

    def html_bottom(self):
        self.response.write('</body></html>')

#def html_top(self):
#    self.response.write('<html>')

#def html_bottom(self):
#    self.response.write('</html>')

#WSGIApplication instance routes incoming requests to handlers based on URL
#MainPage is mapped to the root URL /
#Guestbook is mapped to /sign
#!!!TODO: set debug to false before final deploy!!!
app = webapp2.WSGIApplication([
    ('/weather',Weather),
], debug=False)
