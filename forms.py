from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField 
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
    email = StringField('Email')
    bio = StringField('bio')
    img = StringField('Image link')
    
class MessageForm(FlaskForm):
    message = TextAreaField('Message')
    submit = SubmitField('Send message')

class EditProfileForm(FlaskForm):

    username = StringField('Username')
    email = StringField('E-mail')
    bio = StringField('Bio')
    img = StringField('Image URL')
    password = PasswordField('Confirm password')
    submit = SubmitField('Save changes')
    
class FavoriteChoice(FlaskForm):
    
    fav_choice = BooleanField()
    