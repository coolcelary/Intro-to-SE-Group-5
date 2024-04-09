import sqlite3
import sys

def admin_login(username, password):
    if not username or not password:
        return
    
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()

    userid = cursor.execute("SELECT * FROM Authentication WHERE username = ? AND password = ? AND UserType = ?", (username, password, "admin")).fetchone()
    if userid:
        print(userid[0])
        return
    else:
        return