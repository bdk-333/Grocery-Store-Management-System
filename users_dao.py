from sql_connection import connect_to_sql


def get_user(cnx):
    cursor = cnx.cursor()
    query = "select * from users"
    cursor.execute(query)
    users = cursor.fetchall()

    return users


def verify_user(cnx, username):
    users = get_user(cnx)

    for user in users:
        if user[1] == username:
            return True

    return False


if __name__ == "__main__":
    connection = connect_to_sql()
    print(verify_user(connection, "abc"))
