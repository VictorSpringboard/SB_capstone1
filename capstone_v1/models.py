from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

    
    