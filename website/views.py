from flask import Blueprint, render_template, redirect, url_for

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@views.route('/login')
def login():
    return render_template("login.html")


@views.route('/logout')
def logout():
    return redirect(url_for('auth.login'))


@views.route('/sign-up')
def sign_up():
    return render_template("sign_up.html")
