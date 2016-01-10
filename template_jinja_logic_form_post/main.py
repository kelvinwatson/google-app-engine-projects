import webapp2

#WSGIApplication instance routes incoming requests to handlers based on URL
#MainPage is mapped to the root URL /
#Guestbook is mapped to /sign
#!!!TODO: set debug to false before final deploy!!!
application = webapp2.WSGIApplication([
    ('/', 'base_page.HelloWorld'),
], debug=True)
