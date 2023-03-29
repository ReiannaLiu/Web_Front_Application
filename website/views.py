from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/login')
def login():
    return render_template("login.html")


@views.route('/logout')
def logout():
    return "<p>Logout</p>"


@views.route('/sign-up')
def sign_up():
    return render_template("sign_up.html")
