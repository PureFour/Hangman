from app import db, loginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    score = db.Column(db.Integer)

    def __repr__(self):
        return '<User {} score: {}>'.format(self.email, self.score)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_point(self, points):
        if points < 0:
            raise ValueError('points value must be greater than 0!')
        self.score += points  

@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)
    category = db.Column(db.String(16), index=True)
    description = db.Column(db.String(100), unique=True)
    img = db.Column(db.String(100))
    points = db.Column(db.Integer)

    def __repr__(self):
        return '<Word: {}\nCategory: {}\nDescription: {}\nImg: {}\nPoints: {}>'.format(self.name, self.category, self.description, self.img, self.points)