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
from website.videoServer.UDPserverWithAudio import runVideoServer
from website.videoServer.UDPclientWithAudio import runClient
from website import socketio
from website.videoServer.DownloadYTvid import *
import time

rooms = {}      #Initialize python dictionary to hold the rooms users connect to

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
        
        return redirect(url_for('views.home'))
    

    return render_template("connectUsers.html", user= current_user)


@views.route('/home', methods=['POST', 'GET'])
def home():

                                
    
    room = session.get("room")   
    if room is None or session.get("name") is None or room not in rooms:
        
        return redirect(url_for('views.connect'))
    
    
    


    video_id=rooms[room]["video_id"]
    #Checks if a POST request has been made (user entering a link) (we can add error handling here if we deem it necessary in the case that a link is not entered)
    
    #print(newVideo)

    return render_template("home.html", video_id = video_id, user=current_user, code= room, messages = rooms[room]["messages"] )

'''
This function is not currently used and was replaced by "insertVideo" but may be used in the future
'''
@socketio.on("changeVideo") 
def change_video(data):
    
        room = session.get("room")          #makes sure room exists and exits if it doesn't return to previous page
        if room not in rooms:
            return
       
        video_url = data["videoUrl"]

        video_id = extract_video_id(video_url)
        

        rooms[room]["video_id"]=video_id
        

'''
This is an event listener for when a new video is entered
'''
@socketio.on("insertVideo")                
def insertVideo(data):
    room = session.get("room")

    #these 3 lines are for the iframe 
    video_url = data["videoUrl"]
    video_id = extract_video_id(video_url)
    client_ip = request.remote_addr
    #Get the ip address of the user entering the video (doesn't do anything at the moment since this is run on the local port)
    ip_address = request.headers.get('X-Forwarded-For', request.headers.get('X-Real-IP', request.remote_addr))
    #Generates an iframe to be passed to the webpage
    iframe = f'<iframe width ="560" height="315" src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1" frameborder="0" allowfullscreen></iframe>'
    
    #print("User from IP "+client_ip+" and Port :""has changed the video")                  #This is how we get the current users IP to connect them to the UDP server that will be created when video is inputted
    
    #These lines are to download the video locally
    video_output_path = 'WatchParty/website/Videos/'
    audio_output_path = 'WatchParty/website/Videos/'        #audio will be implemented after video is confirmed to work
    downloaded_video_path = download_youtube_video(video_url, video_output_path)
    new_audio_path = extract_audio(downloaded_video_path, audio_output_path ) 
    print(ip_address)
    iframe2 =f'<iframe width ="560" height="315" src="{downloaded_video_path}" allowfullscreen></iframe>'
    socketio.emit('videoIframe',  iframe, room=room)    #Emit event to the webpage to update the iframe

    time.sleep(1)
    
    runVideoServer(downloaded_video_path, new_audio_path)   #This launches the video server with the locally downloaded file

#This is an event listener for the other user connected to the room when a video is entered
@socketio.on("connectToVideoServer")
def connectToVideo():
    time.sleep(8)       #this is needed to avoid the client searching for a connection before the server is set up
    runClient()         #This runs the client code to connect to the video server



    
    

        
        
    

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
    rooms[room]["messages"].append(content)          #this is only needed so that the page can be refreshed and keep chat
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
    socketio.emit('joined', room = room)  #adding this to get room name in javascript
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