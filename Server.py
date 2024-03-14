import categories_dao
import orders_dao
import products_dao
import uom_dao
import users_dao
from flask import Flask, render_template, request, jsonify
from sql_connection import connect_to_sql
from datetime import datetime

app = Flask(__name__)

__connection = connect_to_sql()


@app.route("/getProducts")
def get_products():
    products = products_dao.get_all_products(__connection)
    sorted_products = sorted(products, key=lambda d: d['name'])
    categories = categories_dao.get_categories(__connection)
    current_route = request.path
    return render_template('products.html', current_route=current_route, products=sorted_products, categories=categories)

    # return render_template("products.html",)
    # response = jsonify(products)
    # response.headers.add("Access-Control-Allow-Origin", "*")
    # return response


@app.route("/getUom", methods=["GET"])
def get_uoms():
    uoms = uom_dao.get_uoms(__connection)
    response = jsonify(uoms)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


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


@app.route("/deleteProduct", methods=["POST"])
def delete_product():
    products_dao.delete_product(__connection, request.form.get("product_id"))
    return get_products()


@app.route("/")
def login():
    current_route = request.path
    return render_template('login.html', current_route=current_route)


# @app.route("/products")
# def show_products_page():
#     return render_template("products.html", data = )


@app.route("/orders")
def show_orders_page():
    # return render_template("orders.html")
    current_route = request.path
    orders = orders_dao.get_orders(__connection)
    product_names = products_dao.get_product_names(__connection)
    return render_template('orders.html', orders=orders, products=product_names, current_route=current_route)


@app.route("/deleteOrder", methods=["POST"])
def delete_order():
    orders_dao.delete_order(__connection, request.form.get("id"))
    return show_orders_page()


@app.route('/login', methods=["GET", "POST"])
def landing_page():
    product_count = products_dao.count_products(__connection)
    order_count = orders_dao.count_orders(__connection)
    user = request.form.get("username")
    user_exists = users_dao.verify_user(__connection, user)

    if user_exists:
        return render_template('index.html', product_count=product_count, order_count=order_count)
    else:
        return render_template("register.html")


@app.route("/home")
def index():
    product_count = products_dao.count_products(__connection)
    order_count = orders_dao.count_orders(__connection)
    return render_template("index.html", product_count=product_count, order_count=order_count)


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
    app.run(port=5000, debug=True)
