from models import db, connect_db, User, Favorite, Grocery
from app import app
import datetime


connect_db(app)
app.app_context().push()

db.drop_all()
db.create_all()



users = [
    {
        'id': 0,
        'username': 'test',
        'password': 'test',
        'email': 'test@test.com'
    },
    {
        'id': 1,
        'username': 'HankHill',
        'password': 'propane',
        'email': 'hank@strickland.com'
    },
    {
        'id': 2,
        'username': 'PeggyHill',
        'password': 'boggle',
        'email': 'peggy@boggle.com'
    },
    {
        'id': 3,
        'username': 'BobbyHill',
        'password': 'comedy',
        'email': 'bobby@thatsmypurse.com'
    },
    {
        'id': 4,
        'username': 'Boomhauer',
        'password': 'dang',
        'email': 'dangole@talkinbout.com'
    },
]

for user in users:
    new = User.register_user(id=user['id'],
                username=user['username'],
                pwd=user['password'],
                email=user['email'])
    db.session.add(new)
    db.session.commit()
