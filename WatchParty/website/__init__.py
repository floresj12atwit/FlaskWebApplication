#When __init__.py file is present in a file it will become a python package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import re   #this is going to be used to get the url for the video
from flask_login import LoginManager
from flask_socketio import SocketIO
db = SQLAlchemy()
DB_NAME = "database.db"

socketio = SocketIO()           #initalize socketio instance that is going to be used throughout the application

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdfasdfasdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)  #this assigns the database to the app we are making

    
    

    from .auth import auth
    from .views import views
    
    socketio.init_app(app)
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    

    from .models import User, Note  #import the model files so that the database model classes are defined

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

   
    
    

    @login_manager.user_loader
    def load_user(id):
         return User.query.get(int(id))

    

    return app

def create_database(app):       #checks if a database already exists and if it does not it will create it 
        if not path.exists('website/' + DB_NAME):
            db.create_all(app=app)      
            print('Created Database')

