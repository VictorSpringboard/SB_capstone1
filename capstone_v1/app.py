from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from forms import ModelForm, LoginForm, RegisterUserForm
from models import db, connect_db, User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/yumble'
app.config['SQLALCHEMY_BINDS'] = {'testDB': 'sqlite:///test_yumble.db'}

app.debug = False
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
    


@app.route('/')
def home():
    return render_template('home.html')



#################### Register/Login/Logout Routes ####################
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        
        register_new_user = User.register_user(username, password, email)
        
        db.session.add(register_new_user)
            
        try:
            db.session.commit()
            
        except IntegrityError:
            form.user.errors.append('Username already exists. Please choose another')
            return render_template('register.html')
        flash('SUCCESS! USER CREATED')
        return redirect('/')
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    flash('Goodbye')
    return redirect('/')
