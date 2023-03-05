from pandas import read_csv
from models import db, connect_db, User, Favorite, Match
from app import app
import datetime
import requests
from sqlalchemy.exc import IntegrityError

connect_db(app)
app.app_context().push()

def drop_create():
    db.drop_all()
    db.create_all()
# drop_create()


# df = read_csv('users_db.csv', index_col='id')
# df_dict = df.to_dict('id')

# for i in range(1, 156):
#     new = User.register_user(id=i,
#                 username=df_dict[i]['username'],
#                 pwd=df_dict[i]['password'],
#                 email=df_dict[i]['email'],
#                 bio=df_dict[i]['bio'],
#                 img=df_dict[i]['img'])
#     db.session.add(new)
#     db.session.commit()
   
   
# faves_db = read_csv('favorites_db.csv')
# faves_df = faves_db.to_dict('id')
# for i in range(len(faves_df)):
#     # pass
#     new = Favorite.add_favorites(user_id=faves_df[i]['user_id'],
#                                  recipe_id=faves_df[i]['recipe_id'],
#                                  title=faves_df[i]['title'],
#                                  ingredients=faves_df[i]['ingredients'],
#                                  measurements=faves_df[i]['measurements'],
#                                  instructions=faves_df[i]['instructions'],
#                                  category=faves_df[i]['category'],
#                                  area=faves_df[i]['area'],
#                                  original=faves_df[i]['original'],
#                                  )
    # db.session.add(new)
    # db.session.commit()
    
    
matches_db = read_csv('matches_db.csv')
matches_df = matches_db.to_dict('id')

for i in range(len(matches_df)):
    # pass
    new = Match.add_matches(user_id=matches_df[i]['user_id'],
                            match_id=matches_df[i]['match_id']
                                 )
    db.session.add(new)
    db.session.commit()