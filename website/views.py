from flask import Blueprint, render_template, request, flash, redirect, url_for, g, session
from werkzeug.security import generate_password_hash, check_password_hash
from website import DATABASEURI
from sqlalchemy import *
from sqlalchemy.pool import NullPool

views = Blueprint('views', __name__)

engine = create_engine(DATABASEURI)


@views.route('/home', methods=['GET', 'POST'])
def home():
    userp = session['email']

    if request.method == 'POST':
        search = request.form.get('search')
        search = search.rstrip()

        with engine.connect() as g.conn:

            cursor = g.conn.execute(text(
                "SELECT * FROM product WHERE description LIKE '%'|| :val ||'%' "), {'val': search})

            rowResults = []

            for result in cursor:
                print(result)
                rowResults.append({
                    'Product': result[4],
                    'description': result[1],
                    'color': result[5],
                    'size': result[6]
                })

        print(rowResults)
        cursor.close()
        return render_template("search.html", recentRecords=rowResults)

    return render_template("home.html")
