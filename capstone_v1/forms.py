from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateTimeField, BooleanField
from wtforms_alchemy import model_form_factory
from models import db, User
from wtforms.validators import InputRequired


BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class RegisterUserForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    email = StringField('Email address') 
    
class SearchForm(FlaskForm):
    search_string = StringField('Search recipes!')