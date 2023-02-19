from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from forms import ModelForm, LoginForm, RegisterUserForm, SearchForm
from models import db, connect_db, User
from secrets import API_KEY
import requests, json

app = Flask(__name__)

# home db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/yumble'

# work db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yumble.db'

# test db
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate_user(username, password)
        if user:
            flash(f'Welcome back {user.username}')
            session['username'] = user.username
            return redirect('/')
        else:
            form.username.errors = ['INVALID PASSORD!']
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    flash('Goodbye')
    return redirect('/')


###############################  Recipe Routes  #########################################

# @app.route('/get_a_recipe/', methods=['GET', 'POST'])
# def get_some_recipes(qry):
#     print(res)

@app.route('/recipe_details/<int:meal_id>', methods=['GET', 'POST'])
def get_details(meal_id):
    res = requests.get(f'https://www.themealdb.com/api/json/v2/{API_KEY}/lookup.php?i={meal_id}')
    example_dict = res.json()
    example_ingredients = [ing[1] for ing in example_dict['meals'][0].items() if 'Ingredient' in ing[0] and ing[1]]

    return render_template('recipe_details.html', details=example_dict, example_ingredients=example_ingredients)
