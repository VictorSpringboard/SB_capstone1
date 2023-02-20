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

class Grocery(db.Model):
    __tablename__ = 'groceries'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    
    groceries = db.relationship('User', secondary='groceries', primaryjoin=(Grocery.user_id == id))
    
    favorites = db.relationship('User', secondary='favorites', primaryjoin=(Favorite.user_id == id))

    def __repr__(self):
        return f'User: {self.username}, email: {self.email}'
    
    @classmethod
    def register_user(cls, id, username, pwd, email):
        
        hashed = bcrypt.generate_password_hash(pwd)
        
        hashed_utf8 = hashed.decode('utf8')
        
        return cls(id=id,
                    username=username, 
                    password=hashed_utf8,
                    email=email)
    
    @classmethod
    def authenticate_user(cls, username, pwd):
        
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
        
    
    
        
class Recipe(db.Model):
    __tablename__ = 'recipes' 
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    measurements = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    area = db.Column(db.Text, nullable=False)
    original = db.Column(db.Text, nullable=False)
    