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


def main():
    command = sys.argv[1]
    if command == "login":
        admin_login(sys.argv[2], sys.argv[3])
    elif command == "listall":
        list_users()
        #list_products()
    elif command == "ban":
        ban_user(sys.argv[2])

if __name__ == "__main__":
    main()
