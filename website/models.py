
from . import db
from flask_login import UserMixin 
from sqlalchemy.sql import func
#database models are just a blueprint/layout of an object that's going
#to be stored in a database
class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())  #func gets the current date and time when the note object is created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))          #this is a one to many relationships one user has many notes so you store an FK on child objects that reference parent object


#This database model was created by me to possibly hold the videos that users watch (This may or may not be used)
'''
class Videos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    creator = db.Column(db.String(1000))
    length = db.Column(db.Integer)
    '''


#All users are held in a schema that looks like this vvv
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    #currently_watching_video_id = db.Column(db.ForeignKey('videos.id'))     #this line may be useful when we embed youtube into the website