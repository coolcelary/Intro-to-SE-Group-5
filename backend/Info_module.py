import sqlite3
import sys

def get_info(userid, query=""):
    
    # Connect to the SQLite database
    conn = sqlite3.connect('./backend/EcommerceDB.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Authentication WHERE UserID = ?", (userid,))
    rows = cursor.fetchall()
    
    result = list();
    
    for row in rows:
        Authentication = cursor.execute("SELECT * FROM Authentication WHERE product_id = ?", (row[1],))
        Authentication = Authentication.fetchone()
        if not Authentication:
            continue
        if query and query not in Authentication[1]:
            continue
        userInfo = dict()
        userInfo["username"] = Authentication[1]
        userInfo["password"] = Authentication[2]
        userInfo["email"] = Authentication[4]
        userInfo["phoneNum"] = Authentication[5]
        result.append(userInfo)
    print(result)

    # Close the database connection
    conn.close()
    
    