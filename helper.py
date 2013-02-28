import webapp2
from google.appengine.api import users

class AuthenticatedRequestHandler(webapp2.RequestHandler):
    def authenticate_user(request_handler):
        user = users.get_current_user()
        if not user:
            request_handler.redirect(users.create_login_url(request_handler.request.uri))
            return []
        else:
            return [user.nickname(), users.create_logout_url(request_handler.request.uri)]
