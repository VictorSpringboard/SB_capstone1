from models import db, connect_db, User, Favorite, Grocery, Match
from app import app
import datetime
import requests
from secrets import API_KEY
from sqlalchemy.exc import IntegrityError

connect_db(app)
app.app_context().push()

def drop_create():
    db.drop_all()
    db.create_all()



users = [
    {
        'id': 151,
        'username': 'test',
        'password': 'test',
        'email': 'test@test.com',
        'bio': 'I am a test user. I love to test things. Testing is fun',
        'img': 'https://thumbs.dreamstime.com/b/student-trying-to-cheat-test-male-class-34669006.jpg'
    },
    {
        'id': 152,
        'username': 'HankHill',
        'password': 'propane',
        'email': 'hank@strickland.com',
        'bio': 'I sell propane and propane accessories. I love mowing lawns and using WD-40',
        'img': 'https://play-lh.googleusercontent.com/iQaRYz9z_TsVyyzjtpaJ73ms9RPiT4e_UB5DOndoPmxIQ10LU5jGubR1X7hVI1U-_wM'
    },
    {
        'id': 153,
        'username': 'PeggyHill',
        'password': 'boggle',
        'email': 'peggy@boggle.com',
        'bio': 'I am a substitute spanish teacher at Tom Landry Middle School. I love boggle and playing softball',
        'img': 'https://static.tvtropes.org/pmwiki/pub/images/char_6989_4107.jpg'
    },
    {
        'id': 154,
        'username': 'BobbyHill',
        'password': 'comedy',
        'email': 'bobby@thatsmypurse.com',
        'bio': 'I am an amateur comedian and I like to hang out with my friends Connie and Joseph',
        'img': 'https://imgix.ranker.com/list_img_v2/14514/2754514/original/bobby-hill-feminist-hero'
    },
    {
        'id':155,
        'username': 'Boomhauer',
        'password': 'dang',
        'email': 'dangole@talkinbout.com',
        'bio': "Dang ole, tawmbout. Dang ole...biography",
        'img': 'https://upload.wikimedia.org/wikipedia/en/b/be/Jeff_Boomhauer.png'
    },
]

def set_users():

    for user in users:
        new = User.register_user(
                    id=user['id'],
                    username=user['username'],
                    pwd=user['password'],
                    email=user['email'],
                    bio=user['bio'],
                    img=user['img'])
        db.session.add(new)
        db.session.commit()




def get_meal_data():
    res = requests.get(f'https://www.themealdb.com/api/json/v2/{API_KEY}/randomselection.php')
    res_json = res.json()

    res_dict = res_json['meals']


    # breakpoint()
    return res_dict




def set_favs():
    for i in range(1, 156):
        example = get_meal_data()
        for recipe in example:
            new = Favorite(user_id=i, 
                        recipe_id=recipe['idMeal'], 
                        title=recipe['strMeal'],
                        ingredients='example of ingredients',
                        measurements='example of measurements',
                        instructions=recipe['strInstructions'],
                        category=recipe['strCategory'],
                        area=recipe['strArea'],
                        original='example',
                        )
            db.session.add(new)
            db.session.commit()

matches = [
    (151, 152),
    (151, 45),
    (152, 154),
    (152, 67),
    (152, 33),
    (153, 152),
    (153, 56),
    (154, 153),
    (154, 1),
    (155, 154),
    (155, 30)
]

def set_matches():
    for user, match in matches:
        new = Match(user_id=user, match_id=match)
        db.session.add(new)
        db.session.commit()

def clear_matches():
    for user, match in matches:
        new = Match(user_id=0, match_id=0)
        db.session.add(new)
        db.session.commit()



# drop_create()

# set_users()
set_favs()                                                    
# set_matches()
# clear_matches()