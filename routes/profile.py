"""Routes Profile"""

from extensions import db

from flask import render_template, request, flash, redirect, session, url_for, g, Blueprint
from forms import UserEditForm
from models import db, User, Message

# Create a Blueprint instance for the routes
profile_bp = Blueprint('profile', __name__)

CURR_USER_KEY = "curr_user"
##############################################################################
# User signup/login/logout


@profile_bp.before_request
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


##############################################################################
# General user routes:

@profile_bp.route('/')
def list_users():
    """Page with listing of users.

    Can take a 'q' param in querystring to search by that username.
    """

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/index.html', users=users)


@profile_bp.route('/<int:user_id>')
def show_user(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    # snagging messages in order from the database;
    # user.messages won't be in order by default
    messages = (Message
                .query
                .filter(Message.user_id == user_id)
                .order_by(Message.timestamp.desc())
                .limit(100)
                .all())


    return render_template('users/show.html', user=user, messages=messages)


@profile_bp.route('/<int:user_id>/following')
def show_following(user_id):
    """Show list of people this user is following."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("url_for('home.show_home')")

    user = User.query.get_or_404(user_id)
    return render_template('users/following.html', user=user)


@profile_bp.route('/<int:user_id>/followers')
def show_followers(user_id):
    """Show list of followers of this user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('users/followers.html', user=user)

@profile_bp.route('/<int:user_id>/likes')
def show_likes(user_id):
    """Show list of Likes of this User"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = User.query.get_or_404(user_id)
    liked_msg_ids = [msg.id for msg in user.likes]
    print('#############', liked_msg_ids)
    return render_template('users/likes.html', user=user)


@profile_bp.route('/follow/<int:follow_id>', methods=['POST'])
def add_follow(follow_id):
    """Add a follow for the currently-logged-in user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get_or_404(follow_id)
    g.user.following.append(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")


@profile_bp.route('/stop-following/<int:follow_id>', methods=['POST'])
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get(follow_id)
    g.user.following.remove(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")


@profile_bp.route('/profile', methods=["GET", "POST"])
def update_user():
    """Update profile for current user."""
    # user_id = session[CURR_USER_KEY]

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = g.user
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.location = form.location.data
            user.bio = form.bio.data
            user.image_url = form.image_url.data or "/static/images/default-pic.png"
            user.header_image_url = form.header_image_url.data or "/static/images/warbler-hero.jpg"
            
        flash('Wrong Pasword or Username!', 'danger')
        db.session.commit()
        return redirect(url_for('profile.show_user', user_id=user.id ))
    
    return render_template('users/edit.html', form=form)


@profile_bp.route('/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")

@profile_bp.route('/add_like/<int:message_id>', methods=["GET", "POST"])
def add_like(message_id):
    """Toggle (Like or "Dislike") a Message from a User"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    liked_message = Message.query.get_or_404(message_id)
    if liked_message.user_id == g.user.id:
        return redirect("/")

    user_likes = g.user.likes
    if liked_message in user_likes:
        g.user.likes = [like for like in user_likes if like != liked_message]
    else:
        g.user.likes.append(liked_message)

    db.session.commit()
    return redirect("/")
       

@profile_bp.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
