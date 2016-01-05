import cgi
import datetime
import time
import urllib
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'kelvin_guestbook'

GUESTBOOK_PAGE_HEADER_HTML = """\
<html style="font-family:Arial">
    <head>
        <title>HELLO CLOUD (CS496 Assignment 1)</title>
        <link href="http://fonts.googleapis.com/css?family=Inconsolata" rel="stylesheet"
        type="text/css"/>
    </head>
    <body>
        <table>
            <tr>
                <th style="font-size:1.3em;border-right:solid thin green; padding-right:10px">CS 496 Assignment 1: Hello Cloud</th>
                <td style="font-size:0.9em;padding-left:10px">Programmed by Kelvin Watson</td>
            </tr>
        </table>
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
        <table width="50%" style="background-color:#9ACD32;float:left;border:solid thin green">
            <tr>
                <th style="width:36em;border-bottom:solid thin green">Past Guestbook Entries</th>
            <tr>"""


GUESTBOOK_PAGE_FOOTER_HTML = """</table></body><footer style="clear:both;"><br><div style="font-size:0.85em;clear:both;border-top:solid thin green">Last Modified: 4 Jan 2015, 19:22hr</div></footer></html>"""

def guestbook_key(guestbook_name='DEFAULT_GUESTBOOK_NAME'):
    """Constructs a Datastore key for a Guestbook entity
    The key is guestbook_name."""
    return ndb.Key('Guestbook',guestbook_name)

class Author(ndb.Model):
    """Submodel for representing an author."""
    identity = ndb.StringProperty(indexed=False)

class Greeting(ndb.Model):
    """Model for representing an individual Guestbook entry."""
    author=ndb.StructuredProperty(Author)
    content=ndb.StringProperty(indexed=False)
    date=ndb.DateTimeProperty(auto_now_add=True)

class Guestbook(webapp2.RequestHandler):
    def get(self):
        self.response.write(GUESTBOOK_PAGE_HEADER_HTML)
        #get the guestbook_name, if one isn't specified, use default_guestbook
        guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)
        #run to clean all entries
        #self.delete_all_entries(greetings)
        for greeting in greetings:
            if greeting.author:
                format = "On %a %b %d, %Y at %H:%M:%S,"
                dt = greeting.date
                dt = dt.strftime(format)
                self.response.write('<tr><td>%s <b>%s</b> wrote:' % (dt, greeting.author.identity))
            else: self.response.write('An anonymous person wrote:')
            self.response.write('<blockquote style="font-style:italic">%s</blockquote></td></tr>' %cgi.escape(greeting.content))
        sign_query_params = urllib.urlencode({'guestbook_name':guestbook_name})
        self.response.write(GUESTBOOK_PAGE_FOOTER_HTML)

    def post(self):
        guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        greeting.author = Author(identity=self.request.get('nick_name'))
        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/guestbook')

    def delete_all_entries(self, greetings):
        if greetings is not None:
            for greeting in greetings: greeting.key.delete()

app = webapp2.WSGIApplication([
    ('/guestbook', Guestbook),
], debug=True)
