from app import login, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    
    option1 = db.Column(db.String(140))
    option2 = db.Column(db.String(140))
    option3 = db.Column(db.String(140))
    option4 = db.Column(db.String(140))

    answers_option1 = db.Column(db.Integer)
    answers_option2 = db.Column(db.Integer)
    answers_option3 = db.Column(db.Integer)
    answers_option4 = db.Column(db.Integer)


    def __repr__(self):
        return '<Questions {}>'.format(self.body)


        
@login.user_loader
def load_user(id):
    return User.query.get(int(id))