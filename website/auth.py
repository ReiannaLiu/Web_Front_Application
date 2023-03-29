from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website import DATABASEURI
from sqlalchemy import *
from sqlalchemy.pool import NullPool

auth = Blueprint('auth', __name__)

engine = create_engine(DATABASEURI)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(email) > 30:
            flash('Email can not be longer than 30 characters', category='error')
        elif len(user_name) < 2:
            flash('User name must be greater than 1 characters.', category='error')
        elif len(user_name) > 30:
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
                CREATE TABLE IF NOT EXISTS Users(
                    email varchar(30), 
                    user_name varchar(30), 
                    password varchar(30)
                )
                """
                res = conn.execute(text(create_table_command))
                insert_table_command = "INSERT INTO Users VALUES ({}, {}, {})".format(
                    email, user_name, password1)
                res = conn.execute(text(insert_table_command))
                conn.commit()

            flash('Account created!', category='success')

            return redirect(url_for('views.home'))

    return render_template("sign_up.html")
