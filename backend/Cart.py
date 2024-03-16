import sqlite3
import sys



def get_items(userid):
    # Connect to the SQLite database
    conn = sqlite3.connect('./backend/EcommerceDB.db')
    cursor = conn.cursor()

    # Execute a SELECT query to fetch all rows from the Authentication table
    cursor.execute("SELECT * FROM Cart WHERE UserID = ?", (userid,))
    rows = cursor.fetchall()

    # Display the retrieved rows
    result = list()
    for row in rows:
        products = cursor.execute("SELECT * FROM products WHERE product_id = ?", (row[1],))
        product = products.fetchone()
        if not product:
            continue
        item = dict()
        item["id"] = product[0]
        item["name"] = product[1]
        item["price"] = product[2]
        item["category"] = product[3]
        item["image_url"] = product[4]
        result.append(item)
    print(result)

    # Close the database connection
    conn.close()


def add_to_cart(userID, productID):
    # Check if username and password are provided
    if not userID or not productID:
        return False

    # connect to database
    conn = sqlite3.connect('./backend/EcommerceDB.db')
    cursor = conn.cursor()
    existing_entry = cursor.execute("SELECT Quantity FROM Cart WHERE UserID = ? AND ProductID = ?", (userID, productID)).fetchone()
    if existing_entry:
        quantity = int(existing_entry[0]) + 1
    else:
        quantity = 1
    try:
        cursor.execute("INSERT INTO Cart (UserID, ProductID, Quantity) VALUES (?, ?, ?)", (userID, productID, quantity))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()
    
def remove_from_cart(userID, productID):
    # Check if username and password are provided
    if not userID or not productID:
        return False

    # connect to database
    conn = sqlite3.connect('./backend/EcommerceDB.db')
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM Cart WHERE UserID = ? AND ProductID = ?", (userID, productID))
        conn.commit()
        print('valid')
    except sqlite3.Error as e:
        print("Error removing item from cart:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "add":
        if add_to_cart(sys.argv[2], sys.argv[3]):
            print("valid")
    elif command == "remove":
        remove_from_cart(sys.argv[2], sys.argv[3])
    elif command == "search":
        get_items(sys.argv[2])
