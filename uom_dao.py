# uom : Unit of Measurement
# doa : Data Access Object - to get data from the database

from flask import Flask
from sql_connection import connect_to_sql
# import products_dao

app = Flask(__name__)


def get_uoms(cnx):
    cursor = cnx.cursor()
    query = "select * from uom"
    cursor.execute(query)

    response = []
    for (uom_id, uom_name) in cursor:
        response.append(
            {
                "uom_id": uom_id,
                "uom_name": uom_name
            }
        )

    return response


if __name__ == "__main__":
    connection = connect_to_sql()
    # print(get_uoms(connection))
