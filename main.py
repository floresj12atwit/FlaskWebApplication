from website import create_app

app = create_app()

if __name__ == '__main__':  #If we run this file the line below will be executed (The web server)
    app.run(debug=True)     #Starts up a web server, everytime a change is made to python code the web server is going to be re run