'''
This is going to hold pages the users can navigate to
'''
                                             #render template allows us to render the templates we've created to hold the pages (the different files containing the web pages)
from flask import Blueprint, flash, redirect, render_template, session, url_for #Blueprint allows us to separate and organize our project, it has URLS defined in it 
from flask import request
from flask_login import login_required, current_user
import re, random
from flask_socketio import join_room, leave_room, send, SocketIO
from string import ascii_uppercase
from website import socketio


rooms = {}

views = Blueprint('views', __name__)



def generate_room_code(length):             #generates a random room code for users to connect to 
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:           #checks if the code already exists for another room
            break
    return code


'''
This function helps us extract the video id string from the link the user inputs into the form box
This uses Regex (chat gpt helped with this)
'''
def extract_video_id(url):
     if url is None:
         return None
     pattern = r'(?:youtube\.com\/watch\?v=|youtu.be\/|youtube.com\/embed\/|youtube.com\/v\/|youtube.com\/embed\/videoseries\?list=)([\w-]+)'
     match = re.search(pattern, url)

     if match:
      return match.group(1)    
     return None

#This route now allows GET and POST requests which is needed for the user to enter link (GET requests are the default method so its good practice to make it explicit)
@views.route('/', methods=['GET','POST']) #this decorates a function to register it with a given URL 
@login_required
def connect():                                #this technically should be put in the auth.py folder but it's directly linked to the home page which is going to act as a room so I put in views.py
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")         #forms are python dictionaries so get will try to find the value associated with the passed in key in this case the name 
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("connectUsers.html", error="Please enter a name.", code = code, name = name, user=current_user)
        if join != False and not code:
            return render_template("connectUsers.html", error="Please enter a room code.", code = code, name = name, user=current_user)   

        room = code 
        if create != False:
            room = generate_room_code(4) 
            rooms[room]= {"members": 0, "messages": [], "video_id": ""}   #creates a dictionary that holds numbers of users as well as all the messages in the room in the form of a list
        elif code not in rooms:
            return render_template("connectUsers.html", error="Room does not exist", code = code, name = name, user=current_user)   

        session["room"] = room   #temporary session is used to hold user data (we have a database so maybe we won't need this Im just following the tutorial right now)
        session["name"] = name
        session["video_id"] = ""
        return redirect(url_for('views.home'))
    

    return render_template("connectUsers.html", user= current_user)


@views.route('/home', methods=['POST', 'GET'])
def home():

                                
    
    room = session.get("room")   
    if room is None or session.get("name") is None or room not in rooms:
        
        return redirect(url_for('views.connect'))
    
    

        
    
    #Checks if a POST request has been made (user entering a link) (we can add error handling here if we deem it necessary in the case that a link is not entered)
    

    return render_template("home.html", video_id=rooms[room]["video_id"], user=current_user, code= room, messages = rooms[room]["messages"] )


@socketio.on("changeVideo") 
def change_video(data):
    #if request == "POST":
        room = session.get("room")

        video_url = data["videoUrl"]
        video_id = extract_video_id(video_url)  #video id is the string of characters at the end of a youtube link
        
        if room in rooms:
            rooms[room]["video_id"]= video_id

        print(rooms[room]["video_id"])
        return
        
        
    

#this is the serving receiving the message from a user and then sending it all other users, as the users aren't connected 
#they are connected via the server so the way it works is the server recieves the message and then displays it to all users
#enabling communication between users 
@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms: 
        return
    
    content = {                         #instead of doing this the messages could be saved on the server instead
        "name": session.get("name"),
        "message": data["data"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)          
    print(f"{session.get('name')} says: {data['data']}")


#socket connection happens here
@socketio.on("connect")         #this is where we implement the "listen" for a socket connection
def connect(auth):              #rooms are created when a socket connection is made 
    

    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room
        return
    
    join_room(room)  #rooms are collections of users much simpler way of connecting them than exchanging IP addresses manually
    send({"name": name, "message":"has entered the room"}, to= room)
    rooms[room]["members"] += 1
    
    print(f"{name} joined room {room}")

@socketio.on("disconnect")      #this handles the event of users leaving the room (socket disconnects)
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -=1
        if rooms[room]["members"] <=0:      #checks if room is empty so that it can be deleted, no need to store the data anymore
            del rooms[room]
    
    send({"name": name, "message":"has left the room"}, to= room)
    print(f"{name} left the room {room}")