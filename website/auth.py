from flask import Blueprint, render_template, request, flash, redirect, url_for, g, session
from website import DATABASEURI
from sqlalchemy import *
from sqlalchemy.pool import NullPool

auth = Blueprint('auth', __name__)

engine = create_engine(DATABASEURI)


@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        with engine.connect() as g.conn:
            params = {}
            params["email"] = email

            user = g.conn.execute(
                text("SELECT * FROM users WHERE email = :email"), params).fetchone()

            if (user is None):
                flash('Email does not exist.', category='error')
            else:
                true_password = user[2]
                if len(true_password) != 0:
                    if true_password == password:
                        session.clear()
                        session['email'] = user[0]
                        flash('Logged in successfully!', category='success')
                        return redirect(url_for('views.home'))
                    else:
                        flash('Incorrect password, try again.', category='error')

    return render_template("login.html")


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        with engine.connect() as g.conn:
            params = {}
            params["email"] = email

            cursor = g.conn.execute(
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
            with engine.connect() as g.conn:
                create_table_command = """
                CREATE TABLE IF NOT EXISTS users(
                    email varchar(30),
                    username varchar(30),
                    password varchar(30)
                )
                """
                g.conn.execute(text(create_table_command))

                params = {}
                params["email"] = email
                params["username"] = username
                params["password"] = password1

                g.conn.execute(
                    text('INSERT INTO users(email, username, password) VALUES (:email, :username, :password)'), params)
                g.conn.commit()

            flash('Account created!', category='success')

            return redirect(url_for('auth.login'))

    return render_template("sign_up.html")
