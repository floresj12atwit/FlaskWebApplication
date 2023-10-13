#When __init__.py file is present in a file it will become a python package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdfasdfasdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)  #this assigns the database to the app we are making


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note  #import the model files so that the database model classes are defined

    with app.app_context():
        db.create_all()

    return app 

def create_database(app):       #checks if a database already exists and if it does not it will create it 
        if not path.exists('website/' + DB_NAME):
            db.create_all(app=app)      
            print('Created Database')
            