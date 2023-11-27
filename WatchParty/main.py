from website import create_app, socketio
from flask_socketio import SocketIO, emit, join_room, leave_room



app= create_app()



# events happen HERE
# solution could be to simply run the app in views? OR have events run here 

if __name__ == '__main__':  #If we run this file the line below will be executed (The web server)
    socketio.run(app, debug=True)     #Starts up a web server, everytime a change is made to python code the web server is going to be re run_

    '''
    This website base taken from this youtube video as we were not completely familiar with 
    web development we wanted to implement it in a website

    https://www.youtube.com/watch?v=dam0GPOAvVI&t=334s
    Github for the youtube video code shown:
    https://github.com/techwithtim/Flask-Web-App-Tutorial

    For the video and audio transmission we adapted the one from the resource below 
    https://pyshine.com/How-to-send-audio-video-of-MP4-using-sockets-in-Python/

    We had to change it so that the sockets exit gracefully instead of simply stopping the program 
    '''



    