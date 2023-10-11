from flask import Blueprint #Blueprint allows us to separate and organize our project, it has URLS defined in it 

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return "<p>Login</p>"

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up')
def sign_up():
    return "<p>Sign Up</p>"


