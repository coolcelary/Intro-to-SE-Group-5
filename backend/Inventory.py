import sqlite3
import sys
import json

def search_products(name, category):
    # Connect to your SQL database
    conn = sqlite3.connect('./backend/EcommerceDB.db')
    cursor = conn.cursor()

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
        item["price"] = row[2].replace("'", "").replace('"', '')
        item["category"] = row[3].replace("'", "").replace('"', '')
        item["image_url"] = row[4].replace("'", "").replace('"', '')
        processed.append(item)
    return processed

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "search":
        name = sys.argv[2]
        category = sys.argv[3]
        products = search_products(name, category)
        print(products)
    
