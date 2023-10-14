'''
This is going to hold pages the users can navigate to
'''
                                             #render template allows us to render the templates we've created to hold the pages (the different files containing the web pages)
from flask import Blueprint, render_template #Blueprint allows us to separate and organize our project, it has URLS defined in it 
from flask_login import login_required,  current_user
views = Blueprint('views', __name__)



@views.route('/') #this decorates a function to register it with a given URL 
@login_required
def home():
    return render_template("home.html")



