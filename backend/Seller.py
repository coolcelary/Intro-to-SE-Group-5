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
        return userid[0]  # Returning the seller_id
    else:
        return None

def add_product(name, price, category, image_url, seller_id):
    try:
        conn = sqlite3.connect("./backend/EcommerceDB.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Products (product_id, name, price, category, image_url, SellerID, quantity) VALUES (NULL, ?, ?, ?, ?, ?, ?)",
                       (name, str(price), category, image_url, seller_id, 5))
        conn.commit()
        print("valid")
    except:
        print("Invalid")

def edit_product(product_id, name, price, category, image_url, seller_id):
    try:
        conn = sqlite3.connect("./backend/EcommerceDB.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE Products SET name=?, price=?, category=?, image_url=? WHERE product_id=? AND SellerID=?",
                       (name, price, category, image_url, product_id, seller_id))
        conn.commit()
        print("Product edited successfully")
    except Exception as e:
        print("Error editing product:", e)

def get_products(seller_id):
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()
    products = cursor.execute("SELECT * FROM Products WHERE SellerID = ?", (seller_id,)).fetchall()
    results = []
    for row in products:
        item = dict()
        item["id"] = row[0]
        item["name"] = row[1]
        item["price"] = row[2]
        item["category"] = row[3]
        item["image_url"] = row[4]
        results.append(item)
    print(results)


if __name__ == "__main__":
    command = sys.argv[1]
    
    if command == "login":
        seller_id = seller_login(sys.argv[2], sys.argv[3])
        if seller_id:
            print("Login successful. Seller ID:", seller_id)
        else:
            print("Login failed")
    
    elif command == "add":
        add_product(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    
    elif command == "edit":
        edit_product(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    
    elif command == "search":
        get_products(sys.argv[2])
