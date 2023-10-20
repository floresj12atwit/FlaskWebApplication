'''
This is going to hold pages the users can navigate to
'''
                                             #render template allows us to render the templates we've created to hold the pages (the different files containing the web pages)
from flask import Blueprint, render_template #Blueprint allows us to separate and organize our project, it has URLS defined in it 
from flask import request
from flask_login import login_required, current_user
import re


views = Blueprint('views', __name__)

'''
This function helps us extract the video id string from the link the user inputs into the form box
This uses Regex (chat gpt helped with this)
'''
def extract_video_id(url):
     pattern = r'(?:youtube\.com\/watch\?v=|youtu.be\/|youtube.com\/embed\/|youtube.com\/v\/|youtube.com\/embed\/videoseries\?list=)([\w-]+)'
     match = re.search(pattern, url)

     if match:
      return match.group(1)    
     return None

#This route now allows GET and POST requests which is needed for the user to enter link (GET requests are the default method so its good practice to make it explicit)
@views.route('/', methods=['GET','POST']) #this decorates a function to register it with a given URL 
@login_required
def home():
    video_id = None

    #Checks if a POST request has been made (user entering a link) (we can add error handling here if we deem it necessary in the case that a link is not entered)
    if request.method == 'POST':
        video_url = request.form['video_url']
        video_id = extract_video_id(video_url)

    return render_template("home.html", video_id=video_id, user=current_user)



