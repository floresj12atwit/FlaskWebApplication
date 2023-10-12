from flask import Blueprint, render_template, request #Blueprint allows us to separate and organize our project, it has URLS defined in it, render template allows us to render the templates we've created for the pages
                                                      
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])          #Allows us to accept both GET and POST requests at both of these routes (only GET by default)
def login():
    data = request.form                 #request allows us to get information that was sent to access this route URL, method and data, data that was sent as a part of the form will be retrieved from this line
    print(data)                         #notice the difference when empty POST request is sent (Pressing login) vs empty GET request is sent (referesshing the page)
    return render_template("login.html", boolean=True)

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    return render_template("sign_up.html")


