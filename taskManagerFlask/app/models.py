import re
from app import login, db # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    passwordHash = db.Column("password_hash", db.String(128))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(256), index=True)
    startDateTime = db.Column(db.String(32), index=True)
    endDateTime = db.Column(db.String(32), index=True)
    users = db.Column(db.String(64), index=True)
    admins = db.Column(db.String(64), index=True)
    status = db.Column(db.String(32), index=True, default="pending")

    def __repr__(self):
        return '<Event {} - {}>'.format(self.id, self.name)

    def as_calender_event(self):
        eventData = {
            "id": self.id,
            "title":self.name,
            "start":self.startDateTime,
            "end": self.endDateTime,
            "description": self.description,
            "status": self.status,
            "classNames": "status-" + self.status
            }
        return eventData

def load_events():
    return Event.query.all()
    




