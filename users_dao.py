from sql_connection import connect_to_sql


def get_user(cnx):
    cursor = cnx.cursor()
    query = "select * from users"
    cursor.execute(query)

    users = []

    for (user_id, user_role, username, password) in cursor:
        users.append(
            {
                "user_id": user_id,
                "user_role": user_role,
                "username": username,
                "password": password
            }
        )

    return users


def count_users(cnx):
    users = get_user(cnx)
    return len(users)


def verify_user(cnx, username, password):
    users = get_user(cnx)

    usernames_b = [d["username"] for d in users]
    passwords_b = [d["password"] for d in users]

    users_dict = dict(zip(usernames_b, passwords_b))
    return username in users_dict and users_dict[username] == password

    # true_user = False
    # true_password = False
    #
    # for username_b in usernames_b:
    #     if username_b == username:
    #         true_user = True
    #
    # for password_b in passwords_b:
    #     if password_b == password:
    #         true_password = True
    #
    # if true_user and true_password:
    #     return True
    # else:
    #     return False


def insert_user(cnx, user):
    cursor = cnx.cursor()
    query = "insert into users (user_role, username, password) values (%s, %s, %s)"
    data = (user["user_role"], user["username"], user["password"])

    cursor.execute(query, data)
    cnx.commit()

    return cursor.lastrowid


def delete_user(cnx, user_id):
    cursor = cnx.cursor()
    query = "delete from users where user_id=" + str(user_id)
    cursor.execute(query)
    cnx.commit()


if __name__ == "__main__":
    connection = connect_to_sql()
    # print(get_user(connection))
    # print(verify_user(connection, "kirtan", "abc"))

    # print(insert_user(connection, {
    #     "user_role": "employee",
    #     "username": "new_emp",
    #     "password": "password"
    # }))
    print(count_users(connection))
