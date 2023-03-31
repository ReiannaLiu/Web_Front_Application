from flask import Blueprint, render_template, request, flash, redirect, url_for, g, session
from website import DATABASEURI
from sqlalchemy import *
from sqlalchemy.pool import NullPool

views = Blueprint('views', __name__)

engine = create_engine(DATABASEURI)


@views.route('/home', methods=['GET', 'POST'])
def home():
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
                    'product_id': result[0],
                    'product': result[4],
                    'description': result[1],
                    'color': result[5],
                    'size': result[6],
                    'unit_price': result[3]
                })

        cursor.close()
        return render_template("search.html", recentRecords=rowResults)

    return render_template("home.html")


@views.route('/collect', methods=['GET', 'POST'])
def collect():
    userp = session['email']

    if request.method == 'POST':
        product_id = request.form.get("btn-pressed")

        with engine.connect() as g.conn:
            create_table_command = """
            CREATE TABLE IF NOT EXISTS collects(
                email varchar(30),
                product_id varchar(10)
            )
            """

            g.conn.execute(text(create_table_command))

            params = {}
            params['email'] = userp
            params['product_id'] = product_id

            cursor = g.conn.execute(
                text(
                    "SELECT * FROM collects WHERE email = :email AND product_id = :product_id"), params
            )

            row = cursor.fetchone()

            if row == None:
                g.conn.execute(
                    text(
                        'INSERT INTO collects(email, product_id) VALUES (:email, :product_id)'), params
                )
                g.conn.commit()

                flash('Collected! Check it in your cart!',
                      category='success')
            else:
                flash(
                    'You\'ve already collected the product. Check it in your cart!', category='error')
        cursor.close()

    return render_template("search.html")
