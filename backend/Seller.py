import sys
import sqlite3



def seller_login(username, password):
    if not username or not password:
        return
    
    conn = sqlite3.connect("./backend/EcommerceDB.db")
    cursor = conn.cursor()

    userid = cursor.execute("SELECT * FROM Sellers WHERE username = ? AND password = ?", (username, password)).fetchone()
    if userid:
        print(userid[0])
        return
    else:
        return


if __name__ == "__main__":
    command = sys.argv[1]
    
    if command == "login":
        seller_login(sys.argv[2], sys.argv[3])
