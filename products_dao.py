# dao - Data Access Object
import categories_dao
from sql_connection import connect_to_sql


def get_all_products(cnx):
    cursor = cnx.cursor()

    # query = "select * from gs.products"
    query = "select products.product_id, products.name, products.uom_id, products.price_per_unit, products.stock, " \
            "products.category, " \
            "uom.uom_name from " \
            "products inner join uom on products.uom_id=uom.uom_id; "

    cursor.execute(query)
    response = []
    for (product_id, name, uom_id, price_per_unit, stock, category, uom_name) in cursor:
        response.append(
            {
                "product_id": product_id,
                "name": name,
                "uom_id": uom_id,
                "price_per_unit": price_per_unit,
                "stock": stock,
                "category": category,
                "uom_name": uom_name
            }
        )

    return response


def get_product_names(cnx):
    cursor = cnx.cursor()
    query = "select name from products"
    cursor.execute(query)

    names = []
    for name in cursor:
        names.append(name[0])

    return names


def get_product_stock(cnx):
    cursor = cnx.cursor()
    query = "select stock from products"
    cursor.execute(query)

    stocks = []
    for name in cursor:
        stocks.append(name[0])

    return stocks


def get_categories(cnx):
    categories = categories_dao.get_categories(cnx)
    return categories


def count_products(cnx):
    products = get_all_products(cnx)

    return len(products)


def insert_new_product(cnx, product):
    cursor = cnx.cursor()
    query = "insert into products " \
            "(name, uom_id, price_per_unit, stock, category) " \
            "values " \
            "(%s, %s, %s, %s, %s);"

    data = (
        product["product_name"], product["uom_id"], product["price_per_unit"], product["stock"], product["category"])
    cursor.execute(query, data)
    cnx.commit()

    return cursor.lastrowid


def edit_product(cnx, product):
    cursor = cnx.cursor()
    query = "update products set "
    data = []

    if product["name"]:
        query += "name=%s, "
        data.append(product["name"])
    if product["price"]:
        query += "price_per_unit=%s, "
        data.append(product["price"])
    if product["stock"]:
        query += "stock=%s, "
        data.append(product["stock"])
    if product["category"]:
        query += "category=%s, "
        data.append(product["category"])

    query = query.rstrip(', ')
    query += " where name=%s"
    data.append(product["selected_product"])

    cursor.execute(query, data)
    cnx.commit()


def delete_product(cnx, product_id):
    cursor = cnx.cursor()
    query = ("delete from products where product_id=" + str(product_id))
    cursor.execute(query)
    cnx.commit()


def recent_products(cnx):
    cursor = cnx.cursor()
    query = "select name, price_per_unit, uom_name from products inner join uom on products.uom_id=uom.uom_id " \
            "order by product_id desc limit 5;"
    cursor.execute(query)

    recents = []

    for (name, price_per_unit, uom_name) in cursor:
        recents.append(
            {
                "name": name,
                "unit": uom_name,
                "price_per_unit": price_per_unit
            }
        )

    return recents


def low_stock_products(cnx):
    cursor = cnx.cursor()
    query = "select name, price_per_unit, stock, uom_name from products inner join uom on products.uom_id=uom.uom_id " \
            "where stock<10 order by name;"
    cursor.execute(query)

    low_stocks = []

    for (name, price_per_unit, stock, uom_name) in cursor:
        low_stocks.append(
            {
                "name": name,
                "price": price_per_unit,
                "stock": stock,
                "unit": uom_name
            }
        )
    return low_stocks


def category_frequency(cnx):
    cursor = cnx.cursor()
    query = "select category from products"
    cursor.execute(query)
    categories = []

    for category in cursor:
        categories.append(category[0])

    frequency_category = {}

    for category in categories:
        if category in frequency_category:
            frequency_category[category] += 1
        else:
            frequency_category[category] = 1

    return dict((category, frequency) for category, frequency in frequency_category.items() if frequency >= 3)


if __name__ == "__main__":
    connection = connect_to_sql()
    # last_row_id = insert_new_products(connection, {
    #     "product_name": "trimmer",
    #     "uom_id": 1,
    #     "price_per_unit": 250
    # })
    # delete_product(connection, 6)
    # print(last_row_id)

    # print(count_products(connection))
    print(get_product_names(connection))
    print(get_product_stock(connection))

    print(dict(zip(get_product_names(connection), get_product_stock(connection))))

    # print(get_categories(connection))

    # edit_product(connection, {
    #     "name": None,
    #     "product_id": 33,
    #     "price": None,
    #     "stock": 25,
    #     "category": "Vegetables"
    # })

    print(get_all_products(connection))

    # print(recent_products(connection))

    # print(low_stock_products(connection))

    # print(category_frequency(connection))
