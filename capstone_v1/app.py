from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from models import db, connect_db


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/yumble'
app.config['SQLALCHEMY_BINDS'] = {'testDB': 'sqlite:///test_yumble.db'}

app.debug = False
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
    

# USER-RELATED ROUTES
@app.route('/')
def home():
    return 'fart'
