from flask import Blueprint, render_template, request, flash, redirect, url_for #Blueprint allows us to separate and organize our project, it has URLS defined in it, render template allows us to render the templates we've created for the pages
from .models import User  
from werkzeug.security import generate_password_hash, check_password_hash  #ensures password is not stored as plain text
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])          #Allows us to accept both GET and POST requests at both of these routes (only GET by default)
def login():

                                                #request allows us to get information that was sent to access this route URL, method and data, data that was sent as a part of the form will be retrieved from this line
                                                #notice the difference when empty POST request is sent (Pressing login) vs empty GET request is sent (referesshing the page)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()    #this is what you use when you want to look in specific column of the database for a piece of data
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category = 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.connect'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')   #Flashes can be used to notify the user of constraints or any messages dev deems it necessary for user to know
        elif len(first_name) < 2:
            flash('Email must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
           new_user = User(email = email, first_name=first_name, password=generate_password_hash(password1, method='scrypt'))
           db.session.add(new_user)
           db.session.commit()
           login_user(new_user, remember=True)
           flash('Account created!', category='sucess')
           return redirect(url_for("views.connect"))
    
    return render_template("sign_up.html", user=current_user)




