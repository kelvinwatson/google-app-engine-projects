import webapp2
import ProviderHandler as PH
import ReviewHandler as RH

#WSGIApplication instance routes incoming requests to handlers based on URL
#TODO: set debug to false before final deploy

routes = [
    webapp2.Route(r'/provider/<pid:[0-9]+><:/?>', handler=PH.ProviderHandler, name='provider-list'),
    webapp2.Route(r'/provider<:/?>', handler=PH.ProviderHandler, name='provider-list'),
    webapp2.Route(r'/review/<revid:[0-9]+>/<repid:[0-9]+><:/?>', handler=RH.ReviewHandler, name='review-list'),
    webapp2.SimpleRoute(r'/review/?', handler=RH.ReviewHandler, name='review-list'),
    webapp2.Route(r'/review', handler=RH.ReviewHandler, name='review-list'),
    webapp2.Route(r'/', handler=RH.ReviewHandler, name='provider-list'),
]

application = webapp2.WSGIApplication(routes, debug=True)
