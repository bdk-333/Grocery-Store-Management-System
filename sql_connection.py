import mysql.connector

# global sql connection
__cnx = None


def connect_to_sql():
    global __cnx
    if __cnx is None:
        __cnx = mysql.connector.connect(user="root", password="ilovemc5", host="127.0.0.1", database="gs")

    return __cnx
