from sql_connection import connect_to_sql


def get_categories(cnx):
    cursor = cnx.cursor()
    query = "select category from categories"
    cursor.execute(query)

    categories = []

    for category in cursor:
        categories.append(
            category[0]
        )
    return categories


if __name__ == "__main__":
    connection = connect_to_sql()

    print(get_categories(connection))
