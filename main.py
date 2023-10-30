from website import create_app
from flask_socketio import SocketIO, emit, join_room, leave_room

app = create_app()
socketio = SocketIO(app)

if __name__ == '__main__':  #If we run this file the line below will be executed (The web server)
    socketio.run(app, debug=True)     #Starts up a web server, everytime a change is made to python code the web server is going to be re run_