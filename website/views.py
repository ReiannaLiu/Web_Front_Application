from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website import DATABASEURI
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask_login import login_user, login_required, logout_user, current_user
url_for, request

views = Blueprint('views', __name__)

engine = create_engine(DATABASEURI)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search = request.form.get('search')

        with engine.connect() as conn:
            params = {}
            params["search"] = search

            cursor = conn.execute(
                text("SELECT name, color, size, description FROM product P LIMIT 5")
            )

            rowResults = cursor.fetchall()
        return render_template("search.html", recentRecords=rowResults)

    return render_template("home.html")
