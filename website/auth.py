from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website import DATABASEURI
from sqlalchemy import *
from sqlalchemy.pool import NullPool

auth = Blueprint('auth', __name__)

engine = create_engine(DATABASEURI)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        with engine.connect() as conn:
            params = {}
            params["email"] = email

            cursor = conn.execute(
                text("SELECT password FROM users WHERE email = :email"), params)

            true_password = []
            for result in cursor:
                true_password.append(result[0])
            cursor.close()

            if len(true_password) != 0:
                if true_password[0] == password:
                    flash('Logged in successfully!', category='success')
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')

    return render_template("login.html")


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        with engine.connect() as conn:
            params = {}
            params["email"] = email

            cursor = conn.execute(
                text("SELECT email FROM users WHERE email = :email"), params)
            existing_email = []
            for result in cursor:
                existing_email.append(result[0])
            cursor.close()

        if len(existing_email) != 0:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(email) > 30:
            flash('Email can not be longer than 30 characters', category='error')
        elif len(username) < 2:
            flash('User name must be greater than 1 characters.', category='error')
        elif len(username) > 30:
            flash('User name can not be longer than 30 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(password1) > 30:
            flash('Password cannot be longer than 30 characters', category='error')
        else:
            with engine.connect() as conn:
                create_table_command = """
                CREATE TABLE IF NOT EXISTS users(
                    email varchar(30),
                    username varchar(30),
                    password varchar(30)
                )
                """
                conn.execute(text(create_table_command))

                params = {}
                params["email"] = email
                params["username"] = username
                params["password"] = password1

                conn.execute(
                    text('INSERT INTO users(email, username, password) VALUES (:email, :username, :password)'), params)
                conn.commit()

            flash('Account created!', category='success')

            return redirect(url_for('views.home'))

    return render_template("sign_up.html")
