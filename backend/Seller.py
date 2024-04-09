import sys
import sqlite3



def seller_login(username, password):
    if not username or not password:
        return
    
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()

    userid = cursor.execute("SELECT * FROM Authentication WHERE Username = ? AND Password = ? AND UserType = 'seller'", (username, password)).fetchone()
    if userid:
        print(userid[0])
        return
    else:
        return

def add_product(name, price, category, image_url, seller_id):
    try:
        conn = sqlite3.connect("./backend/EcommerceDB.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Products (product_id, name, price, category, image_url, SellerID) VALUES (NULL, ?, ?, ?, ?, ?)",
                       (name, str(price), category, image_url, seller_id))
        conn.commit()
        print("valid")
    except:
        print("Invalid")

def get_products(seller_id):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    products = cursor.execute("SELECT * FROM Products WHERE SellerID = ?", (seller_id,)).fetchall()
    results = list()
    for row in products:
        item = dict()
        item["id"] = row[0]
        item["name"] = row[1].replace("'", "").replace('"', '')
        item["price"] = str(row[2]).replace("'", "").replace('"', '')
        item["category"] = row[3].replace("'", "").replace('"', '')
        item["image_url"] = row[4].replace("'", "").replace('"', '')
        results.append(item)
    print(results)


if __name__ == "__main__":
    command = sys.argv[1]
    
    if command == "login":
        seller_login(sys.argv[2], sys.argv[3])

    if command == "add":
        add_product(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    if command == "search":
        get_products(sys.argv[2])

