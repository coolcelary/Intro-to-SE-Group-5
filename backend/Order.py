import sys
import sqlite3


def checkout(userid):
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
        cursor.execute("INSERT INTO Orders (OrderID, UserID, ProductID, Quantity) VALUES (NULL, ?, ?, ?)", (item[0], item[1], item[2]))

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

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "checkout":
        checkout(sys.argv[2])
    elif command == "verify":
        has_ordered(sys.argv[2], sys.argv[3])

