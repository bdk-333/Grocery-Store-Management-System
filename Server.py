import json
import products_dao
import uom_dao
from flask import Flask, render_template, request, jsonify
from sql_connection import connect_to_sql

app = Flask(__name__)

connection = connect_to_sql()


@app.route("/getProducts", methods=["GET"])
def get_products():
    products = products_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/getUom", methods=["GET"])
def get_uoms():
    uoms = uom_dao.get_uoms(connection)
    response = jsonify(uoms)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/insertProduct", methods=["POST"])
def insert_product():
    request_payload = json.loads(request.form["data"])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify(
        {
            "product_id": product_id
        }
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/deleteProduct", methods=["POST"])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form["product_id"])
    response = jsonify(
        {
            "product_id": return_id
        }
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/products")
def show_products_page():
    return render_template("products.html")


@app.route("/orders")
def show_orders_page():
    return render_template("orders.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
