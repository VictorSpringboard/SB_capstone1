from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
    
    
    
class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
    recipe_id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    measurements = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    area = db.Column(db.Text, nullable=False)
    original = db.Column(db.Text, nullable=False)
    is_top_3 = db.Column(db.Boolean)
    order = db.Column(db.Integer)
    
    def getTitles(self):
        return {'title': self.title}
    
    @classmethod
    def add_favorites(cls,
                      user_id,
                      recipe_id,
                      title,
                      ingredients,
                      instructions,
                      measurements,
                      category,
                      area,
                      original,
                      is_top_3,
                      order):
        
        return cls(user_id=user_id, recipe_id=recipe_id,
                   title=title, ingredients=ingredients,
                   instructions=instructions,
                   measurements=measurements, category=category,
                   area=area, original=original,
                   is_top_3=is_top_3, order=order)
    
    

class Match(db.Model):
    __tablename__ = 'matches'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
    match_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)



    def __repr__(self):
        return f'{self.match_id}'
    
    @classmethod
    def add_matches(cls,
                    user_id,
                    match_id):
        return cls(user_id=user_id,
                   match_id=match_id)


# Code adapted from a flask tutorial at blog.miguelgrinberg.com
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default = datetime.datetime.utcnow)


    
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)
    img = db.Column(db.Text)
    
    
    favorites = db.relationship('User', secondary='favorites', primaryjoin=(Favorite.user_id == id))

    matches = db.relationship('User', secondary='matches', primaryjoin=(Match.user_id == id), secondaryjoin=(Match.match_id == id))

    matched_by = db.relationship('User', secondary='matches', primaryjoin=(Match.match_id == id), secondaryjoin=Match.user_id == id)
    
    sent_msgs = db.relationship('Message', foreign_keys=Message.sender_id, backref='author', lazy='dynamic')
    received_msgs = db.relationship('Message', foreign_keys=Message.receiver_id, backref='recipient', lazy='dynamic')
    def __repr__(self):
        return f'User: {self.username}, email: {self.email}'
    
    def is_liking(self, other_user):
        '''Does this user like the other user?'''

        found_user_list = [user for user in self.matches if user == other_user]
        return len(found_user_list) == 1

    def is_liked_by(self, other_user):
        '''Is this user liked by the other user'''
        
        found_user_list = [user for user in self.matched_by if user == other_user]
        return len(found_user_list) == 1
        
    def get_messages(self):
        return Message.query.all()
    
    
    
    @classmethod
    def register_user(cls, id, username, password, email, bio, img):
        
        
        hashed = bcrypt.generate_password_hash(password)
        
        hashed_utf8 = hashed.decode('utf8')
        
        user = User(id=id,
                    username=username,
                    password=hashed_utf8,
                    email=email,
                    bio=bio,
                    img=img)
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate_user(cls, username, password):
        
        u = cls.query.filter_by(username=username).first()
        
        if u:
            is_auth = bcrypt.check_password_hash(u.password, password)
            if is_auth:
                return u
        return False
        
    
    
        
