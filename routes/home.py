"""Routes Home"""

from extensions import db

from flask import render_template, request, flash, redirect, session, url_for, g, Blueprint
from models import db, User, Message, Likes

# Create a Blueprint instance for the routes
home = Blueprint('home', __name__)

CURR_USER_KEY = "curr_user"


##############################################################################
# User signup/login/logout

@home.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



@home.route('/')
def show_home():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    if g.user:
       
        follower_ids = [follower.id for follower in g.user.following] + [g.user.id]
        print(follower_ids)
        messages = (Message
                    .query
                    .filter(Message.user_id.in_(follower_ids))
                    .order_by(Message.timestamp.desc())
                    .limit(100)
                    .all())

        liked_msg_ids = [msg.id for msg in g.user.likes]
        

        return render_template('home.html', messages=messages, likes=liked_msg_ids)

    else:
        return render_template('home-anon.html')


@home.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
