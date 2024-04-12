import sys
import sqlite3


def checkout(userid, name, address, email, card_number, expiration_date, card_name, cvv):
    if not userid:
        return
    
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    cart_items = cursor.execute("SELECT * FROM Cart WHERE UserID = ?", (userid,)).fetchall()
    if len(cart_items) < 0:
        print("Invalid")
        return
    cursor.execute("DELETE FROM Cart WHERE UserID = ?", (userid,))
    for item in cart_items:
        cursor.execute("INSERT INTO Orders (OrderID, UserID, ProductID, Quantity, Name, Address, Email, CardNumber, ExpirationDate, CardName, CVV) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (item[0], item[1], item[2], name, address, email, card_number, expiration_date, card_name, cvv))

    print("valid")
    conn.commit()


def has_ordered(userid, itemid):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    if cursor.execute("SELECT * FROM Orders WHERE UserID = ? AND ProductID = ?", (userid, itemid)).fetchone():
        print("valid")
        return True
    else:
        print("Invalid")
        return False

def get_orders(productID):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    orders = cursor.execute("SELECT * FROM Orders WHERE ProductID = ?", (productID,)).fetchall()
    result = list()
    for order in orders:
        item = dict()
        item["quantity"] = order[3]
        item["name"] = order[4]
        result.append(item)
    if result:
        print(result)

def getuserhistory(userid, query=""):
    # Connect to the SQLite database
    conn = sqlite3.connect('./backend/EcommerceDB.db')
    cursor = conn.cursor()

    # Execute a SELECT query to fetch all rows from the Authentication table
    cursor.execute("SELECT * FROM Orders WHERE UserID = ?", (userid,))
    rows = cursor.fetchall()

    # Display the retrieved rows
    result = list()
    for row in rows:
        products = cursor.execute("SELECT * FROM Orders WHERE UserID = ?", (row[1],))
        product = products.fetchone()
        if not product:
            continue
        if query and query not in product[1]:
            continue
        item = dict()
        item["user_id"] = product[0]
        item["product_id"] = product[1]
        item["quantity"] = product[2]
        item["name"] = product[3]
        item["address"] = product[4]
        item["email"] = product[5]
        item["card_number"] = product[6]
        result.append(item)
    print(result)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "checkout":
        checkout(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])
    elif command == "verify":
        has_ordered(sys.argv[2], sys.argv[3])
    elif command == "get":
        get_orders(sys.argv[2])

