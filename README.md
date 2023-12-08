# FlaskWebApplication
This project is a web application where users can connect to eachother to chat and watch a youtube video together.

This is built using Flask as well as SocketIO for the socket programming needed to connect users together in a web server.

Much of the base of the web application is adapted from TechWithTim's tutorial on how to create a basic Flask website as well as a chat feature.

Through that tutorial a database to hold users as well as the basic set up of the application was created.  

SocketIO has a feature called "rooms" where users can connect to (once they're connected to the same web server) in order to share data.

When users connect to a room they are shown a room code which they can share to other members they'd like to be in their room.

They have the option to chat and or input a video link.

SocketIO takes care of the connection between users for chat but for the transmission of the video we attempted to implement it using raw Python Sockets.

The Python socket protocol implementation exists in the VideoServer directory of the project.

When a user enters a video link and clicks watch this (assuming 2 users are connected) the Server and client of the python video protocol are run, OpenCV frames will pop up and transmit the desired video.

The videos are always played in an iframe that's automatically updated on the page when a user enters a new video.

For future updates we may remove the python sockets entirely and opt for a library that allows us to sync video for all users connected to a room through socketIO, such as WebRTC
DISCLAIMER:  This currently only runs on the local host as this web application is not deployed to an official web server.

How to run the program:

  -Run main.py

  
  -Open the local host or click the link in the output that opens the local host 

  
  -Sign up with a fake email (this does not check of legitimacy of data)

  
  -Once you are signed up log in

  
  -Do the same for another user but in incognito mode or another browser 

  
  -You can now chat between users 

  
  -Enter a video link and click watch this, see the video get transmitted 
    

