from flask import g, Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from forms import LoginForm, RegisterUserForm, MessageForm, EditProfileForm, FavoriteChoiceForm
from models import db, connect_db, User, Favorite, Match, Message
import requests, json, random
from sqlalchemy.exc import IntegrityError
from flask_bootstrap import Bootstrap
import os

'''
March 16 commit notes:

Current Plan:

Abandon JS solutions. Try an 'edit individual favorite' page. You can choose whether its a top or not, then choose to delete it
if you want. Just 2 options, top 3 and delete. 
'''




CURR_USER_KEY = 'curr_user'
API_KEY = 9973533

app = Flask(__name__)
bootstrap = Bootstrap()
# home db
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:admin@localhost/yumble')

# work db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yumble.db'

# test db
app.config['SQLALCHEMY_BINDS'] = {'testDB': 'sqlite:///test_yumble.db'}
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///yumble.db')

app.debug = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'my_secret')
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
    pass
    

def do_logout():
    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    flash('LOGGED OUT')
    return redirect('/login')



@app.route('/')
def home():
    return render_template('home.html')



#################### Register/Login/Logout Routes ####################
@app.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegisterUserForm()
    last_user_added = User.query.order_by(User.id.desc()).first()
    if form.validate_on_submit():
        # try:
            new_user = User.register_user(
                                        id=last_user_added.id + 1,
                                        username=form.username.data,
                                        password=form.password.data,
                                        email=form.email.data,
                                        bio=form.bio.data,
                                        img=form.img.data
                                        )
            db.session.commit()
            
        # except IntegrityError:
        #     flash('Username already exists. Please choose another')
        #     return render_template('register.html', form=form)
        
            do_login(new_user)
        
            return redirect('/')
    
    else:
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
    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    
    flash('Goodbye')
    return redirect('/')


#####################################  User Routes  ###################################################

@app.route('/users/<user_id>/show_likes', methods=['GET', 'POST'])
def show_liking(user_id):
    '''Show a list of people this user likes'''

    user = User.query.get_or_404(user_id)
    return render_template('user_likes.html', user=user)


@app.route('/users/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    
    form = EditProfileForm()
    
    if form.validate_on_submit():
        g.user.username = form.username.data if form.username.data else g.user.username
        g.user.email = form.email.data if form.email.data else g.user.email
        g.user.bio = form.bio.data if form.bio.data else g.user.bio
        g.user.img = form.img.data if form.img.data else g.user.img
        
        if g.user == g.user.authenticate_user(g.user.username, form.password.data):
            db.session.add(g.user)
            db.session.commit()
            flash('Profile successfully edited')
            return redirect(f'/users/{g.user.id}/profile')
        else:
            flash('wrong password')
            return redirect(f'/users/{g.user.id}/profile')
            
    return render_template('edit_profile.html', form=form)


@app.route('/users/<user_id>/profile', methods=['GET', 'POST'])
def view_user_profile(user_id):
    
    user = User.query.get_or_404(user_id)
    favorites = Favorite.query.filter_by(user_id=user_id).all()



    return render_template('user_profile.html', 
                                user=user, 
                                favorites=favorites)












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
@app.route('/users/<user_id>/favorites', methods=['GET', 'POST'])
def view_user_favorites(user_id):
    user = User.query.get_or_404(user_id)
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    ordered_favorites = sorted(favorites, key=lambda x: x.order)


    return render_template('show_favorites.html', user=user, favorites=ordered_favorites)

@app.route('/users/<user_id>/edit_favorites', methods=['GET', 'POST'])
def edit_favorites(user_id):
    user_id = g.user.id
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    ordered_favorites = sorted(favorites, key=lambda x: x.order)

    form = FavoriteChoiceForm()


    return render_template('edit_favorites_order.html', favorites=ordered_favorites, form=form)


@app.route('/users/<int:user_id>/favs/<int:fav_id>/edit_fav', methods=['GET', 'POST'])
def edit_individual_fav(user_id, fav_id):

    fav = Favorite.query.filter_by(recipe_id=fav_id, user_id=user_id).all()
    form = FavoriteChoiceForm()
    return render_template('edit_fav.html', fav=fav, form=form)

@app.route('/users/<user_id>/get_favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get_or_404(user_id)
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    all_favs = [fav.getTitles() for fav in favorites]
    
    return jsonify(all_favs=all_favs)


  
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
                                original=res_dict['strSource'],
                                is_top_3=False,
                                # NEED TO FIX THIS. Order isn't 0 anymore, I seeded the db with the actual orders.
                                # this is going to make a weird bug I bet. 
                                order=0)
        db.session.add(new_favorite)
        
    flash('Successfully added recipe to favorites!')
    db.session.commit()
    
    return redirect('/')



    
    

        
#####################################   Message Routes   #############################################
@app.route('/users/<int:user_id>/messages')
def view_messages(user_id):
    user_id = g.user.id
    messages = g.user.received_msgs.all()
    
    return render_template('view_messages.html', messages=messages)

@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=g.user, recipient=user, body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        return redirect(f'/users/{g.user.id}/profile')
    return render_template('send_message.html', form=form, recipient=user)

@app.route('/users/<int:message_id>/delete_message', methods=['GET', 'POST'])
def delete_message(message_id):
    
    user_id = g.user.id
    msg = Message.query.get(message_id)
    db.session.delete(msg)
    db.session.commit()
    
    return redirect(f'/users/{user_id}/messages')