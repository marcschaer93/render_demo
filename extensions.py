"""Extensions for playlist app."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension


bcrypt = Bcrypt()
db = SQLAlchemy()
debug = DebugToolbarExtension()