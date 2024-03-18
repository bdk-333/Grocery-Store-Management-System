import os

import categories_dao
import orders_dao
import products_dao
import uom_dao
import users_dao
from flask import Flask, render_template, request, jsonify, session
from sql_connection import connect_to_sql
from datetime import datetime

app = Flask(__name__)

__connection = connect_to_sql()
username = ""


@app.route("/")
def login():
    current_route = request.path
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return index()


@app.route('/login', methods=["GET", "POST"])
def landing_page():
    product_count = products_dao.count_products(__connection)
    order_count = orders_dao.count_orders(__connection)
    category_count = categories_dao.count_categories(__connection)
    user_count = users_dao.count_users(__connection)
    user = request.form.get("username")
    password = request.form.get("password")
    user_exists = users_dao.verify_user(__connection, user, password)

    recent_products = products_dao.recent_products(__connection)
    highest_selling = orders_dao.highest_selling_products(__connection)

    global username
    username = user

    if user_exists:
        session['logged_in'] = True
        return index()
        # return render_template('index.html', product_count=product_count, order_count=order_count,
        #                        user_count=user_count, category_count=category_count, username=username,
        #                        recent_products=recent_products, highest_selling=highest_selling)
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return login()


@app.route("/home")
def index():
    product_count = products_dao.count_products(__connection)
    order_count = orders_dao.count_orders(__connection)
    user_count = users_dao.count_users(__connection)
    category_count = categories_dao.count_categories(__connection)
    recent_products = products_dao.recent_products(__connection)
    highest_selling = orders_dao.highest_selling_products(__connection)
    return render_template("index.html", product_count=product_count, order_count=order_count, user_count=user_count,
                           category_count=category_count, username=username, recent_products=recent_products,
                           highest_selling=highest_selling)


@app.route("/getProducts")
def get_products():
    products = products_dao.get_all_products(__connection)
    sorted_products = sorted(products, key=lambda d: d['name'])
    product_names = products_dao.get_product_names(__connection)
    categories = categories_dao.get_category_names(__connection)
    current_route = request.path
    return render_template('products.html', current_route=current_route, products=sorted_products,
                           categories=categories, product_names=product_names, username=username)

    # return render_template("products.html",)
    # response = jsonify(products)
    # response.headers.add("Access-Control-Allow-Origin", "*")
    # return response


@app.route("/insertProduct", methods=["GET", "POST"])
def insert_product():
    # request_payload = json.loads(request.form["data"])
    # product_id = products_dao.insert_new_product(__connection, request_payload)
    # response = jsonify(
    #     {
    #         "product_id": product_id
    #     }
    # )
    # response.headers.add("Access-Control-Allow-Origin", "*")
    form_data = request.form

    product_name = form_data.get("name")
    uom_id = form_data.get("uom")
    price_per_unit = form_data.get("price")
    stock = form_data.get("stock")
    category = form_data.get("category")

    product = {
        "product_name": product_name,
        "uom_id": uom_id,
        "price_per_unit": price_per_unit,
        "stock": stock,
        "category": category
    }

    product_id = products_dao.insert_new_product(__connection, product)

    return get_products()


@app.route("/editproduct.html")
def edit_product_page():
    product_names = products_dao.get_product_names(__connection)
    categories = categories_dao.get_category_names(__connection)
    return render_template("editproduct.html", product_names=product_names, categories=categories, username=username)


@app.route("/editProduct", methods=["GET", "POST"])
def edit_product():
    form_data = request.form

    selected_product = form_data.get("selected_product")
    name = (form_data.get("name"))
    # product_id = (form_data.get("product_id"))
    price_per_unit = (form_data.get("price"))
    stock = (form_data.get("stock"))
    category = (form_data.get("category"))

    product = {
        "selected_product": selected_product,
        "name": name,
        "price": price_per_unit,
        "stock": stock,
        "category": category
    }

    products_dao.edit_product(__connection, product)

    return get_products()


@app.route("/deleteProduct", methods=["POST"])
def delete_product():
    products_dao.delete_product(__connection, request.form.get("product_id"))
    return get_products()


@app.route("/getUom", methods=["GET"])
def get_uoms():
    uoms = uom_dao.get_uoms(__connection)
    response = jsonify(uoms)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/orders")
def show_orders_page():
    # return render_template("orders.html")
    current_route = request.path
    orders = orders_dao.get_orders(__connection)
    sorted_orders = sorted(orders, key=lambda d: d['customer_name'])
    product_names = products_dao.get_product_names(__connection)
    return render_template('orders.html', orders=sorted_orders, products=product_names, current_route=current_route,
                           username=username)


@app.route('/insertOrder', methods=["GET", "POST"])
def insert_order():
    cursor = __connection.cursor()

    customer_name = request.form.get("customer_name")
    product_name = request.form.get("product_name")
    quantity = request.form.get("quantity")
    status = "pending"
    created_at = datetime.now()

    prod_id = []
    query = "SELECT product_id, price_per_unit FROM products WHERE name = %s;"
    cursor.execute(query, (product_name,))

    for (product_id, price_per_unit) in cursor:
        prod_id.append(
            {
                "product_id": product_id,
                "price_per_unit": price_per_unit
            }
        )

    price_value = prod_id[0].get("price_per_unit")
    int_price = int(price_value)
    total_price = int(quantity) * int_price

    new_order = {
        "customer_name": customer_name,
        "total_price": total_price,
        "status": status,
        "created_at": created_at,
        "order_items": [
            {
                "product_id": [d["product_id"] for d in prod_id][0],
                "quantity": quantity,
                "total_price": total_price
            }
        ]
    }

    order_id = orders_dao.insert_order(__connection, new_order)

    return show_orders_page()


@app.route("/editorder.html", methods=["GET", "POST"])
def edit_order_page():
    product_names = products_dao.get_product_names(__connection)
    customer_names = orders_dao.get_customer_names(__connection)
    return render_template("editorder.html", product_names=product_names, customer_names=customer_names,
                           username=username)


@app.route("/editOrder", methods=["GET", "POST"])
def editorders():
    selected_order = request.form.get("selected_order")
    customer_name = request.form.get("customer_name")
    status = request.form.get("order_status")

    new_order = {
        "selected_order": selected_order,
        "customer_name": customer_name,
        "status": status
    }

    orders_dao.edit_order(__connection, new_order)

    return show_orders_page()


@app.route("/deleteOrder", methods=["POST"])
def delete_order():
    orders_dao.delete_order(__connection, request.form.get("id"))
    return show_orders_page()


@app.route("/getCategories")
def show_categories():
    categories = categories_dao.get_categories(__connection)
    sorted_category = sorted(categories, key=lambda d: d['category_id'])
    category_names = categories_dao.get_category_names(__connection)

    return render_template("categories.html", categories=sorted_category, category_names=category_names, username=username)


@app.route("/insertCategory", methods=["GET", "POST"])
def insert_category():
    category = request.form.get("name")

    category_id = categories_dao.insert_category(__connection, category)

    return show_categories()


@app.route("/editCategory", methods=["GET", "POST"])
def edit_category():
    selected_category = request.form.get("selected_category")
    category_name = request.form.get("category")

    category = {
        "category": category_name,
        "selected_category": selected_category
    }

    categories_dao.edit_category(__connection, category)
    return show_categories()


@app.route("/deleteCategory", methods=["GET", "POST"])
def delete_category():
    categories_dao.delete_category(__connection, request.form.get("category_id"))
    return show_categories()


@app.route("/getUsers")
def show_users():
    users = users_dao.get_user(__connection)

    return render_template("users.html", users=users, username=username)


@app.route("/insertUser", methods=["GET", "POST"])
def insert_new_user():
    username = request.form.get("username")
    user_role = request.form.get("user_role")
    password = request.form.get("password")

    new_user = {
        "user_role": user_role,
        "username": username,
        "password": password
    }

    user_id = users_dao.insert_user(__connection, new_user)

    return show_users()


@app.route("/deleteUser", methods=["GET", "POST"])
def delete_user():
    users_dao.delete_user(__connection, request.form.get("user_id"))
    return show_users()


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/new_register', methods=["GET", "POST"])
def new_register():
    # insert new user into the database
    username = request.form.get("username")
    password = request.form.get("password")
    user_role = request.form.get("user_role")

    new_user = {
        "user_role": user_role,
        "username": username,
        "password": password
    }

    user_id = users_dao.insert_user(__connection, new_user)

    return render_template("login.html")


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(port=5000, debug=True)
