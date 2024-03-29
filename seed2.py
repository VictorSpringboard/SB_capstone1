from pandas import read_csv
from models import db, connect_db, User, Favorite, Match
from app import app
import datetime
import requests
import random
from sqlalchemy.exc import IntegrityError


'''
NOTE:
When coding on my computer at work, run this seed file to populate yumble.db.

'''



connect_db(app)
app.app_context().push()

def drop_create():
    db.drop_all()
    db.create_all()
drop_create()


df = read_csv('./dummy_data/usersDB_3-20.csv')
df_dict = df.to_dict('id')

for i in range(len(df_dict)):
    new = User.register_user(id=df_dict[i]['id'],
                username=df_dict[i]['username'],
                password=df_dict[i]['password'],
                email=df_dict[i]['email'],
                bio=df_dict[i]['bio'],
                img=df_dict[i]['img'])
    db.session.add(new)
    db.session.commit()
   
   
faves_db = read_csv('./dummy_data/favoritesDB_3-20.csv')
faves_df = faves_db.to_dict('id')
for i in range(len(faves_df)):
    new = Favorite.add_favorites(user_id=faves_df[i]['user_id'],
                                 recipe_id=faves_df[i]['recipe_id'],
                                 title=faves_df[i]['title'],
                                 ingredients=faves_df[i]['ingredients'],
                                 measurements=faves_df[i]['measurements'],
                                 instructions=faves_df[i]['instructions'],
                                 category=faves_df[i]['category'],
                                 area=faves_df[i]['area'],
                                 original=faves_df[i]['original'],
                                 is_top_3=faves_df[i]['is_top_3'],
                                 order=faves_df[i]['order'])
    db.session.add(new)
    db.session.commit()
    
    
matches_db = read_csv('./dummy_data/matchesDB_3-20.csv')
matches_df = matches_db.to_dict('id')

for i in range(len(matches_df)):
    new = Match.add_matches(user_id=matches_df[i]['user_id'],
                            match_id=matches_df[i]['match_id']
                                 )
    db.session.add(new)
    db.session.commit()