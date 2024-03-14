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
        if user[2] == username:
            return True

    return False


def insert_user(cnx, user):
    cursor = cnx.cursor()
    query = "insert into users (user_role, username, password) values (%s, %s, %s)"
    data = (user["user_role"], user["username"], user["password"])

    cursor.execute(query, data)
    cnx.commit()

    return cursor.lastrowid


if __name__ == "__main__":
    connection = connect_to_sql()
    # print(get_user(connection))
    print(verify_user(connection, "emp"))

    # print(insert_user(connection, {
    #     "user_role": "employee",
    #     "username": "new_emp",
    #     "password": "password"
    # }))

