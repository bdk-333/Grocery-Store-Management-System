# dao - Data Access Object
from datetime import datetime

from sql_connection import connect_to_sql


# def insert_order(connection, order):
#     # insert order
#     cursor = connection.cursor()
#     order_query = ("insert into orders "
#                    "(customer_name, total, date_time) "
#                    "values (%s %s %s)")
#     order_data = (order["customer_name"], order["total"], order["date_time"])
#
#     cursor.execute(order_query, order_data)
#     order_id = cursor.lastrowid
#
#     # insert order details
#     order_details_query = ("insert into order_details "
#                            "(order_id, product_id, quantity, total_price)"
#                            "values (%s, %s, %s, %s)")
#
#     order_details_data = []
#
#     for order_detail_record in order["order_details"]:
#         order_details_data.append([
#             order_id,
#             int(order_detail_record["product_id"]),
#             float(order_detail_record["quantity"]),
#             float(order_detail_record["total_price"])
#         ])
#     cursor.executemany(order_details_query, order_details_data)
#     connection.commit()
#     return order_id

def insert_order(connection, order):
    cursor = connection.cursor()

    order_query = ("INSERT INTO orders "
             "(customer_name, total, date_time)"
             "VALUES (%s, %s, %s)")
    order_data = (order['customer_name'], order['total'], datetime.now())

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    order_details_query = ("INSERT INTO order_details "
                           "(order_id, product_id, quantity, total_price)"
                           "VALUES (%s, %s, %s, %s)")

    order_details_data = []
    for order_detail_record in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_detail_record['product_id']),
            float(order_detail_record['quantity']),
            float(order_detail_record['total_price'])
        ])
    cursor.executemany(order_details_query, order_details_data)

    connection.commit()

    return order_id

if __name__ == "__main__":
    connection = connect_to_sql()
    print(insert_order(connection, {
        'customer_name': 'sample',
        'total': '500',
        'date_time': datetime.now(),
        'order_details': [
            {
                'product_id': 10,
                'quantity': 2,
                'total_price': 50
            },
            {
                'product_id': 15,
                'quantity': 1,
                'total_price': 30
            }
        ]
    }))