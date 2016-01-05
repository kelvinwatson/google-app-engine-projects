import cgi
import urllib
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'kelvin_guestbook'

GUESTBOOK_PAGE_HEADER_TEMPLATE = """\
<html>
    <body>
        <table>
            <tr>
                <th style="font-size:1.3em;border-right:solid thin green; padding-right:10px">CS 496 Assignment 1: Hello Cloud</th>
                <td style="font-size:0.9em;padding-left:10px">Programmed by Kelvin Watson</td>
            </tr>
        </table>
        <h4 style="width:36em;border-bottom:solid thin green">Guestbook</h4>\
        <p>Please feel free to sign my guestbook</p>
        <form action="/guestbook" method="post">
          <input type="text" name="nick_name" placeholder="Nickname" style="width:200px"><br>
          <textarea name="content" rows="3" placeholder="Your comment here" style="width:200px"></textarea><br>
          <div><input type="submit" value="Sign Guestbook"></div>
        <h4 style="width:36em;border-bottom:solid thin green">Past Guestbook Entries</h4>"""


GUESTBOOK_PAGE_FOOTER_TEMPLATE = """\
  </body>
</html>"""

def guestbook_key(guestbook_name='DEFAULT_GUESTBOOK_NAME'):
    """Constructs a Datastore key for a Guestbook entity
    The key is guestbook_name."""
    return ndb.Key('Guestbook',guestbook_name)

class Author(ndb.Model):
    """Submodel for representing an author."""
    identity = ndb.StringProperty(indexed=False)

class Greeting(ndb.Model):
    """Main model for representing an individual Guestbook entry."""
    author=ndb.StructuredProperty(Author)
    content=ndb.StringProperty(indexed=False)
    date=ndb.DateTimeProperty(auto_now_add=True)

class Guestbook(webapp2.RequestHandler):
    def get(self):
        self.response.write(GUESTBOOK_PAGE_HEADER_TEMPLATE)

        #get the guestbook_name, if one isn't specified, use default_guestbook
        guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)
        print("GREETINGS="+str(greetings))
        for greeting in greetings:
            if greeting.author:
                self.response.write('<b>%s</b> wrote:' % greeting.author.identity)
            else: self.response.write('An anonymous person wrote:')
            self.response.write('<blockquote>%s</blockquote>' %cgi.escape(greeting.content))
        sign_query_params = urllib.urlencode({'guestbook_name':guestbook_name})
        self.response.write(GUESTBOOK_PAGE_FOOTER_TEMPLATE)

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        greeting.author = Author(identity=self.request.get('nick_name'))
        greeting.content = self.request.get('content')
        greeting.put()

        #query_params = {'guestbook_name': guestbook_name}
        self.redirect('/guestbook')

app = webapp2.WSGIApplication([
    ('/guestbook', Guestbook),
], debug=True)
