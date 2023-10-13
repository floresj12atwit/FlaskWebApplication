from flask import Blueprint, render_template, request, flash #Blueprint allows us to separate and organize our project, it has URLS defined in it, render template allows us to render the templates we've created for the pages
                                                      
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])          #Allows us to accept both GET and POST requests at both of these routes (only GET by default)
def login():
                     #request allows us to get information that was sent to access this route URL, method and data, data that was sent as a part of the form will be retrieved from this line
                     #notice the difference when empty POST request is sent (Pressing login) vs empty GET request is sent (referesshing the page)
    return render_template("login.html", boolean=True)

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')   #Flashes can be used to notify the user of constraints or any messages dev deems it necessary for user to know
        elif len(firstName) < 2:
            flash('Email must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
           flash('Account created!', category='sucess')
           #add user to database
    
    return render_template("sign_up.html")


