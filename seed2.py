from pandas import read_csv
from models import db, connect_db, User, Favorite, Match
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

df = read_csv('150_users.csv', index_col='id')
df_dict = df.to_dict('id')

for i in range(1, 151):
    new = User.register_user(id=i,
                username=df_dict[i]['username'],
                pwd=df_dict[i]['password'],
                email=df_dict[i]['email'],
                bio=df_dict[i]['bio'],
                img=df_dict[i]['img'])
    db.session.add(new)
    db.session.commit()