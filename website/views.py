'''
This is going to hold pages the users can navigate to
'''

from flask import Blueprint #Blueprint allows us to separate and organize our project, it has URLS defined in it 

views = Blueprint('views', __name__)



@views.route('/') #this decorates a function to register it with a given URL 
def home():
    return "<h1>TestingLol<h1>"


