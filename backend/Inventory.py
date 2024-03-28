import sqlite3
import sys
import json

def search_products(name, category):
    # Connect to your SQL database
    conn = sqlite3.connect('./backend/EcommerceDB.db')
    cursor = conn.cursor()
    params = ()

    # Base SQL query
    sql_query = "SELECT * FROM products WHERE 1"

    # Check if name is provided
    if name:
        sql_query += " AND name LIKE ?"
        name_param = '%' + name + '%'
        params = (name_param,)
    else:
        params = ()

    # Check if category is provided
    if category:
        sql_query += " AND category = ?"
        params += (category,)

    # Execute the SQL query
    cursor.execute(sql_query, params)
    products = cursor.fetchall()

    # Close the connection
    conn.close()
    processed = list()
    for row in products:
        item = dict()
        item["id"] = row[0]
        item["name"] = row[1].replace("'", "").replace('"', '')
        item["price"] = str(row[2]).replace("'", "").replace('"', '')
        item["category"] = row[3].replace("'", "").replace('"', '')
        item["image_url"] = row[4].replace("'", "").replace('"', '')
        processed.append(item)
    return processed

def search_by_id(id):
    conn = sqlite3.connect('./backend/EcommerceDB.db')
    cursor = conn.cursor()
    items = cursor.execute("SELECT * FROM products WHERE product_id = ?", (id,))
    for item in items:
        return {"id" : item[0], "name" : item[1], "price" : item[2], "category": item[3], "image_url" : item[4]}


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "search":
        name = sys.argv[2]
        category = sys.argv[3]
        products = search_products(name, category)
        print(products)

    if command == "idsearch":
        id = sys.argv[2]
        print(search_by_id(id))
    
