from flask import g, Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from forms import ModelForm, LoginForm, RegisterUserForm
from models import db, connect_db, User, Favorite, Match
from secrets import API_KEY
import requests, json, random
from sqlalchemy.exc import IntegrityError



CURR_USER_KEY = 'curr_user'

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
    
@app.before_request
def add_user_to_g():
    
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.id
    

def do_logout():
    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]




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
            do_login(user)
            flash(f'Welcome back {user.username}')
            return redirect('/')
        else:
            form.username.errors = ['INVALID PASSORD!']
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    
    do_logout()
    
    flash('Goodbye')
    return redirect('/')


#####################################  User Routes  ###################################################
@app.route('/users/<user_id>/profile', methods=['GET', 'POST'])
def view_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    user_matches = Match.query.filter_by(user_id=user_id).all()
    match_matches = Match.query.filter_by(match_id=user_id).all()
    
    my_matches = [match.id for match in g.user.matches]
    their_matches = [match.id for match in user.matches]
    
    
    return render_template('user_profile.html', 
                           user=user, 
                           favorites=favorites, 
                           matches=user_matches, 
                           match_matches=match_matches,
                           my_matches=my_matches,
                           their_matches=their_matches)
    

@app.route('/users/<user_id>/favorites', methods=['GET', 'POST'])
def view_user_favorites(user_id):
    user = User.query.get_or_404(user_id)
    favorites = Favorite.query.filter_by(user_id=user_id).all()

    return render_template('favorites.html', user=user, favorites=favorites)






######################################   Match Routes   ########################################################
@app.route('/users/<user_id>/find_matches', methods=['GET', 'POST'])
def find_matches(user_id):
    user = User.query.get_or_404(user_id)
    all_users = User.query.all()
    rando_user = random.choice(all_users)
    rando_user_favs = Favorite.query.filter_by(user_id=rando_user.id)
    
    my_matches = [match.id for match in g.user.matches]
    their_matches = [match.id for match in user.matches]


    return render_template('matches.html', rando_user=rando_user, rando_user_favs=rando_user_favs,my_matches=my_matches, their_matches=their_matches)

@app.route('/users/<user_id>/another_match', methods=['GET', 'POST'])
def get_different_match(user_id):
    return redirect(f'/users/{user_id}/find_matches')

@app.route('/users/<user_id>/add_to_matches/<match_id>', methods=['GET', 'POST'])
def add_to_matches(user_id, match_id):
    user = User.query.get_or_404(user_id)
    match = User.query.get_or_404(match_id)

    g.user.matches.append(match)

    db.session.commit()

    flash('You liked a user!')
    return redirect(f'/users/{user_id}/profile')






###############################  Recipe Routes  #########################################

# @app.route('/get_a_recipe/', methods=['GET', 'POST'])
# def get_some_recipes(qry):
#     print(res)

@app.route('/recipe_details/<int:meal_id>', methods=['GET', 'POST'])
def get_details(meal_id):
    res = requests.get(f'https://www.themealdb.com/api/json/v2/{API_KEY}/lookup.php?i={meal_id}')
    res_json = res.json()
    res_dict = res_json['meals'][0]
    res_ingredients = [ing[1] for ing in res_dict.items() if 'Ingredient' in ing[0] and ing[1]]
    ingredient_measurements = [ing[1] for ing in res_dict.items() if 'Measure' in ing[0] and ing[1] is not ' ']
    ingredients_and_measurements = dict(zip(res_ingredients, ingredient_measurements))

    return render_template('recipe_details.html', details=res_dict, example_ingredients=res_ingredients)

@app.route('/recipes/<int:recipe_id>/favorite', methods=['GET', 'POST'])
def add_to_favorites(recipe_id):
    
    # if not g.user or g.user.id != user_id:
    #     flash('not authorized')
    #     return redirect('/')
    
    
    
    
    favorites = Favorite.query.filter(Favorite.user_id == g.user.id)
    favorite_ids = [favorite.recipe_id for favorite in favorites]
    
    if recipe_id not in favorite_ids:
        res = requests.get(f'https://www.themealdb.com/api/json/v2/{API_KEY}/lookup.php?i={recipe_id}')
        res_json = res.json()
        
        res_dict = res_json['meals'][0]
        res_ingredients = [ing[1] for ing in res_dict.items() if 'Ingredient' in ing[0] and ing[1]]
        ingredient_measurements = [ing[1] for ing in res_dict.items() if 'Measure' in ing[0] and (ing[1] is not None and ing[1] is not ' ')]
        ingredients_and_measurements = dict(zip(res_ingredients, ingredient_measurements))

        new_favorite = Favorite(user_id=g.user.id, recipe_id = recipe_id, 
                                title=res_dict['strMeal'],
                                ingredients=' '.join(ingredients_and_measurements.keys()),
                                measurements=' '.join(ingredients_and_measurements.values()),
                                instructions=res_dict['strInstructions'],
                                category=res_dict['strCategory'],
                                area=res_dict['strArea'],
                                original=res_dict['strSource'])
        db.session.add(new_favorite)
        
    flash('Successfully added recipe to favorites!')
    db.session.commit()
    
    return redirect('/')
        
        
        
'''
commit notes:
Current functionality
    1 - can multisearch by ingredients. Click on individual recipes to be taken to a recipe detail page. 
    2 - started working on db models. First task is:
                                            ability to add recipe to a favorites list

'''