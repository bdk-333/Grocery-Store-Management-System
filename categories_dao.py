from sql_connection import connect_to_sql


def get_categories(cnx):
    cursor = cnx.cursor()
    query = "select * from categories"
    cursor.execute(query)

    categories = []

    for (category_id, category) in cursor:
        categories.append(
            {
                "category_id": category_id,
                "category": category
            }
        )
    return categories


def get_category_names(cnx):
    categories = get_categories(cnx)
    category_names = [d["category"] for d in categories]

    return category_names


def count_categories(cnx):
    categories = get_categories(cnx)
    return len(categories)


def insert_category(cnx, category):
    cursor = cnx.cursor()
    query = "insert into categories (category) values(%s)"
    cursor.execute(query, (category, ))
    cnx.commit()

    return cursor.lastrowid


def edit_category(cnx, category):
    cursor = cnx.cursor()
    query = "update categories set category=%s where category=%s"
    data = (category["category"], category["selected_category"])
    cursor.execute(query, data)
    cnx.commit()


def delete_category(cnx, category_id):
    cursor = cnx.cursor()
    query = "delete from categories where category_id=" + str(category_id)
    cursor.execute(query)
    cnx.commit()


if __name__ == "__main__":
    connection = connect_to_sql()

    # print(insert_category(connection, "Baby items"))
    # print(get_categories(connection))
    print(get_category_names(connection))
