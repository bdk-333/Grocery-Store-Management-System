import json
import products_dao
import uom_dao
import users_dao
from flask import Flask, render_template, request, jsonify
from sql_connection import connect_to_sql

app = Flask(__name__)

__connection = connect_to_sql()


@app.route("/getProducts")
def get_products():
    products = products_dao.get_all_products(__connection)
    sorted_products = sorted(products, key=lambda d: d['name'])
    current_route = request.path
    return render_template('products.html', current_route=current_route, products=sorted_products)

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

    product = {
        "product_name": product_name,
        "uom_id": uom_id,
        "price_per_unit": price_per_unit
    }

    product_id = products_dao.insert_new_product(__connection, product)

    return get_products()


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
    return render_template('orders.html', current_route=current_route)


@app.route('/login', methods=["GET", "POST"])
def landing_page():
    user = request.form.get("username")
    user_exists = users_dao.verify_user(__connection, user)

    if user_exists:
        return render_template('index.html')
    else:
        return render_template("register.html")


@app.route("/home")
def index():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
