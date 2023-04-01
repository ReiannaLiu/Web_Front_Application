Part 3: Reianna Liu (rl3176), Zhizhuo Zhang (zz3012)

PosgreSQL account name: rl3176

URL of the web: <http://127.0.0.1:5000>

#### Description of the web application

**1. Features in the original proposal**

- **Recommend and range categories to users based on different attributes in the filter, such as size and color.**
You can click the ``filter`` button (showed on the upper right corner of the image) to open the ==filter page== and select specific attribute and click go.
![](2023-03-31-21-22-26.png)
Then you can see the result of the filter showed below.
![](2023-03-31-21-23-55.png)

- **Show the range of the age and the proportion of gender of customers who ordered some specific categories.**
Similarly, you can also selct the age and the gender attribute in the filter.

- **Search for the reviews for a specific supplier**
The ``filter`` button also allow the search of some specific suppliers.

- **The user can collect or like one product.**
If you want to collect some products, you can click the ``star`` button on the left of every product.
![](2023-03-31-21-29-04.png)
If the product has been added into the cart, the web application will notice you when you try to repeatedly add the same product.

- **Search for ratings of the specific product**
Similarly, you can see the rating while searching different products in the ==search page==.

**2. New features**

- **Search bar**
![](2023-03-31-21-16-19.png)
This is the ==home page== of the web application, you can type in the name of the product you want to buy, and click the ```search``` button. You can see its information on the ==search page== if it exists in our database.
If you don't type in anything and click the ```search``` button directly, you can see all products in our database.
![](2023-03-31-21-30-48.png)

- **User management and title bar**
At the first time you open the web application, you can see the ==login page==. 
![](2023-03-31-21-35-34.png)
If you don't have the account of this web application, you should click the ```Sign up here``` button to registrate.
![](2023-03-31-21-36-32.png)
After registration, you can login to the ==home page==. There are several buttons on the title bar, whose features will be described later.
![](2023-03-31-21-38-17.png)

- **Cart management**
Continuing from the collection function stated above, the ```cart``` button on the upper right of the ==home page== can open the ==cart page==.
![](2023-03-31-21-43-12.png)
In this page, you can see all products added in the cart and choose whether to delete it by clicking the ```delete``` button on the right of the product.
![](2023-03-31-21-47-08.png)

- **User profile**
You can click the ```profile``` button to visit the ==profile page==. All the information in this page is related to the email you input when logging in.
![](2023-03-31-21-57-54.png)

**3. Missing part**

- **Shipping speed of every order**
We replace it with the **order status** attribute.

#### Two interesting pages

Briefly describe two of the web pages that require (what you consider) the most interesting database operations in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.

**1. Filter page**

In ```filter.html``` file, we use this code to receive input values from the web page.
```html
<form action="{{ url_for('views.filter') }}"class="form-inline" method="POST">
    <div class="form-group">
      <div class="input-group">
        <select name= "select-filter" class="form-select" aria-label="Default select example">
        <option selected value="0">Open this select menu</option>
        <option value="1">Number of Purchases</option>
        <option value="2">Size</option>
        <option value="3">Color</option>
        <option value="4">Gender</option>
        <option value="5">Age</option>
        <option value="6">Supplier</option>
        </select>
      </div>
      <input
        type="hidden"
        name="tbn-pressed"
        value="select-filter"
      />
      <button type="submit" class="btn btn-outline-primary">Go</button>
    </div>
</form>
```

As you can see in the code showed above, every option in the ```select``` menu has its unique value, when you click the button in this ```form```, the ```views.py``` file located in the backend can get the value of the option by using this code

```python
filter_parameter = request.values.get('select-filter')
```

After that, the program can execute postgresql query and post the result back to ```filter.html``` file based on different value.

```python
if filter_parameter == "1":
    with engine.connect() as g.conn:
        cursor = g.conn.execute(text("""SELECT name, SUM(quantity_ordered) as Quantity_Ordered
                                        FROM order_contains 
                                        NATURAL JOIN product
                                        GROUP BY name
                                        ORDER BY Quantity_Ordered DESC 
                                        LIMIT 10"""))
        rowResults = []
        for result in cursor:
            rowResults.append({'product_name': result[0],
                              'quantity': result[1]})
        cursor.close()

    return render_template("filter.html", recentRecords=rowResults)
```
Eventually, you can see different results when you choose different option on this page. We think this is an ingenious design.

**2. Collect page**

The design of this page can be divided into two sections. The first is to display the products in a specific user's shopping cart. The second is to delete a specific product in the shopping cart as his wish.

- **Filter products**
We use session module in flask library to ensure the web application can remember the user's login email address when he enter the ==collect page==. Then we use postgresql query language in ```views.py``` file to get information about the products in the shopping cart corresponding to the email address, and send it to ```collect.html``` file.

```python
with engine.connect() as g.conn:

    params = {}
    params['email'] = userp

    cursor = g.conn.execute(text("""SELECT *
                                    FROM collects C
                                    NATURAL JOIN product P
                                    WHERE C.email = :email
                                    """), params)

    rowResults = []
    for result in cursor:
        print(result)
        rowResults.append({'product_id': result[0],
                          'product': result[5],
                          'description': result[2],
                          'color': result[6],
                          'size': result[7],
                          'unit_price': result[4]})
    cursor.close()
return render_template("collect.html", recentRecords=rowResults)
```

In ```collect.html``` file, we use a table to display information from backend program.

```html
<table class="table table-hover" cellspacing="0">
    <thead>
      <tr>
        <th scope="col">Product Name</th>
        <th scope="col">Description</th>
        <th scope="col">Color</th>
        <th scope="col">Size</th>
        <th scope="col">Price</th>
      </tr>
    </thead>
    <tbody>
      {% if recentRecords == [] %}
      <p>You have not collected any product!</p>
      {% else %} {% for rows in recentRecords %}
      <tr>
        <td>{{ rows.product }}</td>
        <td>{{ rows.description }}</td>
        <td>{{ rows.color }}</td>
        <td>{{ rows.size }}</td>
        <td>{{ rows.unit_price}}</td>
        <td>
          <form action="{{ url_for('views.delect_collect')}}" method="POST">
            <input
              type="hidden"
              name="btn-pressed"
              value="{{rows.product_id}}"
            />
            <button type="submit" class="btn btn-outline-default waves-effect">
              <ion-icon name="trash-outline"></ion-icon>
            </button>
          </form>
        </td>
      </tr>
      {% endfor %} {% endif %}
    </tbody>
  </table>
```

- **Delete products**
It's worth nothing that there is a ```delete``` button in such table. When you click on it, the code will redirect to the ```delete_collect``` function in ```views.py``` file. The backend file will also get the specific ID of the product you want to delete at the same time. Based on this ID, the postgresql query can delete the specific information in the collect table created before and notice you with a flash on the web application.

```python
product_id = request.form.get("btn-pressed")
    with engine.connect() as g.conn:

        params = {}
        params['email'] = userp
        params['product_id'] = product_id

        g.conn.execute(text("DELETE FROM collects WHERE email = :email AND product_id = :product_id"
                            ), params)
        g.conn.commit()

        flash('Deleted! Search the website for more product you like.', category='success')
```
