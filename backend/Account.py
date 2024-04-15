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
        information = cursor.execute("SELECT * FROM Authentication WHERE product_id = ?", (row[1],))
        info = information.fetchone()
        if not info:
            continue
        if query and query not in info[1]:
            continue
        userInfo = dict()
        userInfo["username"] = info[1]
        userInfo["password"] = info[2]
        userInfo["email"] = info[4]
        userInfo["phoneNum"] = info[5]
        result.append(userInfo)
    print(result)

    # Close the database connection
    conn.close()
    
    