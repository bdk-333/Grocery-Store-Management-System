# dao - Data Access Object
from datetime import datetime

from sql_connection import connect_to_sql


def get_orders(cnx):
    cursor = cnx.cursor()
    order_query = "select orders.id, orders.customer_name, orders.status, order_items.order_id, " \
                  "order_items.product_id, " \
                  "order_items.quantity, order_items.total_price \
                   from orders " \
                  "inner join order_items on orders.id=order_items.order_id; "

    cursor.execute(order_query)

    response = []

    for (id, customer_name, status, order_id, product_id, quantity, total_price) in cursor:
        response.append(
            {
                "id": id,
                "customer_name": customer_name,
                "order_status": status,
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "total_price": total_price,
            }
        )

    for i in range(len(response)):
        query = "select name from products where product_id=" + str(response[i]["product_id"])
        cursor.execute(query)
        for name in cursor:
            response[i]["product_id"] = name[0]

    return response


def get_customer_names(cnx):
    cursor = cnx.cursor()
    query = "select customer_name from orders;"
    cursor.execute(query)
    names = []

    for customer_name in cursor:
        names.append(customer_name[0])

    return names


def count_orders(cnx):
    orders = get_orders(cnx)
    return len(orders)


def insert_order(cnx, order):
    # insert order
    cursor = cnx.cursor()
    order_query = ("insert into orders "
                   "(customer_name, created_at, status, total_price) "
                   "values (%s, %s, %s, %s)")
    order_data = (order["customer_name"], order["created_at"], order["status"], order["total_price"])

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    # insert order details
    order_details_query = ("insert into order_items "
                           "(order_id, product_id, quantity, total_price)"
                           "values (%s, %s, %s, %s)")

    order_details_data = []

    for order_detail_record in order["order_items"]:
        order_details_data.append([
            order_id,
            int(order_detail_record["product_id"]),
            float(order_detail_record["quantity"]),
            float(order_detail_record["total_price"])
        ])
    cursor.executemany(order_details_query, order_details_data)
    cnx.commit()

    return order_id


def edit_order(cnx, order):
    cursor = cnx.cursor()
    query = "update orders set "
    data = []

    if order["customer_name"]:
        query += "customer_name=%s, "
        data.append(order["customer_name"])

    if order["status"]:
        query += "status=%s, "
        data.append(order["status"])

    query = query.rstrip(", ")
    query += " where customer_name=%s"
    data.append(order["selected_order"])

    cursor.execute(query, data)
    cnx.commit()


def delete_order(cnx, order_id):
    cursor = cnx.cursor()

    order_details_query = "delete from order_items where order_id=%s"
    cursor.execute(order_details_query, (order_id,))

    order_query = "delete from orders where id=%s"
    cursor.execute(order_query, (order_id,))
    cnx.commit()


def highest_selling_products(cnx):
    cursor = cnx.cursor()
    query = "select order_items.product_id, order_items.quantity, order_items.total_price \
            from orders \
            inner join order_items on orders.id=order_items.order_id order by quantity desc limit 5;"

    cursor.execute(query)

    response = []

    for (product_id, quantity, total_price) in cursor:
        response.append(
            {
                "product_id": product_id,
                "quantity": quantity,
                "total_price": total_price,
            }
        )

    for i in range(len(response)):
        query = "select name from products where product_id=" + str(response[i]["product_id"])
        cursor.execute(query)
        for name in cursor:
            response[i]["product_id"] = name[0]

    return response


def pending_orders(cnx):
    cursor = cnx.cursor()

    query = "select orders.customer_name, orders.status,  \
            order_items.product_id,  \
            order_items.quantity, order_items.total_price \
            from orders  \
            inner join order_items on orders.id=order_items.order_id \
            where status='pending' order by created_at;"

    cursor.execute(query)

    response = []

    for (customer_name, status, product_id, quantity, total_price) in cursor:
        response.append(
            {
                "customer_name": customer_name,
                "status": status,
                "product_id": product_id,
                "quantity": quantity,
                "total_price": total_price
            }
        )

    for i in range(len(response)):
        query = "select name from products where product_id=" + str(response[i]["product_id"])
        cursor.execute(query)
        for name in cursor:
            response[i]["product_id"] = name[0]

    return response


if __name__ == "__main__":
    connection = connect_to_sql()
    # print(insert_order(connection, {
    #     'customer_name': 'sample',
    #     'total_price': '500',
    #     'status': 'pending',
    #     'created_at': datetime.now(),
    #     'order_items': [
    #         {
    #             'product_id': 19,
    #             'quantity': 2,
    #             'total_price': 100
    #         },
    #         {
    #             'product_id': 15,
    #             'quantity': 1,
    #             'total_price': 50
    #         }
    #     ]
    # }))

    # print(get_orders(connection))
    # print(count_orders(connection))

    # delete_order(connection, 3)

    # orders_list = get_orders(connection)
    # for _ in orders_list:
    #     print(_)

    # print(get_customer_names(connection))

    # print(highest_selling_products(connection))

    p = pending_orders(connection)
    for _ in p:
        print(_)
