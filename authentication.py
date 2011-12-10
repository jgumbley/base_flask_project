from flask import Response
from functools import wraps
from flaskext.oauth import OAuth
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from flask.blueprints import Blueprint
from flask.globals import g
from flask.helpers import flash

# blueprint for authenication pages
from orm import User

authweb = Blueprint('authweb', __name__)

# TWITTER AUTH STUFF:

# OAuth config:
oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='http://api.twitter.com/1/',
    request_token_url='http://api.twitter.com/oauth/request_token',
    access_token_url='http://api.twitter.com/oauth/access_token',
    authorize_url='http://api.twitter.com/oauth/authenticate',
    consumer_key='u9ePtkkR3z9zYicizhzdQ',
    consumer_secret='is1UoQghHUz3k2CjpzSnkgqWPxojuvvzWBOiSWLUWs'
)

@twitter.tokengetter
def get_twitter_token():
    return session.get('twitter_token')

# pages for twitter auth:

@authweb.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session["user"] = User(resp['screen_name'], resp['user_id'])
    session['twitter_user'] = resp['screen_name']
    session['twitter_user_id'] = resp['user_id']
    return redirect(next_url)

@authweb.route('/login')
def login():
    return twitter.authorize(callback=url_for('authweb.oauth_authorized',
            next=request.args.get('next') or request.referrer or None))

# ADMIN AUTH STUFF

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'fiveninesix'

def local_authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('twitter_user') is None:
            return redirect(url_for('authweb.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return local_authenticate()
        return f(*args, **kwargs)
    return decorated