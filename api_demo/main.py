import webapp2

app = webapp2.WSGIApplication([
    ('/mod', 'mod.Mod'), #one basic route
], debug=True)
app.router.add(webapp2.Route(r'/mod/<id:[0-9]+><:/?>', 'mod.Mod'))
app.router.add(webapp2.Route(r'/mod/search', 'mod.ModSearch'))
app.router.add(webapp2.Route(r'/channel', 'channel.Channel'))
app.router.add(webapp2.Route(r'/channel/<cid:[0-9]+>/mod/<mid:[0-9]+><:/?>', 'channel.ChannelMods'))

#Missing restful components:
#missing URI's navigate?
#no cache properties sent out
