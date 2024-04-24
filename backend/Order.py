import sys
import sqlite3

def checkout(userid, name, address, email, card_number, expiration_date, card_name, cvv):
    if not userid:
        return
    
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    cart_items = cursor.execute("SELECT * FROM Cart WHERE UserID = ?", (userid,)).fetchall()
    if len(cart_items) < 1:
        print("Invalid")
        return
    cursor.execute("DELETE FROM Cart WHERE UserID = ?", (userid,))
    for item in cart_items:
        cursor.execute("INSERT INTO Orders (OrderID, UserID, ProductID, Quantity, Name, Address, Email, CardNumber, ExpirationDate, CardName, CVV) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (userid, item[1], item[2], name, address, email, card_number, expiration_date, card_name, cvv,))
        seller = cursor.execute("SELECT SellerID, price FROM products WHERE product_id = ?", (item[1],)).fetchone()
        if seller:
            cursor.execute("UPDATE Authentication SET Money = ? WHERE UserID = ?", (seller[1] * item[2], seller[0]))
        # Subtract quantity from the product in the Products table
        cursor.execute("UPDATE products SET quantity = Quantity - ? WHERE product_id = ?", (item[2], item[1]))

    print("valid")
    conn.commit()
    conn.close()

def has_ordered(userid, itemid):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    if cursor.execute("SELECT * FROM Orders WHERE UserID = ? AND ProductID = ?", (userid, itemid)).fetchone():
        print("valid")
        return True
    else:
        print("Invalid")
        return False
    conn.close()

def get_orders(productID):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    orders = cursor.execute("SELECT * FROM Orders WHERE ProductID = ?", (productID,)).fetchall()
    result = list()
    for order in orders:
        item = dict()
        item["userid"] = order[1]
        item["quantity"] = order[3]
        item["name"] = order[4]
        result.append(item)
    print(result)
    conn.close()

def get_user_orders(userid):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    user_orders = cursor.execute("SELECT * FROM Orders WHERE UserID = ?", (userid,)).fetchall()
    result = []
    for order in user_orders:
        item = {
            "order_id": order[0],
            "product_id": order[2],
            "quantity": order[3],
            "name": order[4],
            "address": order[5],
            "email": order[6],
            "card_number": order[7],
            "expiration_date": order[8],
            "card_name": order[9],
            "cvv": order[10]
        }
        result.append(item)
    print(result)
    conn.close()

def return_item(product_id, userid):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    order_count = cursor.execute("SELECT Quantity FROM Orders WHERE ProductID = ? AND UserID = ?", (product_id,userid,)).fetchone()
    cursor.execute("DELETE FROM Orders WHERE ProductID = ? AND UserID = ?", (product_id,userid,))
    inventory_count = cursor.execute("SELECT quantity FROM products WHERE product_id = ?", (product_id,)).fetchone()
    if inventory_count and order_count:
        cursor.execute("UPDATE products SET quantity = ? WHERE product_id = ?", (order_count[0] + inventory_count[0], product_id))
    conn.commit()
    print("valid")

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "checkout":
        checkout(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])
    elif command == "verify":
        has_ordered(sys.argv[2], sys.argv[3])
    elif command == "get":
        get_user_orders(sys.argv[2])
    elif command == "getorders":
        get_orders(sys.argv[2])
    elif command == "return":
        return_item(sys.argv[2], sys.argv[3])
