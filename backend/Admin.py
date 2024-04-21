import sqlite3
import sys

def admin_login(username, password):
    if not username or not password:
        return
    
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()

    userid = cursor.execute("SELECT * FROM admin WHERE Username = ? AND Password = ?", (username, password,)).fetchone()
    if userid:
        print(userid[0])
        return
    else:
        return


def list_users():
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    users = cursor.execute("SELECT * FROM Authentication").fetchall()
    result = list()
    for user in users:
        item = dict()
        item["id"] = user[0]
        item["username"] = user[1]
        item["password"] = user[2]
        item["user_type"] = user[3]
        item["email"] = user[4]
        item["phone"] = user[5]
        result.append(item)
    if result:
        print(result)

def ban_user(userid):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Authentication WHERE UserID = ?", (userid,))
        user = cursor.execute("SELECT * FROM Authentication WHERE UserID = ?", (userid,)).fetchone()
        if user:
            print("invalid")
            return
        print("valid")
        conn.commit()
    except:
        print("invalid")

def list_products():
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    products = cursor.execute("SELECT * FROM products").fetchall()
    result = list()
    for product in products:
        item = dict()
        item["product_id"] = product[0]
        item["name"] = product[1]
        item["price"] = product[2]
        item["category"] = product[3]
        result.append(item)
    if result:
        print(result)

def ban_product(product_id):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        product = cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
        if product:
            print("invalid")
            return
        print("valid")
        conn.commit()
    except:
        print("invalid")

def check_approved(seller_id):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    approved_user = cursor.execute("SELECT * FROM Authentication WHERE UserID = ? AND Approved = TRUE", (seller_id,)).fetchone()
    if approved_user:
        print("yes")
    else:
        print("no")

def approve(seller_id):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Authentication SET Approved = TRUE WHERE UserID = ?", (seller_id,))
        conn.commit()
        print("valid")
    except:
        print("Invalid")

def get_pending():
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    pending = cursor.execute("SELECT UserID, Username, Approved FROM Authentication WHERE UserType = 'seller'").fetchall()
    result = list()
    for user in pending:
        if not user[2]:
            item = dict()
            item["id"] = user[0]
            item["name"] = user[1]
            result.append(item)
    print(result)

def block_product(product_id):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    conn.commit()
    print("valid")



def main():
    command = sys.argv[1]
    if command == "login":
        admin_login(sys.argv[2], sys.argv[3])
    elif command == "listall":
        list_users()
    elif command == "ban":
        ban_user(sys.argv[2])
    elif command == "isapproved":
        check_approved(sys.argv[2])
    elif command == "approve":
        approve(sys.argv[2])
    elif command == "getpending":
        get_pending()
    elif command == "block":
        block_product(sys.argv[2])

if __name__ == "__main__":
    main()
