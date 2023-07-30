import os

from flask import Flask, session, g, Blueprint
from extensions import db, debug, bcrypt
# from routes import main
from models import User

from routes.home import home
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.message import message_bp

# Config
CURR_USER_KEY = "curr_user"

###############################################################################################
# CREATE_APP

def create_app():
    app = Flask(__name__)
    
    # Get DB_URI from environ variable (useful for production/testing) or,
    # if not set there, use development local db.
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        os.environ.get('DATABASE_URL', 'postgresql:///render_demo'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

    # Load configuration and set up other app settings (if needed)

    # Initialize the database, debugToolbar
    db.init_app(app)
    debug.init_app(app)
    bcrypt.init_app(app)

 
    # Import and register blueprints
    # app.register_blueprint(main, url_prefix="")
    app.register_blueprint(home, url_prefix="")
    app.register_blueprint(auth_bp, url_prefix="")
    app.register_blueprint(profile_bp, url_prefix="/users")
    app.register_blueprint(message_bp, url_prefix="/messages")

    with app.app_context():
        db.create_all()

    # Import and register Blueprints (if you have any)
    # Example:
    # from .blueprints import some_blueprint
    # app.register_blueprint(some_blueprint)

    return app



# Call the create_app function to get the Flask app instance
app = create_app()


if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True)




    # postgres://render_demo_3m9m_user:bguGf8HLKkk7xOoqr3aeAACubVKfkRZm@dpg-cj38bp18g3n1jki1gt40-a.frankfurt-postgres.render.com/render_demo_3m9m