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

            cursor = g.conn.execute(text("""
                                         SELECT * 
                                         FROM product p
                                         LEFT JOIN order_contains o ON p.product_id = o.product_id
                                         LEFT JOIN rating r ON o.order_id = r.order_id
                                         WHERE description LIKE '%'|| :val ||'%'
                                         """), {'val': search})

            rowResults = []

            for result in cursor:
                rowResults.append({
                    'product_id': result[0],
                    'product': result[4],
                    'description': result[1],
                    'color': result[5],
                    'size': result[6],
                    'unit_price': result[3],
                    'rating': result[12]
                })

        cursor.close()
        return render_template("search.html", recentRecords=rowResults)

    return render_template("home.html")


@views.route('/add_collect', methods=['GET', 'POST'])
def add_collect():
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

                return redirect(url_for('views.home'))
            else:
                flash(
                    'You\'ve already collected the product. Check it in your cart!', category='error')
        cursor.close()

    return redirect(url_for('views.home'))


@views.route('/collect', methods=['GET', 'POST'])
def collect():
    userp = session['email']

    if request.method == 'POST':

        with engine.connect() as g.conn:

            params = {}
            params['email'] = userp

            cursor = g.conn.execute(text(
                """
                SELECT *
                FROM collects C
                NATURAL JOIN product P
                WHERE C.email = :email
                """), params)

            rowResults = []

            for result in cursor:
                print(result)
                rowResults.append({
                    'product_id': result[0],
                    'product': result[5],
                    'description': result[2],
                    'color': result[6],
                    'size': result[7],
                    'unit_price': result[4]
                })

        cursor.close()
        return render_template("collect.html", recentRecords=rowResults)

    return render_template("collect.html")


@views.route('/delete_collect', methods=['GET', 'POST'])
def delect_collect():
    userp = session['email']

    if request.method == 'POST':
        product_id = request.form.get("btn-pressed")

        with engine.connect() as g.conn:

            params = {}
            params['email'] = userp
            params['product_id'] = product_id

            g.conn.execute(
                text(
                    "DELETE FROM collects WHERE email = :email AND product_id = :product_id"
                ), params
            )

            g.conn.commit()

            flash('Deleted! Search the website for more product you like.',
                  category='success')

    return redirect(url_for('views.collect'))


@views.route('/filter', methods=['GET', 'POST'])
def filter():
    if request.method == 'POST':
        filter_parameter = request.values.get('select-filter')

        if filter_parameter == "0":
            return render_template("filter.html", recentRecords=[])

        elif filter_parameter == "1":
            with engine.connect() as g.conn:
                cursor = g.conn.execute(text("""
                                             SELECT name, SUM(quantity_ordered) as Quantity_Ordered
                                             FROM order_contains 
                                             NATURAL JOIN product
                                             GROUP BY name
                                             ORDER BY Quantity_Ordered DESC 
                                             LIMIT 10
                                             """
                                             ))
                rowResults = []

                for result in cursor:
                    rowResults.append({
                        'product_name': result[0],
                        'quantity': result[1]
                    })

                cursor.close()

            return render_template("filter.html", recentRecords=rowResults)

        elif filter_parameter == "2":
            with engine.connect() as g.conn:
                cursor = g.conn.execute(text("""
                                             SELECT size, SUM(quantity_ordered) as Quantity_Ordered
                                             FROM order_contains 
                                             NATURAL JOIN product
                                             GROUP BY size
                                             ORDER BY Quantity_Ordered DESC 
                                             LIMIT 10
                                             """
                                             ))
                rowResults = []

                for result in cursor:
                    rowResults.append({
                        'size': result[0],
                        'quantity': result[1]
                    })

                cursor.close()

            return render_template("filter.html", recentRecords=rowResults)

        elif filter_parameter == "3":
            with engine.connect() as g.conn:
                cursor = g.conn.execute(text("""
                                             SELECT color, SUM(quantity_ordered) as Quantity_Ordered
                                             FROM order_contains 
                                             NATURAL JOIN product
                                             GROUP BY color
                                             ORDER BY Quantity_Ordered DESC 
                                             LIMIT 10
                                             """
                                             ))
                rowResults = []

                for result in cursor:
                    rowResults.append({
                        'color': result[0],
                        'quantity': result[1]
                    })

                cursor.close()

            return render_template("filter.html", recentRecords=rowResults)

        elif filter_parameter == "4":
            with engine.connect() as g.conn:
                cursor = g.conn.execute(text("""
                                             SELECT gender, name, SUM(quantity_ordered) as Quantity_Ordered
                                             FROM order_contains 
                                             NATURAL JOIN product
                                             NATURAL JOIN customer
                                             GROUP BY name, gender
                                             ORDER BY Quantity_Ordered DESC 
                                             LIMIT 10
                                             """
                                             ))
                rowResults = []

                for result in cursor:
                    rowResults.append({
                        'gender': result[0],
                        'product_name': result[1],
                        'quantity': result[2]
                    })

                cursor.close()

            return render_template("filter.html", recentRecords=rowResults)

        elif filter_parameter == "5":
            with engine.connect() as g.conn:
                cursor = g.conn.execute(text("""
                                             SELECT age, name, SUM(quantity_ordered) as Quantity_Ordered
                                             FROM order_contains 
                                             NATURAL JOIN product
                                             NATURAL JOIN customer
                                             GROUP BY name, age
                                             ORDER BY Quantity_Ordered DESC 
                                             LIMIT 10
                                             """
                                             ))
                rowResults = []

                for result in cursor:
                    rowResults.append({
                        'age': result[0],
                        'product_name': result[1],
                        'quantity': result[2]
                    })

                cursor.close()

            return render_template("filter.html", recentRecords=rowResults)

        elif filter_parameter == "6":
            with engine.connect() as g.conn:
                cursor = g.conn.execute(text("""
                                             SELECT supplier_name, name, SUM(quantity_ordered) as Quantity_Ordered
                                             FROM order_contains 
                                             NATURAL JOIN product
                                             NATURAL JOIN supplier
                                             GROUP BY name, supplier_name
                                             ORDER BY Quantity_Ordered DESC 
                                             LIMIT 10
                                             """
                                             ))
                rowResults = []

                for result in cursor:
                    rowResults.append({
                        'supplier_name': result[0],
                        'product_name': result[1],
                        'quantity': result[2]
                    })

                cursor.close()

            return render_template("filter.html", recentRecords=rowResults)

    return render_template("filter.html", recentRecords=[])


@views.route('/profile', methods=['GET', 'POST'])
def profile():
    userp = session['email']

    with engine.connect() as conn:

        params = {}
        params['email'] = userp

        username = conn.execute(text(
            "SELECT username FROM users WHERE email = :email"
        ), params).fetchone()[0]

        cursor = conn.execute(text(
            """
            SELECT first_name, last_name, gender, age, phone_number
            FROM customer
            NATURAL JOIN phone
            WHERE email = :email
            """
        ), params)

        rowResults = []

        for result in cursor:
            rowResults.append({
                'first_name': result[0],
                'last_name': result[1],
                'gender': result[2],
                'age': result[3],
                'phone_number': result[4]
            })

        cursor = conn.execute(text(
            """
            SELECT street_address, city, province, zipcode 
            FROM shipping_address
            NATURAL JOIN customer
            WHERE email = :email
            """
        ), params)

        address = []

        for result in cursor:
            address.append({
                'street_address': result[0],
                'city': result[1],
                'province': result[2],
                'zipcode': result[3]
            })

        cursor = conn.execute(text(
            """
            SELECT order_status, shipper_name, order_id, name
            FROM transaction_order
            NATURAL JOIN customer
            NATURAL JOIN shipper
            NATURAL JOIN order_contains
            NATURAL JOIN product
            WHERE email = :email
            """
        ), params)

        order = []

        for result in cursor:
            order.append({
                'order_status': result[0],
                'shipper_name': result[1],
                'order_id': result[2],
                'name': result[3]
            })

        cursor.close()

    return render_template("profile.html", username=username, email=userp, personal_info=rowResults, address=address, order=order)
