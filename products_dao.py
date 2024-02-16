# dao - Data Access Object

from sql_connection import connect_to_sql


def get_all_products(cnx):
    cursor = cnx.cursor()

    # query = "select * from gs.products"
    query = "select products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name from " \
            "products inner join uom on products.uom_id=uom.uom_id; "

    cursor.execute(query)
    response = []
    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append(
            {
                "product_id": product_id,
                "name": name,
                "uom_id": uom_id,
                "price_per_unit": price_per_unit,
                "uom_name": uom_name
            }
        )

    return response


def insert_new_product(cnx, product):
    cursor = cnx.cursor()
    query = "insert into products " \
            "(name, uom_id, price_per_unit) " \
            "values " \
            "(%s, %s, %s);"

    data = (product["product_name"], product["uom_id"], product["price_per_unit"])
    cursor.execute(query, data)
    cnx.commit()

    return cursor.lastrowid


def delete_product(cnx, product_id):
    cursor = cnx.cursor()
    query = ("delete from products where product_id=" + str(product_id))
    cursor.execute(query)
    cnx.commit()


if __name__ == "__main__":
    connection = connect_to_sql()
    # last_row_id = insert_new_products(connection, {
    #     "product_name": "trimmer",
    #     "uom_id": 1,
    #     "price_per_unit": 250
    # })
    # delete_product(connection, 6)
    # print(last_row_id)

    print(get_all_products(connection))
